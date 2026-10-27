"""Exercise the production pack invalidation methods with controlled scheduling.

Host fixtures do not claim Android broadcast, rendering or device acceptance.
"""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def method(source, signature):
    start = source.index(signature)
    end = source.index('{', start) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--jdk', required=True, type=Path)
    parser.add_argument('--source-root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    base = args.source_root / 'launcher/tools/java'
    host = (base / 'com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java').read_text('utf8')
    pack = (base / 'com/smartisanos/home/settings/icons/IconPackManager.java').read_text('utf8')
    update = method(host, '    public static void onIconPackOverridesChanged(')
    reset = method(pack, '    public static synchronized void resetCache()')
    java = r'''
import java.util.*;
public class PackInvalidationProbe {
 static int checks;
 static void check(boolean value,String label) {checks++;if(!value)throw new AssertionError(label);}
 static class Context {Context application=this;String selected="__disabled__",packages="";Context getApplicationContext(){return application;}}
 static class TextUtils {static boolean isEmpty(String s){return s==null||s.length()==0;}}
 static class Looper {static Looper getMainLooper(){return new Looper();}}
 static final List<Runnable> main=new ArrayList<>(),work=new ArrayList<>();
 static class Handler {Handler(Looper l){}void post(Runnable r){main.add(r);}}
 static class RedirectIconInfo {String packageName,mode,pack;RedirectIconInfo(String p,String m,String k){packageName=p;mode=m;pack=k;}}
 static class RedirectIconDB {
  static final String MODE_PACK="pack";static List<RedirectIconInfo> entries=new ArrayList<>();
  static List<RedirectIconInfo> listAllInfo(Context c){return entries;}
  static String modeOf(RedirectIconInfo i){return i.mode;}
  static String packNameOf(RedirectIconInfo i){return i.pack;}
 }
 static class Cache extends HashMap<String,String>{void evictAll(){clear();}}
 static class IconPackManager {
  static long sPackGeneration;static String sLoadedPackage;
  static Object sIconPackList;static Map<String,String> sPackageToDrawable=new HashMap<>(),sComponentToDrawable=new HashMap<>(),sPackMapCache=new HashMap<>();
  static Cache sCandidateCache=new Cache();
  static String getSelectedIconPackPackage(Context c){return c.selected;}
  RESET
 }
 static class IconPreviewRepository {
  enum Priority{P1_ADJACENT}
  static final IconPreviewRepository instance=new IconPreviewRepository();static int invalidations;
  static IconPreviewRepository get(Context c){if(c==null)throw new AssertionError("null application context");return instance;}
  void invalidateCandidates(){invalidations++;}
  void schedule(Priority p,Runnable r){work.add(r);}
 }
 static class Host {
  static Set<String> delivered=new HashSet<>();static int dispatches,replicas,adapters;
  static String allLauncherPackages(Context c){return c.packages;}
  static void applyIconChanges(Context c,Collection<String> p){if(c==null)throw new AssertionError();dispatches++;delivered.addAll(p);}
  static void refreshEnabledDoppelgangerIcons(Context c){replicas++;}
  static void invalidateActiveIconAdapter(){adapters++;}
  UPDATE
 }
 static Context setup(String selected){
  main.clear();work.clear();RedirectIconDB.entries.clear();Host.delivered.clear();Host.dispatches=Host.replicas=Host.adapters=IconPreviewRepository.invalidations=0;
  Context c=new Context();c.selected=selected;c.packages="app.auto,app.without.record,app.custom,app.auto";
  RedirectIconDB.entries.add(new RedirectIconInfo("app.explicit","pack","pack.a"));
  RedirectIconDB.entries.add(new RedirectIconInfo("app.unrelated","pack","pack.b"));
  RedirectIconDB.entries.add(new RedirectIconInfo("app.custom","custom",null));return c;
 }
 static void drain(){while(!work.isEmpty())work.remove(0).run();while(!main.isEmpty())main.remove(0).run();}
 static void updateChecks(){
  Context c=setup("pack.a");Host.onIconPackOverridesChanged(c,"pack.a");
  check(Host.dispatches==0&&work.size()==1,"retain existing worker boundary");
  drain();check(Host.delivered.contains("app.auto")&&Host.delivered.contains("app.without.record"),"selected pack event must refresh global AUTO and absent rows");
  check(Host.delivered.contains("app.explicit"),"retain explicit override refresh");
  check(Host.dispatches==1&&Host.replicas==1&&Host.adapters==1,"merge into one original update and replica/adapter refresh");
  check(Host.delivered.size()==4,"deduplicate global and explicit packages");
  check("custom".equals(RedirectIconDB.entries.get(2).mode)&&"pack.a".equals(c.selected),"invalidation must not change source choices");
  c=setup("pack.a");Host.onIconPackOverridesChanged(c,"pack.b");drain();
  check(Host.delivered.equals(Collections.singleton("app.unrelated")),"unselected pack stays scoped to explicit users");
  c=setup("__disabled__");Host.onIconPackOverridesChanged(c,"pack.a");drain();
  check(Host.delivered.equals(Collections.singleton("app.explicit")),"disabled global pack must not refresh all");
  c=setup("pack.a");Host.onIconPackOverridesChanged(c,"ordinary.app");drain();
  check(Host.dispatches==0&&Host.replicas==0&&Host.adapters==1,"ordinary app event does not refresh all icons");
  c=setup("pack.a");c.packages="";RedirectIconDB.entries.clear();Host.onIconPackOverridesChanged(c,"pack.a");drain();
  check(Host.dispatches==0&&!Host.delivered.contains(""),"empty launcher set does not dispatch empty package");
  c=setup("pack.a");c.application=null;Host.onIconPackOverridesChanged(c,"pack.a");drain();
  check(Host.delivered.contains("app.auto"),"retain supplied context if application is unavailable");
  c=setup("pack.a");Host.onIconPackOverridesChanged(null,"pack.a");Host.onIconPackOverridesChanged(c,"");Host.onIconPackOverridesChanged(c,null);
  check(work.isEmpty()&&main.isEmpty(),"invalid events have no work");
  c=setup("pack.a");Host.onIconPackOverridesChanged(c,"pack.a");c.selected="pack.b";drain();
  check(Host.delivered.contains("app.auto"),"selection at event time survives a later preference change");
 }
 static void resetChecks(){
  IconPackManager.sCandidateCache.put("app/Activity","old");IconPackManager.sLoadedPackage="pack.a";IconPackManager.sIconPackList=new Object();
  IconPackManager.sPackageToDrawable.put("app","old");IconPackManager.sComponentToDrawable.put("app/Activity","old");IconPackManager.sPackMapCache.put("pack.a","old");
  long generation=IconPackManager.sPackGeneration;IconPackManager.resetCache();
  check(IconPackManager.sCandidateCache.isEmpty(),"reset must evict candidate metadata as well as maps");
  check(IconPackManager.sPackGeneration==generation+1,"reset advances existing generation");
  check(IconPackManager.sLoadedPackage==null&&IconPackManager.sIconPackList==null,"reset selected and installed metadata");
  check(IconPackManager.sPackageToDrawable.isEmpty()&&IconPackManager.sComponentToDrawable.isEmpty()&&IconPackManager.sPackMapCache.isEmpty(),"reset all original artwork maps");
  IconPackManager.resetCache();check(IconPackManager.sCandidateCache.isEmpty(),"empty reset is safe");
 }
 public static void main(String[] args){if(args.length>0&&args[0].equals("reset"))resetChecks();else updateChecks();System.out.println("PASS "+checks+" checks");}
}
'''.replace('RESET', reset).replace('UPDATE', update)
    args.output.mkdir(parents=True, exist_ok=True)
    source = args.output / 'PackInvalidationProbe.java'
    source.write_text(java, 'utf8')
    subprocess.run([str(args.jdk / 'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(args.output), str(source)], check=True)
    results = []
    for mode in ['update', 'reset']:
        result = subprocess.run([str(args.jdk / 'bin/java.exe'), '-cp', str(args.output), 'PackInvalidationProbe', mode], capture_output=True, text=True)
        print(mode, result.stdout, result.stderr, end='')
        (args.output / (mode + '.log')).write_text(result.stdout + result.stderr, 'utf8')
        results.append(result.returncode)
    if any(results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
