"""Run the production persistence bridge and bounded admission with worker barriers."""
import argparse
import importlib.util
import pathlib
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("preview_tests", ROOT / "tools/tests/icon_preview/run_tests.py")
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jdk", type=pathlib.Path, required=True)
    parser.add_argument("--source", type=pathlib.Path,
                        default=ROOT / "launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java")
    args = parser.parse_args()
    source = args.source.read_text(encoding="utf-8")
    repository = (ROOT / "launcher/tools/java/com/smartisanos/home/settings/icons/IconPreviewRepository.java").read_text(encoding="utf-8")
    methods = "\n".join(preview.block(source, marker) for marker in (
        "    public static void onDesktopPageReady()", "    private static void scheduleSourceWrites()",
        "    private static void persistSource(", "    public static Bitmap prepareUncachedStaticSource(",
        "    public static Bitmap composeUncachedStaticApplicationIconTexture(",
        "    private static Bitmap prepareUncachedStaticSource("))
    fixture = '''package com.smartisanos.launcher.theme;
import java.util.*; import java.util.concurrent.*;
import android.util.Log;
import android.graphics.Bitmap;
import com.smartisanos.launcher.data.ItemInfo;
import com.smartisanos.home.settings.icons.IconPreviewRepository;
public class DeferredProbe {
 static final String TAG="test";
 static final Map<String,Object> PENDING_SOURCE_WRITES=new LinkedHashMap<>();
 static boolean sDesktopPageReady,sSourceWriteScheduled;
 static boolean shouldUseHighResolutionDesktopRaster(Object item){return item instanceof ItemInfo&&((ItemInfo)item).normal;}
 static boolean isDesktopSettingsShortcut(Object item){return ((ItemInfo)item).settings;}
 static Bitmap prepareStaticSource(Object item,Bitmap cached){return ((ItemInfo)item).available?new Bitmap():null;}
 static class StaticSource {Object drawable;boolean legacyDefaultBitmap;String identity="FORMAL";}
 static StaticSource resolveStaticSource(Object item,Bitmap cached){StaticSource s=new StaticSource();s.drawable=((ItemInfo)item).available?new Object():null;return s;}
 static Bitmap prepareResolvedStaticSource(Object item,Bitmap cached,StaticSource resolved){return prepareStaticSource(item,cached);}
 // This fixture exercises queue ownership; native borrowed-source ownership has its own device suite.
 static Bitmap borrowedCompositionSource(Object item,StaticSource resolved){return null;}
 static Bitmap composePreparedStaticSource(Object item,Bitmap source,int mode,StaticSource resolved,boolean borrowed){
  if(Thread.holdsLock(PENDING_SOURCE_WRITES))throw new AssertionError("composition held persistence lock");return source;
 }
 static String itemField(Object item,String name){try{return String.valueOf(item.getClass().getField(name).get(item));}catch(Exception e){throw new RuntimeException(e);}}
 METHODS
 static void check(boolean b,String m){if(!b)throw new AssertionError(m);}
 static void ready(int count){sDesktopPageReady=false;for(int i=1;i<=count;i++){ItemInfo item=new ItemInfo();item.id=i;com.smartisanos.launcher.Aa.items.put((long)i,item);PENDING_SOURCE_WRITES.put("item"+i,item);}}
 static void waitDone()throws Exception{long end=System.nanoTime()+TimeUnit.SECONDS.toNanos(5);while(System.nanoTime()<end){synchronized(PENDING_SOURCE_WRITES){if(!sSourceWriteScheduled&&PENDING_SOURCE_WRITES.isEmpty())return;}Thread.yield();}throw new AssertionError("persistence did not drain");}
 public static void main(String[] args)throws Exception {
  for(String type:new String[]{"DEFAULT","IMPROVED","PACK","CUSTOM","RESOURCE"}) {
   ItemInfo item=new ItemInfo();item.sourceType=type;
   check(prepareUncachedStaticSource(item)!=null,"missing legacy cache must not force encode before rendering "+type);
   check(PENDING_SOURCE_WRITES.size()==1&&com.smartisanos.launcher.e.s.writes==0,"queue necessary persistence without synchronous write "+type);
   PENDING_SOURCE_WRITES.clear();item.iconRawData=new byte[]{1};
   check(prepareUncachedStaticSource(item)==null&&PENDING_SOURCE_WRITES.isEmpty(),"existing bytes retain original path "+type);
   item.iconRawData=new byte[0];item.available=false;
   check(prepareUncachedStaticSource(item)==null&&PENDING_SOURCE_WRITES.isEmpty(),"missing formal source retains fallback "+type);
   item.available=true;item.normal=false;
   check(prepareUncachedStaticSource(item)==null,"non-static/active/folder gate "+type);
   item.normal=true;item.settings=true;
   check(prepareUncachedStaticSource(item)==null,"settings shortcut remains resource-owned "+type);
   item.settings=false;item.iconRawData=null;
   check(composeUncachedStaticApplicationIconTexture(item,12)!=null,"uncached composition retains admission "+type);
   check(PENDING_SOURCE_WRITES.size()==1&&com.smartisanos.launcher.e.s.writes==0,"composition queues item without synchronous DB write "+type);
   PENDING_SOURCE_WRITES.clear();
  }
  ItemInfo bounded=new ItemInfo();for(int i=0;i<512;i++)PENDING_SOURCE_WRITES.put("full"+i,bounded);
  check(prepareUncachedStaticSource(bounded)==null&&PENDING_SOURCE_WRITES.size()==512,"pending queue cap retains original path");
  check(composeUncachedStaticApplicationIconTexture(bounded,12)==null&&PENDING_SOURCE_WRITES.size()==512,"uncached compositor respects same pending cap");
  PENDING_SOURCE_WRITES.clear();
  IconPreviewRepository repo=IconPreviewRepository.get(new android.content.Context());
  CountDownLatch entered=new CountDownLatch(1),release=new CountDownLatch(1);
  repo.onlinePool.execute(()->{entered.countDown();try{release.await();}catch(Exception e){throw new RuntimeException(e);}});entered.await();
  repo.pauseP2=true;ready(20);onDesktopPageReady();onDesktopPageReady();
  check(repo.onlinePool.getQueue().size()==1,"batch must use one admission and coalesce page events");
  release.countDown();waitDone();
  check(com.smartisanos.launcher.e.s.writes==20,"paused previews dropped mandatory writes");
  CountDownLatch busy=new CountDownLatch(1),resume=new CountDownLatch(1);
  repo.onlinePool.execute(()->{busy.countDown();try{resume.await();}catch(Exception e){throw new RuntimeException(e);}});busy.await();
  CountDownLatch queueEmpty=new CountDownLatch(1);repo.onlinePool.execute(()->queueEmpty.countDown());
  ready(1);onDesktopPageReady();
  check(!sSourceWriteScheduled&&PENDING_SOURCE_WRITES.size()==1,"rejected batch must remain offerable");
  resume.countDown();check(queueEmpty.await(5,TimeUnit.SECONDS),"queue barrier");
  onDesktopPageReady();waitDone();check(com.smartisanos.launcher.e.s.writes==21,"next page event did not recover rejection");
  ready(1);com.smartisanos.launcher.Aa.items.get(1L).componentName="Replacement";
  // A separate retained item represents the old component.
  PENDING_SOURCE_WRITES.put("item1",new ItemInfo());onDesktopPageReady();waitDone();
  check(com.smartisanos.launcher.e.s.writes==21,"replaced identity was persisted");
  repo.onlinePool.shutdownNow();System.out.println("PASS: paused preview persistence, single batch admission, coalescing, bounded rejection/re-offer, stale identity");
 }
}'''.replace("METHODS", methods)
    sources = {
        "com/smartisanos/launcher/theme/DeferredProbe.java": fixture,
        "com/smartisanos/home/settings/icons/IconPreviewRepository.java": '''package com.smartisanos.home.settings.icons;
import java.util.concurrent.*;
public class IconPreviewRepository {
 public boolean pauseP2;
 public final ThreadPoolExecutor onlinePool=new ThreadPoolExecutor(1,1,1,TimeUnit.SECONDS,new ArrayBlockingQueue<Runnable>(1),r->{Thread t=new Thread(r);t.setDaemon(true);return t;},new ThreadPoolExecutor.AbortPolicy());
 static final IconPreviewRepository instance=new IconPreviewRepository();
 public static IconPreviewRepository get(android.content.Context c){return instance;}
''' + preview.block(repository, "    public boolean schedulePersistence(") + "}",
        "android/content/Context.java": "package android.content; public class Context {}",
        "android/graphics/Bitmap.java": "package android.graphics; public class Bitmap {}",
        "android/util/Log.java": "package android.util; public class Log {public static int i(String t,String m){return 0;}public static int w(String t,String m){return 0;}public static int w(String t,String m,Throwable e){throw new AssertionError(m,e);}}",
        "com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java": "package com.smartisanos.launcher.theme; public class MaintainedLauncherSettingsHost {public static android.content.Context currentApplicationContext(){return new android.content.Context();} public static String desktopIconSourceType(Object i){return ((com.smartisanos.launcher.data.ItemInfo)i).sourceType;}}",
        "com/smartisanos/launcher/data/ItemInfo.java": "package com.smartisanos.launcher.data; public class ItemInfo {public long id=1;public String packageName=\"example.app\",componentName=\"Main\",sourceType=\"DEFAULT\";public boolean normal=true,settings,available=true;public int userId=0;public byte[] iconRawData;}",
        "com/smartisanos/launcher/Aa.java": "package com.smartisanos.launcher; import com.smartisanos.launcher.data.ItemInfo;public class Aa {public static java.util.Map<Long,ItemInfo> items=new java.util.HashMap<>();public static ItemInfo i(long id){return items.get(id);}}",
        "com/smartisanos/launcher/e/s.java": "package com.smartisanos.launcher.e;public class s {public static volatile int writes;public static byte[] a(com.smartisanos.launcher.data.ItemInfo item,boolean persist){writes++;return new byte[]{1,2,3};}}",
    }
    with tempfile.TemporaryDirectory(prefix="launcher-deferred-source-") as folder:
        work = pathlib.Path(folder)
        for name, content in sources.items():
            target = work / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        subprocess.run([str(args.jdk / "bin/javac.exe"), "-d", str(work / "classes"), *map(str, work.rglob("*.java"))], check=True)
        subprocess.run([str(args.jdk / "bin/java.exe"), "-cp", str(work / "classes"), "com.smartisanos.launcher.theme.DeferredProbe"], check=True, timeout=20)


if __name__ == "__main__":
    main()
