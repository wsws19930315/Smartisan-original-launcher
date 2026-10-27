"""Compare the actual badge crop methods on native Android Bitmaps, including IO counts."""
import argparse
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'launcher/tools/java/com/smartisanos/launcher/quickdesktop/QuickDesktopContentView.java'


def method(path):
    source = path.read_text('utf8')
    start = source.index('    private Bitmap cropTransparentBounds(')
    end = source.index('{', start) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def main():
    parser = argparse.ArgumentParser(__doc__)
    for key in ('serial', 'jdk', 'sdk', 'output', 'baseline'):
        parser.add_argument('--' + key, required=True)
    parser.add_argument('--candidate', type=Path, default=SOURCE)
    args = parser.parse_args()
    out, jdk, sdk = Path(args.output), Path(args.jdk), Path(args.sdk)
    out.mkdir(parents=True, exist_ok=True)
    owners = []
    for name, path in [('Before', Path(args.baseline)), ('After', args.candidate)]:
        body = method(path)
        owners.append('static class ' + name + '{' + body + '}')
        counted = body.replace('source.getPixel(', 'pixel(source,').replace('source.getPixels(', 'pixels(source,')
        owners.append('static class Counted' + name + '{' + counted + '}')
    java = out / 'BadgeCropProbe.java'
    java.write_text(PROBE.replace('OWNERS', '\n'.join(owners)), 'utf8')
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
         '-bootclasspath', sdk / 'platforms/android-36/android.jar', '-d', classes, java], 'compile.log')
    os.environ['JAVA_HOME'] = str(jdk)
    run([sdk / 'build-tools/37.0.0/d8.bat', '--min-api', '23', '--output', dex,
         *sorted(classes.glob('*.class'))], 'dex.log')
    adb = [sdk / 'platform-tools/adb.exe', '-s', args.serial]
    remote = '/data/local/tmp/qd-badge-crop-20261026'
    run([*adb, 'push', dex / 'classes.dex', remote + '.dex'], 'push.log')
    run([*adb, 'push', ROOT / 'launcher/assets/quickdesktop_original/wechat_badge.png', remote + '.png'], 'image-push.log')
    try:
        result = run([*adb, 'shell', 'CLASSPATH=' + remote + '.dex', 'app_process',
                      '/system/bin', 'BadgeCropProbe', remote + '.png'], 'result.log')
        assert 'PASS BADGE_CROP' in result, result
        print(result)
    finally:
        run([*adb, 'shell', 'rm', '-f', remote + '.dex', remote + '.png'], 'cleanup.log')


PROBE = r'''
import android.graphics.*;
import java.util.*;
public class BadgeCropProbe {
 static int checks,pixelCalls,bulkCalls;
 static int pixel(Bitmap b,int x,int y){pixelCalls++;return b.getPixel(x,y);}
 static void pixels(Bitmap b,int[] p,int o,int s,int x,int y,int w,int h){bulkCalls++;b.getPixels(p,o,s,x,y,w,h);}
 OWNERS
 static void check(boolean ok,String message){checks++;if(!ok)throw new AssertionError(message);}
 static int[] data(Bitmap b){int[] p=new int[b.getWidth()*b.getHeight()];b.getPixels(p,0,b.getWidth(),0,0,b.getWidth(),b.getHeight());return p;}
 static void release(Bitmap result,Bitmap source){if(result!=null&&result!=source&&!result.isRecycled())result.recycle();}
 static void compare(Bitmap source)throws Exception{
  int[] previous=data(source);Bitmap before=new Before().cropTransparentBounds(source),after=new After().cropTransparentBounds(source);
  check(before.getWidth()==after.getWidth()&&before.getHeight()==after.getHeight(),"exact crop dimensions");
  check(Arrays.equals(data(before),data(after)),"exact native cropped pixels");
  check((before==source)==(after==source),"same ownership and identity fallback");
  check(!source.isRecycled()&&Arrays.equals(previous,data(source)),"borrowed source stays unchanged and live");
  release(before,source);release(after,source);
 }
 static double time(Object owner,Bitmap source)throws Exception{
  long start=System.nanoTime();Bitmap out=owner instanceof Before?((Before)owner).cropTransparentBounds(source):((After)owner).cropTransparentBounds(source);
  double ms=(System.nanoTime()-start)/1e6;release(out,source);return ms;
 }
 public static void main(String[] args){try{run(args);}catch(Throwable error){error.printStackTrace(System.out);System.out.flush();System.exit(1);}}
 static void run(String[] args)throws Exception{
  Bitmap actual=BitmapFactory.decodeFile(args[0]);check(actual!=null,"original PNG decoded");compare(actual);
  pixelCalls=bulkCalls=0;Bitmap old=new CountedBefore().cropTransparentBounds(actual);int beforePixels=pixelCalls,beforeBulk=bulkCalls;release(old,actual);
  pixelCalls=bulkCalls=0;Bitmap now=new CountedAfter().cropTransparentBounds(actual);release(now,actual);
  check(beforePixels==actual.getWidth()*actual.getHeight()&&beforeBulk==0,"old per-pixel call count");
  check(pixelCalls==0&&bulkCalls==actual.getHeight(),"one bulk read per row, no per-pixel JNI");
  for(int width:new int[]{1,2,7,32,73})for(int height:new int[]{1,3,16,47})for(int shape=0;shape<7;shape++){
   Bitmap b=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888);int[] p=new int[width*height];
   for(int y=0;y<height;y++)for(int x=0;x<width;x++){
    int alpha=shape==0?0:shape==1?255:shape==2?(x==width/2&&y==height/2?1:0):shape==3?(x>0&&x<width-1&&y>0&&y<height-1?128:0):shape==4?((x+y)%2==0?1:0):shape==5?(x==0||y==0||x==width-1||y==height-1?255:0):(x*73+y*29)%256;
    p[y*width+x]=Color.argb(alpha,(x*37)%256,(y*61)%256,197);
   }
   b.setPixels(p,0,width,0,0,width,height);compare(b);b.recycle();
  }
  check(new Before().cropTransparentBounds(null)==null&&new After().cropTransparentBounds(null)==null,"null unchanged");
  Bitmap dead=Bitmap.createBitmap(2,2,Bitmap.Config.ARGB_8888);dead.recycle();
  check(new Before().cropTransparentBounds(dead)==dead&&new After().cropTransparentBounds(dead)==dead,"recycled unchanged");
  Before before=new Before();After after=new After();time(before,actual);time(after,actual);
  double[] a=new double[5],b=new double[5];
  for(int i=0;i<5;i++){if(i%2==0){a[i]=time(before,actual);b[i]=time(after,actual);}else{b[i]=time(after,actual);a[i]=time(before,actual);}}
  System.out.println("TIMING_NATIVE before="+Arrays.toString(a)+" after="+Arrays.toString(b));
  Arrays.sort(a);Arrays.sort(b);System.out.println("MEDIAN_NATIVE before="+a[2]+" after="+b[2]);
  System.out.println("PASS BADGE_CROP checks="+checks+" source="+actual.getWidth()+"x"+actual.getHeight()+" perPixel="+beforePixels+"->"+pixelCalls+" bulk="+beforeBulk+"->"+bulkCalls+" sourceOwnership=preserved");actual.recycle();
 }
}'''

if __name__ == '__main__':
    main()
