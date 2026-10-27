"""Exercise extracted production resource-ID metadata and live candidate checks on Android."""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]


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
    ap.add_argument('--serial', required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--source', type=Path, default=ROOT/'launcher/tools/java/com/smartisanos/home/settings/icons/IconPreviewRepository.java')
    args = ap.parse_args()
    source = args.source.read_text(encoding='utf8')
    metadata = source[source.index('    private static final int DRAWABLE_ID_OWNER_LIMIT'):source.index('    public interface Callback')]
    candidate = block(source, 'private boolean checkCandidateExists(')
    trim = block(source, 'public void trimMemory(int level)')
    config = block(source, '@Override public void onConfigurationChanged(')
    low = block(source, '@Override public void onLowMemory(')
    java = PROBE.replace('@METADATA@', metadata).replace('@CANDIDATE@', candidate).replace('@TRIM@', trim).replace('@CONFIG_CALLBACK@', config).replace('@LOW_CALLBACK@', low)
    out = args.output
    (out/'classes').mkdir(parents=True, exist_ok=True)
    (out/'dex').mkdir(exist_ok=True)
    (out/'ResourceIdProbe.java').write_text(java, encoding='utf8')
    jdk = Path('E:/Program Files/Android/Android Studio/jbr/bin')
    sdk = Path('D:/sdk')

    def run(cmd, name):
        r = subprocess.run(list(map(str, cmd)), capture_output=True, timeout=120)
        (out/name).write_bytes(r.stdout+r.stderr)
        if r.returncode:
            raise RuntimeError((r.stdout+r.stderr).decode(errors='replace'))
        return r.stdout.decode(errors='replace')

    run([jdk/'javac.exe', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-cp', sdk/'platforms/android-36/android.jar', '-d', out/'classes', out/'ResourceIdProbe.java'], 'javac.log')
    run([sdk/'build-tools/37.0.0/d8.bat', '--lib', sdk/'platforms/android-36/android.jar', '--output', out/'dex', *sorted((out/'classes').glob('*.class'))], 'd8.log')
    adb = [sdk/'platform-tools/adb.exe', '-s', args.serial]
    remote = '/data/local/tmp/resource-id-probe.dex'
    run([*adb, 'push', out/'dex/classes.dex', remote], 'push.log')
    try:
        print(run([*adb, 'shell', 'CLASSPATH='+remote, 'app_process', '/system/bin', 'ResourceIdProbe'], 'result.log'))
    finally:
        run([*adb, 'shell', 'rm', remote], 'cleanup.log')


PROBE = r'''
import android.content.res.*;import android.content.ComponentCallbacks2;import android.util.LruCache;
import android.text.TextUtils;import java.io.*;import java.util.*;import java.util.concurrent.*;
public class ResourceIdProbe implements ComponentCallbacks2 {
 @METADATA@
 static int checks;
 static void check(boolean v,String msg){checks++;if(!v){System.out.println("FAIL RESOURCE_ID_ANDROID: "+msg);throw new AssertionError(msg);}}
 static class Spy extends Resources {
  final Configuration cfg=new Configuration(Resources.getSystem().getConfiguration());
  final Map<String,Integer> values=new HashMap<>();int calls;boolean fail;
  volatile CountDownLatch entered,proceed;
  Spy(){super(Resources.getSystem().getAssets(),Resources.getSystem().getDisplayMetrics(),new Configuration(Resources.getSystem().getConfiguration()));}
  @Override public Configuration getConfiguration(){return cfg;}
  @Override public int getIdentifier(String name,String type,String pkg){
   int value;CountDownLatch wait;
   synchronized(this){calls++;if(fail){fail=false;throw new Resources.NotFoundException("controlled");}value=values.containsKey(pkg+":"+name)?values.get(pkg+":"+name):0;wait=proceed;}
   if(wait!=null){entered.countDown();try{if(!wait.await(5,TimeUnit.SECONDS))throw new AssertionError("barrier deadline");}catch(InterruptedException e){throw new AssertionError(e);}}
   return value;
  }
 }
 static class App {final Resources r;final File dir;App(Resources res,File d){r=res;dir=d;}Resources getResources(){return r;}String getPackageName(){return "probe";}File getFilesDir(){return dir;}}
 static class IconLibraryCatalog {static IconLibraryCatalog current;final Set<String> names=new HashSet<>();static IconLibraryCatalog peek(){return current;}boolean contains(String k){return names.contains(k);}}
 static class IconPackManager {static void trimMemory(App a,int level){}}
 static class Cache {void evictAll(){}void trimToSize(int n){}int maxSize(){return 10;}}
 final Cache cache=new Cache();boolean pauseP2;App app;Map<String,List<String>> sVariantsMap=new HashMap<>();
 @CANDIDATE@
 @TRIM@
 @CONFIG_CALLBACK@
 @LOW_CALLBACK@
 @Override public void onTrimMemory(int level){trimMemory(level);}
 public static void main(String[] args)throws Exception {
  ResourceIdProbe probe=new ResourceIdProbe();Spy a=new Spy();
  a.values.put("probe:a",11);clearDrawableResourceIds();
  check(drawableResourceId(a,"a","probe")==11,"first positive");
  for(int i=0;i<50;i++)check(drawableResourceId(a,"a","probe")==11,"positive hit");
  check(a.calls==1,"one native positive lookup");
  check(drawableResourceId(a,"missing","probe")==0,"first missing ID");
  check(drawableResourceId(a,"missing","probe")==0&&a.calls==2,"zero IDs reused as table metadata only");
  a.values.put("other:a",22);check(drawableResourceId(a,"a","other")==22,"package namespace separated");
  Spy b=new Spy();b.values.put("probe:a",33);check(drawableResourceId(b,"a","probe")==33,"Resources identity separated");
  a.values.put("probe:a",44);a.cfg.orientation=a.cfg.orientation==1?2:1;
  check(drawableResourceId(a,"a","probe")==44,"configuration invalidates automatically");
  a.values.put("probe:a",55);probe.onConfigurationChanged(new Configuration());
  check(drawableResourceId(a,"a","probe")==55,"configuration callback clears tables");
  a.values.put("probe:a",66);probe.trimMemory(ComponentCallbacks2.TRIM_MEMORY_RUNNING_LOW);
  check(drawableResourceId(a,"a","probe")==66,"trim clears metadata");
  a.values.put("probe:a",77);probe.onLowMemory();check(drawableResourceId(a,"a","probe")==77,"low memory clears metadata");
  clearDrawableResourceIds();int before=a.calls;drawableResourceId(a,"first","probe");
  for(int i=0;i<DRAWABLE_ID_LIMIT;i++)drawableResourceId(a,"key"+i,"probe");
  drawableResourceId(a,"first","probe");check(a.calls==before+DRAWABLE_ID_LIMIT+2,"ID capacity enforced");
  synchronized(drawableResourceIds){check(drawableResourceIds.get(a).ids.size()<=DRAWABLE_ID_LIMIT,"bounded entries");}
  clearDrawableResourceIds();before=a.calls;drawableResourceId(a,"a","probe");
  for(int i=0;i<DRAWABLE_ID_OWNER_LIMIT;i++)drawableResourceId(new Spy(),"a","probe");
  drawableResourceId(a,"a","probe");check(a.calls==before+2,"owner capacity evicts old resource table");
  synchronized(drawableResourceIds){check(drawableResourceIds.size()<=DRAWABLE_ID_OWNER_LIMIT,"bounded owners");}
  clearDrawableResourceIds();a.fail=true;before=a.calls;
  try{drawableResourceId(a,"throw","probe");throw new AssertionError("exception swallowed");}catch(Resources.NotFoundException expected){}
  drawableResourceId(a,"throw","probe");check(a.calls==before+2,"exceptions are never cached");
  File root=new File("/data/local/tmp/resource-id-probe-files");File dir=new File(root,"online_icon_cache_v4");dir.mkdirs();File icon=new File(dir,"late.png");icon.delete();
  probe.app=new App(a,root);clearDrawableResourceIds();check(!probe.checkCandidateExists("late"),"initial full candidate miss");before=a.calls;
  try(FileOutputStream out=new FileOutputStream(icon)){out.write(1);}
  check(probe.checkCandidateExists("late")&&a.calls==before,"late downloaded file remains visible with cached zero ID");icon.delete();
  check(!probe.checkCandidateExists("late"),"deleted disk file no longer visible");
  probe.sVariantsMap.put("late",Arrays.asList("variant"));check(probe.checkCandidateExists("late"),"late variants checked live");probe.sVariantsMap.clear();
  IconLibraryCatalog.current=new IconLibraryCatalog();IconLibraryCatalog.current.names.add("late");check(probe.checkCandidateExists("late"),"late catalog checked live");IconLibraryCatalog.current=null;
  dir.delete();root.delete();
  for(boolean configurationRace:new boolean[]{false,true}){
   clearDrawableResourceIds();final Spy s=new Spy();s.values.put("probe:race",1);s.entered=new CountDownLatch(1);s.proceed=new CountDownLatch(1);
   final Throwable[] error=new Throwable[1];Thread worker=new Thread(()->{try{check(drawableResourceId(s,"race","probe")==1,"in-flight lookup result preserved");}catch(Throwable t){error[0]=t;}});
   worker.start();check(s.entered.await(5,TimeUnit.SECONDS),"framework lookup reached barrier");
   s.values.put("probe:race",2);if(configurationRace)s.cfg.orientation=s.cfg.orientation==1?2:1;else clearDrawableResourceIds();
   s.proceed.countDown();worker.join(5000);check(!worker.isAlive()&&error[0]==null,"lookup completes outside lock");s.proceed=null;
   check(drawableResourceId(s,"race","probe")==2&&s.calls==2,"stale in-flight miss never repopulates invalid table");
  }
  clearDrawableResourceIds();Resources actual=Resources.getSystem();int expected=actual.getIdentifier("sym_def_app_icon","drawable","android");
  check(expected!=0&&drawableResourceId(actual,"sym_def_app_icon","android")==expected,"real framework resource ID equal");
  check(drawableResourceId(actual,"sym_def_app_icon","android")==expected,"real framework warm lookup equal");
  System.out.println("PASS RESOURCE_ID_ANDROID checks="+checks+" native resource identity/configuration/callback/trim/bounds/races/live file/catalog/variants");
 }
}
'''

if __name__ == '__main__':
    main()
