"""Exercise production image validation using allocation/failure tracking decoder doubles."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('extract', ROOT / 'tools/tests/search_index_state/run_tests.py')
extract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extract)

STUBS = {
    'android/graphics/Bitmap.java': '''package android.graphics; public class Bitmap {
 public static int live, recycled; final int w,h;
 Bitmap(int w,int h){this.w=w;this.h=h;live++;}
 public int getWidth(){if(BitmapFactory.failRead)throw new IllegalStateException("read");return w;}
 public int getHeight(){return h;}public void recycle(){live--;recycled++;}
}''',
    'android/graphics/BitmapFactory.java': '''package android.graphics; public class BitmapFactory {
 public static int width=64,height=64,decodes,sample; public static boolean failDecode,failRead;
 public static class Options {public boolean inJustDecodeBounds;public int outWidth,outHeight,inSampleSize;}
 public static Bitmap decodeByteArray(byte[] b,int off,int len,Options o){
  if(o.inJustDecodeBounds){o.outWidth=width;o.outHeight=height;return null;}
  decodes++;sample=o.inSampleSize;if(failDecode)return null;
  return new Bitmap(Math.max(1,width/sample),Math.max(1,height/sample));}
 public static Bitmap decodeByteArray(byte[] b,int off,int len){decodes++;sample=1;return new Bitmap(width,height);}
}'''
}
PREFIX = '''import android.graphics.*;public class IconBackupCodec {
 static int checks;static void check(boolean b,String m){checks++;if(!b)throw new AssertionError(m);}
'''
TEST = '''public static void main(String[] args) {
 byte[] data=new byte[]{(byte)137,80,78,71,13,10,26,10};
 for(int w:new int[]{0,1,47,48,64,1024,1025,8192,Integer.MAX_VALUE})
 for(int h:new int[]{0,47,48,1024,1025,Integer.MAX_VALUE}) {
  BitmapFactory.width=w;BitmapFactory.height=h;int before=BitmapFactory.decodes;
  boolean expected=w>=48&&h>=48&&w<=1024&&h<=1024;
  check(validSource(data)==expected,"portable dimensions "+w+"x"+h);
  check(BitmapFactory.decodes-before==(expected?1:0),"reject portable bounds before allocation");
  check(Bitmap.live==0,"validation retains no pixels");
 }
 for(int w:new int[]{1,64,1024,2048,8192,Integer.MAX_VALUE}) {
  BitmapFactory.width=w;BitmapFactory.height=64;
  check(isValidImage(data,1,Integer.MAX_VALUE),"large custom original remains accepted");
  check(w/BitmapFactory.sample<=1024,"bounded custom validation allocation");
  check(Bitmap.live==0,"custom released");
 }
 BitmapFactory.width=64;BitmapFactory.height=64;BitmapFactory.failDecode=true;
 check(!isValidImage(data,1,Integer.MAX_VALUE),"corrupt raster rejected");BitmapFactory.failDecode=false;
 BitmapFactory.failRead=true;
 try{isValidImage(data,1,Integer.MAX_VALUE);throw new AssertionError("missing failure");}
 catch(IllegalStateException expected){check(Bitmap.live==0,"finally releases on validation failure");}
 BitmapFactory.failRead=false;
 check(!isValidImage(null,1,Integer.MAX_VALUE),"null rejected");
 check(!isValidImage(new byte[0],1,Integer.MAX_VALUE),"empty rejected");
 System.out.println("PASS BACKUP_IMAGE_CHECKS="+checks);
}}
'''


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--jdk', required=True, type=Path)
    ap.add_argument('--source-owner', type=Path, default=ROOT / 'launcher/tools/java/com/smartisanos/launcher/backup/RestoreIconSourceReconciler.java')
    args = ap.parse_args()
    codec = (ROOT / 'launcher/tools/java/com/smartisanos/launcher/backup/IconBackupCodec.java').read_text(encoding='utf-8')
    helper = extract.method(codec, '    static boolean isValidImage(')
    source = extract.method(args.source_owner.read_text(encoding='utf-8'), '    private static boolean validSource(')
    with tempfile.TemporaryDirectory(prefix='backup-images-') as tmp:
        tmp = Path(tmp)
        files = []
        for name, text in STUBS.items():
            p = tmp / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding='utf-8')
            files.append(str(p))
        p = tmp / 'IconBackupCodec.java'
        p.write_text(PREFIX + 'static final long MAX_SOURCE_BYTES=512L*1024L;\n' + helper + source + TEST, encoding='utf-8')
        subprocess.run([str(args.jdk / 'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(tmp), *files, str(p)], check=True)
        subprocess.run([str(args.jdk / 'bin/java.exe'), '-cp', str(tmp), 'IconBackupCodec'], check=True)


if __name__ == '__main__':
    main()
