"""Exercise the exact wallpaper-owner block with deterministic Android I/O substitutes.

Validates selection, serialization and system-only writes; not OEM visual presentation.
"""
from pathlib import Path
import argparse, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[3]
STUBS = {
"android/app/Activity.java": "package android.app; public class Activity extends android.content.Context {public boolean finishing,destroyed;public boolean isFinishing(){return finishing;}public boolean isDestroyed(){return destroyed;}}",
"android/os/Build.java": "package android.os; public class Build {public static class VERSION {public static int SDK_INT=36;}}",
"android/os/Looper.java": "package android.os; public class Looper {public static Looper getMainLooper(){return new Looper();}}",
"android/os/Handler.java": "package android.os; public class Handler {public Handler(Looper l){} public boolean post(Runnable r){r.run();return true;}}",
"android/util/Log.java": "package android.util; public class Log {public static int i(String a,String b){return 0;}public static int w(String a,String b,Throwable c){return 0;}}",
"android/util/DisplayMetrics.java": "package android.util; public class DisplayMetrics {public int widthPixels=100,heightPixels=200;}",
"android/text/TextUtils.java": "package android.text; public class TextUtils {public static boolean isEmpty(CharSequence s){return s==null||s.length()==0;}}",
"android/net/Uri.java": "package android.net; public class Uri {String value;private Uri(String s){value=s;}public static Uri parse(String s){return new Uri(s);}public String toString(){return value;}}",
"android/graphics/Rect.java": "package android.graphics; public class Rect {public Rect(int l,int t,int r,int b){}}",
"android/graphics/Bitmap.java": """package android.graphics;
public class Bitmap {public int width,height;public String source;public Bitmap(int w,int h,String s){width=w;height=h;source=s;}
public int getWidth(){return width;}public int getHeight(){return height;}public void recycle(){}
public static Bitmap createScaledBitmap(Bitmap b,int w,int h,boolean f){return new Bitmap(w,h,b.source);}}""",
"android/graphics/BitmapFactory.java": """package android.graphics;
public class BitmapFactory {public static int decodes;public static Bitmap decodeStream(java.io.InputStream in){
 try {String[] s=new String(in.readAllBytes(),java.nio.charset.StandardCharsets.UTF_8).split(":",3);decodes++;return new Bitmap(Integer.parseInt(s[0]),Integer.parseInt(s[1]),s[2]);}
 catch(java.io.IOException e){return null;}}} """,
"android/content/res/AssetManager.java": """package android.content.res;
public class AssetManager {public final java.util.Map<String,byte[]> files=new java.util.HashMap<>();
public java.io.InputStream open(String name)throws java.io.IOException {byte[] b=files.get(name);if(b==null)throw new java.io.FileNotFoundException(name);return new java.io.ByteArrayInputStream(b);}}""",
"android/content/res/Resources.java": """package android.content.res; public class Resources {
public final AssetManager assets=new AssetManager();public AssetManager getAssets(){return assets;}public android.util.DisplayMetrics getDisplayMetrics(){return new android.util.DisplayMetrics();}}""",
"android/content/ContentResolver.java": """package android.content; public class ContentResolver {
public final java.util.Map<String,byte[]> files=new java.util.HashMap<>();
public java.io.InputStream openInputStream(android.net.Uri uri)throws java.io.IOException{byte[] b=files.get(uri.toString());if(b==null)throw new java.io.FileNotFoundException(uri.toString());return new java.io.ByteArrayInputStream(b);}}""",
"android/content/SharedPreferences.java": """package android.content; public interface SharedPreferences {
String getString(String k,String d);int getInt(String k,int d);Editor edit();
interface Editor {Editor putString(String k,String v);Editor putInt(String k,int v);boolean commit();}}
""",
"android/content/Context.java": """package android.content; public class Context {
public static final int MODE_PRIVATE=0;public boolean transparent;public String uri="";public int errors;
public final android.app.WallpaperManager manager=new android.app.WallpaperManager();
public final ContentResolver resolver=new ContentResolver();public final android.content.res.Resources resources=new android.content.res.Resources();
public final Prefs prefs=new Prefs();public Context getApplicationContext(){return this;}public ContentResolver getContentResolver(){return resolver;}
public android.content.res.Resources getResources(){return resources;}public SharedPreferences getSharedPreferences(String n,int m){return prefs;}
public static class Prefs implements SharedPreferences,SharedPreferences.Editor {
public final java.util.Map<String,Object> values=new java.util.HashMap<>();public String getString(String k,String d){return (String)values.getOrDefault(k,d);}public int getInt(String k,int d){return (Integer)values.getOrDefault(k,d);}
public SharedPreferences.Editor edit(){return this;}public SharedPreferences.Editor putString(String k,String v){values.put(k,v);return this;}public SharedPreferences.Editor putInt(String k,int v){values.put(k,v);return this;}public boolean commit(){return true;}}
} """,
"android/widget/Toast.java": """package android.widget; public class Toast {public static final int LENGTH_SHORT=0;android.content.Context context;
public static Toast makeText(android.content.Context c,String s,int n){Toast t=new Toast();t.context=c;return t;}public void show(){context.errors++;}}""",
"android/app/WallpaperManager.java": """package android.app; public class WallpaperManager {
public static final int FLAG_SYSTEM=1,FLAG_LOCK=2;public int id=1,writes,legacyWrites,lastFlags,width,height;public String source;
public boolean supported=true,allowed=true,fail;public Runnable duringWrite;
public static WallpaperManager getInstance(android.content.Context c){return c.manager;}
public int getWallpaperId(int flags){return id;}public boolean isWallpaperSupported(){return supported;}
public boolean isSetWallpaperAllowed(){if(android.os.Build.VERSION.SDK_INT<24)throw new AssertionError("API24 called on API23");return allowed;}
public void suggestDesiredDimensions(int w,int h){}
public int setBitmap(android.graphics.Bitmap b,android.graphics.Rect r,boolean backup,int flags)throws java.io.IOException{
 if(fail)throw new java.io.IOException("denied");if(flags!=FLAG_SYSTEM)throw new AssertionError("lockscreen modified");
 if(duringWrite!=null){Runnable task=duringWrite;duringWrite=null;task.run();}writes++;lastFlags=flags;width=b.width;height=b.height;source=b.source;return ++id;}
public void setBitmap(android.graphics.Bitmap b)throws java.io.IOException{if(fail)throw new java.io.IOException("denied");legacyWrites++;width=b.width;height=b.height;source=b.source;}
} """,
"com/smartisanos/launcher/data/Constants.java": "package com.smartisanos.launcher.data; public class Constants {public static boolean ENABLE_LARGE_SCREEN_MODE;public static int window_width=100,window_height=200;}",
"com/smartisanos/launcher/pb.java": "package com.smartisanos.launcher; public class pb {public static String path(String s){return \"Textures/1080p/\"+s;}}",
"com/smartisanos/launcher/theme/v.java": """package com.smartisanos.launcher.theme; public class v {
public String mId,mPackage="theme.package",mPath="";public android.content.res.Resources mResources=new android.content.res.Resources();
public v(String id,String pixel){mId=id;mResources.assets.files.put("Textures/1080p/background.png",("100:150:"+pixel).getBytes(java.nio.charset.StandardCharsets.UTF_8));}}""",
"com/smartisanos/launcher/theme/X.java": "package com.smartisanos.launcher.theme; public class X {public static v theme,previous;public static v eg(){return theme;}public static v fa(String id){return previous;}}",
}

PREFIX = """package com.smartisanos.launcher.theme;
import android.app.Activity;import android.app.WallpaperManager;import android.content.*;import android.content.res.*;
import android.graphics.*;import android.net.Uri;import android.os.*;import android.util.*;
import android.text.TextUtils;import android.widget.Toast;import java.io.InputStream;
public class MaintainedLauncherSettingsHost {
static java.lang.ref.WeakReference<Activity> sDeferredLauncherActivity;
static boolean sLauncherPageTasksPosted;
public static void startup(boolean ready){sDeferredLauncherActivity=new java.lang.ref.WeakReference<Activity>(new Activity());sLauncherPageTasksPosted=ready;}
static final String LOG_TAG="test",WALLPAPER_PREFS="launcher_settings";
static final QueueExecutor THEME_PREVIEW_FETCH_EXECUTOR=new QueueExecutor();
public static class QueueExecutor {public final java.util.ArrayDeque<Runnable> queue=new java.util.ArrayDeque<>();public void execute(Runnable r){queue.add(r);}public void drain(){while(!queue.isEmpty())queue.remove().run();}}
static boolean isTransparentThemeEnabled(Context c){return c.transparent;}
static String selectedWallpaperUri(Context c){return c.uri;}
static String readTransparentPreviousTheme(Context c){return "smartisan_theme_black";}
static void publishDefaultWallpaperSource(Context c, ThemeWallpaperSource s, Bitmap b){}
static Bitmap decodeLauncherWallpaperBitmap(Context c,String uri){try{return BitmapFactory.decodeStream(c.getContentResolver().openInputStream(Uri.parse(uri)));}catch(java.io.IOException e){return null;}}
static Bitmap centerCropToScreen(Context c,Bitmap b){return Bitmap.createScaledBitmap(b,com.smartisanos.launcher.data.Constants.window_width,com.smartisanos.launcher.data.Constants.window_height,true);}
public static void drain(){THEME_PREVIEW_FETCH_EXECUTOR.drain();}
public static int queued(){return THEME_PREVIEW_FETCH_EXECUTOR.queue.size();}
public static void reset(){sDeferredLauncherActivity=null;sLauncherPageTasksPosted=false;sThemeWallpaperRequestKey=null;THEME_PREVIEW_FETCH_EXECUTOR.queue.clear();}
public static void invalidate(){invalidateThemeWallpaperSync();}
"""

TEST = """import android.content.Context;import android.os.Build;
import com.smartisanos.launcher.theme.*;
public class WallpaperTest {
static int checks;static void check(boolean ok,String name){checks++;if(!ok)throw new AssertionError(name);}
static Context start(String id,String marker){MaintainedLauncherSettingsHost.reset();Context c=new Context();X.theme=new v(id,marker);return c;}
static void sync(Context c){MaintainedLauncherSettingsHost.ensureThemeSystemWallpaper(c);MaintainedLauncherSettingsHost.drain();}
public static void main(String[] args) {
for(int sdk:new int[]{23,24,28,31,34,36}) {
 Build.VERSION.SDK_INT=sdk;Context c=start("smartisan_theme_black","black");sync(c);
 check("black".equals(c.manager.source),"active original asset chosen");check(c.manager.width==100&&c.manager.height==200,"screen-sized wallpaper");
 check(sdk<24?c.manager.legacyWrites==1:c.manager.writes==1&&c.manager.lastFlags==1,"system-only destination or legacy API");
 for(int i=0;i<30;i++)MaintainedLauncherSettingsHost.ensureThemeSystemWallpaper(c);
 check(MaintainedLauncherSettingsHost.queued()==0,"hot HOME does not queue wallpaper work");
 int writes=c.manager.writes+c.manager.legacyWrites;MaintainedLauncherSettingsHost.invalidate();sync(c);
 check(c.manager.writes+c.manager.legacyWrites==writes,"persistent fingerprint skips unchanged image");
}
Build.VERSION.SDK_INT=36;Context c=start("smartisan_theme_black","black");c.uri="file://custom";c.resolver.files.put(c.uri,"80:200:photo".getBytes());sync(c);
check("black".equals(c.manager.source),"ordinary theme ignores saved aero/trans photo");
c=start("smartisan_theme_aero","aero-default");c.uri="file://custom";c.resolver.files.put(c.uri,"80:200:photo".getBytes());sync(c);
check("photo".equals(c.manager.source),"aero uses original selected photo");check(c.manager.lastFlags==1,"selected photo writes system only");
c.transparent=true;sync(c);check(c.manager.writes==1,"same photo across aero/transparent does not rewrite wallpaper");
c.uri="file://same-photo-copy";c.resolver.files.put(c.uri,"80:200:photo".getBytes());sync(c);check(c.manager.writes==1,"identical photo under new URI does not rewrite wallpaper");
c=start("smartisan_theme_black","black");c.transparent=true;c.uri="file://custom";c.resolver.files.put(c.uri,"80:200:photo".getBytes());sync(c);
check("photo".equals(c.manager.source),"transparent uses selected photo, not opaque theme");
c=start("smartisan_theme_black","black");c.transparent=true;sync(c);check(c.manager.writes==1 && "black".equals(c.manager.source),"transparent default syncs the active theme background");
c=start("smartisan_theme_black","black");MaintainedLauncherSettingsHost.ensureThemeSystemWallpaper(c);X.theme=new v("smartisan_theme_blue","blue");MaintainedLauncherSettingsHost.ensureThemeSystemWallpaper(c);MaintainedLauncherSettingsHost.drain();
check(c.manager.writes==1&&"blue".equals(c.manager.source),"stale queued theme skipped");
final Context racing=start("smartisan_theme_black","black");racing.manager.duringWrite=()->{X.theme=new v("smartisan_theme_blue","blue");MaintainedLauncherSettingsHost.ensureThemeSystemWallpaper(racing);};sync(racing);
check(racing.manager.writes==2&&"blue".equals(racing.manager.source),"in-flight older write cannot be final wallpaper");
c=start("smartisan_theme_black","black");c.manager.fail=true;sync(c);check(c.manager.writes==0&&c.manager.legacyWrites==0,"failed modern write never falls back to lockscreen-affecting legacy");check(c.errors==1,"sync error visible");
MaintainedLauncherSettingsHost.ensureThemeSystemWallpaper(c);check(MaintainedLauncherSettingsHost.queued()==0,"failure does not retry on every HOME");
c=start("smartisan_theme_black","black");c.manager.allowed=false;sync(c);check(c.manager.writes==0&&c.errors==1,"policy rejection reported");
c=start("smartisan_theme_black","black");sync(c);c.manager.id++;MaintainedLauncherSettingsHost.invalidate();sync(c);check(c.manager.writes==2,"explicit theme selection detects a different external wallpaper ID");
c=start("smartisan_theme_black","black");X.theme.mResources.assets.files.clear();sync(c);check(c.manager.writes==0&&c.errors==1,"missing active asset does not pick guessed background");
c=start("smartisan_theme_trans","alpha-overlay");c.transparent=true;X.previous=new v("smartisan_theme_black","underlying");sync(c);check("underlying".equals(c.manager.source),"transparent default does not write its alpha overlay");
c=start("smartisan_theme_black","black");com.smartisanos.launcher.data.Constants.ENABLE_LARGE_SCREEN_MODE=true;sync(c);check(c.manager.writes==0,"tablet path not changed");
com.smartisanos.launcher.data.Constants.ENABLE_LARGE_SCREEN_MODE=false;c=start("smartisan_theme_black","black");MaintainedLauncherSettingsHost.startup(false);sync(c);check(c.manager.writes==0 && MaintainedLauncherSettingsHost.queued()==0,"startup defers optional wallpaper PNG work");MaintainedLauncherSettingsHost.startup(true);sync(c);check(c.manager.writes==1,"page ready releases latest wallpaper");
System.out.println("PASS "+checks+" actual-owner selection/write/ordering assertions; not OEM pixel proof");
}}
"""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--jdk',type=Path,required=True)
    ap.add_argument('--android-jar',type=Path,required=True)
    args=ap.parse_args()
    owner=(ROOT/'launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java').read_text(encoding='utf-8')
    start=owner.index('    private static final Object SYSTEM_WALLPAPER_WRITE_LOCK')
    end=owner.index('    public static void applyNavigationBarIfChanged(',start)
    with tempfile.TemporaryDirectory(prefix='theme-wallpaper-') as tmp:
        tmp=Path(tmp);classes=tmp/'classes';classes.mkdir();files=[]
        for name,source in STUBS.items():
            p=tmp/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(source,encoding='utf-8');files.append(str(p))
        p=tmp/'com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java';p.write_text(PREFIX+owner[start:end]+'}\n',encoding='utf-8');files.append(str(p))
        p=tmp/'WallpaperTest.java';p.write_text(TEST,encoding='utf-8');files.append(str(p))
        subprocess.run([str(args.jdk/'bin/javac.exe'),'-encoding','UTF-8','-cp',str(args.android_jar),'-d',str(classes),*files],check=True)
        subprocess.run([str(args.jdk/'bin/java.exe'),'-cp',str(classes),'WallpaperTest'],check=True)

if __name__=='__main__': main()
