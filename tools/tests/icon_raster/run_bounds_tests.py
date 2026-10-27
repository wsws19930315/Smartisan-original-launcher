"""Compare extracted production compositor/report paths with native Android pixels.

Source, geometry, profile badge, projection and shadow owners are controlled fixtures;
the compositor, bounds scanner, report-once gate and log formulas are actual source.
"""
import argparse,json,os,subprocess
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'prepared_icon_source'))
from run_device_tests import block,ROOT


def main():
 ap=argparse.ArgumentParser(__doc__)
 ap.add_argument('--serial',required=True)
 ap.add_argument('--geometry-snapshot',action='store_true',help='Compare identical geometry/pixels while requiring one call-local metrics resolution')
 ap.add_argument('--source-report-snapshot',action='store_true',help='Require report policy reuse without source or preference re-query')
 ap.add_argument('--baseline',required=True,type=Path)
 ap.add_argument('--output',required=True,type=Path)
 ap.add_argument('--source',type=Path,default=ROOT/'launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java')
 args=ap.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
 owners=[]
 for owner,path in [('Before',args.baseline),('After',args.source)]:
  source=path.read_text(encoding='utf8')
  methods='\n'.join(block(source,marker) for marker in (
   '    private static final class VisibleBounds {',
   '    private static final class StaticSource {',
   '    private static Bitmap composeTexture(Bitmap source, int actualLogicalTexture,\n            Object itemInfo, int pageMode, boolean resized, StaticSource resolved)',
   '    private static VisibleBounds analyzeVisibleBounds(',
   '    private static String boundsString(',
   '    private static void reportSourceCanvasOnce('))
  methods += '\n' + block(source, '    public static final class NormalIconRasterSpec {')
  methods += '\n' + block(source, '    private static NormalIconRasterSpec resolveNormalIconRasterSpec(int pageMode)')
  if 'private static NormalIconRasterSpec resolveNormalIconRasterSpec(IconVisualMetrics metrics)' in source:
   methods += '\n' + block(source, '    private static NormalIconRasterSpec resolveNormalIconRasterSpec(IconVisualMetrics metrics)')
  methods=methods.replace('private static VisibleBounds analyzeVisibleBounds(Bitmap bitmap) {',
                          'private static VisibleBounds analyzeVisibleBounds(Bitmap bitmap) { scans++;')
  owners.append('static class '+owner+' extends Fixtures {static int scans;static final Set<String> REPORTED=new HashSet<>();'+methods+'''
   static Bitmap run(Bitmap source,Drawable drawable,String type,Item item,boolean resized){
    return composeTexture(source,0,item,12,resized,new StaticSource(drawable,type,"fixed",false));
   }
  }''')
 java=PROBE.replace('OWNERS','\n'.join(owners)).replace('GEOMETRY_SNAPSHOT',str(args.geometry_snapshot).lower()).replace('SOURCE_REPORT_SNAPSHOT',str(args.source_report_snapshot).lower());src=out/'BoundsProbe.java';src.write_text(java,encoding='utf8')
 classes=out/'classes';classes.mkdir(exist_ok=True);dex=out/'dex';dex.mkdir(exist_ok=True)
 jdk=Path('E:/Program Files/Android/Android Studio/jbr');sdk=Path('D:/sdk')
 def run(cmd,name):
  r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf8',errors='replace',timeout=120)
  (out/name).write_text(r.stdout+r.stderr,encoding='utf8')
  if r.returncode:raise RuntimeError(name+': '+r.stdout+r.stderr)
  return r.stdout
 run([jdk/'bin/javac.exe','-encoding','UTF-8','-source','8','-target','8','-cp',sdk/'platforms/android-36/android.jar','-d',classes,src],'compile.log')
 run([jdk/'bin/jar.exe','cf',out/'probe.jar','-C',classes,'.'],'jar.log')
 os.environ['JAVA_HOME']=str(jdk)
 run([sdk/'build-tools/37.0.0/d8.bat','--min-api','23','--lib',sdk/'platforms/android-36/android.jar','--output',dex,out/'probe.jar'],'d8.log')
 adb=[sdk/'platform-tools/adb.exe','-s',args.serial];remote='/data/local/tmp/smartisan-bounds-probe.dex'
 run([*adb,'push',dex/'classes.dex',remote],'push.log')
 try:
  text=run([*adb,'shell','env','CLASSPATH='+remote,'app_process','/system/bin','BoundsProbe'],'device.log')
  payload=json.loads(next(l[7:]for l in text.splitlines()if l.startswith('RESULT ')))
  (out/'summary.json').write_text(json.dumps(payload,indent=2));print(text)
 finally:run([*adb,'shell','rm',remote],'cleanup.log')

PROBE=r'''
import android.graphics.*;import android.graphics.drawable.*;import java.util.*;import org.json.*;
public class BoundsProbe {
 static final boolean geometrySnapshot=GEOMETRY_SNAPSHOT;
 static final boolean sourceReportSnapshot=SOURCE_REPORT_SNAPSHOT;
 static int checks,cases;static List<String> logs=new ArrayList<>();
 static class Item {String pkg="fixture",component="Main";boolean circle,acceptance=true,settings;}
 static class Fixtures {
  static final String TAG="test",RASTER_CACHE_VERSION="fixture";static final int DIAGNOSTIC_ALPHA_CUTOFF=40;
  static int decoration;static boolean mutateProjection,mutateShadow,failShadow;
  static int projectionCalls,shadowCalls;static Bitmap lastArtwork;
  static int artwork=96,texture=128,geometryResolves;static boolean unavailable;
  static int sourceQueries,circleReads;static String liveType="DEFAULT";
  static boolean flipPolicy;
  static class Log {static void i(String tag,String s){logs.add(s);}static void w(String tag,String s){logs.add(s);}}
  static String itemField(Object item,String key){Item i=(Item)item;return key.equals("packageName")?i.pkg:key.equals("componentName")?i.component:"title";}
  static boolean isDesktopSettingsShortcut(Object item){return ((Item)item).settings;}
  static boolean isAcceptanceSample(Object item){return ((Item)item).acceptance;}
  static int layoutSize(int mode,String key){return key.equals("icon_size_with_shadow")?128:key.equals("icon_size_origin_resize")?80:96;}
  static int currentLayoutSize(String key){return layoutSize(12,key);}
  static class IconVisualMetrics {int iconSizeSetting=0,surfaceWidth=1080;int logicalArtworkBox=96,logicalTextureBox=128,physicalArtworkPx=artwork,physicalTexturePx=texture;float physicalScale=artwork/96f;String id="fixture";static IconVisualMetrics resolve(int mode){geometryResolves++;return unavailable?null:new IconVisualMetrics();}}
  static class MaintainedLauncherSettingsHost {
   static boolean desktopDefaultCircleEnabled(Object i,String t){circleReads++;return ((Item)i).circle&&(!sourceReportSnapshot||"DEFAULT".equals(t));}
   static boolean desktopDefaultCircleEnabled(Object i){return sourceReportSnapshot?desktopDefaultCircleEnabled(i,desktopIconSourceType(i)):((Item)i).circle;}
   static String desktopIconSourceType(Object i){sourceQueries++;return liveType;}
  }
  static Bitmap decorateProfileIcon(Object i,Bitmap b,String t){
   if(decoration==1){Bitmap copy=b.copy(Bitmap.Config.ARGB_8888,true);new Canvas(copy).drawRect(copy.getWidth()-8,0,copy.getWidth(),8,new Paint(0){{setColor(0xffee0000);}});return copy;}
   if(decoration==2){b.setPixel(0,0,0xff00ff00);return b;}
   if(decoration==3)return null;return b;
  }
  static class StartupPageSceneDiagnostics {static long detailBegin(){return 0;}static void detailEnd(Object i,String s,long t){}}
  static class IconIlluminationCompat {static void prepare(Object i,Bitmap b){projectionCalls++;if(mutateProjection)b.setPixel(0,b.getHeight()-1,0xff0000ff);if(flipPolicy){liveType=((Item)i).circle?"CUSTOM":"DEFAULT";((Item)i).circle=!((Item)i).circle;}}}
  static class LauncherSettingBridge {
   static Bitmap composeStaticIconTextureWithOriginalShadow(Bitmap b,int size,float scale){
    shadowCalls++;lastArtwork=b;if(mutateShadow)b.setPixel(b.getWidth()-1,b.getHeight()-1,0xffffffff);
    if(failShadow)return null;Bitmap result=Bitmap.createBitmap(size,size,Bitmap.Config.ARGB_8888);
    Canvas c=new Canvas(result);c.drawBitmap(b,(size-b.getWidth())*.5f,(size-b.getHeight())*.25f,new Paint());return result;
   }
  }
  static void debugDump(Object i,String s,Bitmap b){}
  static void debugMetrics(Object...values){}
  static void reportPhysicalOnce(Object...values){}
  static String lifecycleToken(Object i){return "COLD";}static String gridToken(int m){return "12";}
 }
 OWNERS
 static void check(boolean b,String m){checks++;if(!b)throw new AssertionError(m);}
 static int[] pixels(Bitmap b){int[] p=new int[b.getWidth()*b.getHeight()];b.getPixels(p,0,b.getWidth(),0,0,b.getWidth(),b.getHeight());return p;}
 static void runCase(Bitmap source,Drawable drawable,String type,Item item,boolean resized,boolean repeated)throws Exception {
  Before.REPORTED.clear();After.REPORTED.clear();
  for(int round=0;round<(repeated?2:1);round++){
   int[] input=pixels(source);Rect bounds=drawable==null?null:new Rect(drawable.getBounds());
   logs.clear();Fixtures.geometryResolves=0;Before.scans=0;Fixtures.projectionCalls=Fixtures.shadowCalls=0;
   Fixtures.sourceQueries=Fixtures.circleReads=0;if(sourceReportSnapshot)Fixtures.liveType=type;
   Bitmap old=Before.run(source,drawable,type,item,resized);List<String> oldLogs=new ArrayList<>(logs);
   int oldSourceQueries=Fixtures.sourceQueries,oldCircleReads=Fixtures.circleReads;
   int oldGeometry=Fixtures.geometryResolves;
   int oldProjection=Fixtures.projectionCalls,oldShadow=Fixtures.shadowCalls,oldScans=Before.scans;
   check(Fixtures.lastArtwork==null||Fixtures.lastArtwork.isRecycled(),"baseline artwork released");
   logs.clear();Fixtures.geometryResolves=0;After.scans=0;Fixtures.projectionCalls=Fixtures.shadowCalls=0;
   Fixtures.sourceQueries=Fixtures.circleReads=0;
   Bitmap now=After.run(source,drawable,type,item,resized);
   if(sourceReportSnapshot){
    check(oldSourceQueries==(round==0?("DEFAULT".equals(type)?2:1):0),"baseline report source queries");
    check(Fixtures.sourceQueries==0,"candidate report must reuse selected policy");
    check(oldCircleReads-Fixtures.circleReads==(round==0&&"DEFAULT".equals(type)?1:0),"report preference query removed");
   }
   check(old.getWidth()==now.getWidth()&&old.getHeight()==now.getHeight()&&Arrays.equals(pixels(old),pixels(now)),"compositor pixels "+type);
   check(oldLogs.equals(logs),"unchanged diagnostic metrics "+type+" decoration="+Fixtures.decoration+" old="+oldLogs+" now="+logs);
   check(Arrays.equals(input,pixels(source))&&!source.isRecycled(),"source pixels/ownership");
   check(drawable==null||bounds.equals(drawable.getBounds()),"drawable bounds restored");
   check(Fixtures.lastArtwork==null||Fixtures.lastArtwork.isRecycled(),"candidate artwork released");
   check(oldProjection==Fixtures.projectionCalls&&oldShadow==Fixtures.shadowCalls,"same projection/shadow admissions");
   boolean changed=Fixtures.decoration==1||Fixtures.decoration==2||Fixtures.mutateProjection||Fixtures.mutateShadow;
   if(geometrySnapshot)check(oldGeometry==2&&Fixtures.geometryResolves==1,"geometry resolves 2->1, before="+oldGeometry+" after="+Fixtures.geometryResolves);
   int expected=geometrySnapshot||sourceReportSnapshot||round>0||changed?oldScans:oldScans-1;
   check(After.scans==expected,"scan requirement old="+oldScans+" now="+After.scans+" expected="+expected+" changed="+changed+" round="+round);
   old.recycle();now.recycle();cases++;
  }
 }
 public static void main(String[] args){try{test();}catch(Throwable e){e.printStackTrace();System.exit(1);}}
 static void test()throws Exception {
  Item item=new Item();Random random=new Random(1021);
  for(int pattern=0;pattern<5;pattern++)for(int size:new int[]{32,96,256}){
   Bitmap source=Bitmap.createBitmap(size,size,Bitmap.Config.ARGB_8888);int[] p=new int[size*size];
   for(int y=0;y<size;y++)for(int x=0;x<size;x++)p[y*size+x]=pattern==0?0:pattern==1?0xffcccccc:pattern==2?(x<size/2?0x2700ffff:0x2800ffff):pattern==3?random.nextInt():(x>size/4&&y>size/4&&x<3*size/4&&y<3*size/4?0xffabcdef:0);
   source.setPixels(p,0,size,0,0,size,size);
   for(int decoration=0;decoration<4;decoration++)for(boolean mutated:new boolean[]{false,true}){
    Fixtures.decoration=decoration;Fixtures.mutateProjection=mutated;Fixtures.mutateShadow=false;
    for(boolean useDrawable:new boolean[]{false,true})for(boolean resized:new boolean[]{false,true}){
     Drawable drawable=useDrawable?new BitmapDrawable(android.content.res.Resources.getSystem(),source):null;
     if(drawable!=null)drawable.setBounds(3,4,15,16);
     runCase(source,drawable,"CUSTOM",item,resized,true);
    }
   }
   Fixtures.decoration=0;Fixtures.mutateProjection=false;Fixtures.mutateShadow=true;runCase(source,null,"PACK",item,false,false);
   Fixtures.mutateShadow=false;Fixtures.failShadow=true;runCase(source,null,"IMPROVED",item,false,false);Fixtures.failShadow=false;
   item.circle=true;runCase(source,new BitmapDrawable(android.content.res.Resources.getSystem(),source),"DEFAULT",item,false,false);item.circle=false;
   source.recycle();
  }
  // Same identity can receive new pixels between calls: no scan data survives a call.
  Bitmap fresh=Bitmap.createBitmap(64,64,Bitmap.Config.ARGB_8888);fresh.eraseColor(0xff112233);
  runCase(fresh,null,"RESOURCE",item,false,false);fresh.eraseColor(0xff445566);runCase(fresh,null,"RESOURCE",item,false,false);fresh.recycle();
  if(geometrySnapshot){
   Fixtures.decoration=0;Fixtures.mutateProjection=Fixtures.mutateShadow=Fixtures.failShadow=false;
   Bitmap b=Bitmap.createBitmap(64,64,Bitmap.Config.ARGB_8888);b.eraseColor(0xffabcdef);
   for(int art:new int[]{64,144,216}){Fixtures.artwork=art;Fixtures.texture=art*4/3;runCase(b,null,"CUSTOM",item,false,false);}
   Fixtures.artwork=96;Fixtures.texture=128;Fixtures.unavailable=true;
   Fixtures.geometryResolves=0;Bitmap old=Before.run(b,null,"CUSTOM",item,false);check(old==b&&Fixtures.geometryResolves==1,"old unavailable geometry fallback");
   Fixtures.geometryResolves=0;Bitmap now=After.run(b,null,"CUSTOM",item,false);check(now==b&&Fixtures.geometryResolves==1&&!b.isRecycled(),"candidate unavailable geometry input stays live");Fixtures.unavailable=false;
   Fixtures.geometryResolves=0;check(After.run(null,null,"CUSTOM",item,false)==null&&Fixtures.geometryResolves==0,"missing source skips geometry");b.recycle();
  }
  if(sourceReportSnapshot){
   Fixtures.decoration=0;Fixtures.mutateProjection=Fixtures.mutateShadow=Fixtures.failShadow=false;
   Bitmap b=Bitmap.createBitmap(64,64,Bitmap.Config.ARGB_8888);b.eraseColor(0xffabcdef);
   for(String type:new String[]{"DEFAULT","CUSTOM","RESOURCE","PACK","IMPROVED",null})for(boolean circle:new boolean[]{false,true}){
    item.circle=circle;runCase(b,null,type,item,false,true);
   }
   // The report describes this draw even when selection/preferences change afterwards.
   for(boolean circle:new boolean[]{false,true}){
    String type=circle?"DEFAULT":"CUSTOM";item.circle=circle;Fixtures.liveType=type;Fixtures.flipPolicy=true;
    Before.REPORTED.clear();After.REPORTED.clear();logs.clear();Bitmap old=Before.run(b,null,type,item,false);
    item.circle=circle;Fixtures.liveType=type;Fixtures.sourceQueries=0;logs.clear();Bitmap now=After.run(b,null,type,item,false);
    check(Arrays.equals(pixels(old),pixels(now)),"late source/preference change keeps pixels");
    check(Fixtures.sourceQueries==0,"late change does not query source");
    String policy=circle?"DEFAULT_CIRCLE_CANONICAL":"SOURCE_FULL_BOUNDS";
    check(logs.stream().anyMatch(s->s.contains("sourceCanvasPolicy="+policy)),"report uses actual drawn policy");
    check(!b.isRecycled(),"late change source ownership");old.recycle();now.recycle();cases++;
   }
   Fixtures.flipPolicy=false;item.circle=false;Fixtures.liveType="DEFAULT";
   Fixtures.unavailable=true;Fixtures.sourceQueries=0;check(After.run(b,null,"DEFAULT",item,false)==b&&Fixtures.sourceQueries==0,"unavailable geometry keeps source and skips report");Fixtures.unavailable=false;
   Fixtures.sourceQueries=0;check(After.run(null,null,"DEFAULT",item,false)==null&&Fixtures.sourceQueries==0,"missing source skips report");b.recycle();
  }
  System.out.println("RESULT "+new JSONObject().put("geometrySnapshot",geometrySnapshot).put("sourceReportSnapshot",sourceReportSnapshot).put("cases",cases).put("checks",checks).put("ordinaryScans",geometrySnapshot||sourceReportSnapshot?"unchanged":"3->2").put("badgeOrMutationScans","3->3").put("repeatedReportScans","2->2").put("scope","actual compositor/report/scanner source, native Android Canvas; controlled geometry/profile/projection/shadow owners; not full GL acceptance"));
 }
}
'''
if __name__=='__main__':main()
