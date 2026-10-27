"""Native Bitmap/file protocol and extracted repository ownership admission tests.

Scheduling and cache directory are fixtures; codec and queue methods are production.
No installed Launcher data or settings are accessed.
"""
import argparse
from pathlib import Path
import subprocess
import uuid
from run_device_tests import block


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--serial', required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--codec', type=Path, required=True)
    ap.add_argument('--repository', type=Path, required=True)
    args = ap.parse_args()
    out = args.output
    (out/'classes').mkdir(parents=True, exist_ok=True)
    (out/'dex').mkdir(exist_ok=True)
    source = args.repository.read_text(encoding='utf8')
    methods = '\n'.join(block(source, marker) for marker in [
        'public Bitmap readFinalTexture(', 'public void persistFinalTexture(',
        'private void drainFinalTextures()', 'public void releaseFinalTextures()'])
    fields = '\n'.join(line for line in source.splitlines()
                       if any(token in line for token in ['private final Map<String, Bitmap> finalWrites',
                                                         'private long finalWriteBytes;',
                                                         'private boolean finalWriterRunning;',
                                                         'private boolean finalTexturesReleased;']))
    java = PROBE.replace('OWNER_FIELDS', fields).replace('OWNER_METHODS', methods)
    probe = out/'FinalFileProbe.java'
    probe.write_text(java, encoding='utf8')
    jdk = Path('E:/Program Files/Android/Android Studio/jbr/bin')
    sdk = Path('D:/sdk')

    def run(command, name, check=True):
        r = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                           encoding='utf8', errors='replace', timeout=180)
        (out/name).write_text(r.stdout+r.stderr, encoding='utf8')
        if check and r.returncode:
            raise RuntimeError(r.stdout+r.stderr)
        return r

    run([jdk/'javac.exe', '-encoding', 'UTF-8', '-source', '8', '-target', '8',
         '-cp', sdk/'platforms/android-36/android.jar', '-d', out/'classes',
         args.codec, probe], 'javac.log')
    classes = sorted((out/'classes').rglob('*.class'))
    run([jdk/'java.exe', '-cp', sdk/'build-tools/37.0.0/lib/d8.jar', 'com.android.tools.r8.D8',
         '--min-api', '28', '--lib', sdk/'platforms/android-36/android.jar',
         '--output', out/'dex', *classes], 'd8.log')
    adb = [sdk/'platform-tools/adb.exe', '-s', args.serial]
    remote = '/data/local/tmp/smartisan-final-cache-'+uuid.uuid4().hex
    run([*adb, 'shell', 'mkdir', remote], 'mkdir.log')
    run([*adb, 'push', out/'dex/classes.dex', remote+'/probe.dex'], 'push.log')
    try:
        result = run([*adb, 'shell', 'env', 'CLASSPATH='+remote+'/probe.dex', 'app_process',
                      '/system/bin', 'FinalFileProbe', remote, 'write'], 'result.log')
        assert 'PASS FINAL_FILE' in result.stdout, result.stdout
        print(result.stdout)
        result = run([*adb, 'shell', 'env', 'CLASSPATH='+remote+'/probe.dex', 'app_process',
                      '/system/bin', 'FinalFileProbe', remote, 'read'], 'fresh-process.log')
        assert 'PASS FRESH_PROCESS' in result.stdout, result.stdout
        print(result.stdout)
    finally:
        assert remote.startswith('/data/local/tmp/smartisan-final-cache-') and len(remote.rsplit('/', 1)[1]) > 32
        run([*adb, 'shell', 'rm', '-r', remote], 'cleanup.log', check=False)


PROBE = r'''
import android.graphics.*;
import com.smartisanos.home.settings.icons.FinalIconTextureFile;
import java.io.*;import java.util.*;
public class FinalFileProbe {
 static int checks;
 static void check(boolean value,String name){checks++;if(!value)throw new AssertionError(name);}
 static class App {File root;App(File root){this.root=root;}File getCacheDir(){return root;}}
 static class Owner {
  final App app;boolean reject;Runnable scheduled;static final int DISK_LIMIT_BYTES=64*1024*1024;
  Owner(File root){app=new App(root);}
  boolean schedulePersistence(Runnable operation){if(reject)return false;scheduled=operation;return true;}
  void drain(){Runnable next=scheduled;scheduled=null;next.run();}
  OWNER_FIELDS
  OWNER_METHODS
 }
 static Bitmap bitmap(int width,int height,int color){Bitmap b=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888);b.eraseColor(color);return b;}
 static byte[] bytes(File f)throws Exception {try(FileInputStream in=new FileInputStream(f);ByteArrayOutputStream out=new ByteArrayOutputStream()){byte[] b=new byte[4096];int n;while((n=in.read(b))!=-1)out.write(b,0,n);return out.toByteArray();}}
 static void bytes(File f,byte[] data)throws Exception {try(FileOutputStream out=new FileOutputStream(f)){out.write(data);}}
 public static void main(String[] args){try{run(args);}catch(Throwable error){error.printStackTrace(System.out);System.exit(1);}}
 static void run(String[] args)throws Exception {
  File root=new File(args[0]),dir=new File(root,"codec");dir.mkdirs();
  Bitmap b=bitmap(64,64,0xff123456);
  if(args[1].equals("read")){
   Bitmap read=FinalIconTextureFile.read(dir,"stable",64);check(read!=null&&read.sameAs(b),"fresh process native pixel read");read.recycle();
   check(FinalIconTextureFile.read(dir,"stable:changed-source",64)==null,"fresh process source miss");
   check(FinalIconTextureFile.read(dir,"stable",65)==null,"fresh process dimensions miss");
   System.out.println("PASS FRESH_PROCESS checks="+checks);return;
  }
  check(FinalIconTextureFile.read(dir,"absent",64)==null,"missing is a miss");
  check(FinalIconTextureFile.write(dir,"stable",b),"first atomic publication");
  Bitmap read=FinalIconTextureFile.read(dir,"stable",64);check(read!=null&&read.sameAs(b),"native opaque pixels");read.recycle();
  Bitmap alpha=bitmap(64,64,0x80123456);new Canvas(alpha).drawCircle(20.2f,22.5f,18.8f,new Paint(Paint.ANTI_ALIAS_FLAG));
  check(FinalIconTextureFile.write(dir,"alpha",alpha),"alpha write");read=FinalIconTextureFile.read(dir,"alpha",64);
  check(read!=null&&read.sameAs(alpha),"premultiplied alpha native roundtrip");read.recycle();alpha.recycle();
  File stable=FinalIconTextureFile.file(dir,"stable");byte[] original=bytes(stable);
  for(int offset:new int[]{0,4,8,12,16,48,80,original.length-1}){
   byte[] corrupt=original.clone();corrupt[offset]^=1;bytes(stable,corrupt);
   check(FinalIconTextureFile.read(dir,"stable",64)==null,"corrupt field/payload offset="+offset);
  }
  for(int length:new int[]{0,10,79,80,original.length-1,original.length+1}){
   bytes(stable,Arrays.copyOf(original,length));check(FinalIconTextureFile.read(dir,"stable",64)==null,"truncated/extra length="+length);
  }
  bytes(stable,original);
  for(String dimension:new String[]{"theme","circle","source","version","grid","shadow","profile"})
   check(FinalIconTextureFile.read(dir,"stable:"+dimension,64)==null,"different complete identity "+dimension);
  File wrong=FinalIconTextureFile.file(dir,"wrong");bytes(wrong,original);
  check(FinalIconTextureFile.read(dir,"wrong",64)==null,"wrong entry renamed under requested digest");
  File orphan=new File(dir,"final-crash.tmp");bytes(orphan,new byte[]{1,2,3});
  read=FinalIconTextureFile.read(dir,"stable",64);check(read!=null&&read.sameAs(b),"interrupted temp leaves previous final");read.recycle();
  Bitmap changed=bitmap(64,64,0xff654321);check(FinalIconTextureFile.write(dir,"stable",changed),"atomic replacement");
  read=FinalIconTextureFile.read(dir,"stable",64);check(read!=null&&read.sameAs(changed),"replacement complete");read.recycle();
  check(FinalIconTextureFile.write(dir,"stable",b),"restore stable for next process");changed.recycle();
  String digest=FinalIconTextureFile.pixels(b);b.setPixel(0,0,0xff123457);b.setPixel(1,0,0xff123437);
  check(!digest.equals(FinalIconTextureFile.pixels(b)),"actual pixels defeat old +1/-31 polynomial collision");b.eraseColor(0xff123456);
  File invalidTarget=FinalIconTextureFile.file(dir,"rename-failure");invalidTarget.mkdirs();
  boolean failed=false;try{FinalIconTextureFile.write(dir,"rename-failure",b);}catch(Exception expected){failed=true;}
  check(failed&&invalidTarget.isDirectory(),"failed publication preserves existing target");
  int temporaries=0;for(File f:dir.listFiles())if(f.getName().endsWith(".tmp"))temporaries++;
  check(temporaries==1,"failed publication removes only its temporary");
  File trim=new File(root,"trim");trim.mkdirs();
  for(int i=0;i<8;i++)check(FinalIconTextureFile.write(trim,"entry"+i,b),"trim setup");
  File unrelated=new File(trim,"keep.txt");bytes(unrelated,new byte[]{1});FinalIconTextureFile.trim(trim,1);
  check(unrelated.exists()&&trim.listFiles().length==1,"bounded trim preserves unrelated files");
  Owner owner=new Owner(new File(root,"owner"));owner.persistFinalTexture("wait",b);
  check(owner.scheduled==null&&owner.finalWriteBytes>0,"writes wait for real page readiness");
  owner.reject=true;owner.releaseFinalTextures();check(owner.finalWriteBytes==0&&owner.finalWrites.isEmpty(),"rejected page release drops copies");
  owner.persistFinalTexture("reject",b);
  check(owner.finalWrites.isEmpty()&&owner.finalWriteBytes==0&&!owner.finalWriterRunning,"rejected admission releases copy");
  check(!b.isRecycled(),"rejected admission never recycles caller");owner.reject=false;
  owner.persistFinalTexture("kept",b);Bitmap copy=owner.finalWrites.get("kept");
  check(copy!=b&&!copy.isRecycled()&&owner.finalWriteBytes==b.getByteCount(),"repository owns bounded copy only");
  owner.persistFinalTexture("kept",b);check(owner.finalWrites.size()==1,"duplicate admission bounded");
  b.recycle();owner.drain();check(copy.isRecycled()&&owner.finalWrites.isEmpty()&&owner.finalWriteBytes==0&&!owner.finalWriterRunning,"drain releases all ownership");
  read=owner.readFinalTexture("kept",64);check(read!=null&&read.getPixel(0,0)==0xff123456,"caller recycled before worker remains safe");read.recycle();
  Bitmap large=bitmap(1024,1024,0xff123456);owner.persistFinalTexture("one",large);owner.persistFinalTexture("two",large);owner.persistFinalTexture("three",large);
  check(owner.finalWrites.size()==2&&owner.finalWriteBytes==8*1024*1024,"8MiB admission includes pending copies");owner.drain();
  check(!large.isRecycled()&&owner.finalWriteBytes==0,"large inputs remain caller owned");large.recycle();
  Bitmap small=bitmap(1,1,0xffabcdef);for(int i=0;i<65;i++)owner.persistFinalTexture("small"+i,small);
  check(owner.finalWrites.size()==64,"entry cap");owner.drain();small.recycle();
  check(owner.finalWrites.isEmpty()&&owner.finalWriteBytes==0,"small queue drained");
  File ownerDir=new File(owner.app.getCacheDir(),"final_icon_v1");File oldTemp=new File(ownerDir,"final-old.tmp");bytes(oldTemp,new byte[]{1});
  Bitmap last=bitmap(64,64,0xff123456);owner.persistFinalTexture("last",last);owner.drain();last.recycle();check(!oldTemp.exists(),"serial writer clears crash leftover");
  System.out.println("PASS FINAL_FILE checks="+checks);
 }
}
'''

if __name__ == '__main__':
    main()
