"""Check the built production geometry helper on Android, without installed Launcher data."""
import argparse
import os
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def check_folder_paint_owner(factory):
    root = ROOT/'launcher/smali'
    references = {p.relative_to(root).as_posix() for p in root.rglob('*.smali')
                  if 'Mc;->GO:Landroid/graphics/Paint;' in p.read_text(encoding='utf-8')}
    assert references == {'com/smartisanos/launcher/view/Mc.smali',
                          'com/smartisanos/launcher/view/b/a.1.smali',
                          'com/smartisanos/smengine/F.smali'}, references
    source = (root/'com/smartisanos/launcher/view/Mc.smali').read_text(encoding='utf-8')
    methods = {part.splitlines()[0]: part for part in source.split('.method ')[1:]}
    writers = {name for name, body in methods.items()
               if re.search(r'sput-object[^\n]*Mc;->GO:', body)}
    assert writers == {'static constructor <clinit>()V', 'public static hq()V'}, writers
    rebuild = methods['public static hq()V']
    assignment = rebuild.index('sput-object v1, Lcom/smartisanos/launcher/view/Mc;->GO:')
    assert 'new-instance v1, Landroid/graphics/Paint;' in rebuild[assignment-220:assignment]
    factory_source = factory.read_text(encoding='utf-8')
    assert factory_source.count('retainFolderLabelTexture(') == 1, \
        'scoped folder-label admission is missing from the factory'
    assert 'if-nez v5, :rebuild_text_texture' in factory_source, \
        'large-screen text raster path must retain original rebuilding'
    descriptor = (root/'com/smartisanos/smengine/Da.smali').read_text(encoding='utf-8')
    upload = descriptor.index('P;->texImage2D(IILandroid/graphics/Bitmap;I)V')
    stamp = descriptor.index('iput v5, p0, Lcom/smartisanos/smengine/Da;->mContextGeneration:I')
    assert upload < stamp < upload + 450, 'context generation must be recorded after texture upload'
    print('PASS FOLDER_PAINT_OWNER; other mutable Paint owners remain excluded')


def main():
    parser = argparse.ArgumentParser(__doc__)
    for key in ('serial', 'jdk', 'sdk', 'output'):
        parser.add_argument('--' + key, required=True)
    parser.add_argument('--helper-dex', type=Path, default=ROOT/'build/scratch/dex/classes2.dex')
    parser.add_argument('--factory-source', type=Path,
                        default=ROOT/'launcher/smali/com/smartisanos/smengine/F.smali')
    args = parser.parse_args()
    check_folder_paint_owner(args.factory_source)
    out, jdk, sdk = Path(args.output), Path(args.jdk), Path(args.sdk)
    out.mkdir(parents=True, exist_ok=True)
    classes, dex = out/'classes', out/'dex'
    classes.mkdir(exist_ok=True); dex.mkdir(exist_ok=True)

    def run(cmd, log):
        r = subprocess.run(list(map(str, cmd)), capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=60)
        (out/log).write_text(r.stdout+r.stderr, 'utf-8')
        if r.returncode:
            raise RuntimeError(r.stdout+r.stderr)
        return r.stdout

    fixtures = {
        'com/smartisanos/smengine/Camera.java':
            'package com.smartisanos.smengine; public class Camera {}',
        'com/smartisanos/smengine/Ra.java': '''package com.smartisanos.smengine;
public class Ra {
 public static int calls;
 private static final Ra INSTANCE=new Ra();
 public static Ra getInstance(){calls++;return INSTANCE;}
 public Stage at(){return new Stage();} public Textures rt(){return new Textures();}
 public static class Stage {public Camera Vj(){return new Camera();}}
 public static class Textures {public Texture bb(String key){return new Texture();}}
 public static class Texture {public int getWidth(){return 100;}public int getHeight(){return 100;}}
}''',
        'com/smartisanos/launcher/view/V.java':
            'package com.smartisanos.launcher.view; public class V {}',
        'com/smartisanos/launcher/view/b/M.java':
            'package com.smartisanos.launcher.view.b; public class M {}',
        'com/smartisanos/launcher/data/Constants.java': '''package com.smartisanos.launcher.data;
public class Constants {
 public static class Geometry { public float page_width=100, page_height=100,cell_width=100,cell_height=100; }
 private static final Geometry[] modes=new Geometry[14];
 static {for(int i=0;i<modes.length;i++) modes[i]=new Geometry();modes[13].page_height=50;modes[10].page_height=50;modes[13].cell_width=modes[10].cell_width=30;modes[13].cell_height=modes[10].cell_height=10;}
 public static Geometry mode(int value){return modes[value];}
}''',
    }
    files = [Path(__file__).with_name(name) for name in
             ('OverviewAspectProbe.java', 'PixelGridMetadataProbe.java', 'FolderLabelTextureProbe.java')]
    for name, source in fixtures.items():
        path=out/'src'/name;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(source,'utf-8');files.append(path)
    run([jdk/'bin/javac.exe','-encoding','UTF-8','-source','8','-target','8',
         '-bootclasspath',sdk/'platforms/android-30/android.jar',
         '-classpath',ROOT/'build/scratch/classes','-d',classes,*files],'compile.log')
    run([jdk/'bin/jar.exe','cf',out/'probe.jar','-C',classes,'.'],'jar.log')
    os.environ['JAVA_HOME']=str(jdk)
    run([sdk/'build-tools/36.0.0/d8.bat','--min-api','26','--output',dex,out/'probe.jar'],'dex.log')
    adb=sdk/'platform-tools/adb.exe'
    remote='/data/local/tmp/smartisan-overview-aspect'
    run([adb,'-s',args.serial,'push',dex/'classes.dex',remote+'-probe.dex'],'push-probe.log')
    run([adb,'-s',args.serial,'push',args.helper_dex,remote+'-helper.dex'],'push-helper.log')
    try:
        for name, marker in [('OverviewAspectProbe','OVERVIEW_ASPECT'),
                             ('PixelGridMetadataProbe','PIXEL_GRID_METADATA'),
                             ('FolderLabelTextureProbe','FOLDER_LABEL_TEXTURE')]:
            result=run([adb,'-s',args.serial,'shell',f'CLASSPATH={remote}-probe.dex:{remote}-helper.dex '
                        'app_process /system/bin com.smartisanos.launcher.theme.'+name],name+'.log')
            assert 'PASS '+marker in result, result
            print(result)
    finally:
        run([adb,'-s',args.serial,'shell','rm','-f',remote+'-probe.dex',remote+'-helper.dex'],'cleanup.log')


if __name__ == '__main__':
    main()
