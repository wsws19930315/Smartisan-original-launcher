"""Measure real Android custom-icon metadata reads without accessing installed app data."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[3]
JAVA = ROOT / 'launcher/tools/java'


def block(source, marker):
    start = source.index(marker)
    end = source.index('{', start) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def main():
    ap = argparse.ArgumentParser(__doc__)
    for key in ('serial', 'jdk', 'sdk', 'output', 'baseline'):
        ap.add_argument('--' + key, required=True)
    ap.add_argument('--allow-full-reads', action='store_true')
    args = ap.parse_args()
    out, jdk, sdk, baseline = map(Path, (args.output, args.jdk, args.sdk, args.baseline))
    out.mkdir(parents=True, exist_ok=True)
    classes, dex = out / 'classes', out / 'dex'
    classes.mkdir(exist_ok=True)
    dex.mkdir(exist_ok=True)

    def run(command, name):
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                                encoding='utf8', errors='replace', timeout=90)
        (out / name).write_text(result.stdout + result.stderr, encoding='utf8')
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        return result.stdout

    sources = []

    def write(name, source):
        path = out / 'src' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding='utf8')
        sources.append(path)

    manager = 'com/smartisanos/home/settings/icons/IconManager.java'
    sources.append(JAVA / manager)
    write(manager.replace('IconManager', 'BaselineIconManager'),
          (baseline / 'IconManager.java').read_text(encoding='utf8').replace('IconManager', 'BaselineIconManager'))
    for name in ('RedirectIconDB', 'RedirectIconInfo'):
        sources.append(JAVA / 'com/smartisanos/launcher/data/redirectIcon' / (name + '.java'))
    write('com/smartisanos/home/settings/icons/IconPreviewRepository.java', '''package com.smartisanos.home.settings.icons;
public class IconPreviewRepository {
 public static IconPreviewRepository get(android.content.Context c){return new IconPreviewRepository();}
 public android.graphics.Bitmap getCachedOfficialIcon(String p,String c,long u,long v,int s){return null;}
}''')
    write('com/smartisanos/launcher/model/ProfileRepository.java', '''package com.smartisanos.launcher.model;
public class ProfileRepository {public static java.util.List<android.content.pm.ResolveInfo> queryLauncherActivities(
android.content.pm.PackageManager p,android.content.Intent i,int f){return java.util.Collections.emptyList();}}''')
    for name, path in [('MaintainedLauncherSettingsHost', JAVA / 'com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java'),
                       ('BaselineHost', baseline / 'MaintainedLauncherSettingsHost.java')]:
        source = path.read_text(encoding='utf8')
        methods = '\n'.join(block(source, marker) for marker in (
            'public static String displayNameForDesktopItem(',
            'private static boolean isOriginalIconForced(',
            'private static boolean hasManualIconOverride('))
        write('com/smartisanos/launcher/theme/' + name + '.java', '''package com.smartisanos.launcher.theme;
import android.content.*;import android.content.pm.*;import android.text.TextUtils;
import com.smartisanos.launcher.data.redirectIcon.*;
public class NAME {
 public static Context app;
 static Context currentApplicationContext(){return app;}
 public static boolean original(ResolveInfo i){return isOriginalIconForced(i);}
 public static boolean manual(Context c,ActivityInfo i){return hasManualIconOverride(c,i);}
METHODS
}'''.replace('NAME', name).replace('METHODS', methods))
    write('IconMetadataProbe.java', PROBE)
    run([jdk / 'bin/javac.exe', '-encoding', 'UTF-8', '-source', '8', '-target', '8',
         '-cp', sdk / 'platforms/android-36/android.jar', '-d', classes, *sources], 'compile.log')
    run([jdk / 'bin/jar.exe', 'cf', out / 'probe.jar', '-C', classes, '.'], 'jar.log')
    os.environ['JAVA_HOME'] = str(jdk)
    run([sdk / 'build-tools/37.0.0/d8.bat', '--min-api', '26', '--output', dex, out / 'probe.jar'], 'dex.log')
    adb = [sdk / 'platform-tools/adb.exe', '-s', args.serial]
    remote = '/data/local/tmp/icon-metadata-' + uuid.uuid4().hex
    (out / 'remote.txt').write_text(remote, encoding='utf8')
    run([*adb, 'shell', 'mkdir', remote], 'mkdir.log')
    run([*adb, 'push', dex / 'classes.dex', remote + '/probe.dex'], 'push.log')
    result = run([*adb, 'shell', 'CLASSPATH=' + remote + '/probe.dex app_process /system/bin IconMetadataProbe '
                  + remote + (' baseline' if args.allow_full_reads else '')], 'device.log')
    payload = json.loads(next(line[7:] for line in result.splitlines() if line.startswith('RESULT ')))
    (out / 'summary.json').write_text(json.dumps(payload, indent=2), encoding='utf8')
    print(result)


PROBE = r'''
import android.content.*;import android.content.pm.*;import android.graphics.*;import android.os.*;
import java.io.*;import java.util.*;import java.lang.reflect.*;
import org.json.*;
import com.smartisanos.home.settings.icons.*;
import com.smartisanos.launcher.data.redirectIcon.*;
import com.smartisanos.launcher.theme.*;
public class IconMetadataProbe {
 static int checks;
 static void check(boolean b,String m){checks++;if(!b)throw new AssertionError(m);}
 static class Fixture extends ContextWrapper {
  final Map<String,Object> values=new HashMap<>(); final File dir; int fileReads;
  final SharedPreferences prefs=(SharedPreferences)Proxy.newProxyInstance(SharedPreferences.class.getClassLoader(),
   new Class[]{SharedPreferences.class},(p,m,a)->{
    if(m.getName().startsWith("get"))return values.containsKey(a[0])?values.get(a[0]):a[1];
    throw new UnsupportedOperationException(m.getName());
   });
  Fixture(File d){super(null);dir=d;}
  public Context getApplicationContext(){return this;}
  public SharedPreferences getSharedPreferences(String n,int mode){return prefs;}
  public File getFilesDir(){fileReads++;return dir;}
  void record(String pkg,String mode,String label){String p="r."+pkg+";Main.";
   values.put(p+"pkg",pkg);values.put(p+"cmp","Main");values.put(p+"drawable",mode);
   values.put(p+"display_name",label);values.put(p+"use",true);values.put(p+"owner",7L);
  }
 }
 static File image(Fixture c,String pkg){return new File(new File(c.dir,"redirect_icons"),Integer.toHexString((pkg+";Main").hashCode())+".png");}
 static volatile String sink;
 static long[] sample(Runnable r){long[] result=new long[2];long cpu=Debug.threadCpuTimeNanos(),wall=System.nanoTime();
  for(int i=0;i<12;i++)r.run();result[0]=System.nanoTime()-wall;result[1]=Debug.threadCpuTimeNanos()-cpu;return result;}
 public static void main(String[] args){try{runProbe(args);System.exit(0);}catch(Throwable error){error.printStackTrace();System.exit(1);}}
 static void runProbe(String[] args)throws Exception {
  System.out.println("PROBE_START");
  Fixture c=new Fixture(new File(args[0]));new File(c.dir,"redirect_icons").mkdirs();
  MaintainedLauncherSettingsHost.app=c;BaselineHost.app=c;
  Bitmap b=Bitmap.createBitmap(512,512,Bitmap.Config.ARGB_8888);int[] pixels=new int[512*512];Random random=new Random(13);
  for(int i=0;i<pixels.length;i++)pixels[i]=random.nextInt();b.setPixels(pixels,0,512,0,0,512,512);
  try(FileOutputStream out=new FileOutputStream(image(c,"fixture.custom"))){check(b.compress(Bitmap.CompressFormat.PNG,100,out),"fixture PNG");}b.recycle();
  c.record("fixture.custom","custom","Custom label");c.record("fixture.broken","custom","Broken label");
  System.out.println("PROBE_IMAGE_READY");
  try(FileOutputStream out=new FileOutputStream(image(c,"fixture.broken"))){out.write(new byte[]{1,2,3});}
  IconManager current=new IconManager(c);BaselineIconManager old=new BaselineIconManager(c);
  System.out.println("PROBE_MANAGERS_READY");
  boolean allow=args.length>1;
  for(String mode:new String[]{"auto","original","resource:fixture","pack:fixture#one","custom"}){
   System.out.println("PROBE_MODE "+mode);
   c.record("fixture.mode",mode,"Alias");
   RedirectIconInfo metadata=RedirectIconDB.getRedirectIconMetadata(c,"fixture.mode","Main");
   check(mode.equals(metadata.drawableName)&&metadata.ownerId==7&&metadata.iconData==null,"metadata identity "+mode);
   ActivityInfo ai=new ActivityInfo();ai.packageName="fixture.mode";ai.name="Main";ResolveInfo ri=new ResolveInfo();ri.activityInfo=ai;
   c.fileReads=0;
   boolean original=MaintainedLauncherSettingsHost.original(ri);
   if(!allow)check(c.fileReads==0,"original mode check avoids image file "+mode);
   check(original==BaselineHost.original(ri),"original mode unchanged "+mode);
   c.fileReads=0;boolean manual=MaintainedLauncherSettingsHost.manual(c,ai);
   if(!allow)check(c.fileReads==0,"manual mode check avoids image file "+mode);
   check(manual==BaselineHost.manual(c,ai),"manual mode unchanged "+mode);
  }
  for(String pkg:new String[]{"fixture.custom","fixture.broken","fixture.missing"}){
   System.out.println("PROBE_LABEL "+pkg);
   c.fileReads=0;String label=current.getLableForPackage(pkg,"Main");
   check(label.equals(old.getLableForPackage(pkg,"Main")),"label and corrupt-image independence "+pkg);
   c.fileReads=0;current.getLableForPackage(pkg,"Main");
   if(!allow)check(c.fileReads==0,"label must not read custom image file "+pkg);
   c.fileReads=0;
   check(MaintainedLauncherSettingsHost.displayNameForDesktopItem(pkg,"Main","Fallback")
    .equals(BaselineHost.displayNameForDesktopItem(pkg,"Main","Fallback")),"desktop title unchanged "+pkg);
   c.fileReads=0;MaintainedLauncherSettingsHost.displayNameForDesktopItem(pkg,"Main","Fallback");
   if(!allow)check(c.fileReads==0,"desktop title must not read custom image file "+pkg);
  }
  byte[] data=RedirectIconDB.getRedirectIcon(c,"fixture.custom","Main");
  check(data!=null,"image-consuming API retains bytes");Bitmap actual=BitmapFactory.decodeByteArray(data,0,data.length);
  check(actual.getWidth()==512&&actual.getHeight()==512,"image dimensions unchanged");int[] decoded=new int[pixels.length];
  actual.getPixels(decoded,0,512,0,0,512,512);actual.recycle();
  // PNG normalization is retained; compare against the same real decode path, including premultiplied alpha.
  Bitmap expected=BitmapFactory.decodeFile(image(c,"fixture.custom").getAbsolutePath());int[] expectedPixels=new int[pixels.length];
  expected.getPixels(expectedPixels,0,512,0,0,512,512);expected.recycle();check(Arrays.equals(decoded,expectedPixels),"normalized pixels unchanged");
  check(RedirectIconDB.getRedirectIcon(c,"fixture.broken","Main")==null,"bad image fallback unchanged");
  Runnable a=()->{sink=old.getLableForPackage("fixture.custom","Main");sink=BaselineHost.displayNameForDesktopItem("fixture.custom","Main","Fallback");};
  Runnable z=()->{sink=current.getLableForPackage("fixture.custom","Main");sink=MaintainedLauncherSettingsHost.displayNameForDesktopItem("fixture.custom","Main","Fallback");};
  a.run();z.run();JSONArray before=new JSONArray(),after=new JSONArray();
  for(int i=0;i<5;i++){long[] x,y;if(i%2==0){x=sample(a);y=sample(z);}else{y=sample(z);x=sample(a);}
   before.put(new JSONArray(x));after.put(new JSONArray(y));}
  c.fileReads=0;sample(z);int currentReads=c.fileReads;c.fileReads=0;sample(a);int baselineReads=c.fileReads;
  System.out.println("RESULT "+new JSONObject().put("checks",checks).put("baselineWallCpuNs",before).put("currentWallCpuNs",after)
   .put("labelsPerSample",24).put("baselineFileReads",baselineReads).put("currentFileReads",currentReads).put("bitmapSize",512));
  System.out.println("PASS ICON_METADATA_ANDROID");
 }
}
'''


if __name__ == '__main__':
    main()
