"""Execute the actual theme initialization Smali on ART with controlled theme and engine owners."""
import argparse,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
ap=argparse.ArgumentParser(__doc__);ap.add_argument('--serial',required=True);ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);jdk=Path('E:/Program Files/Android/Android Studio/jbr');sdk=Path('D:/sdk');classes=out/'classes';classes.mkdir(exist_ok=True)
def run(cmd,name):
 r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf8',errors='replace',timeout=120);(out/name).write_text(r.stdout+r.stderr,encoding='utf8')
 if r.returncode:raise RuntimeError(name+': '+r.stdout+r.stderr)
 return r.stdout
paths=[]
for name,path in [('BeforeThemeInit',a.baseline),('AfterThemeInit',a.source)]:
 s=path.read_text(encoding='utf8');i=s.index('.method public static da(Landroid/content/Context;)');j=s.index('.end method',i)+len('.end method');method=s[i:j]
 for old,new in [('com/smartisanos/launcher/theme/X','ThemeFixture'),('com/smartisanos/launcher/theme/v','ThemeFixture$Theme'),('com/smartisanos/launcher/data/Constants','ThemeFixture$Constants'),('com/smartisanos/launcher/e/s','ThemeFixture$Assets'),('com/smartisanos/smengine/Ra','ThemeFixture$Engine'),('com/smartisanos/launcher/theme/LauncherSettingBridge','ThemeFixture$Bridge')]:method=method.replace('L'+old+';','L'+new+';')
 p=out/(name+'.smali');p.write_text('.class public L'+name+';\n.super Ljava/lang/Object;\n'+method,encoding='utf8');paths.append(p)
(out/'Assemble.java').write_text('''import java.io.File;import brut.androlib.smali.SmaliBuilder;import com.android.tools.smali.dexlib2.Opcodes;import com.android.tools.smali.dexlib2.writer.builder.DexBuilder;import com.android.tools.smali.dexlib2.writer.io.FileDataStore;public class Assemble{public static void main(String[] a)throws Exception{DexBuilder d=new DexBuilder(new Opcodes(28));SmaliBuilder b=new SmaliBuilder(28);for(int i=1;i<a.length;i++)if(!b.buildFile(new File(a[i]),d))throw new AssertionError(a[i]);d.writeTo(new FileDataStore(new File(a[0])));}}''')
run([jdk/'bin/javac.exe','-cp',ROOT/'tools/apktool.jar','-d',classes,out/'Assemble.java'],'assemble-compile.log');run([jdk/'bin/java.exe','-cp',str(classes)+os.pathsep+str(ROOT/'tools/apktool.jar'),'Assemble',out/'owners.dex',*paths],'assemble.log')
(out/'ThemeFixture.java').write_text(r'''
import android.content.Context;import android.content.res.*;import android.app.*;import java.util.*;
public class ThemeFixture {
 public static class Theme {public String mPath="fixture",mId="fixture";public Resources mResources=Resources.getSystem();public boolean gaussian,fixed;}
 public static class Constants {public static boolean sIsGaussianTheme,isTransparentTheme,ENABLE_LARGE_SCREEN_MODE;public static int window_width,window_height;public static String THEME_PATH,sWallpaperUri,sGaussianResSuffix,sStatusbarColorSuffix,sNaviBarLightOrDarkSuffix;public static int classified;
 public static void setIconType(Theme value){events.add("iconType");}
 public static void initGaussianDarkLight(Context context){classified++;sGaussianResSuffix=(brightness&1)==0?"":"_light";sStatusbarColorSuffix=(brightness&2)==0?"":"_light";sNaviBarLightOrDarkSuffix=(brightness&4)==0?"":"_light";}}
 public static Theme theme=new Theme();public static int brightness;public static final ArrayList<String> events=new ArrayList<>();
 public static Theme va(Context context){events.add("theme");return theme;}public static void k(Theme value){events.add("publish");}public static boolean i(Theme value){return value.gaussian;}public static boolean h(Theme value){return value.fixed;}
 public static class Bridge {public static void ensureTransparentThemeRegistered(Context c){events.add("ensure");}}
 public static class Engine {static final Engine instance=new Engine();public static Engine getInstance(){return instance;}public void a(AssetManager a){events.add("assets");}}
 public static class Assets {public static String ha(Context c){events.add("source");return "fixture-source";}public static void n(Theme t){events.add("status:base");}public static void d(Theme t,String s){events.add("status:"+s);}public static void c(Theme t,String s){events.add("nav:"+s);}}
 public static void reset(boolean gaussian,boolean transparent,boolean large,boolean fixed,int w,int h,int color){theme.gaussian=gaussian;theme.fixed=fixed;Constants.isTransparentTheme=transparent;Constants.ENABLE_LARGE_SCREEN_MODE=large;Constants.window_width=w;Constants.window_height=h;Constants.classified=0;Constants.sGaussianResSuffix=Constants.sStatusbarColorSuffix=Constants.sNaviBarLightOrDarkSuffix="old";Constants.sWallpaperUri="existing";Constants.THEME_PATH="old";brightness=color;events.clear();}
}
''',encoding='utf8')
(out/'ThemeGateProbe.java').write_text(r'''
import android.content.*;import android.app.*;import java.util.*;import java.lang.reflect.*;import org.json.*;
public class ThemeGateProbe {
 static int checks,cases;static void check(boolean ok,String why){checks++;if(!ok)throw new AssertionError(why);}
 public static void main(String[] args)throws Exception{try{run();}catch(Throwable e){System.out.println("PROBE_FAILED "+e.getClass().getName()+": "+e.getMessage());e.printStackTrace(System.out);System.exit(1);}}
 static void run()throws Exception{if(android.os.Looper.myLooper()==null)android.os.Looper.prepare();Method before=Class.forName("BeforeThemeInit").getMethod("da",Context.class),after=Class.forName("AfterThemeInit").getMethod("da",Context.class);Application application=new Application();Context[] contexts={application,new Activity(),new ContextWrapper(application)};int[] sizes={-1,0,1,1080};
 for(Context context:contexts)for(int flags=0;flags<16;flags++)for(int w:sizes)for(int h:sizes)for(int color=0;color<8;color++){
 boolean gaussian=(flags&1)!=0,transparent=(flags&2)!=0,large=(flags&4)!=0,fixed=(flags&8)!=0,skip=context instanceof Application&&!gaussian&&!transparent&&!large&&!fixed&&w==0&&h==0;
 ThemeFixture.reset(gaussian,transparent,large,fixed,w,h,color);before.invoke(null,context);ArrayList<String> be=new ArrayList<>(ThemeFixture.events);String source=ThemeFixture.Constants.sWallpaperUri;check(ThemeFixture.Constants.classified==1,"baseline classifies");
 ThemeFixture.reset(gaussian,transparent,large,fixed,w,h,color);after.invoke(null,context);check(ThemeFixture.Constants.classified==(skip?0:1),"classification gate exact scope");check(be.equals(ThemeFixture.events),"same theme/source/asset/bar/nav operations");check(Objects.equals(source,ThemeFixture.Constants.sWallpaperUri),"selected source preserved");check("fixture".equals(ThemeFixture.Constants.THEME_PATH),"theme path preserved");
 if(skip){ThemeFixture.Constants.window_width=1080;ThemeFixture.Constants.window_height=2280;ThemeFixture.Constants.initGaussianDarkLight(context);check(ThemeFixture.Constants.classified==1,"normal layout phase still classifies");check(ThemeFixture.Constants.sGaussianResSuffix.equals((color&1)==0?"":"_light"),"final desktop suffix");check(ThemeFixture.Constants.sStatusbarColorSuffix.equals((color&2)==0?"":"_light"),"final status suffix");}
 cases++;
 }
 System.out.println("RESULT "+new JSONObject().put("cases",cases).put("checks",checks).put("scope","actual X.da Smali on ART; controlled theme/resource/engine/classifier; all flags/context/zero-partial-valid geometry"));
 }
}
''',encoding='utf8')
run([jdk/'bin/javac.exe','-encoding','UTF-8','-source','8','-target','8','-cp',sdk/'platforms/android-36/android.jar','-d',classes,out/'ThemeFixture.java',out/'ThemeGateProbe.java'],'probe-compile.log')
jar=out/'probe.jar';run([jdk/'bin/jar.exe','cf',jar,'-C',classes,'ThemeFixture.class','-C',classes,'ThemeGateProbe.class',*sum((['-C',classes,x.name]for x in classes.glob('ThemeFixture$*.class')),[])],'jar.log');dex=out/'dex';dex.mkdir(exist_ok=True);os.environ['JAVA_HOME']=str(jdk);run([sdk/'build-tools/37.0.0/d8.bat','--min-api','23','--lib',sdk/'platforms/android-36/android.jar','--output',dex,jar],'d8.log');adb=[sdk/'platform-tools/adb.exe','-s',a.serial];remote='/data/local/tmp/smartisan-theme-gate';run([*adb,'push',out/'owners.dex',remote+'-owners.dex'],'push-owners.log');run([*adb,'push',dex/'classes.dex',remote+'-probe.dex'],'push-probe.log')
try:
 text=run([*adb,'shell','env','CLASSPATH='+remote+'-owners.dex:'+remote+'-probe.dex','app_process','/system/bin','ThemeGateProbe'],'device.log');row=json.loads(next(x[7:]for x in text.splitlines()if x.startswith('RESULT ')));(out/'summary.json').write_text(json.dumps(row,indent=2));print(text)
finally:run([*adb,'shell','rm','-f',remote+'-owners.dex',remote+'-probe.dex'],'cleanup.log')
