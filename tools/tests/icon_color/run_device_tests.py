"""Compare actual baseline/candidate Smali color classifiers on Android Bitmaps."""
import argparse,collections,json,os,struct,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]

def main():
 p=argparse.ArgumentParser(__doc__)
 for key in ('serial','baseline','output'):p.add_argument('--'+key,required=True)
 p.add_argument('--jdk',default='E:/Program Files/Android/Android Studio/jbr')
 p.add_argument('--sdk',default='D:/sdk')
 p.add_argument('--source',type=Path,default=ROOT/'launcher/smali/com/smartisanos/launcher/actions/sort/color/f.smali')
 p.add_argument('--apk',type=Path,default=ROOT/'build/launcher-signed.apk')
 a=p.parse_args();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
 jdk=Path(a.jdk);sdk=Path(a.sdk);classes=out/'classes';classes.mkdir(exist_ok=True)
 def run(cmd,name,timeout=120):
  r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf8',errors='replace',timeout=timeout)
  (out/name).write_text(r.stdout+r.stderr,encoding='utf8')
  if r.returncode:raise RuntimeError(name+': '+r.stdout+r.stderr)
  return r.stdout
 paths=[]
 for name,src in [('BaselineColor',Path(a.baseline)),('CandidateColor',a.source)]:
  s=src.read_text(encoding='utf8').replace('Lcom/smartisanos/launcher/actions/sort/color/f;','Lcom/smartisanos/launcher/actions/sort/color/'+name+';')
  path=out/(name+'.smali');path.write_text(s);paths.append(path)
 (out/'Assemble.java').write_text('''import java.io.File;import brut.androlib.smali.SmaliBuilder;
import com.android.tools.smali.dexlib2.Opcodes;import com.android.tools.smali.dexlib2.writer.builder.DexBuilder;
import com.android.tools.smali.dexlib2.writer.io.FileDataStore;
public class Assemble {public static void main(String[] a)throws Exception {
 DexBuilder d=new DexBuilder(new Opcodes(28));SmaliBuilder b=new SmaliBuilder(28);
 for(int i=1;i<a.length;i++)if(!b.buildFile(new File(a[i]),d))throw new AssertionError(a[i]);
 d.writeTo(new FileDataStore(new File(a[0])));
}}''')
 run([jdk/'bin/javac.exe','-cp',ROOT/'tools/apktool.jar','-d',classes,out/'Assemble.java'],'assemble-compile.log')
 run([jdk/'bin/java.exe','-cp',str(classes)+os.pathsep+str(ROOT/'tools/apktool.jar'),'Assemble',out/'color.dex',*paths],'assemble.log')
 (out/'ColorProbe.java').write_text(PROBE)
 run([jdk/'bin/javac.exe','-encoding','UTF-8','-source','8','-target','8','-cp',sdk/'platforms/android-36/android.jar','-d',classes,out/'ColorProbe.java'],'probe-compile.log')
 run([jdk/'bin/jar.exe','cf',out/'probe.jar','-C',classes,'ColorProbe.class'],'jar.log')
 dex=out/'dex';dex.mkdir(exist_ok=True);os.environ['JAVA_HOME']=str(jdk)
 run([sdk/'build-tools/37.0.0/d8.bat','--min-api','23','--output',dex,out/'probe.jar'],'d8.log')
 adb=[sdk/'platform-tools/adb.exe','-s',a.serial];remote='/data/local/tmp/smartisan-color-20261021'
 run([*adb,'shell','mkdir','-p',remote],'mkdir.log')
 for src,name in [(out/'color.dex','color.dex'),(dex/'classes.dex','probe.dex'),(a.apk,'launcher.apk')]:run([*adb,'push',src,remote+'/'+name],'push-'+name+'.log')
 try:
  text=run([*adb,'shell','env','CLASSPATH='+remote+'/color.dex:'+remote+'/probe.dex:'+remote+'/launcher.apk','app_process','/system/bin','ColorProbe'],'device.log')
  for owner in ('baseline','candidate'):run([*adb,'pull',remote+'/'+owner+'-count.trace',out/(owner+'-count.trace')],'pull-'+owner+'.log')
  payload=json.loads(next(l[7:] for l in text.splitlines() if l.startswith('RESULT ')))
  payload['bitmapReadEntryCounts']=read_counts([out/(owner+'-count.trace') for owner in ('baseline','candidate')])
  (out/'summary.json').write_text(json.dumps(payload,indent=2));print(text)
 finally:run([*adb,'shell','rm','-r',remote],'cleanup.log')

def read_counts(paths):
 completed=collections.Counter();counts={n:collections.Counter() for n in ('BaselineColor','CandidateColor')}
 for path in paths:
  raw=path.read_bytes();end=raw.index(b'*end\n')+5;header=raw[:end].decode();data=raw[end:]
  assert 'data-file-overflow=false' in header and 'clock=dual' in header
  methods={int(l.split('\t')[0],16):l.split('\t')[1:] for l in header.split('*methods\n')[1].splitlines() if l.startswith('0x')}
  size=struct.unpack_from('<H',data,16)[0];assert size==14
  stacks={}
  for offset in range(32,len(data),size):
   tid,encoded,cpu,wall=struct.unpack_from('<HIII',data,offset);mid,action=encoded&~3,encoded&3
   stack=stacks.setdefault(tid,[]);meta=methods.get(mid,[])
   if action==0:
    if meta[:2] in (['android.graphics.Bitmap','getPixel'],['android.graphics.Bitmap','getPixels']):
     for owner in counts:
      if any(methods.get(m,[])[:2]==['com.smartisanos.launcher.actions.sort.color.'+owner,'d'] for m in stack):counts[owner][meta[1]]+=1
    stack.append(mid)
   elif mid in stack:
    if meta and meta[1]=='d' and meta[0].rsplit('.',1)[-1] in counts:completed[meta[0].rsplit('.',1)[-1]]+=1
    del stack[len(stack)-1-stack[::-1].index(mid):]
 assert completed=={'BaselineColor':1,'CandidateColor':1},('incomplete trace',completed)
 result={k:dict(v) for k,v in counts.items()}
 assert result=={'BaselineColor':{'getPixel':4096},'CandidateColor':{'getPixels':1}},result
 return result

PROBE=r'''
import android.graphics.*;import java.lang.reflect.*;import java.util.*;import org.json.*;
public class ColorProbe {
 static Class<?> oldType,newType;static int checks;
 static Object call(Class<?> c,String method,Bitmap b)throws Exception{return c.getMethod(method,Bitmap.class).invoke(null,b);}
 static String snapshot(Object o)throws Exception {
  if(o==null)return "null";TreeMap<String,String> m=new TreeMap<>();
  for(Field f:o.getClass().getFields())if(!Modifier.isStatic(f.getModifiers())) {
   Object v=f.get(o);m.put(f.getName(),v instanceof float[]?Arrays.toString((float[])v):String.valueOf(v));
  }return m.toString();
 }
 static void compare(Bitmap b,String method)throws Exception {
  int[] before=new int[b.getWidth()*b.getHeight()];b.getPixels(before,0,b.getWidth(),0,0,b.getWidth(),b.getHeight());
  String old=snapshot(call(oldType,method,b)),now=snapshot(call(newType,method,b));
  if(!old.equals(now))throw new AssertionError(method+" "+b.getWidth()+"x"+b.getHeight()+" "+old+" != "+now);
  int[] after=new int[before.length];b.getPixels(after,0,b.getWidth(),0,0,b.getWidth(),b.getHeight());
  if(!Arrays.equals(before,after)||b.isRecycled())throw new AssertionError("input ownership");checks++;
 }
 static String failure(Class<?> c,Bitmap b)throws Exception {try{call(c,"d",b);return "none";}catch(InvocationTargetException e){return e.getCause().getClass().getName();}}
 static long bench(Class<?> c,Bitmap b,int count)throws Exception {long start=android.os.Debug.threadCpuTimeNanos();for(int i=0;i<count;i++)call(c,"d",b);return android.os.Debug.threadCpuTimeNanos()-start;}
 public static void main(String[] args)throws Exception {
  oldType=Class.forName("com.smartisanos.launcher.actions.sort.color.BaselineColor");newType=Class.forName("com.smartisanos.launcher.actions.sort.color.CandidateColor");
  for(String method:new String[]{"c","d"})if(!snapshot(call(oldType,method,null)).equals(snapshot(call(newType,method,null))))throw new AssertionError("null");else checks++;
  Random random=new Random(947261);int[] colors={0,0x01000000,0x7fffffff,0xff000000,0xffffffff,0xff888888,0xffff0000,0xff00ff00,0xff0000ff};
  for(int[] size:new int[][]{{1,1},{1,64},{64,1},{7,13},{32,32},{63,64},{64,64},{65,64},{64,65},{127,83},{256,256}}) {
   for(int pattern=0;pattern<13;pattern++) {
    int w=size[0],h=size[1];Bitmap b=Bitmap.createBitmap(w,h,Bitmap.Config.ARGB_8888);int[] px=new int[w*h];
    for(int y=0;y<h;y++)for(int x=0;x<w;x++)px[y*w+x]=pattern<9?colors[pattern]:pattern==9?colors[(x+y)%colors.length]:pattern==10?((x<w/2)?0xffff0000:0xff0000ff):pattern==11?random.nextInt():(x<3||y<3?0:0xffabcdef);
    b.setPixels(px,0,w,0,0,w,h);compare(b,"d");compare(b,"c");b.recycle();
   }
  }
  for(Bitmap.Config cfg:new Bitmap.Config[]{Bitmap.Config.RGB_565,Bitmap.Config.ALPHA_8,Bitmap.Config.RGBA_F16}){
   Bitmap b=Bitmap.createBitmap(64,64,cfg);b.eraseColor(0x7f123456);compare(b,"d");b.recycle();
  }
  Field threshold=Class.forName("com.smartisanos.launcher.data.Constants").getField("icon_resize_area");
  float originalThreshold=threshold.getFloat(null);
  for(float value:new float[]{0f,0.25f,0.5f,0.75f,1f}) {
   threshold.setFloat(null,value);Bitmap edge=Bitmap.createBitmap(64,64,Bitmap.Config.ARGB_8888);
   for(int x=0;x<64;x++)for(int y=0;y<64;y++)edge.setPixel(x,y,x<32?0:0x0100ff00);
   compare(edge,"d");compare(edge,"c");edge.recycle();
  }threshold.setFloat(null,originalThreshold);
  Bitmap bad=Bitmap.createBitmap(64,64,Bitmap.Config.ARGB_8888);bad.recycle();if(!failure(oldType,bad).equals(failure(newType,bad)))throw new AssertionError("recycled");checks++;
  Bitmap b=Bitmap.createBitmap(64,64,Bitmap.Config.ARGB_8888);b.eraseColor(0xffaf326a);
  Bitmap hw=b.copy(Bitmap.Config.HARDWARE,false);if(hw!=null){if(!failure(oldType,hw).equals(failure(newType,hw)))throw new AssertionError("hardware");checks++;hw.recycle();}
  b.eraseColor(0);
  // Separate captures keep the legacy per-pixel trace below ART's event limit.
  android.os.Debug.startMethodTracing("/data/local/tmp/smartisan-color-20261021/baseline-count.trace",16*1024*1024);
  call(oldType,"d",b);android.os.Debug.stopMethodTracing();
  android.os.Debug.startMethodTracing("/data/local/tmp/smartisan-color-20261021/candidate-count.trace",16*1024*1024);
  call(newType,"d",b);android.os.Debug.stopMethodTracing();
  b.eraseColor(0xffaf326a);
  for(int i=0;i<30;i++){call(oldType,"d",b);call(newType,"d",b);}
  JSONArray samples=new JSONArray();for(int i=0;i<5;i++){
   long old,now;if(i%2==0){old=bench(oldType,b,100);now=bench(newType,b,100);}else{now=bench(newType,b,100);old=bench(oldType,b,100);}
   samples.put(new JSONObject().put("baselineCpuMs",old/1e6).put("candidateCpuMs",now/1e6).put("iterations",100));
  }b.recycle();System.out.println("RESULT "+new JSONObject().put("equalOutputAndOwnershipCases",checks).put("microSamples",samples).put("scope","actual Smali classifiers, native Android Bitmaps; warmed microbenchmark is not app startup speed"));
 }
}
'''
if __name__=='__main__':main()

