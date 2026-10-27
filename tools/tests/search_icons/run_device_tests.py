"""Run the real backend/Bitmap/Looper with isolated model and final-composer doubles.

No APK installation or installed Launcher data access. Complements actual UI tests.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("icon_host_tests", Path(__file__).with_name("run_tests.py"))
host = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host)

PROBE = '''import android.content.*;import android.graphics.*;import android.os.*;
import java.util.*;import java.util.concurrent.*;
import com.smartisanos.launcher.quicksearch.*;
public class AndroidSearchIconProbe {
 static int checks;static void check(boolean b,String m){checks++;if(!b)throw new AssertionError(m);}
 static void waitFor(CountDownLatch l)throws Exception{check(l.await(10,TimeUnit.SECONDS),"completion timeout");}
 static SearchEntry entry(int i){String p="example.app"+i;return new SearchEntry(i==0?"000 Share":"zzz"+i,"",p,"Main",0,0,null,p+"/Main@0");}
 static void runProbe()throws Exception {
  Context context=new ContextWrapper(null){public Context getApplicationContext(){return this;}
   public android.content.res.Resources getResources(){return android.content.res.Resources.getSystem();}
   public Object getSystemService(String n){return null;}};
  Bitmap image=Bitmap.createBitmap(256,256,Bitmap.Config.ARGB_8888);
  int[] pixels=new int[256*256];Random random=new Random(7);for(int i=0;i<pixels.length;i++)pixels[i]=random.nextInt();
  image.setPixels(pixels,0,256,0,0,256,256);java.io.ByteArrayOutputStream out=new java.io.ByteArrayOutputStream();
  check(image.compress(Bitmap.CompressFormat.PNG,100,out),"PNG encode");image.recycle();byte[] png=out.toByteArray();
  check(png.length*48L>8L*1024*1024,"PNG pressure fixture must exceed production maximum cache");
  List<SearchEntry> entries=new ArrayList<>();for(int i=0;i<48;i++){
   SearchEntry e=entry(i);entries.add(e);com.smartisanos.launcher.Aa.Item item=new com.smartisanos.launcher.Aa.Item();
   item.id=i+1;item.packageName=e.packageName;item.iconData=png;com.smartisanos.launcher.Aa.items.put(item.id,item);
  }
  CountDownLatch hydrated=new CountDownLatch(1);SearchIconBackend.scheduleHydration(context,new SearchSnapshot(entries,1),g->hydrated.countDown());waitFor(hydrated);
  check(SearchIconBackend.getEncoded(entries.get(0))==null,"real LRU eviction");
  check(SearchIconBackend.getDecoded(entries.get(0))!=null,"Top5 refill after eviction");
  int scans=com.smartisanos.launcher.Aa.snapshots;
  CountDownLatch visible=new CountDownLatch(1);SearchIconBackend.requestDecoded(context,entries.get(6),(k,g,b)->{
   check(b!=null&&!b.isRecycled(),"visible icon must decode");
   int target=Math.round(36*context.getResources().getDisplayMetrics().density);
   check(b.getWidth()==target&&b.getHeight()==target,"real target raster dimensions");visible.countDown();});waitFor(visible);
  check(com.smartisanos.launcher.Aa.snapshots==scans,"no per-row full scan");
  SearchIconBackend.invalidateAll("fixture");com.smartisanos.launcher.Aa.items.clear();
  com.smartisanos.launcher.Aa.Item absent=new com.smartisanos.launcher.Aa.Item();absent.packageName=entry(0).packageName;absent.iconData=null;
  com.smartisanos.launcher.Aa.items.put(1L,absent);CountDownLatch recovered=new CountDownLatch(1);
  SearchIconBackend.scheduleHydration(context,new SearchSnapshot(Arrays.asList(entry(0)),2),g->recovered.countDown());waitFor(recovered);
  check(SearchIconBackend.getDecoded(entry(0))!=null,"deferred PNG uses final composer");
  System.out.println("PASS ANDROID_SEARCH_ICON_CHECKS="+checks+" pngBytes="+png.length);
 }
 public static void main(String[] args){if(Looper.getMainLooper()==null)Looper.prepareMainLooper();
  new Thread(()->{try{runProbe();System.exit(0);}catch(Throwable e){e.printStackTrace();System.exit(1);}},"icon-test").start();Looper.loop();}
}'''


def main():
    ap = argparse.ArgumentParser(__doc__)
    for key in ("serial", "jdk", "sdk", "output"):
        ap.add_argument("--" + key, required=True)
    a = ap.parse_args()
    out, jdk, sdk = Path(a.output), Path(a.jdk), Path(a.sdk)
    out.mkdir(parents=True, exist_ok=True)
    classes, dex = out / "classes", out / "dex"
    classes.mkdir(exist_ok=True)
    dex.mkdir(exist_ok=True)
    def run(cmd):
        r = subprocess.run(list(map(str, cmd)), capture_output=True, text=True, encoding="utf8", errors="replace", timeout=90)
        if r.returncode:
            raise RuntimeError(r.stdout + r.stderr)
        return r.stdout
    sources = {
        "com/smartisanos/launcher/Aa.java": host.SOURCES["com/smartisanos/launcher/Aa.java"],
        "com/smartisanos/launcher/theme/IconRasterDiagnostics.java": '''package com.smartisanos.launcher.theme;
public class IconRasterDiagnostics {public static android.graphics.Bitmap composeStaticApplicationIconTexture(Object i,android.graphics.Bitmap b){
 android.graphics.Bitmap result=android.graphics.Bitmap.createBitmap(256,256,android.graphics.Bitmap.Config.ARGB_8888);result.eraseColor(0xff337799);return result;}}''',
        "AndroidSearchIconProbe.java": PROBE,
    }
    files = []
    for name, source in sources.items():
        p = out / "src" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(source, encoding="utf8")
        files.append(p)
    for name in ("SearchIconBackend", "SearchEntry", "SearchSnapshot", "QuickSearchIndexLogger"):
        files.append(ROOT / "launcher/tools/java/com/smartisanos/launcher/quicksearch" / (name + ".java"))
    run([jdk / "bin/javac.exe", "-source", "8", "-target", "8", "-encoding", "UTF-8", "-cp", sdk / "platforms/android-36/android.jar", "-d", classes, *files])
    run([jdk / "bin/jar.exe", "cf", out / "probe.jar", "-C", classes, "."])
    os.environ["JAVA_HOME"] = str(jdk)
    run([sdk / "build-tools/37.0.0/d8.bat", "--min-api", "26", "--output", dex, out / "probe.jar"])
    adb = sdk / "platform-tools/adb.exe"
    def device(*cmd):
        return run([adb, "-s", a.serial, *cmd])
    remote = "/data/local/tmp/search-icon-test-" + uuid.uuid4().hex
    device("shell", "mkdir", remote)
    device("push", dex / "classes.dex", remote + "/probe.dex")
    before = device("shell", "pidof", "com.smartisanos.launcher").strip()
    result = device("shell", "CLASSPATH=" + remote + "/probe.dex app_process /system/bin AndroidSearchIconProbe")
    after = device("shell", "pidof", "com.smartisanos.launcher").strip()
    assert "PASS ANDROID_SEARCH_ICON_CHECKS=" in result, result
    (out / "summary.json").write_text(json.dumps({"result": result, "pid_before": before, "pid_after": after, "serial": a.serial, "scope": __doc__}, ensure_ascii=False, indent=2), encoding="utf8")
    print(result)


if __name__ == "__main__":
    main()
