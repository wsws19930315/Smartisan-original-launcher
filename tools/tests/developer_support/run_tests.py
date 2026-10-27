"""Check real page selection/lifecycle methods and local resource contracts."""
import argparse
from pathlib import Path
import re
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]


def extract(source, declaration):
    start = source.index(declaration)
    brace = source.index('{', start)
    depth, end = 1, brace + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--jdk', required=True)
    args = parser.parse_args()
    base = ROOT / 'launcher/tools/maintained_settings_res/res'
    keys = []
    for folder in ['values', 'values-en', 'values-zh-rCN']:
        keys.append({node.attrib['name'] for node in ET.parse(base / folder / 'developer_support.xml').getroot()})
    assert keys[0] == keys[1] == keys[2] and len(keys[0]) == 9
    for name in ['wechat', 'alipay']:
        data = (base / 'drawable-nodpi' / ('donate_' + name + '.png')).read_bytes()
        assert data[:8] == b'\x89PNG\r\n\x1a\n'
        width, height = struct.unpack('>II', data[16:24])
        assert 300 <= width == height <= 1024
    android = '{http://schemas.android.com/apk/res/android}'
    follow = ET.parse(base/'layout/setting_follow_view.xml').getroot()
    ids = [node.get(android+'id', '').split('/')[-1] for node in follow]
    assert ids.index('setting_follow_website') + 1 == ids.index('setting_developer_support')
    assert list(follow)[-1].get(android+'background') == '@drawable/setting_item_down'
    website = next(node for node in follow if node.get(android+'id', '').endswith('/setting_follow_website'))
    assert website.get(android+'background') == '@drawable/more_item_middle'
    page = ET.parse(base/'layout/setting_developer_support.xml').getroot()
    panel = next(node for node in page.iter() if node.get(android+'id', '').endswith('/donate_code_panel'))
    assert panel.get(android+'layout_width') == 'match_parent'
    assert panel.get(android+'background') == '@drawable/setting_item_down_normal'
    assert android+'layout_marginTop' not in panel.attrib
    assert not any(node.get(android+'text') == '@string/donate_heading' for node in page.iter())
    assert panel.get(android+'paddingLeft') == panel.get(android+'paddingRight') == '@dimen/setting_item_text_left'
    image = next(node for node in panel if node.get(android+'id', '').endswith('/donate_code'))
    assert image.get(android+'scaleType') == 'fitCenter'
    assert android+'layout_marginLeft' not in image.attrib and android+'layout_marginRight' not in image.attrib
    source = (ROOT / 'launcher/tools/java/com/smartisanos/launcher/theme/DeveloperSupportPage.java').read_text(encoding='utf-8')
    assert not re.search(r'https?://|startActivity|new Thread|Handler|WebView|recycle\(', source)
    assert not re.search(r'[\u4e00-\u9fff]', source)
    production = '\n'.join(extract(source, method) for method in [
        '    private void select(', '    public void onViewAttachedToWindow(',
        '    public void onViewDetachedFromWindow('])
    fixture = r'''
import java.util.*;
public class SupportProbe {
    static int checks;
    static void check(boolean value) { checks++; if (!value) throw new AssertionError("check " + checks); }
    static class Drawable { }
    static class Resources { static class NotFoundException extends RuntimeException { NotFoundException(String message) { super(message); } } }
    static class View {
        static final int VISIBLE=0, INVISIBLE=4, GONE=8;
        int visibility; boolean selected; String description;
        Map<String,View> children=new HashMap<String,View>();
        void setVisibility(int value){visibility=value;}
        void setSelected(boolean value){selected=value;}
        void setContentDescription(String value){description=value;}
    }
    static class ImageView extends View {
        Drawable drawable;
        void setImageDrawable(Drawable value){drawable=value;}
        Drawable getDrawable(){return drawable;}
    }
    static class Log { static void w(String tag,String message,Throwable error) { } }
    static class IconBitmapDecoder {
        static int calls; static Set<Integer> failures=new HashSet<Integer>();
        static Drawable loadResourceDrawablePreservingPixels(Resources resources,int id) {
            calls++; if(failures.contains(id)) throw new Resources.NotFoundException("test missing resource");
            return new Drawable();
        }
    }
    final Resources resources=new Resources();
    final View root=new View();
    final Drawable[] images=new Drawable[2];
    int selected=-1;
    static View find(Resources resources,View root,String id) {
        if(!root.children.containsKey(id))root.children.put(id,id.equals("donate_code")?new ImageView():new View());
        return root.children.get(id);
    }
    static int drawable(Resources resources,String name){return name.equals("donate_wechat")?1:2;}
    static String text(Resources resources,String name){return name;}
    ImageView code(){return (ImageView)find(resources,root,"donate_code");}
    void run() {
        select(0); check(IconBitmapDecoder.calls==1 && code().drawable==images[0]);
        check(find(resources,root,"donate_wechat_checked").visibility==View.VISIBLE);
        check(find(resources,root,"donate_alipay_checked").visibility==View.INVISIBLE);
        for(int i=0;i<20;i++)select(0);check(IconBitmapDecoder.calls==1);
        select(1);check(IconBitmapDecoder.calls==2 && code().drawable==images[1]);
        for(int i=0;i<20;i++){select(0);select(1);}check(IconBitmapDecoder.calls==2);
        check(find(resources,root,"donate_alipay_option").selected);
        check(!find(resources,root,"donate_wechat_option").selected);
        onViewDetachedFromWindow(root);check(code().drawable==null && images[0]==null && images[1]==null);
        onViewAttachedToWindow(root);check(code().drawable!=null && code().description.equals("donate_alipay_code"));
        onViewDetachedFromWindow(root);IconBitmapDecoder.failures.add(1);select(0);
        check(code().visibility==View.GONE && code().drawable==null);
        check(find(resources,root,"donate_image_error").visibility==View.VISIBLE);
        select(1);check(code().visibility==View.VISIBLE && code().drawable!=null);
        check(find(resources,root,"donate_image_error").visibility==View.GONE);
        onViewDetachedFromWindow(root);check(images[0]==null && images[1]==null);
        System.out.println("PASS production support page checks="+checks);
    }
    public static void main(String[] args){new SupportProbe().run();}
'''
    with tempfile.TemporaryDirectory(prefix='support-page-') as temporary:
        folder = Path(temporary)
        (folder/'SupportProbe.java').write_text(fixture + production + '\n}', encoding='utf-8')
        subprocess.run([str(Path(args.jdk)/'bin/javac.exe'), '-encoding', 'UTF-8', str(folder/'SupportProbe.java')], check=True)
        subprocess.run([str(Path(args.jdk)/'bin/java.exe'), '-cp', str(folder), 'SupportProbe'], check=True)
    print('PASS locale parity, bounded nodpi PNGs and offline source contract')


if __name__ == '__main__':
    main()
