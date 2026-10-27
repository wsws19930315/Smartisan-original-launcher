"""Exercise production custom-icon storage and backup with Android Bitmap/JSON and real files.

Preferences and Context are isolated doubles. No installed launcher data is accessed.
The optional before directory must contain saved RedirectIconDB.java/IconBackupCodec.java.
"""
import argparse
import os
from pathlib import Path
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[3]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ('jdk', 'sdk', 'out'):
        ap.add_argument('--' + key, type=Path, required=True)
    ap.add_argument('--serial', required=True)
    ap.add_argument('--before', type=Path)
    args = ap.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    classes, dex = out / 'classes', out / 'dex'
    classes.mkdir(exist_ok=True)
    dex.mkdir(exist_ok=True)

    def run(command, log):
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=120)
        (out / log).write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        return result.stdout

    java = ROOT / 'launcher/tools/java/com/smartisanos/launcher'
    if not args.before:
        host = (java / 'theme/MaintainedLauncherSettingsHost.java').read_text(encoding='utf-8')
        importer = host.split('private static byte[] saveCustomIcon(', 1)[1].split('private static Bitmap squareIcon(', 1)[0]
        assert 'RedirectIconDB.customFileName(parts[0], parts[1])' in importer
        assert 'hashCode()' not in importer
        print('PASS CUSTOM_IMPORT_FILENAME_OWNER_CHECK=1')
    probe = out / 'CustomStorageProbe.java'
    probe.write_text(PROBE, encoding='utf-8')
    controller = out / 'DesktopBackupController.java'
    controller.write_text('package com.smartisanos.launcher.backup; public class DesktopBackupController {'
                          'public static class CancellationToken { public void throwIfCancelled() '
                          'throws java.io.IOException {} }}', encoding='utf-8')
    sources = [probe, controller, java / 'backup/BackupFileUtils.java',
               java / 'data/redirectIcon/RedirectIconInfo.java']
    for folder, name in [('data/redirectIcon', 'RedirectIconDB'), ('backup', 'IconBackupCodec')]:
        sources.append(args.before / (name + '.java') if args.before else java / folder / (name + '.java'))
    run([args.jdk / 'bin/javac.exe', '-encoding', 'UTF-8', '-source', '8', '-target', '8',
         '-cp', args.sdk / 'platforms/android-36/android.jar', '-d', classes, *sources], 'compile.log')
    run([args.jdk / 'bin/jar.exe', 'cf', out / 'probe.jar', '-C', classes, '.'], 'jar.log')
    os.environ['JAVA_HOME'] = str(args.jdk)
    run([args.sdk / 'build-tools/37.0.0/d8.bat', '--min-api', '23', '--output', dex,
         out / 'probe.jar'], 'dex.log')
    adb = [args.sdk / 'platform-tools/adb.exe', '-s', args.serial]
    remote = '/data/local/tmp/smartisan-custom-storage-' + uuid.uuid4().hex
    (out / 'remote.txt').write_text(remote, encoding='utf-8')
    run([*adb, 'shell', 'mkdir', remote], 'mkdir.log')
    try:
        run([*adb, 'push', dex / 'classes.dex', remote + '/probe.dex'], 'push.log')
        print(run([*adb, 'shell', 'CLASSPATH=' + remote + '/probe.dex app_process /system/bin '
                   'com.smartisanos.launcher.backup.CustomStorageProbe ' + remote + '/data'], 'device.log'))
    finally:
        # Probe finally deletes only its own fixture data. Keep unexpected leftovers visible.
        for name in ('probe.dex', 'oat/arm64/probe.odex', 'oat/arm64/probe.vdex',
                     'oat/x86_64/probe.odex', 'oat/x86_64/probe.vdex'):
            subprocess.run([*map(str, adb), 'shell', 'rm', '-f', remote + '/' + name], capture_output=True)
        subprocess.run([*map(str, adb), 'shell', 'rmdir', remote + '/oat/arm64', remote + '/oat/x86_64',
                        remote + '/oat', remote], capture_output=True)


PROBE = r'''
package com.smartisanos.launcher.backup;
import android.content.*;import android.graphics.*;import java.io.*;import java.util.*;
import java.lang.reflect.*;import org.json.*;
import com.smartisanos.launcher.data.redirectIcon.*;
public final class CustomStorageProbe {
 static int checks;
 static void check(boolean value,String message){checks++;if(!value)throw new AssertionError(message);}
 static class Fixture extends ContextWrapper {
  final File dir;final Map<String,Object> values=new HashMap<>();
  final SharedPreferences prefs=(SharedPreferences)Proxy.newProxyInstance(SharedPreferences.class.getClassLoader(),new Class[]{SharedPreferences.class},(p,m,a)->{
   if(m.getName().equals("edit"))return editor();
   if(m.getName().equals("getAll"))return new HashMap<>(values);
   if(m.getName().startsWith("get"))return values.containsKey(a[0])?values.get(a[0]):a[1];
   throw new UnsupportedOperationException(m.getName());
  });
  Fixture(File dir){super(null);this.dir=dir;dir.mkdirs();}
  Object editor(){final Map<String,Object> pending=new HashMap<>();final boolean[] clear={false};
   return Proxy.newProxyInstance(SharedPreferences.Editor.class.getClassLoader(),new Class[]{SharedPreferences.Editor.class},(p,m,a)->{
    String n=m.getName();if(n.startsWith("put")){pending.put((String)a[0],a[1]);return p;}
    if(n.equals("remove")){pending.put((String)a[0],null);return p;}
    if(n.equals("clear")){clear[0]=true;return p;}
    if(n.equals("apply")||n.equals("commit")){if(clear[0])values.clear();for(String k:pending.keySet()){Object v=pending.get(k);if(v==null)values.remove(k);else values.put(k,v);}return n.equals("commit")?Boolean.TRUE:null;}
    throw new UnsupportedOperationException(n);
   });}
  public Context getApplicationContext(){return this;}
  public SharedPreferences getSharedPreferences(String name,int mode){return prefs;}
  public File getFilesDir(){return dir;}
  void custom(String pkg){String prefix="r."+pkg+";Main.";values.put(prefix+"pkg",pkg);values.put(prefix+"cmp","Main");values.put(prefix+"drawable","custom");values.put(prefix+"use",true);}
 }
 static byte[] png(int color){Bitmap b=Bitmap.createBitmap(16,16,Bitmap.Config.ARGB_8888);b.eraseColor(color);ByteArrayOutputStream o=new ByteArrayOutputStream();b.compress(Bitmap.CompressFormat.PNG,100,o);b.recycle();return o.toByteArray();}
 static int color(byte[] bytes){check(bytes!=null,"image bytes exist");Bitmap b=BitmapFactory.decodeByteArray(bytes,0,bytes.length);check(b!=null,"image decodes");int c=b.getPixel(8,8);b.recycle();return c;}
 static int read(Fixture c,String pkg){return color(RedirectIconDB.getRedirectIcon(c,pkg,"Main"));}
 public static void main(String[] args){File root=new File(args[0]);int status=0;try{run(root);System.out.println("PASS CUSTOM_STORAGE_CHECKS="+checks);}
 catch(Throwable e){e.printStackTrace();status=1;}finally{BackupFileUtils.deleteRecursively(root);}if(status!=0)System.exit(status);}
 static void run(File root)throws Exception {
  String a="fixture.Aa",b="fixture.BB";check((a+";Main").hashCode()==(b+";Main").hashCode(),"known legacy hash collision");
  byte[] red=png(0xffff0000),green=png(0xff00ff00),blue=png(0xff0000ff);
  Fixture c=new Fixture(new File(root,"current"));c.custom(a);c.custom(b);
  String oldName=Integer.toHexString((a+";Main").hashCode())+".png";
  File old=new File(c.dir,"redirect_icons/"+oldName);BackupFileUtils.writeBytes(old,blue);
  check(read(c,a)==0xff0000ff,"old redirect_icons readable");
  RedirectIconDB.updateCustomIcon(c,a,"Main",red);RedirectIconDB.updateCustomIcon(c,b,"Main",green);
  check(read(c,a)==0xffff0000,"colliding identities preserve first image");check(read(c,b)==0xff00ff00,"colliding identities preserve second image");
  check(Arrays.equals(BackupFileUtils.readBytes(old,10000),blue),"new writes do not overwrite shared legacy file");
  RedirectIconDB.resetIconToDefault(c,a,"Main");check(read(c,b)==0xff00ff00,"reset does not delete other image");
  check(old.exists(),"reset leaves potentially shared legacy file intact");
  RedirectIconDB.updateCustomIcon(c,a,"Main",red);
  File extracted=new File(root,"extracted");JSONObject encoded=IconBackupCodec.encode(c,new File(extracted,"icons/custom"));
  JSONArray records=encoded.getJSONArray("records");check(records.length()==2,"both records exported");
  check(!records.getJSONObject(0).getString("customFile").equals(records.getJSONObject(1).getString("customFile")),"archive names distinct");
  Fixture restored=new Fixture(new File(root,"restored"));IconBackupCodec.restore(restored,encoded,extracted);
  check(read(restored,a)==0xffff0000&&read(restored,b)==0xff00ff00,"restore keeps colliding identities separate");
  File legacyRoot=new File(root,"legacy-extracted");BackupFileUtils.writeBytes(new File(legacyRoot,"icons/custom/"+oldName),blue);
  JSONObject oldRecord=new JSONObject().put("packageName",a).put("componentName","Main").put("mode","custom").put("drawableName","custom").put("use",true).put("customFile",oldName);
  Fixture oldRestore=new Fixture(new File(root,"old-restored"));IconBackupCodec.restore(oldRestore,new JSONObject().put("records",new JSONArray().put(oldRecord)),legacyRoot);
  check(read(oldRestore,a)==0xff0000ff,"old archive arbitrary valid file name still restores");
  Fixture oldest=new Fixture(new File(root,"old-custom"));oldest.custom(a);File oldestFile=new File(oldest.dir,"custom_icons/"+oldName);BackupFileUtils.writeBytes(oldestFile,blue);
  check(read(oldest,a)==0xff0000ff,"custom_icons legacy readable");check(oldestFile.exists(),"legacy read never renames shared file");
 }
}
'''


if __name__ == '__main__':
    main()
