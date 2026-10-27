"""Compile actual Host policy, source preparation and cache-shape expression on Android.

Selection/PackageManager are fixtures; Canvas/Bitmap and the renderer are real.
No application settings are changed. --host runs a saved source as a negative control.
"""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import os
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
THEME = ROOT / 'launcher/tools/java/com/smartisanos/launcher/theme'
spec = importlib.util.spec_from_file_location('source_blocks', Path(__file__).parent.parent / 'prepared_icon_source/run_device_tests.py')
blocks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blocks)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ('serial', 'jdk', 'sdk', 'output'):
        p.add_argument('--' + key, required=True)
    p.add_argument('--host', type=Path)
    args = p.parse_args()
    out, jdk, sdk = Path(args.output), Path(args.jdk), Path(args.sdk)
    out.mkdir(parents=True, exist_ok=True)
    host = (args.host or THEME / 'MaintainedLauncherSettingsHost.java').read_text(encoding='utf-8')
    raster = (THEME / 'IconRasterDiagnostics.java').read_text(encoding='utf-8')
    marker = 'public static boolean desktopDefaultCircleEnabled(Object itemInfo, String effectiveType)'
    fixed = marker in host
    policy = blocks.block(host, marker if fixed else 'public static boolean desktopDefaultCircleEnabled(Object itemInfo)')
    if not fixed:
        policy += '''static boolean desktopDefaultCircleEnabled(Object i,String t){return desktopDefaultCircleEnabled(i);}'''
    methods = blocks.block(raster, 'private static Bitmap prepareResolvedStaticSource(')
    methods += blocks.block(raster, 'private static final class StaticSource {')
    shape = raster.split('+ ":defaultShape=" + ', 1)[1].split('+ ":defaultShapeVersion="', 1)[0].strip()
    java = '''import android.content.*;import android.graphics.*;import android.graphics.drawable.*;
import java.lang.reflect.*;import com.smartisanos.launcher.theme.DefaultIconCircleRenderer;
public class FallbackPolicyProbe{
 static boolean enabled;static String mode="";static int checks;static final int CANONICAL_DEFAULT_SOURCE_SIZE=256;
 static Context context=new ContextWrapper(null){public SharedPreferences getSharedPreferences(String n,int m){
  return (SharedPreferences)Proxy.newProxyInstance(getClass().getClassLoader(),new Class[]{SharedPreferences.class},
   new InvocationHandler(){public Object invoke(Object p,Method m,Object[] a){if(m.getName().equals("getString"))
    return enabled?"circle":"follow_app";throw new AssertionError(m.getName());}});}};
 static class RedirectIconInfo{}
 static class RedirectIconDB{static String MODE_ORIGINAL="original",MODE_CUSTOM="custom",MODE_RESOURCE="resource",MODE_PACK="pack";
  static RedirectIconInfo getRedirectIconMetadata(Context c,String p,String n){return new RedirectIconInfo();}
  static String modeOf(RedirectIconInfo i){return mode;}}
 enum Type{DEFAULT,IMPROVED,PACK}
 static class IconSourceManager{Type type;static final IconSourceManager instance=new IconSourceManager();
  static IconSourceManager get(Context c){return instance;}}
 static class MaintainedLauncherSettingsHost{
  static Context currentApplicationContext(){return context;}static String itemFieldValue(Object i,String k){return "fixture";}
  POLICY
 }
 static class StartupPageSceneDiagnostics{static long detailBegin(){return 0;}static void detailEnd(Object i,String s,long n){}}
 static boolean isDesktopSettingsShortcut(Object i){return false;}
 static Bitmap sourceBitmap(Drawable d){return ((BitmapDrawable)d).getBitmap().copy(Bitmap.Config.ARGB_8888,false);}
 METHODS
 static String shapeKey(String sourceType,Object itemInfo){return ":defaultShape="+SHAPE;}
 static void check(boolean b,String s){checks++;if(!b)throw new AssertionError(s+" global="+IconSourceManager.instance.type+" mode="+mode);}
 public static void main(String[] a){try{run();}catch(Throwable t){t.printStackTrace(System.out);System.exit(1);}}
 static void run(){Object item=new Object();Bitmap raw=Bitmap.createBitmap(32,32,Bitmap.Config.ARGB_8888);raw.eraseColor(0xff336699);
  Drawable drawable=new BitmapDrawable(android.content.res.Resources.getSystem(),raw);
  for(Type global:new Type[]{Type.IMPROVED,Type.PACK,Type.DEFAULT})for(String selected:new String[]{"","original","custom","resource","pack"}){
   IconSourceManager.instance.type=global;mode=selected;
   for(boolean on:new boolean[]{true,false}){
    enabled=on;StaticSource fallback=new StaticSource(drawable,"DEFAULT","APK_DEFAULT",false);
    Bitmap framed=prepareResolvedStaticSource(item,null,fallback);
    check((framed.getWidth()==256)==on,"actual APK fallback must honor circle switch");
    check(((framed.getPixel(0,0)>>>24)==0)==on,"circle removes outer square corners");
    String token=shapeKey("DEFAULT",item);check(token.contains(on?"circle":"follow_app"),"key agrees with rendered fallback");
    framed.recycle();
    for(String matched:new String[]{"IMPROVED","PACK","CUSTOM","RESOURCE"}){
     Bitmap kept=prepareResolvedStaticSource(item,null,new StaticSource(drawable,matched,"managed",false));
     check(kept.getWidth()==32&&kept.getPixel(0,0)==raw.getPixel(0,0),"matched artwork stays intact");kept.recycle();
     check(shapeKey(matched,item).contains("not-default"),"managed key excludes fallback circle");
    }
   }
  }
  enabled=true;IconSourceManager.instance.type=Type.IMPROVED;mode="";
  check(MaintainedLauncherSettingsHost.desktopDefaultCircleEnabled(item,"DEFAULT"),"missing source framed");
  check(!MaintainedLauncherSettingsHost.desktopDefaultCircleEnabled(item,"IMPROVED"),"arrived source replaces fallback unframed");
  check(MaintainedLauncherSettingsHost.desktopDefaultCircleEnabled(item,"DEFAULT"),"later source miss framed again");
  check(IconSourceManager.instance.type==Type.IMPROVED&&mode.equals(""),"selection not rewritten on fallback");
  raw.recycle();System.out.println("PASS FALLBACK_CIRCLE_POLICY checks="+checks);
 }
}'''.replace('\n  POLICY\n', '\n'+policy+'\n').replace('\n METHODS\n', '\n'+methods+'\n').replace('SHAPE;', shape+';')
    source = out / 'FallbackPolicyProbe.java'
    source.write_text(java, encoding='utf-8')
    def run(cmd, log):
        r = subprocess.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
        (out/log).write_text(r.stdout+r.stderr,encoding='utf-8')
        if r.returncode: raise RuntimeError(r.stdout+r.stderr)
        return r.stdout
    classes, dex = out/'classes',out/'dex'
    classes.mkdir(exist_ok=True);dex.mkdir(exist_ok=True)
    run([jdk/'bin/javac.exe','-encoding','UTF-8','-source','8','-target','8','-bootclasspath',sdk/'platforms/android-36/android.jar','-d',classes,source,THEME/'DefaultIconCircleRenderer.java'],'compile.log')
    run([jdk/'bin/jar.exe','cf',out/'probe.jar','-C',classes,'.'],'jar.log')
    os.environ['JAVA_HOME']=str(jdk)
    run([sdk/'build-tools/37.0.0/d8.bat','--min-api','23','--output',dex,out/'probe.jar'],'dex.log')
    adb=[sdk/'platform-tools/adb.exe','-s',args.serial]
    remote='/data/local/tmp/fallback-circle-policy.dex'
    run([*adb,'push',dex/'classes.dex',remote],'push.log')
    try:
        result=run([*adb,'shell','CLASSPATH='+remote+' app_process /system/bin FallbackPolicyProbe'],'device.log')
        assert 'PASS FALLBACK_CIRCLE_POLICY' in result
        print(result.strip())
    finally:
        run([*adb,'shell','rm','-f',remote],'cleanup.log')


if __name__ == '__main__':
    main()
