"""Actual final-cache admission method with Android Drawable/tint/Bitmap objects.

Item/source settings and geometry key are controlled fixtures, not Launcher UI.
"""
import argparse
from pathlib import Path
import subprocess
from run_device_tests import block


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--serial', required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--raster', type=Path, required=True)
    ap.add_argument('--codec', type=Path, required=True)
    args = ap.parse_args()
    out = args.output
    (out/'classes').mkdir(parents=True, exist_ok=True)
    (out/'dex').mkdir(exist_ok=True)
    source = args.raster.read_text(encoding='utf8')
    methods = block(source, 'private static String persistentFinalKey(')
    methods += block(source, 'private static final class StaticSource {')
    (out/'FinalAdmissionProbe.java').write_text(PROBE.replace('METHODS', methods), encoding='utf8')
    (out/'FinalIconTextureFile.java').write_bytes(args.codec.read_bytes())
    sdk = Path('D:/sdk'); jdk = Path('E:/Program Files/Android/Android Studio/jbr/bin')

    def run(command, name):
        r = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                           encoding='utf8', errors='replace', timeout=120)
        (out/name).write_text(r.stdout+r.stderr, encoding='utf8')
        if r.returncode:
            raise RuntimeError(r.stdout+r.stderr)
        return r.stdout

    run([jdk/'javac.exe','-encoding','UTF-8','-source','8','-target','8','-cp',sdk/'platforms/android-36/android.jar',
         '-d',out/'classes',out/'FinalAdmissionProbe.java',out/'FinalIconTextureFile.java'], 'javac.log')
    run([jdk/'java.exe','-cp',sdk/'build-tools/37.0.0/lib/d8.jar','com.android.tools.r8.D8','--min-api','28',
         '--lib',sdk/'platforms/android-36/android.jar','--output',out/'dex',*sorted((out/'classes').rglob('*.class'))], 'd8.log')
    adb = [sdk/'platform-tools/adb.exe','-s',args.serial]; remote='/data/local/tmp/smartisan-final-admission.dex'
    run([*adb,'push',out/'dex/classes.dex',remote], 'push.log')
    try:
        result = run([*adb,'shell','env','CLASSPATH='+remote,'app_process','/system/bin','FinalAdmissionProbe'], 'result.log')
        assert 'PASS FINAL_ADMISSION' in result, result
        print(result)
    finally:
        run([*adb,'shell','rm','-f',remote], 'cleanup.log')


PROBE = r'''
import android.graphics.*;import android.graphics.drawable.*;import android.content.*;import android.content.res.*;
public class FinalAdmissionProbe {
 static int checks,mode=12;static String user="0",itemType="0",pkg="test.app",geometry="one";
 static boolean normal=true,settings,circle,projection,dynamic,context=true;
 static boolean shouldUseHighResolutionDesktopRaster(Object i){return normal;}
 static boolean isDesktopSettingsShortcut(Object i){return settings;}
 static String itemField(Object i,String f){return f.equals("userId")?user:f.equals("itemType")?itemType:pkg;}
 static class IconIlluminationCompat {static boolean enabled(){return projection;}}
 static class LauncherSettingBridge {static boolean isDynamicIconPackage(String p){return dynamic;}}
 static class MaintainedLauncherSettingsHost {
  static Context currentApplicationContext(){return context?new ContextWrapper(null){
   public android.content.pm.ApplicationInfo getApplicationInfo(){android.content.pm.ApplicationInfo i=new android.content.pm.ApplicationInfo();i.sourceDir="/test/base.apk";return i;}
   public Resources getResources(){return Resources.getSystem();}
  }:null;}
  static boolean desktopDefaultCircleEnabled(Object i,String t){return circle;}
 }
 static class Spec {float rasterScale=1;}
 static Spec resolveNormalIconRasterSpec(int m){return m==99?null:new Spec();}
 static int layoutSize(int m,String key){return 100;}
 static String textureCacheKey(Object i,String base,int m){return base+":"+geometry+":"+m;}
 static String buildResolvedTextureCacheKey(Object i,String base,int m,String hash,String type,String identity){return textureCacheKey(i,base,m)+":"+hash+":"+type+":"+identity;}
 METHODS
 static void check(boolean ok,String message){checks++;if(!ok)throw new AssertionError(message);}
 static String key(Object item,Bitmap bitmap,Drawable drawable){return persistentFinalKey(item,bitmap,mode,new StaticSource(drawable,"IMPROVED","same",false),false);}
 public static void main(String[] args){try{run();}catch(Throwable error){error.printStackTrace(System.out);System.exit(1);}}
 static void run(){
  Object item=new Object();Bitmap b=Bitmap.createBitmap(32,32,Bitmap.Config.ARGB_8888);b.eraseColor(0xff556677);
  BitmapDrawable drawable=new BitmapDrawable(Resources.getSystem(),b);Rect bounds=new Rect(1,2,4,6);drawable.setBounds(bounds);
  String original=key(item,b,drawable);check(original!=null,"plain static bitmap admitted");
  check(bounds.equals(drawable.getBounds())&&!b.isRecycled(),"fingerprint preserves source bounds/lifetime");
  check(original.equals(key(item,b,drawable)),"same actual source reuse");
  b.setPixel(0,0,0xff556678);b.setPixel(1,0,0xff556658);check(!original.equals(key(item,b,drawable)),"strong source collision negative control");b.eraseColor(0xff556677);
  drawable.setTint(0xffff0000);String red=key(item,b,drawable);drawable.setTint(0xff00ff00);String green=key(item,b,drawable);
  check(red!=null&&green!=null&&!red.equals(green),"constant tint changes actual draw identity");drawable.setTintList(null);
  check(original.equals(key(item,b,drawable)),"clear tint recovers original key");
  geometry="two";check(!original.equals(key(item,b,drawable)),"render contract changes key");geometry="one";
  check(!original.equals(persistentFinalKey(item,b,mode,new StaticSource(drawable,"IMPROVED","same",false),true)),"actual classification changes key");
  user="10";check(key(item,b,drawable)==null,"profile excluded");user="0";
  itemType="6";check(key(item,b,drawable)==null,"shortcut excluded");itemType="0";
  mode=8;check(key(item,b,drawable)==null,"folder surface excluded");mode=99;check(key(item,b,drawable)==null,"missing geometry excluded");mode=12;
  normal=false;check(key(item,b,drawable)==null,"active or special pipeline excluded");normal=true;
  settings=true;check(key(item,b,drawable)==null,"settings excluded");settings=false;
  projection=true;check(key(item,b,drawable)==null,"projection excluded");projection=false;
  dynamic=true;check(key(item,b,drawable)==null,"dynamic package excluded");dynamic=false;
  context=false;check(key(item,b,drawable)==null,"missing context excluded");context=true;
  check(key(null,b,drawable)==null&&key(item,null,drawable)==null,"null excluded");
  check(persistentFinalKey(item,b,mode,new StaticSource(drawable,"DEFAULT","legacy",true),false)==null,"legacy decorated source excluded");
  check(persistentFinalKey(item,b,mode,new StaticSource(drawable,"DEFAULT","APK_DEFAULT",false),false)==null,"transient APK fallback excluded");
  check(key(item,b,new ColorDrawable(0xff123456))==null,"vector/nonbitmap excluded");
  drawable.setAlpha(128);check(key(item,b,drawable)==null,"paint alpha excluded");drawable.setAlpha(255);
  drawable.setColorFilter(new LightingColorFilter(0xffffff,1));check(key(item,b,drawable)==null,"explicit filter excluded");drawable.setColorFilter((ColorFilter)null);
  drawable.setTileModeX(Shader.TileMode.REPEAT);check(key(item,b,drawable)==null,"tiling excluded");drawable.setTileModeX(null);
  drawable.setGravity(android.view.Gravity.CENTER);check(key(item,b,drawable)==null,"nonfill gravity excluded");drawable.setGravity(android.view.Gravity.FILL);
  circle=true;ColorDrawable source=new ColorDrawable(0xff112233);
  check(persistentFinalKey(item,b,mode,new StaticSource(source,"DEFAULT","default",false),false)!=null,"prepared circle supports already rasterized Drawable");circle=false;
  b.recycle();check(key(item,b,drawable)==null,"recycled input excluded");
  System.out.println("PASS FINAL_ADMISSION checks="+checks);
 }
}
'''

if __name__ == '__main__':
    main()
