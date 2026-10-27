"""Exercise the actual override entry with cold/hot resource-owner boundaries.

This verifies table selection and failure/retry behavior, not Android pixels or OEM rendering.
"""
import argparse
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jdk', type=Path, required=True)
    parser.add_argument('--source', type=Path, default=ROOT / 'launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java')
    args = parser.parse_args()
    source = args.source.read_text(encoding='utf-8')
    start = source.index('    public static Drawable iconOverrideDrawable(')
    pos = source.index('{', start) + 1
    depth = 1
    while depth:
        depth += (source[pos] == '{') - (source[pos] == '}')
        pos += 1
    java = PROBE.replace('ACTUAL_METHOD', source[start:pos])
    with tempfile.TemporaryDirectory(prefix='override-resources-') as directory:
        work = Path(directory)
        path = work / 'OverrideResourcesProbe.java'
        path.write_text(java, encoding='utf-8')
        subprocess.run([str(args.jdk / 'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(work), str(path)], check=True)
        subprocess.run([str(args.jdk / 'bin/java.exe'), '-cp', str(work), 'OverrideResourcesProbe'], check=True)


PROBE = r'''
import java.util.*;
public class OverrideResourcesProbe {
 static int checks;static void check(boolean value,String why){checks++;if(!value)throw new AssertionError(why);}
 static class Resources{}static class Drawable{}static class PackageManager{}
 static class Context{final Resources resources=new Resources();Resources getResources(){return resources;}}
 static class ResolveInfo{boolean blocked;}
 static final class Owner {
  static Context app;static Resources sSettingsResources;static final Resources bundled=new Resources();
  static final Drawable chosen=new Drawable();static int loads,scheduled,selections,wrongTable;static boolean fail,unmanaged,throwSelection;
  static Context currentApplicationContext(){return app;}
  static boolean shouldShowIconEntry(ResolveInfo info){return info!=null&&!info.blocked;}
  static void scheduleSettingsResourcesWarm(Context context){scheduled++;}
  static synchronized Resources settingsResources(Context context){if(sSettingsResources!=null)return sSettingsResources;loads++;if(fail)throw new IllegalStateException("fixture resource archive unavailable");sSettingsResources=bundled;return bundled;}
  static Drawable selectedIconDrawable(Context context,ResolveInfo info,Object label,Resources resources){selections++;if(resources!=bundled){wrongTable++;return null;}if(throwSelection)throw new IllegalStateException("fixture drawable unavailable");return unmanaged?null:chosen;}
  ACTUAL_METHOD
  static void reset(){app=new Context();sSettingsResources=null;loads=scheduled=selections=wrongTable=0;fail=unmanaged=throwSelection=false;}
 }
 public static void main(String[] args)throws Exception{
  ResolveInfo info=new ResolveInfo();PackageManager pm=new PackageManager();
  Owner.reset();Owner.app=null;check(Owner.iconOverrideDrawable(info,pm)==null&&Owner.loads==0,"no context keeps null fallback");
  Owner.reset();check(Owner.iconOverrideDrawable(null,pm)==null&&Owner.loads==0,"missing activity does not load resources");
  Owner.reset();info.blocked=true;check(Owner.iconOverrideDrawable(info,pm)==null&&Owner.loads==0,"excluded entry does not load resources");info.blocked=false;
  Owner.reset();check(Owner.iconOverrideDrawable(info,pm)==Owner.chosen,"cold explicit choice uses its defining resource table");
  check(Owner.loads==1&&Owner.scheduled==0&&Owner.wrongTable==0,"cold override uses existing synchronous resource owner");
  for(int i=0;i<20;i++)check(Owner.iconOverrideDrawable(info,pm)==Owner.chosen,"hot explicit choice unchanged");
  check(Owner.loads==1,"resource archive owner reused");
  Owner.reset();Owner.fail=true;check(Owner.iconOverrideDrawable(info,pm)==null,"failed settings archive retains null fallback");
  check(Owner.wrongTable==0&&Owner.selections==0,"failed archive never substitutes launcher table");
  Owner.fail=false;check(Owner.iconOverrideDrawable(info,pm)==Owner.chosen&&Owner.loads==2,"later real request retries failed load");
  Owner.reset();Owner.unmanaged=true;check(Owner.iconOverrideDrawable(info,pm)==null,"unmanaged selection remains null");
  Owner.reset();Owner.throwSelection=true;check(Owner.iconOverrideDrawable(info,pm)==null,"unavailable selected drawable retains fallback");
  Owner.throwSelection=false;check(Owner.iconOverrideDrawable(info,pm)==Owner.chosen&&Owner.loads==1,"selection retry reuses healthy archive");
  Owner.reset();List<Throwable> failures=Collections.synchronizedList(new ArrayList<>());List<Thread> threads=new ArrayList<>();
  for(int i=0;i<12;i++){Thread t=new Thread(()->{try{if(Owner.iconOverrideDrawable(info,pm)!=Owner.chosen)throw new AssertionError("concurrent choice");}catch(Throwable e){failures.add(e);}});threads.add(t);t.start();}
  for(Thread t:threads)t.join();check(failures.isEmpty()&&Owner.loads==1&&Owner.wrongTable==0,"concurrent callers share resource owner");
  System.out.println("PASS OVERRIDE_RESOURCE_OWNER_CHECKS="+checks);
 }
}
'''


if __name__ == '__main__':
    main()
