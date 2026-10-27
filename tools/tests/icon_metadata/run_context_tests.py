"""Exercise the extracted context accessor on ART with a controlled reflection provider."""
import argparse,json,os,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'prepared_icon_source'))
from run_device_tests import block,ROOT
ap=argparse.ArgumentParser(__doc__);ap.add_argument('--serial',required=True);ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
owners=[]
for name,path in [('Before',args.baseline),('After',args.source)]:
 s=path.read_text(encoding='utf8');field='private static volatile android.app.Application sCurrentApplication;';has=field in s
 method=block(s,'    public static Context currentApplicationContext()').replace('android.app.ActivityThread','ContextProbe$Provider')
 owners.append('static class '+name+' {'+(field if has else '')+method+'static void reset(){'+('sCurrentApplication=null;' if has else '')+'}}')
java=r'''
import android.app.Application;import android.content.Context;import android.content.ContextWrapper;import java.util.concurrent.atomic.AtomicInteger;
public class ContextProbe {
 static int checks;static void check(boolean ok,String why){checks++;if(!ok)throw new AssertionError(why);}
 public static class Provider {static final AtomicInteger calls=new AtomicInteger();static Object value;static boolean fail;
  public static Object currentApplication(){calls.incrementAndGet();if(fail)throw new IllegalStateException("fixture");return value;}}
 OWNERS
 static void reset(){Before.reset();After.reset();Provider.calls.set(0);Provider.fail=false;Provider.value=null;}
 public static void main(String[] args)throws Exception{try{runTests();}catch(AssertionError error){System.out.println("ASSERTION_FAILED "+error.getMessage());System.exit(1);}}
 static void runTests()throws Exception{
  reset();check(After.currentApplicationContext()==null,"null");Application app=new Application();Provider.value=app;check(After.currentApplicationContext()==app,"late app");check(Provider.calls.get()==2,"null must retry");
  for(int i=0;i<100;i++)check(After.currentApplicationContext()==app,"identity");check(Provider.calls.get()==2,"successful application reused");
  reset();Provider.fail=true;check(After.currentApplicationContext()==null,"failure null");Provider.fail=false;Provider.value=app;check(After.currentApplicationContext()==app,"failure retries");check(Provider.calls.get()==2,"failure not cached");
  reset();Provider.value=new Object();check(After.currentApplicationContext()==null,"non context");Provider.value=app;check(After.currentApplicationContext()==app,"non context retry");
  reset();Context wrapped=new ContextWrapper(app);Provider.value=wrapped;check(After.currentApplicationContext()==wrapped,"context compatibility");Provider.value=app;check(After.currentApplicationContext()==app,"activity/wrapper not retained");check(Provider.calls.get()==2,"only Application retained");
  reset();Provider.value=app;for(int i=0;i<100;i++)check(Before.currentApplicationContext()==app,"baseline identity");check(Provider.calls.get()==100,"baseline repeat reflection");
  reset();Provider.value=app;check(After.currentApplicationContext()==app,"publish");AtomicInteger failed=new AtomicInteger();Thread[] ts=new Thread[16];for(int i=0;i<ts.length;i++){ts[i]=new Thread(new Runnable(){public void run(){for(int n=0;n<500;n++)if(After.currentApplicationContext()!=Provider.value)failed.incrementAndGet();}});ts[i].start();}for(Thread t:ts)t.join();check(failed.get()==0,"cross thread identity");check(Provider.calls.get()==1,"warm concurrency no reflection");
  System.out.println("RESULT {\"checks\":"+checks+",\"warmConcurrentCalls\":8000,\"provider\":\"controlled; actual Android Application and accessor on ART\"}");
 }
}
'''.replace('OWNERS','\n'.join(owners));src=out/'ContextProbe.java';src.write_text(java,encoding='utf8');classes=out/'classes';classes.mkdir(exist_ok=True);dex=out/'dex';dex.mkdir(exist_ok=True);jdk=Path('E:/Program Files/Android/Android Studio/jbr');sdk=Path('D:/sdk')
def run(cmd,name):
 r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf8',errors='replace',timeout=120);(out/name).write_text(r.stdout+r.stderr,encoding='utf8')
 if r.returncode:raise RuntimeError(name+': '+r.stdout+r.stderr)
 return r.stdout
run([jdk/'bin/javac.exe','-encoding','UTF-8','-source','8','-target','8','-cp',sdk/'platforms/android-36/android.jar','-d',classes,src],'compile.log');run([jdk/'bin/jar.exe','cf',out/'probe.jar','-C',classes,'.'],'jar.log');os.environ['JAVA_HOME']=str(jdk)
run([sdk/'build-tools/37.0.0/d8.bat','--min-api','23','--lib',sdk/'platforms/android-36/android.jar','--output',dex,out/'probe.jar'],'d8.log');adb=[sdk/'platform-tools/adb.exe','-s',args.serial];remote='/data/local/tmp/smartisan-context-probe.dex';run([*adb,'push',dex/'classes.dex',remote],'push.log')
try:
 text=run([*adb,'shell','env','CLASSPATH='+remote,'app_process','/system/bin','ContextProbe'],'device.log');payload=json.loads(next(l[7:]for l in text.splitlines()if l.startswith('RESULT ')));(out/'summary.json').write_text(json.dumps(payload,indent=2));print(text)
finally:run([*adb,'shell','rm',remote],'cleanup.log')
