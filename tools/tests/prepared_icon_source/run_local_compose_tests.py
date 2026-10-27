"""Exercise the production call-local handoff with native Android Bitmaps.

The final compositor is a recording fixture; actual geometry/pixels are checked
by paired launcher screenshots. No fixture is compiled into the launcher APK.
"""
import argparse
from pathlib import Path
import subprocess
from run_device_tests import ROOT, block


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--serial', required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--source', type=Path, default=ROOT / 'launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java')
    ap.add_argument('--uncached', action='store_true')
    ap.add_argument('--expect-borrowed', action='store_true')
    args = ap.parse_args()
    out = args.output
    (out / 'classes').mkdir(parents=True, exist_ok=True)
    (out / 'dex').mkdir(exist_ok=True)
    source = args.source.read_text(encoding='utf8')
    methods = '\n'.join(block(source, marker) for marker in (
        '    private static final class StaticSource {',
        '    private static StaticSource resolveStaticSource(Object itemInfo, Bitmap legacyBitmap)',
        '    private static StaticSource resolveStaticSource(Object itemInfo, Bitmap legacyBitmap,',
        '    private static Bitmap prepareResolvedStaticSource(',
        '    public static Bitmap sourceBitmap(',
        '    public static Bitmap iconRawSource(',
        '    private static void recycleIfOwned(',
        '    public static Bitmap composeCurrentStaticApplicationIconTexture('))
    if 'private static Bitmap composePreparedStaticSource(' in source:
        methods += block(source, '    private static Bitmap composePreparedStaticSource(')
    if 'private static Bitmap borrowedCompositionSource(' in source:
        methods += block(source, '    private static Bitmap borrowedCompositionSource(')
        methods += block(source, '    private static Bitmap composePreparedStaticSource(Object itemInfo, Bitmap prepared,\n            int pageMode, StaticSource resolved, boolean borrowed)')
    disk_candidate = 'private static String persistentFinalKey(' in source
    if disk_candidate:
        # This probe checks call-local ownership. File/identity/queue contracts have separate native probes.
        methods = methods.replace('com.smartisanos.home.settings.icons.IconPreviewRepository', 'DiskRepository')
    optimized = 'public static Bitmap composeUncachedStaticApplicationIconTexture(' in source
    if args.uncached:
        methods += block(source, '    public static Bitmap prepareUncachedStaticSource(Object item)')
        methods += block(source, '    public static Bitmap prepareStaticSource(Object itemInfo, Bitmap cachedSource)')
        if optimized:
            methods += block(source, '    public static Bitmap composeUncachedStaticApplicationIconTexture(')
            methods += block(source, '    private static Bitmap prepareUncachedStaticSource(')
    java = r'''
import android.graphics.*;import android.graphics.drawable.*;import android.util.Log;
public class LocalComposeProbe {
 static final boolean EXPECT_BORROWED=EXPECT_BORROWED_VALUE;
 static final String TAG="test";static final int CANONICAL_DEFAULT_SOURCE_SIZE=256;
 static int loads,checks,compositions,typeQueries,identityQueries;static boolean quick,normal=true,circle,fail,alias,settings,apkFallback;
 static final java.util.Map<String,Object> PENDING_SOURCE_WRITES=new java.util.LinkedHashMap<>();
 static boolean sDesktopPageReady;static int admissions;
 static void scheduleSourceWrites(){admissions++;}
 static String type="CUSTOM";static Drawable formal;static Bitmap preparedSeen;
 static StaticSource resolvedSeen;static Bitmap cached;
 public static class Item {public byte[] iconRawData={1};}
 static boolean isQuickLaunchItem(Object i){return quick;}
 static boolean shouldUseHighResolutionDesktopRaster(Object i){return normal;}
 static boolean isDesktopSettingsShortcut(Object i){return settings;}
 static String itemField(Object i,String n){return "0";}
 static Drawable loadCurrentDesktopDrawable(Object i){loads++;return formal;}
 static class MaintainedLauncherSettingsHost {
  static String desktopIconSourceType(Object i){typeQueries++;return type;}
  static String desktopIconSourceIdentity(Object i,String t){identityQueries++;return "same-identity";}
  static boolean desktopDefaultCircleEnabled(Object i){return circle;}
  static boolean desktopDefaultCircleEnabled(Object i,String t){return circle;}
  static Drawable loadDefaultIconForDesktopItem(android.content.Context c,String p,String n,int u){return apkFallback?new ColorDrawable(0xffabcdef):null;}
 }
 static class StartupPageSceneDiagnostics {
  static long detailBegin(){return 0;}static void detailEnd(Object i,String s,long n){}
  static void shadowCompose(Object i){}
 }
 static class DefaultIconCircleRenderer {
  static Bitmap render(Drawable d,int size){
   Bitmap b=Bitmap.createBitmap(size,size,Bitmap.Config.ARGB_8888);
   Rect old=new Rect(d.getBounds());d.setBounds(0,0,size,size);d.draw(new Canvas(b));d.setBounds(old);return b;
  }
 }
 static boolean resizeClassification(Object item,Bitmap b){
  check(item==null,"null classification fallback matches original null ColorInfo resize=false");
  check(!b.isRecycled(),"prepared input alive while classifying");return Color.red(b.getPixel(0,0))>128;
 }
 static Bitmap composeTexture(Bitmap b,int size,Object item,int mode,boolean resized,StaticSource resolved){
  compositions++;preparedSeen=b;resolvedSeen=resolved;
  check(!b.isRecycled(),"prepared alive in compositor");
  check(resolved.type.equals(type),"current type consumed");
  check(resolved.drawable==formal||(circle&&"DEFAULT".equals(type)&&resolved.drawable==null),"same selected drawable passed directly to original compositor");
  check(resized==(Color.red(b.getPixel(0,0))>128),"current source classification consumed");
  if(fail)throw new IllegalStateException("injected compositor failure");
  return alias?b:b.copy(Bitmap.Config.ARGB_8888,false);
 }
 METHODS
 static void check(boolean ok,String message){checks++;if(!ok)throw new AssertionError(message);}
 public static void main(String[] args){try{test();}catch(Throwable e){e.printStackTrace();System.exit(1);}}
 static void test(){
  Item item=new Item();cached=Bitmap.createBitmap(4,4,Bitmap.Config.ARGB_8888);Bitmap shared=Bitmap.createBitmap(32,32,Bitmap.Config.ARGB_8888);
  for(String t:new String[]{"DEFAULT","CUSTOM","PACK","RESOURCE","IMPROVED"})
   for(boolean framed:new boolean[]{false,true})for(int color:new int[]{0x80cc2211,0xff112233}){
    type=t;circle=framed;shared.eraseColor(color);int generation=shared.getGenerationId(),originalPixel=shared.getPixel(0,0);formal=new BitmapDrawable(android.content.res.Resources.getSystem(),shared);loads=0;
    Bitmap result=composeCurrentStaticApplicationIconTexture(item,cached,12);
    check(loads==1,"one formal source request "+t);check(result.getPixel(0,0)==shared.getPixel(0,0),"native pixels and alpha "+t);
    boolean borrowed=EXPECT_BORROWED&&!(framed&&"DEFAULT".equals(t));
    check(borrowed?preparedSeen==shared&&!preparedSeen.isRecycled():preparedSeen!=shared&&preparedSeen.isRecycled(),"composition input ownership "+t);
    check(!shared.isRecycled()&&!result.isRecycled(),"shared drawable/result remain alive "+t);result.recycle();
    check(shared.getGenerationId()==generation&&shared.getPixel(0,0)==originalPixel,"borrowed input remains unchanged "+t);
   }
  java.io.ByteArrayOutputStream png=new java.io.ByteArrayOutputStream();
  cached.compress(Bitmap.CompressFormat.PNG,100,png);item.iconRawData=png.toByteArray();
  Bitmap decoded1=iconRawSource(item),decoded2=iconRawSource(item);
  check(decoded1!=null&&decoded2!=null&&decoded1!=decoded2&&decoded1!=cached,"raw decoder returns exclusively owned images");
  decoded1.recycle();check(!decoded2.isRecycled()&&!cached.isRecycled(),"raw decode lifetime independent");decoded2.recycle();
  // The same identity/source id is intentionally retained across changed pixels.
  type="CUSTOM";circle=false;shared.eraseColor(0xffabcdef);loads=0;
  Bitmap changed=composeCurrentStaticApplicationIconTexture(item,cached,20);
  check(loads==1&&changed.getPixel(0,0)==0xffabcdef,"fresh source on next call despite unchanged identity");changed.recycle();
  formal=null;loads=0;int count=compositions;
  check(composeCurrentStaticApplicationIconTexture(item,cached,12)==null&&loads==1&&compositions==count,"missing source delegates to original recovery");
  formal=new BitmapDrawable(android.content.res.Resources.getSystem(),shared);
  Bitmap ready=composeCurrentStaticApplicationIconTexture(item,cached,12);
  check(ready!=null&&ready.getPixel(0,0)==0xffabcdef,"source becoming ready is retried next call");ready.recycle();
  for(byte[] raw:new byte[][]{null,new byte[0],new byte[]{1,2,3}}){item.iconRawData=raw;loads=0;
   check(composeCurrentStaticApplicationIconTexture(item,iconRawSource(item),12)==null&&loads==0,"missing/corrupt DB bytes retain original recovery");}
  item.iconRawData=new byte[]{1};quick=true;loads=0;
  check(composeCurrentStaticApplicationIconTexture(item,cached,12)==null&&loads==0,"quick path excluded");quick=false;normal=false;
  check(composeCurrentStaticApplicationIconTexture(item,cached,12)==null&&loads==0,"active/special path excluded");normal=true;
  check(composeCurrentStaticApplicationIconTexture(item,null,12)==null,"null decoded cache retains original path");
  alias=true;Bitmap transferred=composeCurrentStaticApplicationIconTexture(item,cached,12);
  check(!transferred.isRecycled()&&(EXPECT_BORROWED?transferred!=shared&&preparedSeen==shared:transferred==preparedSeen),"geometry fallback returns exclusively owned result");transferred.recycle();check(!shared.isRecycled(),"fallback release leaves borrowed input alive");alias=false;
  fail=true;try{composeCurrentStaticApplicationIconTexture(item,cached,12);throw new AssertionError("failure swallowed");}
  catch(IllegalStateException expected){check(preparedSeen.isRecycled()!=EXPECT_BORROWED&&!shared.isRecycled(),"exception releases only owned temporary");}fail=false;
  Bitmap rgb=Bitmap.createBitmap(16,16,Bitmap.Config.RGB_565);rgb.eraseColor(0xff778899);formal=new BitmapDrawable(android.content.res.Resources.getSystem(),rgb);
  Bitmap rgbResult=composeCurrentStaticApplicationIconTexture(item,cached,12);
  check(preparedSeen!=rgb&&preparedSeen.isRecycled()&&!rgb.isRecycled(),"non ARGB source retains owned conversion");rgbResult.recycle();rgb.recycle();
  ColorDrawable vector=new ColorDrawable(0xff998877);vector.setBounds(3,4,13,14);formal=vector;type="RESOURCE";
  Bitmap vectorResult=composeCurrentStaticApplicationIconTexture(item,cached,12);
  check(vector.getBounds().equals(new Rect(3,4,13,14)),"vector preparation restores bounds");vectorResult.recycle();check(!cached.isRecycled(),"API never recycles caller input");cached.recycle();
  check(composeCurrentStaticApplicationIconTexture(item,cached,12)==null,"recycled cache rejected");shared.recycle();
  System.out.println("PASS LOCAL_COMPOSE checks="+checks+" expectBorrowed="+EXPECT_BORROWED+" defaultCircleOwnsTemporary=true geometryFallbackOwnsResult=true sameIdentityReplacement=true boundary=recording-compositor");
  UNCACHED_CALL
 }
}'''.replace('METHODS', methods).replace('EXPECT_BORROWED_VALUE', 'true' if args.expect_borrowed else 'false').replace('UNCACHED_CALL', 'uncached();' if args.uncached else '')
    if args.uncached:
        extra = UNCACHED.replace('OPTIMIZED', 'true' if optimized else 'false')
        dispatch = ('return composeUncachedStaticApplicationIconTexture(i,12);' if optimized else
                    'Bitmap b=prepareUncachedStaticSource(i);if(b==null)return null;return composeTexture(b,0,i,12,resizeClassification(null,b),resolveStaticSource(i,b,true));')
        java = java[:java.rfind('}')] + extra.replace('DISPATCH', dispatch) + '\n}'
    if 'desktopSourceForComposition(itemInfo)' in source:
        java = java.replace(' static class MaintainedLauncherSettingsHost {', '''
 static boolean snapshotFast;
 static class MaintainedLauncherSettingsHost {
  static class ManagedIconSource {
   Drawable drawable;String desktopType,desktopIdentity;
   ManagedIconSource(Drawable d){drawable=d;desktopType=type;desktopIdentity="same-identity";}
  }
  static ManagedIconSource desktopSourceForComposition(Object item){return snapshotFast?new ManagedIconSource(formal):null;}
''')
        java = java.replace('  ColorDrawable vector=new ColorDrawable', '''
  snapshotFast=true;type="IMPROVED";formal=new BitmapDrawable(android.content.res.Resources.getSystem(),shared);
  loads=typeQueries=identityQueries=0;int composedBefore=compositions;
  Bitmap snapResult=composeCurrentStaticApplicationIconTexture(item,cached,12);
  check(snapResult!=null&&loads==0&&typeQueries==0&&identityQueries==0&&compositions==composedBefore+1,"snapshot skips duplicate source/type/identity queries");
  check(!shared.isRecycled()&&!snapResult.isRecycled(),"snapshot handoff keeps Drawable/result alive");snapResult.recycle();snapshotFast=false;
  ColorDrawable vector=new ColorDrawable''')
    if disk_candidate:
        java = java.replace(' static class MaintainedLauncherSettingsHost {',
                            ' static class MaintainedLauncherSettingsHost { static android.content.Context currentApplicationContext(){return null;}')
        extra = '''
 static String persistentFinalKey(Object i,Bitmap b,int mode,StaticSource source,boolean resized){return null;}
 static class NormalIconRasterSpec {int textureWidth=100;}
 static NormalIconRasterSpec resolveNormalIconRasterSpec(int mode){return new NormalIconRasterSpec();}
 static class DiskRepository {
  static DiskRepository get(android.content.Context context){return new DiskRepository();}
  Bitmap readFinalTexture(String key,int size){throw new AssertionError("disk bypass ownership fixture");}
  void persistFinalTexture(String key,Bitmap b){throw new AssertionError("disk bypass ownership fixture");}
 }
'''
        java = java[:java.rfind('}')] + extra + '\n}'
    src = out / 'LocalComposeProbe.java'
    src.write_text(java, encoding='utf8')
    app = out / 'ja.java'
    app.write_text('package com.smartisanos.launcher; public class ja { public static ja getInstance(){return new ja();} public android.content.Context getApplication(){return new android.content.ContextWrapper(null);} }', encoding='utf8')
    sdk = Path('D:/sdk')
    jdk = Path('E:/Program Files/Android/Android Studio/jbr/bin')

    def run(command, name):
        r = subprocess.run(list(map(str, command)), capture_output=True, text=True, encoding='utf8', errors='replace', timeout=100)
        (out / name).write_text(r.stdout + r.stderr, encoding='utf8')
        if r.returncode:
            raise RuntimeError(r.stdout + r.stderr)
        return r.stdout

    run([jdk / 'javac.exe', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-cp', sdk / 'platforms/android-36/android.jar', '-d', out / 'classes', src, app], 'javac.log')
    run([sdk / 'build-tools/37.0.0/d8.bat', '--lib', sdk / 'platforms/android-36/android.jar', '--output', out / 'dex', *sorted((out / 'classes').rglob('*.class'))], 'd8.log')
    adb = [sdk / 'platform-tools/adb.exe', '-s', args.serial]
    run([*adb, 'push', out / 'dex/classes.dex', '/data/local/tmp/local-compose-probe.dex'], 'push.log')
    try:
        print(run([*adb, 'shell', 'CLASSPATH=/data/local/tmp/local-compose-probe.dex', 'app_process', '/system/bin', 'LocalComposeProbe'], 'result.log'))
    finally:
        run([*adb, 'shell', 'rm', '-f', '/data/local/tmp/local-compose-probe.dex'], 'cleanup.log')


UNCACHED = r'''
 static Bitmap uncachedCall(Item i){DISPATCH}
 static void uncached(){
  final boolean optimized=OPTIMIZED;int began=checks;Item item=new Item();
  Bitmap shared=Bitmap.createBitmap(32,32,Bitmap.Config.ARGB_8888);shared.eraseColor(0xff2468ac);
  settings=false;normal=true;quick=false;fail=false;alias=false;sDesktopPageReady=false;
  PENDING_SOURCE_WRITES.clear();admissions=0;
  for(String t:new String[]{"DEFAULT","CUSTOM","PACK","RESOURCE","IMPROVED"})
   for(boolean framed:new boolean[]{false,true})for(byte[] missing:new byte[][]{null,new byte[0]}){
    type=t;circle=framed;item.iconRawData=missing;
    formal=new BitmapDrawable(android.content.res.Resources.getSystem(),shared);loads=0;typeQueries=0;identityQueries=0;int generation=shared.getGenerationId();
    Bitmap result=uncachedCall(item);
    int expected=optimized||(circle&&"DEFAULT".equals(t))?1:2;
    check(loads==expected,"uncached source count "+t+" circle="+circle);
    check(typeQueries==(optimized?1:2)&&identityQueries==(optimized?1:2),"uncached type/identity requests including DEFAULT circle");
    check(result!=null&&result.getPixel(0,0)==shared.getPixel(0,0),"uncached native pixels "+t);
    boolean borrowed=EXPECT_BORROWED&&!(framed&&"DEFAULT".equals(t));
    check(borrowed?preparedSeen==shared&&!preparedSeen.isRecycled():preparedSeen.isRecycled()==optimized,"uncached temporary ownership "+t);
    check(!shared.isRecycled()&&!result.isRecycled(),"uncached shared source/result alive");
    check(shared.getGenerationId()==generation,"uncached borrowed source unchanged");
    check(PENDING_SOURCE_WRITES.size()==1&&PENDING_SOURCE_WRITES.values().iterator().next()==item,"same pending item coalesces, no bitmap retained");
    check(admissions==0,"no persistence admission before page ready");
    if(preparedSeen!=shared&&!preparedSeen.isRecycled())preparedSeen.recycle();result.recycle();
   }
  PENDING_SOURCE_WRITES.clear();circle=false;item.iconRawData=new byte[]{1};loads=0;
  check(uncachedCall(item)==null&&loads==0&&PENDING_SOURCE_WRITES.isEmpty(),"existing bytes retain cached/corrupt recovery path");
  item.iconRawData=null;settings=true;check(uncachedCall(item)==null&&loads==0,"settings resource shortcut excluded");settings=false;
  normal=false;check(uncachedCall(item)==null&&loads==0,"non-static excluded");normal=true;
  for(int i=0;i<512;i++)PENDING_SOURCE_WRITES.put("full"+i,item);
  check(uncachedCall(item)==null&&loads==0&&PENDING_SOURCE_WRITES.size()==512,"512 cap does not resolve or admit extra item");PENDING_SOURCE_WRITES.clear();
  formal=null;check(uncachedCall(item)==null&&PENDING_SOURCE_WRITES.isEmpty(),"missing formal source leaves original recovery available");
  apkFallback=true;type="PACK";
  if(optimized)check(uncachedCall(item)==null&&PENDING_SOURCE_WRITES.isEmpty(),"APK fallback must not freeze a missing managed source");
  Bitmap fallback=prepareUncachedStaticSource(item);
  check(fallback!=null&&PENDING_SOURCE_WRITES.size()==1,"original fallback preparation/persistence retained");fallback.recycle();PENDING_SOURCE_WRITES.clear();apkFallback=false;
  type="CUSTOM";formal=new BitmapDrawable(android.content.res.Resources.getSystem(),shared);shared.eraseColor(0xffabcdef);loads=0;
  Bitmap persistedSource=prepareStaticSource(item,null);
  check(persistedSource!=shared&&!persistedSource.isRecycled(),"source persistence API still returns an owned copy");persistedSource.recycle();check(!shared.isRecycled(),"persistence release leaves Drawable alive");loads=0;
  Bitmap changed=uncachedCall(item);check(loads==(optimized?1:2)&&changed.getPixel(0,0)==0xffabcdef,"same identity next call sees replacement/current type");
  if(preparedSeen!=shared&&!preparedSeen.isRecycled())preparedSeen.recycle();changed.recycle();
  fail=true;try{uncachedCall(item);throw new AssertionError("uncached failure swallowed");}
  catch(IllegalStateException expected){check(preparedSeen.isRecycled()==(optimized&&!EXPECT_BORROWED)&&!shared.isRecycled(),"uncached exception releases only owned temporary");}
  if(preparedSeen!=shared&&!preparedSeen.isRecycled())preparedSeen.recycle();fail=false;
  PENDING_SOURCE_WRITES.clear();sDesktopPageReady=true;admissions=0;alias=true;
  Bitmap transferred=uncachedCall(item);
  check(!transferred.isRecycled()&&(EXPECT_BORROWED?transferred!=shared&&preparedSeen==shared:transferred==preparedSeen),"uncached alias result ownership transferred");
  check(admissions==1&&PENDING_SOURCE_WRITES.size()==1,"post-page source offers existing persistence owner");transferred.recycle();alias=false;shared.recycle();
  System.out.println("PASS UNCACHED_COMPOSE checks="+(checks-began)+" optimized="+optimized+" expectBorrowed="+EXPECT_BORROWED+" nonCircleSourceRequests="+(optimized?1:2)+" circleDefault=1 typeAndIdentityQueries="+(optimized?1:2)+" pendingLimit=512 queueHasNoBitmaps=true boundary=recording-compositor");
 }
'''


if __name__ == '__main__':
    main()
