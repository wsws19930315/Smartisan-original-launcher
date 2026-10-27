"""Check actual resize-classification reflection, live bitmap results and failure retries on ART."""
import argparse
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java'


def block(source, marker):
    start = source.index(marker)
    end = source.index('{', start) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def main():
    ap = argparse.ArgumentParser(__doc__)
    for name in ('serial', 'baseline', 'output'):
        ap.add_argument('--' + name, required=True)
    ap.add_argument('--candidate', type=Path, default=SOURCE)
    ap.add_argument('--expect-metadata-reuse', action='store_true')
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    owners = []
    for name, path in [('Before', Path(args.baseline)), ('After', args.candidate)]:
        source = path.read_text('utf8')
        methods = block(source, '    private static boolean resizeClassification(Object itemInfo, Bitmap source)')
        methods += block(source, '    private static boolean resizeClassification(Object itemInfo)')
        methods = methods.replace('classifier.getMethod("c", Bitmap.class)', 'lookup(classifier)')
        field = 'static volatile java.lang.reflect.Method sResizeClassifier;' if 'volatile java.lang.reflect.Method sResizeClassifier;' in source else ''
        body = field + methods + '''static final java.util.concurrent.atomic.AtomicInteger lookups=new java.util.concurrent.atomic.AtomicInteger();
static java.lang.reflect.Method lookup(Class<?> c)throws NoSuchMethodException{lookups.incrementAndGet();return c.getMethod("c",Bitmap.class);}
static boolean run(Object i,Bitmap b){return resizeClassification(i,b);}
'''
        owners.append('static class ' + name + '{' + body + '}')
        if name == 'After':
            for alternative, target in [('Missing', 'test.Missing'), ('WrongSignature', 'ClassifierProbe$Wrong')]:
                owners.append('static class ' + alternative + '{' + body.replace('com.smartisanos.launcher.actions.sort.color.f', target) + '}')
    files = []
    for name, source in [('ClassifierProbe.java', PROBE.replace('OWNERS', '\n'.join(owners)).replace('EXPECT_METADATA_REUSE', str(args.expect_metadata_reuse).lower())),
                         ('com/smartisanos/launcher/actions/sort/color/f.java', FIXTURE)]:
        path = out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, 'utf8')
        files.append(path)
    jdk, sdk = Path('E:/Program Files/Android/Android Studio/jbr'), Path('D:/sdk')
    classes, dex = out / 'classes', out / 'dex'
    classes.mkdir(exist_ok=True)
    dex.mkdir(exist_ok=True)

    def run(command, log):
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                                encoding='utf8', errors='replace', timeout=90)
        (out / log).write_text(result.stdout + result.stderr, 'utf8')
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        return result.stdout

    run([jdk / 'bin/javac.exe', '-source', '8', '-target', '8', '-encoding', 'UTF-8',
         '-bootclasspath', sdk / 'platforms/android-36/android.jar', '-d', classes, *files], 'compile.log')
    os.environ['JAVA_HOME'] = str(jdk)
    run([sdk / 'build-tools/37.0.0/d8.bat', '--min-api', '23', '--output', dex,
         *sorted(classes.rglob('*.class'))], 'dex.log')
    adb = [sdk / 'platform-tools/adb.exe', '-s', args.serial]
    remote = '/data/local/tmp/classifier-metadata-20261026.dex'
    run([*adb, 'push', dex / 'classes.dex', remote], 'push.log')
    try:
        result = run([*adb, 'shell', 'CLASSPATH=' + remote, 'app_process', '/system/bin', 'ClassifierProbe'], 'result.log')
        assert 'PASS CLASSIFIER_METADATA' in result, result
        print(result)
    finally:
        run([*adb, 'shell', 'rm', '-f', remote], 'cleanup.log')


FIXTURE = r'''package com.smartisanos.launcher.actions.sort.color;
import android.graphics.Bitmap;
public class f {
 public static final java.util.concurrent.atomic.AtomicInteger calls=new java.util.concurrent.atomic.AtomicInteger();
 public static boolean fail,empty;
 public static class Info {public boolean resize;Info(boolean r){resize=r;}}
 public static Info c(Bitmap b){calls.incrementAndGet();if(fail)throw new IllegalStateException("fixture");if(empty)return null;return new Info((b.getPixel(0,0)>>>24)<128);}
}'''

PROBE = r'''
import android.graphics.Bitmap;import android.util.Log;import com.smartisanos.launcher.actions.sort.color.f;
public class ClassifierProbe {
 static String TAG="ClassifierProbe";static int checks;static final boolean reuse=EXPECT_METADATA_REUSE;
 public static class Color {public boolean resize;}
 public static class Item {public Color color=new Color();}
 public static class Wrong {public static Object c(String value){return null;}}
 OWNERS
 static void check(boolean ok,String message){checks++;if(!ok)throw new AssertionError(message);}
 public static void main(String[] args){try{run();}catch(Throwable e){e.printStackTrace(System.out);System.out.flush();System.exit(1);}}
 static void run()throws Exception{
  Item item=new Item();Bitmap image=Bitmap.createBitmap(3,4,Bitmap.Config.ARGB_8888);
  for(boolean retained:new boolean[]{false,true})for(int alpha=0;alpha<256;alpha++){
   item.color.resize=retained;image.eraseColor((alpha<<24)|0x334455);int before=f.calls.get();
   boolean a=Before.run(item,image),b=After.run(item,image);
   check(a==b&&b==(alpha<128),"live source, not retained Item color");
   check(f.calls.get()==before+2,"both owners invoke the real current classifier every time");
   check(!image.isRecycled()&&image.getWidth()==3,"borrowed bitmap lifetime");
  }
  check(Before.lookups.get()==512&&After.lookups.get()==(reuse?1:512),"method lookup 512 to one");
  for(boolean retained:new boolean[]{false,true}){
   item.color.resize=retained;f.fail=true;
   check(Before.run(item,image)==retained&&After.run(item,image)==retained,"invocation exception fallback");f.fail=false;
   f.empty=true;check(Before.run(item,image)==retained&&After.run(item,image)==retained,"null result fallback");f.empty=false;
   check(Before.run(item,null)==retained&&After.run(item,null)==retained,"null source fallback");
   check(Missing.run(item,image)==retained&&Missing.run(item,image)==retained,"missing class retry fallback");
   check(WrongSignature.run(item,image)==retained&&WrongSignature.run(item,image)==retained,"wrong signature retry fallback");
  }
  check(WrongSignature.lookups.get()==4,"failed method resolution is retried, never cached");
  check(!Before.run(null,null)&&!After.run(null,null),"missing Item fallback");
  image.recycle();check(!After.run(null,image),"recycled source fallback");
  final Bitmap shared=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888);shared.eraseColor(0x11334455);final int sharedPixel=shared.getPixel(0,0);
  final java.util.concurrent.atomic.AtomicReference<Throwable> error=new java.util.concurrent.atomic.AtomicReference<Throwable>();
  Thread[] threads=new Thread[8];int count=f.calls.get(),lookups=After.lookups.get();
  for(int i=0;i<threads.length;i++){threads[i]=new Thread(new Runnable(){public void run(){try{for(int n=0;n<128;n++)if(!After.run(null,shared))throw new AssertionError("concurrent current pixels");}catch(Throwable t){error.set(t);}}});threads[i].start();}
  for(Thread t:threads)t.join();check(error.get()==null,"concurrent classification");
  check(f.calls.get()==count+1024&&After.lookups.get()==lookups+(reuse?0:1024),"metadata reuse does not cache concurrent results");
  check(!shared.isRecycled()&&shared.getPixel(0,0)==sharedPixel,"concurrent borrowed pixels unchanged");shared.recycle();
  System.out.println("PASS CLASSIFIER_METADATA checks="+checks+" ordinaryLookups=512->"+(reuse?1:512)+" classifyCalls=unchanged failures=retry fallback=preserved scope=production reflection, controlled classifier");
 }
}'''

if __name__ == '__main__':
    main()
