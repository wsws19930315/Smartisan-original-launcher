"""Exercise the production resolver against Android Bitmaps and counted source loads."""
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
    ap = argparse.ArgumentParser()
    ap.add_argument('--serial', required=True)
    ap.add_argument('--baseline', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--audit-lifecycle', action='store_true', help='Audit the prepare/compose resolver boundary without production edits')
    args = ap.parse_args()
    out = args.output
    (out / 'classes').mkdir(parents=True, exist_ok=True)
    (out / 'dex').mkdir(exist_ok=True)
    current = (ROOT / 'launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java').read_text(encoding='utf8')
    baseline = args.baseline.read_text(encoding='utf8')
    signature = '    private static StaticSource resolveStaticSource(Object itemInfo, Bitmap legacyBitmap)'
    owners = []
    for name, source in [('Before', baseline), ('After', current)]:
        methods = block(source, signature)
        if name == 'After':
            methods += block(source, '    private static StaticSource resolveStaticSource(Object itemInfo, Bitmap legacyBitmap,')
            if args.audit_lifecycle:
                methods += block(source, '    public static Bitmap prepareStaticSource(Object itemInfo, Bitmap cachedSource)')
                if 'private static Bitmap prepareResolvedStaticSource(' in source:
                    methods += block(source, '    private static Bitmap prepareResolvedStaticSource(')
                methods += block(source, '    public static Bitmap sourceBitmap(android.graphics.drawable.Drawable drawable)')
                methods += block(source, '    private static boolean resizeClassification(Object itemInfo, Bitmap source)')
                methods += block(source, '    private static boolean resizeClassification(Object itemInfo)')
                methods += 'static boolean classify(Object i,Bitmap b){return resizeClassification(i,b);}'
        if args.audit_lifecycle:
            methods += block(source, '    private static Bitmap decorateProfileIcon(')
            methods += 'static Bitmap decorate(Object i,Bitmap b){return decorateProfileIcon(i,b' + (',type' if name == 'After' else '') + ');}'
        owners.append('static class ' + name + '{' + block(source, '    private static final class StaticSource {') + methods
                      + 'static StaticSource get(Object i,Bitmap b){return resolveStaticSource(i,b' + (',true' if name == 'After' else '') + ');}}')
    java = r'''
import android.graphics.*;import android.graphics.drawable.*;import android.util.Log;
public class PreparedSourceProbe {
 static String TAG="test";static int loads,checks;static boolean circle,settings;static String type;
 static Drawable formal;
 static int sourceTypeChecks;static boolean contextPresent,compat,profile,copyBadge;
 static boolean isNonManagedLauncherProfile(android.content.Context c,String p,String n,int u){return profile;}
 static class DoppelgangerCompat {static boolean isDoppelganger(android.content.Context c,String p,String n,int u){return compat;}}
 static final int CANONICAL_DEFAULT_SOURCE_SIZE=256;
 static String itemField(Object i,String n){return "0";}
 static boolean isQuickLaunchItem(Object i){return false;}
 static boolean isDesktopSettingsShortcut(Object i){return settings;}
 static Drawable loadCurrentDesktopDrawable(Object i){loads++;return formal;}
 static class StartupPageSceneDiagnostics {static long detailBegin(){return 0;}static void detailEnd(Object i,String s,long n){}}
 static class MaintainedLauncherSettingsHost {
  static String desktopIconSourceType(Object i){sourceTypeChecks++;return type;}
  static android.content.Context currentApplicationContext(){return contextPresent?new android.content.ContextWrapper(null):null;}
  static Bitmap doppelgangerBitmap(Bitmap b){if(!copyBadge)return b;Bitmap result=b.copy(Bitmap.Config.ARGB_8888,true);result.setPixel(0,0,0xffaabbcc);return result;}
  static String desktopIconSourceIdentity(Object i){return "identity:"+type;}
  static String desktopIconSourceIdentity(Object i,String t){return "identity:"+t;}
  static boolean desktopDefaultCircleEnabled(Object i){return circle;}
  static boolean desktopDefaultCircleEnabled(Object i,String t){return circle;}
  static Drawable loadDefaultIconForDesktopItem(android.content.Context c,String p,String n,int u){return null;}
 }
 static class DefaultIconCircleRenderer {static Bitmap render(Drawable d,int n){throw new AssertionError("circle rendering is outside this lifecycle probe");}}
 OWNERS
 static void check(boolean b,String s){checks++;if(!b)throw new AssertionError(s);}
 public static void main(String[] args){try{test();}catch(Throwable e){e.printStackTrace();System.exit(1);}}
 static void test(){
  Object item=new Object();Bitmap valid=Bitmap.createBitmap(32,32,Bitmap.Config.ARGB_8888);
  Bitmap dead=Bitmap.createBitmap(1,1,Bitmap.Config.ARGB_8888);dead.recycle();
  for(String t:new String[]{"DEFAULT","CUSTOM","PACK","RESOURCE","IMPROVED"})
   for(boolean framed:new boolean[]{false,true})for(boolean special:new boolean[]{false,true})
    for(Bitmap b:new Bitmap[]{null,valid,dead})for(boolean available:new boolean[]{false,true}){
     type=t;circle=framed;settings=special;formal=available?new ColorDrawable(0xff1256ab):null;
     loads=0;Before.StaticSource old=Before.get(item,b);int oldLoads=loads;
     loads=0;After.StaticSource now=After.get(item,b);int newLoads=loads;
     boolean reuse=!special&&framed&&"DEFAULT".equals(t)&&b!=null&&!b.isRecycled();
     check(newLoads==(reuse?0:oldLoads),"source load count "+t);
     check(now.type.equals(old.type),"effective source type "+t);
     if(!reuse){check(now.drawable==old.drawable,"source priority "+t);
       check(now.identity.equals(old.identity)&&now.legacyDefaultBitmap==old.legacyDefaultBitmap,"fallback identity "+t);}
     else{check(now.drawable==null,"prepared bitmap input "+t);check(!b.isRecycled(),"borrowed source lifetime");}
    }
  check(After.get(null,valid).drawable==null,"null item");
  valid.recycle();System.out.println("PASS PREPARED_SOURCE_ANDROID checks="+checks);
  LIFECYCLE_CALL
 }
 LIFECYCLE_METHODS
}'''.replace('OWNERS', '\n'.join(owners)).replace('LIFECYCLE_CALL', 'lifecycle();' if args.audit_lifecycle else '').replace('LIFECYCLE_METHODS', LIFECYCLE if args.audit_lifecycle else '')
    src = out / 'PreparedSourceProbe.java'
    src.write_text(java, encoding='utf8')
    jdk = Path('E:/Program Files/Android/Android Studio/jbr/bin')
    sdk = Path('D:/sdk')

    def run(command, name):
        r = subprocess.run(list(map(str, command)), capture_output=True, text=True, encoding='utf8', errors='replace', timeout=90)
        (out / name).write_text(r.stdout + r.stderr, encoding='utf8')
        if r.returncode:
            raise RuntimeError(r.stdout + r.stderr)
        return r.stdout

    sources = [src]
    if args.audit_lifecycle:
        classifier = out / 'f.java'
        classifier.write_text('package com.smartisanos.launcher.actions.sort.color; import android.graphics.Bitmap; public class f { public static class Info { public boolean resize; } public static Info c(Bitmap b) { Info i=new Info();i.resize=android.graphics.Color.red(b.getPixel(0,0))>128;return i; } }', encoding='utf8')
        sources.append(classifier)
    run([jdk / 'javac.exe', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-cp', sdk / 'platforms/android-36/android.jar', '-d', out / 'classes', *sources], 'javac.log')
    run([sdk / 'build-tools/37.0.0/d8.bat', '--lib', sdk / 'platforms/android-36/android.jar', '--output', out / 'dex', *sorted((out / 'classes').rglob('*.class'))], 'd8.log')
    adb = [sdk / 'platform-tools/adb.exe', '-s', args.serial]
    run([*adb, 'push', out / 'dex/classes.dex', '/data/local/tmp/prepared-source-probe.dex'], 'push.log')
    print(run([*adb, 'shell', 'CLASSPATH=/data/local/tmp/prepared-source-probe.dex', 'app_process', '/system/bin', 'PreparedSourceProbe'], 'result.log'))


LIFECYCLE = r'''
 public static class Info { public boolean resize=false; }
 public static class Item { public Info color=new Info(); }
 static void lifecycle(){
  int began=checks;Item item=new Item();settings=false;circle=false;
  Bitmap shared=Bitmap.createBitmap(32,32,Bitmap.Config.ARGB_8888);shared.eraseColor(0x80cc2211);
  Bitmap legacy=Bitmap.createBitmap(32,32,Bitmap.Config.ARGB_8888);legacy.eraseColor(0xff0011cc);
  for(String t:new String[]{"DEFAULT","CUSTOM","PACK","RESOURCE","IMPROVED"}){
   type=t;formal=new BitmapDrawable(android.content.res.Resources.getSystem(),shared);loads=0;
   Bitmap prepared=After.prepareStaticSource(item,legacy);
   check(loads==1,"prepare formal load "+t);check(prepared!=shared&&prepared!=legacy,"owned preparation copy "+t);
   check(prepared.sameAs(shared),"copy preserves pixels "+t);
   check(Color.alpha(prepared.getPixel(0,0))==128,"copy preserves alpha "+t);
   check(After.classify(item,prepared)&&!item.color.resize,"classification consumes current prepared bitmap "+t);
   After.StaticSource consumed=After.get(item,prepared);
   check(loads==2,"two stage source requests "+t);
   check(((BitmapDrawable)consumed.drawable).getBitmap()==shared,"existing Bitmap can be reused beneath repeat requests "+t);
   prepared.recycle();check(!shared.isRecycled()&&!legacy.isRecycled(),"owned copy independent lifetime "+t);
   System.out.println("PREPARE_COMPOSE_RESOLVER type="+t+" sourceRequests="+loads+" preparedBytes="+shared.getAllocationByteCount());
  }
  type="CUSTOM";formal=new BitmapDrawable(android.content.res.Resources.getSystem(),shared);
  Bitmap first=After.prepareStaticSource(item,legacy);String identity="identity:"+type;
  formal=new BitmapDrawable(android.content.res.Resources.getSystem(),legacy);
  After.StaticSource second=After.get(item,first);
  check(identity.equals(second.identity),"same metadata identity after replacement");
  check(first.getPixel(0,0)!=((BitmapDrawable)second.drawable).getBitmap().getPixel(0,0),"replacement pixels differ despite same identity");first.recycle();
  formal=null;Bitmap fallback=After.prepareStaticSource(item,legacy);
  check(fallback==legacy,"fallback can return borrowed bitmap");check(!legacy.isRecycled(),"fallback keeps caller alive");
  type="DEFAULT";circle=true;formal=new BitmapDrawable(android.content.res.Resources.getSystem(),shared);loads=0;
  After.StaticSource circleSource=After.get(item,legacy);
  check(loads==0&&circleSource.drawable==null,"existing prepared-circle reuse gate");circle=false;
  ColorDrawable vector=new ColorDrawable(0xff998877);vector.setBounds(3,4,13,14);formal=vector;type="RESOURCE";
  Bitmap vectorCopy=After.prepareStaticSource(item,legacy);
  check(vector.getBounds().equals(new Rect(3,4,13,14)),"drawable bounds restored");check(vectorCopy.getPixel(0,0)==0xff998877,"drawable raster content");vectorCopy.recycle();
  shared.recycle();legacy.recycle();
  Bitmap artwork=Bitmap.createBitmap(32,32,Bitmap.Config.ARGB_8888);artwork.eraseColor(0x80112233);int decorationCases=0;
  for(String t:new String[]{"DEFAULT","CUSTOM","PACK","RESOURCE","IMPROVED"})for(boolean ctx:new boolean[]{false,true})
   for(boolean c:new boolean[]{false,true})for(boolean p:new boolean[]{false,true})for(boolean copy:new boolean[]{false,true}){
    type=t;contextPresent=ctx;compat=c;profile=p;copyBadge=copy;
    sourceTypeChecks=0;Bitmap old=Before.decorate(item,artwork);int before=sourceTypeChecks;
    sourceTypeChecks=0;Bitmap now=After.decorate(item,artwork);
    check(before==1&&sourceTypeChecks==0,"decoration metadata lookup 1 -> 0");
    check(old.sameAs(now)&&(old==artwork)==(now==artwork),"decoration return/pixels unchanged");
    check(!artwork.isRecycled(),"decoration input lifetime unchanged");
    if(old!=artwork)old.recycle();if(now!=artwork)now.recycle();decorationCases++;
   }
  check(After.decorate(item,null)==null,"null decoration");artwork.recycle();check(After.decorate(item,artwork)==artwork,"recycled decoration");
  System.out.println("PASS DECORATION cases="+decorationCases+" sourceTypeLookups=1->0 outputPixelsAndOwnershipUnchanged");
  System.out.println("PASS PREPARED_LIFECYCLE checks="+(checks-began)+" classifier=fixture via production reflection; composition boundary=production resolver, not full GPU compositor");
 }
'''

if __name__ == '__main__':
    main()
