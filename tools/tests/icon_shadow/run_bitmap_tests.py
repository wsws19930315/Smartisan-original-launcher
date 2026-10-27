"""Run the actual baseline/candidate shadow Smali with Android native Bitmaps.

Normal copies verify pixels and count methods; separately instrumented copies expose
only call-local temporary references so ownership can be checked after return.
"""
import argparse,collections,json,os,struct,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]


def main():
 ap=argparse.ArgumentParser(__doc__)
 for key in ('serial','baseline','output'):ap.add_argument('--'+key,required=True)
 ap.add_argument('--source',type=Path,default=ROOT/'launcher/smali/com/smartisanos/launcher/data/L.smali')
 ap.add_argument('--apk',type=Path,default=ROOT/'build/launcher-signed.apk')
 a=ap.parse_args();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
 jdk=Path('E:/Program Files/Android/Android Studio/jbr');sdk=Path('D:/sdk')
 def run(cmd,name):
  r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf8',errors='replace',timeout=180)
  (out/name).write_text(r.stdout+r.stderr,encoding='utf8')
  if r.returncode:raise RuntimeError(name+': '+r.stdout+r.stderr)
  return r.stdout
 host=out/'host';host.mkdir(exist_ok=True);classes=out/'classes';classes.mkdir(exist_ok=True)
 paths=[]
 for name,src in [('BaselineShadow',Path(a.baseline)),('CandidateShadow',a.source)]:
  for tracked in (False,True):
   n=name+('Tracked' if tracked else '');s=src.read_text().replace('Lcom/smartisanos/launcher/data/L;','Lcom/smartisanos/launcher/data/'+n+';')
   if tracked:
    start=s.index('.method public static a(Landroid/graphics/Bitmap;Landroid/graphics/Canvas;FI)');end=s.index('.end method',start);m=s[start:end]
    needle='    move-result-object v1\n\n    .line 72'
    assert needle in m;m=m.replace(needle,'    move-result-object v1\n\n    invoke-static {v1}, LShadowProbe;->capturePadding(Landroid/graphics/Bitmap;)V\n\n    .line 72');s=s[:start]+m+s[end:]
    start=s.index('.method a(Landroid/graphics/Bitmap;Landroid/graphics/Canvas;IIF)');end=s.index('.end method',start);m=s[start:end]
    for reg in ('v9','v11','v13','v15'):
     needle='    move-result-object '+reg+'\n'
     if needle in m:m=m.replace(needle,needle+'\n    invoke-static {'+reg+'}, LShadowProbe;->captureAlpha(Landroid/graphics/Bitmap;)V\n',1)
    s=s[:start]+m+s[end:]
   path=out/(n+'.smali');path.write_text(s);paths.append(path)
 (out/'Assemble.java').write_text('''import java.io.File;import brut.androlib.smali.SmaliBuilder;
import com.android.tools.smali.dexlib2.Opcodes;import com.android.tools.smali.dexlib2.writer.builder.DexBuilder;
import com.android.tools.smali.dexlib2.writer.io.FileDataStore;
public class Assemble {public static void main(String[] a)throws Exception {
 DexBuilder d=new DexBuilder(new Opcodes(28));SmaliBuilder b=new SmaliBuilder(28);
 for(int i=1;i<a.length;i++)if(!b.buildFile(new File(a[i]),d))throw new AssertionError(a[i]);
 d.writeTo(new FileDataStore(new File(a[0])));
}}''')
 run([jdk/'bin/javac.exe','-cp',ROOT/'tools/apktool.jar','-d',host,out/'Assemble.java'],'assemble-compile.log')
 run([jdk/'bin/java.exe','-cp',str(host)+os.pathsep+str(ROOT/'tools/apktool.jar'),'Assemble',out/'shadow.dex',*paths],'assemble.log')
 (out/'ShadowProbe.java').write_text(PROBE)
 run([jdk/'bin/javac.exe','-encoding','UTF-8','-source','8','-target','8','-cp',sdk/'platforms/android-36/android.jar','-d',classes,out/'ShadowProbe.java'],'compile.log')
 run([jdk/'bin/jar.exe','cf',out/'probe.jar','-C',classes,'.'],'jar.log')
 dex=out/'dex';dex.mkdir(exist_ok=True);os.environ['JAVA_HOME']=str(jdk)
 run([sdk/'build-tools/37.0.0/d8.bat','--min-api','23','--output',dex,out/'probe.jar'],'d8.log')
 adb=[sdk/'platform-tools/adb.exe','-s',a.serial];remote='/data/local/tmp/smartisan-shadow-probe'
 run([*adb,'shell','mkdir','-p',remote],'mkdir.log')
 for src,name in [(out/'shadow.dex','shadow.dex'),(dex/'classes.dex','probe.dex'),(a.apk,'launcher.apk')]:run([*adb,'push',src,remote+'/'+name],'push-'+name+'.log')
 try:
  text=run([*adb,'shell','env','CLASSPATH='+remote+'/shadow.dex:'+remote+'/probe.dex:'+remote+'/launcher.apk','app_process','/system/bin','ShadowProbe'],'device.log')
  for owner in ('baseline','candidate'):run([*adb,'pull',remote+'/'+owner+'-count.trace',out/(owner+'-count.trace')],'pull-'+owner+'.log')
  payload=json.loads(next(l[7:]for l in text.splitlines()if l.startswith('RESULT ')))
  payload['completeMethodCounts']=read_counts([out/(owner+'-count.trace') for owner in ('baseline','candidate')])
  (out/'summary.json').write_text(json.dumps(payload,indent=2));print(json.dumps(payload,indent=2))
 finally:run([*adb,'shell','rm','-r',remote],'cleanup.log')


def read_counts(paths):
 counts={n:collections.Counter()for n in ('BaselineShadow','CandidateShadow')};complete=collections.Counter()
 for path in paths:
  raw=path.read_bytes();end=raw.index(b'*end\n')+5;header=raw[:end].decode();data=raw[end:];assert 'data-file-overflow=false'in header
  methods={int(l.split('\t')[0],16):l.split('\t')[1:]for l in header.split('*methods\n')[1].splitlines()if l.startswith('0x')}
  size=struct.unpack_from('<H',data,16)[0];assert size==14;stacks={}
  for pos in range(32,len(data),size):
   tid,encoded,cpu,wall=struct.unpack_from('<HIII',data,pos);mid,action=encoded&~3,encoded&3;meta=methods.get(mid,[]);stack=stacks.setdefault(tid,[])
   if action==0:
    if meta[:2]in (['android.graphics.Bitmap','extractAlpha'],['android.graphics.Bitmap','createBitmap']):
     for owner in counts:
      if any(methods.get(m,[])[:3]==['com.smartisanos.launcher.data.'+owner,'a','(Landroid/graphics/Bitmap;Landroid/graphics/Canvas;FI)Landroid/graphics/Bitmap;']for m in stack):
       if meta[1]=='extractAlpha' or meta[2]=='(IILandroid/graphics/Bitmap$Config;)Landroid/graphics/Bitmap;':counts[owner][meta[1]]+=1
    stack.append(mid)
   elif mid in stack:
    if len(meta)>2 and meta[0].rsplit('.',1)[-1]in counts and meta[2]=='(Landroid/graphics/Bitmap;Landroid/graphics/Canvas;FI)Landroid/graphics/Bitmap;':complete[meta[0].rsplit('.',1)[-1]]+=1
    del stack[len(stack)-1-stack[::-1].index(mid):]
 assert complete=={'BaselineShadow':1,'CandidateShadow':1},('incomplete traces',complete)
 result={k:dict(v)for k,v in counts.items()}
 assert result=={'BaselineShadow':{'createBitmap':2,'extractAlpha':4},'CandidateShadow':{'createBitmap':2,'extractAlpha':3}},result
 return result

PROBE=r'''
import android.graphics.*;import java.lang.reflect.*;import java.util.*;import org.json.*;
public class ShadowProbe {
 static int checks,cases;static Bitmap padding;static List<Bitmap> alphas=new ArrayList<>();
 public static void capturePadding(Bitmap b){padding=b;}public static void captureAlpha(Bitmap b){alphas.add(b);}
 static void check(boolean ok,String why){checks++;if(!ok)throw new AssertionError(why);}
 static Class<?> cls(String n)throws Exception{return Class.forName("com.smartisanos.launcher.data."+n);}
 static Bitmap layer(Class<?> c,Bitmap source,float radius,int color)throws Exception {
  Canvas canvas=new Canvas();Bitmap b=(Bitmap)c.getMethod("a",Bitmap.class,Canvas.class,float.class,int.class).invoke(null,source,canvas,radius,color);
  check(canvas.getWidth()==0&&canvas.getHeight()==0,"canvas detached");return b;
 }
 static Bitmap core(Class<?> c,Bitmap source,float radius,int one,int two)throws Exception {
  Constructor<?> constructor=c.getDeclaredConstructor();constructor.setAccessible(true);Object o=constructor.newInstance();
  Method m=c.getDeclaredMethod("a",Bitmap.class,Canvas.class,int.class,int.class,float.class);m.setAccessible(true);
  return (Bitmap)m.invoke(o,source,new Canvas(),one,two,radius);
 }
 static int[] pixels(Bitmap b){int[] p=new int[b.getWidth()*b.getHeight()];b.getPixels(p,0,b.getWidth(),0,0,b.getWidth(),b.getHeight());return p;}
 static void equal(Bitmap a,Bitmap b,String name){check(a.getWidth()==b.getWidth()&&a.getHeight()==b.getHeight(),"dimensions "+name);check(Arrays.equals(pixels(a),pixels(b)),"pixels "+name);}
 static void compare(Bitmap source,float radius,int one,int two)throws Exception {
  int[] before=pixels(source);int generation=source.getGenerationId();Class<?> old=cls("BaselineShadow"),now=cls("CandidateShadow");
  Bitmap a=layer(old,source,radius,one),b=layer(now,source,radius,one);equal(a,b,"layer r="+radius);check(a!=source&&b!=source&&!a.isRecycled()&&!b.isRecycled(),"returned layer owns output");a.recycle();b.recycle();
  a=core(old,source,radius,one,two);b=core(now,source,radius,one,two);equal(a,b,"two color core r="+radius);a.recycle();b.recycle();
  check(!source.isRecycled()&&generation==source.getGenerationId()&&Arrays.equals(before,pixels(source)),"input unchanged and alive");cases++;
 }
 static void ownership(Bitmap source)throws Exception {
  for(String name:new String[]{"BaselineShadowTracked","CandidateShadowTracked"}){
   padding=null;alphas.clear();Bitmap result=layer(cls(name),source,3,0x55000000);boolean changed=name.startsWith("Candidate");
   check(padding!=null&&padding!=source&&padding!=result,"padding is exclusively created, not source/result");
   check(padding.isRecycled()==changed,"padding release candidate="+changed);
   check(alphas.size()==(changed?3:4),"alpha-producing calls tracked");
   for(Bitmap alpha:alphas)check(alpha.isRecycled()&&alpha!=source&&alpha!=result,"owned alpha released");
   check(!source.isRecycled()&&!result.isRecycled(),"source/output survive cleanup");
   if(!padding.isRecycled())padding.recycle();result.recycle();
  }padding=null;alphas.clear();
 }
 static String failure(Class<?> c,Bitmap b,float radius){try{Bitmap result=layer(c,b,radius,0xff000000);result.recycle();return "none";}catch(Throwable e){while(e instanceof InvocationTargetException)e=e.getCause();return e.getClass().getName();}}
 static long bench(Class<?> c,Bitmap b)throws Exception {long start=android.os.Debug.threadCpuTimeNanos();for(int i=0;i<300;i++){Bitmap out=layer(c,b,9,0x55000000);out.recycle();}return android.os.Debug.threadCpuTimeNanos()-start;}
 public static void main(String[] args){try{test();}catch(Throwable e){e.printStackTrace();System.exit(1);}}
 static void test()throws Exception {
  Random random=new Random(102147);int[][] colors={{0x33000000,0x29000000},{0x7fffffff,0x55000000},{0x88ff0000,0x770000ff}};
  for(int[] size:new int[][]{{8,11},{32,32},{96,96},{192,192}})for(int pattern=0;pattern<5;pattern++){
   int w=size[0],h=size[1];Bitmap source=Bitmap.createBitmap(w,h,Bitmap.Config.ARGB_8888);int[] p=new int[w*h];
   for(int y=0;y<h;y++)for(int x=0;x<w;x++)p[y*w+x]=pattern==0?0:pattern==1?0xffabcdef:pattern==2?((y<h/3?83:y<2*h/3?177:255)<<24)|0x112233:pattern==3?(x>w/5&&x<4*w/5&&y>h/5&&y<4*h/5?0xff123456:0):random.nextInt();
   source.setPixels(p,0,w,0,0,w,h);
   for(float r:new float[]{0.5f,1f,3f,9f,16f,24f})for(int[] c:colors)compare(source,r,c[0],c[1]);
   ownership(source);source.recycle();
  }
  for(Bitmap.Config cfg:new Bitmap.Config[]{Bitmap.Config.ALPHA_8,Bitmap.Config.RGB_565,Bitmap.Config.RGBA_F16}){
   Bitmap source=Bitmap.createBitmap(48,48,cfg);source.eraseColor(0x7f112233);compare(source,4.5f,0x33000000,0x44000000);source.recycle();
  }
  Class<?> old=cls("BaselineShadow"),now=cls("CandidateShadow");Bitmap b=Bitmap.createBitmap(128,128,Bitmap.Config.ARGB_8888);b.eraseColor(0x80112233);
  check(failure(old,null,3).equals(failure(now,null,3)),"null exception");
  for(float r:new float[]{0,-1,Float.NaN})check(failure(old,b,r).equals(failure(now,b,r)),"invalid radius exception");
  Bitmap bad=b.copy(Bitmap.Config.ARGB_8888,true);bad.recycle();check(failure(old,bad,3).equals(failure(now,bad,3)),"recycled exception");
  for(String name:new String[]{"baseline","candidate"}){
   android.os.Debug.startMethodTracing("/data/local/tmp/smartisan-shadow-probe/"+name+"-count.trace",16*1024*1024);
   Bitmap result=layer(name.equals("baseline")?old:now,b,3,0x55000000);result.recycle();android.os.Debug.stopMethodTracing();
  }
  for(int i=0;i<8;i++){layer(old,b,9,0x55000000).recycle();layer(now,b,9,0x55000000).recycle();}
  JSONArray times=new JSONArray();for(int i=0;i<5;i++){long a,c;if(i%2==0){a=bench(old,b);c=bench(now,b);}else{c=bench(now,b);a=bench(old,b);}times.put(new JSONObject().put("baselineCpuMs",a/1e6).put("candidateCpuMs",c/1e6).put("iterations",300));}
  b.recycle();System.out.println("RESULT "+new JSONObject().put("pixelCases",cases).put("checks",checks).put("alphaCallsPerLayer","4->3").put("paddingReleasedOnSuccess",true).put("microSamples",times).put("scope","actual Smali with native Bitmap/Canvas/BlurMaskFilter; warmed microbenchmark is not overall startup or physical light acceptance"));
 }
}
'''
if __name__=='__main__':main()
