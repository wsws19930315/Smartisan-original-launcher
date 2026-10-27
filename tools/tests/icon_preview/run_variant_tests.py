"""Compare the extracted variants loader with native Android JSON and counted input fixtures."""
import argparse,json,os,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'prepared_icon_source'))
from run_device_tests import block,ROOT
ap=argparse.ArgumentParser(__doc__);ap.add_argument('--serial',required=True);ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);owners=[]
for name,path in [('Before',args.baseline),('After',args.source)]:
 s=path.read_text(encoding='utf8');methods='\n'.join(block(s,m)for m in ['    private void ensureVariantsMapLoaded()','    private static String stripPng(','    public synchronized java.util.List<String> getVariantsForPackage(']);methods=methods.replace('variants.names()','copyNames(variants)')
 owners.append('static class '+name+' extends Fixture {'+name+'(String text){super(text);}Map<String,List<String>> sVariantsMap;'+methods+'Map<String,List<String>> load(){ensureVariantsMapLoaded();return sVariantsMap;}}')
java=r'''
import android.text.TextUtils;import org.json.*;import java.io.*;import java.util.*;
public class VariantsProbe {
 static int checks,cases;static void check(boolean x,String s){checks++;if(!x)throw new AssertionError(s);}
 static class Fixture {final App app;int copies;Fixture(String text){app=new App(text);}JSONArray copyNames(JSONObject obj){copies++;return obj.names();}}
 static class App {final Assets assets;App(String text){assets=new Assets(text);}Assets getAssets(){return assets;}}
 static class Assets {final byte[] bytes;int opens,closes;boolean failRead,failClose;Assets(String text){try{bytes=text.getBytes("UTF-8");}catch(Exception e){throw new RuntimeException(e);}}
  InputStream open(String name)throws IOException{check(name.equals("icons/variants.json"),"same asset");opens++;if(failRead)throw new IOException("controlled read");return new ByteArrayInputStream(bytes){public void close()throws IOException{closes++;if(failClose)throw new IOException("controlled close");super.close();}};}}
 OWNERS
 static void compare(String input,boolean read,boolean close)throws Exception{
  Before b=new Before(input);After a=new After(input);b.app.assets.failRead=a.app.assets.failRead=read;b.app.assets.failClose=a.app.assets.failClose=close;
  Map<String,List<String>> bm=b.load(),am=a.load();check(bm.equals(am),"complete map and list order");check(a.copies==0,"candidate must avoid names array");
  check(b.app.assets.opens==a.app.assets.opens&&a.app.assets.opens==1,"one open");check(b.app.assets.closes==a.app.assets.closes,"equal close including failure");
  check(a.load()==am&&b.load()==bm,"retained existing map");check(a.app.assets.opens==1,"no second read");
  for(String key:bm.keySet()){List<String> bv=b.getVariantsForPackage(key),av=a.getVariantsForPackage(key);check(bv.equals(av),"package variants order");av.clear();check(a.getVariantsForPackage(key).equals(bv),"returned list owns storage");}
  check(a.getVariantsForPackage("absent").isEmpty(),"missing package");cases++;
 }
 public static void main(String[] args)throws Exception{try{runTests(args[0]);}catch(AssertionError e){System.out.println("ASSERTION_FAILED "+e.getMessage());System.exit(1);}}
 static void runTests(String path)throws Exception{
  String full=new String(java.nio.file.Files.readAllBytes(java.nio.file.Paths.get(path)),"UTF-8");compare(full,false,false);
  Before b=new Before(full);After a=new After(full);check(b.load().size()==EXPECTED_PACKAGES&&a.load().size()==EXPECTED_PACKAGES,"current full asset packages");check(b.copies==1,"baseline names array conversion");check(a.copies==0,"candidate no names array conversion");
  for(String value:new String[]{"{}","{\"variants\":{}}","{\"variants\":null}","{\"variants\":[]}","{\"variants\":{\"x\":1,\"y\":null}}","{bad", ""})compare(value,false,false);
  compare(full,true,false);compare(full,false,true);
  Random random=new Random(4219);for(int n=0;n<180;n++){JSONObject root=new JSONObject(),v=new JSONObject();root.put("variants",v);for(int k=0;k<12;k++){JSONArray values=new JSONArray();for(int j=0;j<15;j++){switch(random.nextInt(8)){case 0:values.put(JSONObject.NULL);break;case 1:values.put("  ");break;case 2:values.put(".PNG");break;case 3:values.put(42);break;case 4:values.put(false);break;default:values.put(" source"+random.nextInt(5)+(j%2==0?".PNG ":".png"));}}v.put(k==0?"":"pkg"+k,values);}compare(root.toString(),false,false);}
  System.out.println("RESULT {\"cases\":"+cases+",\"checks\":"+checks+",\"packages\":EXPECTED_PACKAGES,\"namesConversions\":\"1->0\",\"scope\":\"actual loader/getter/native JSON; controlled stream; map/list order and error policy\"}");
 }
}
'''.replace('OWNERS','\n'.join(owners)).replace('EXPECTED_PACKAGES',str(len(json.loads((ROOT/'launcher/assets/icons/variants.json').read_text(encoding='utf8'))['variants'])));src=out/'VariantsProbe.java';src.write_text(java,encoding='utf8');classes=out/'classes';classes.mkdir(exist_ok=True);dex=out/'dex';dex.mkdir(exist_ok=True);jdk=Path('E:/Program Files/Android/Android Studio/jbr');sdk=Path('D:/sdk')
def run(cmd,name):
 r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf8',errors='replace',timeout=120);(out/name).write_text(r.stdout+r.stderr,encoding='utf8')
 if r.returncode:raise RuntimeError(name+': '+r.stdout+r.stderr)
 return r.stdout
run([jdk/'bin/javac.exe','-encoding','UTF-8','-source','8','-target','8','-cp',sdk/'platforms/android-36/android.jar','-d',classes,src],'compile.log');run([jdk/'bin/jar.exe','cf',out/'probe.jar','-C',classes,'.'],'jar.log');os.environ['JAVA_HOME']=str(jdk);run([sdk/'build-tools/37.0.0/d8.bat','--min-api','26','--lib',sdk/'platforms/android-36/android.jar','--output',dex,out/'probe.jar'],'d8.log');adb=[sdk/'platform-tools/adb.exe','-s',args.serial];remote='/data/local/tmp/smartisan-variants-probe.dex';asset='/data/local/tmp/smartisan-variants-fixture.json';run([*adb,'push',dex/'classes.dex',remote],'push.log');run([*adb,'push',ROOT/'launcher/assets/icons/variants.json',asset],'asset.log')
try:
 text=run([*adb,'shell','env','CLASSPATH='+remote,'app_process','/system/bin','VariantsProbe',asset],'device.log');payload=json.loads(next(l[7:]for l in text.splitlines()if l.startswith('RESULT ')));(out/'summary.json').write_text(json.dumps(payload,indent=2));print(text)
finally:run([*adb,'shell','rm','-f',remote,asset],'cleanup.log')
