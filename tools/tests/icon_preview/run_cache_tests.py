"""Exercise production mirror validation and atomic cache writes with controlled HTTP replies.

Uses actual files/preferences across fresh processes. Optional Android mode adds real PNG
decode checks in an isolated app_process; no launcher data or installed APK is touched.
"""
import argparse
import base64
import json
from pathlib import Path
import struct
import subprocess
import sys
import uuid
import zlib

sys.dont_write_bytecode = True
from run_tests import block

ROOT = Path(__file__).resolve().parents[3]


def png(color, depth=8, interlace=0):
    def chunk(name, data):
        return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data))
    header = chunk(b"IHDR", struct.pack(">IIBBBBB", 64, 64, depth, 6, 0, 0, interlace))
    passes = [(0, 0, 1, 1)] if not interlace else [(0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 0, 4, 4), (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2)]
    raw = b"".join((b"\0" + bytes(color) * len(range(x, 64, dx))) * len(range(y, 64, dy)) for x, y, dx, dy in passes)
    pixels = zlib.compress(raw)
    return b"\x89PNG\r\n\x1a\n" + header + chunk(b"IDAT", pixels) + chunk(b"IEND", b"")


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument("--jdk", type=Path, default=Path("E:/Program Files/Android/Android Studio/jbr"))
    ap.add_argument("--sdk", type=Path, default=Path("D:/sdk"))
    ap.add_argument("--serial")
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args(); out = a.output; out.mkdir(parents=True, exist_ok=True)
    source = (ROOT / "launcher/tools/java/com/smartisanos/home/settings/icons/IconPreviewRepository.java").read_text(encoding="utf-8")
    methods = "\n".join(block(source, m) for m in ["    private boolean fetchOnlineSource(", "    private static boolean hasValidPngChunks(", "    private boolean saveToDiskCache("])
    if "private static boolean hasValidPngData(" in source:
        methods += "\n" + block(source, "    private static boolean hasValidPngData(")
    fixture = r'''
import java.io.*;import java.net.*;import java.nio.file.*;import java.util.*;import java.util.concurrent.atomic.*;import java.util.zip.*;import java.lang.reflect.*;
public class CacheBoundaryProbe {
 static final byte[] RED=Base64.getDecoder().decode("@RED@"),GREEN=Base64.getDecoder().decode("@GREEN@");
 static final byte[] RGBA16=Base64.getDecoder().decode("@RGBA16@"),ADAM7=Base64.getDecoder().decode("@ADAM7@"),BOMB=Base64.getDecoder().decode("@BOMB@");
 static int checks,failures,connections,trims;static OnlineFetch current;static final Deque<Reply> replies=new ArrayDeque<>();
 static class Context {static final int MODE_PRIVATE=0;}
 static class TextUtils {static boolean isEmpty(String s){return s==null||s.isEmpty();}}
 static class OnlineFetch {volatile boolean cancelled;}
 static class App {
  final File root;android.content.SharedPreferences nativePreferences;App(File r){root=r;root.mkdirs();}File getFilesDir(){return root;}
  android.content.SharedPreferences getSharedPreferences(String name,int mode){
   if(nativePreferences!=null)return nativePreferences;
   try {
    Class<?> implementation=Class.forName("android.app.SharedPreferencesImpl");Constructor<?> constructor=implementation.getDeclaredConstructor(File.class,int.class);constructor.setAccessible(true);
    nativePreferences=(android.content.SharedPreferences)constructor.newInstance(new File(root,"prefs.xml"),0);System.out.println("preference backend=platform SharedPreferencesImpl");return nativePreferences;
   }catch(ClassNotFoundException hostJvm){}catch(Exception error){throw new RuntimeException(error);}
   File file=new File(root,"prefs.properties");Properties values=new Properties();
   if(file.exists())try(InputStream in=new FileInputStream(file)){values.load(in);}catch(Exception e){throw new RuntimeException(e);}
   Object editor=Proxy.newProxyInstance(CacheBoundaryProbe.class.getClassLoader(),new Class[]{android.content.SharedPreferences.Editor.class},(o,m,args)->{
    if(m.getName().equals("putLong")){values.setProperty((String)args[0],String.valueOf(args[1]));return o;}
    if(m.getName().equals("remove")){values.remove(args[0]);return o;}
    if(m.getName().equals("apply")||m.getName().equals("commit")){try(OutputStream stream=new FileOutputStream(file)){values.store(stream,"");}return m.getReturnType()==boolean.class?true:null;}
    return null;
   });
   return (android.content.SharedPreferences)Proxy.newProxyInstance(CacheBoundaryProbe.class.getClassLoader(),new Class[]{android.content.SharedPreferences.class},(o,m,args)->{
    if(m.getName().equals("getLong"))return Long.parseLong(values.getProperty((String)args[0],String.valueOf(args[1])));
    if(m.getName().equals("edit"))return editor;return null;
   });
  }
 }
 final App app;CacheBoundaryProbe(File root){app=new App(root);}
 void trimOnlineDiskCacheAsync(){trims++;}
 static class Reply {int code;String type;byte[] data;boolean cancelRead;Reply(int c,String t,byte[] b){code=c;type=t;data=b;}}
 static class Connection extends HttpURLConnection {
  final Reply reply;Connection(URL u,Reply r){super(u);reply=r;}public void connect(){}public void disconnect(){}public boolean usingProxy(){return false;}
  public int getResponseCode(){return reply.code;}public String getContentType(){return reply.type;}
  public InputStream getInputStream(){return new ByteArrayInputStream(reply.data){public synchronized int read(byte[] b,int o,int n){int v=super.read(b,o,n);if(reply.cancelRead&&current!=null)current.cancelled=true;return v;}};}
 }
 static void prepare(){connections=0;trims=0;replies.clear();current=null;}
 static Reply reply(int code,byte[] data){Reply r=new Reply(code,"image/png",data);replies.add(r);return r;}
 static void check(boolean ok,String name){checks++;if(!ok){failures++;System.out.println("FAIL "+name);}}
 static byte[] chunk(String kind,byte[] data)throws Exception{ByteArrayOutputStream b=new ByteArrayOutputStream();DataOutputStream d=new DataOutputStream(b);byte[] type=kind.getBytes("US-ASCII");d.writeInt(data.length);d.write(type);d.write(data);CRC32 crc=new CRC32();crc.update(type);crc.update(data);d.writeInt((int)crc.getValue());return b.toByteArray();}
 static byte[] join(byte[]... all)throws Exception{ByteArrayOutputStream b=new ByteArrayOutputStream();for(byte[] v:all)b.write(v);return b.toByteArray();}
 static byte[] missingData()throws Exception{return join(Arrays.copyOf(RED,33),chunk("IEND",new byte[0]));}
 static File target(CacheBoundaryProbe r,String source){return new File(new File(r.app.root,"online_icon_cache_v4"),source+".png");}
 static boolean content(File f,byte[] data)throws Exception{return f.exists()&&Arrays.equals(Files.readAllBytes(f.toPath()),data);}
 static void tests(File root)throws Exception{
  byte[] noData=missingData(),emptyData=join(Arrays.copyOf(RED,33),chunk("IDAT",new byte[0]),chunk("IEND",new byte[0]));
  byte[] duplicate=join(Arrays.copyOf(RED,33),Arrays.copyOfRange(RED,8,33),Arrays.copyOfRange(RED,33,RED.length));
  check(hasValidPngChunks(RED)&&hasValidPngChunks(GREEN),"valid transparent RGBA PNG chunks accepted");
  check(hasValidPngChunks(join(Arrays.copyOf(RED,33),chunk("IDAT",new byte[0]),Arrays.copyOfRange(RED,33,RED.length))),"zero-length IDAT allowed when real pixel stream follows");
  check(hasValidPngChunks(join(Arrays.copyOf(RED,33),chunk("tEXt","note\0fixture".getBytes("UTF-8")),Arrays.copyOfRange(RED,33,RED.length))),"valid ancillary chunks preserved");
  check(hasValidPngChunks(RGBA16)&&hasValidPngChunks(ADAM7),"RGBA16 and Adam7 pixel streams preserved");
  int compressedLength=java.nio.ByteBuffer.wrap(RED).getInt(33);byte[] compressed=Arrays.copyOfRange(RED,41,41+compressedLength);
  check(hasValidPngChunks(join(Arrays.copyOf(RED,33),chunk("IDAT",Arrays.copyOf(compressed,1)),chunk("IDAT",Arrays.copyOfRange(compressed,1,compressed.length)),chunk("IEND",new byte[0]))),"zlib header split across IDAT chunks accepted");
  check(!hasValidPngChunks(join(Arrays.copyOf(RED,33),chunk("IDAT",Arrays.copyOf(compressed,compressed.length-2)),chunk("IEND",new byte[0]))),"truncated compressed stream rejected despite valid chunk CRC");
  check(!hasValidPngChunks(join(Arrays.copyOf(RED,33),chunk("IDAT",BOMB),chunk("IEND",new byte[0]))),"inflated data above bounded maximum rejected");
  check(!hasValidPngChunks(noData),"IHDR and IEND without pixel stream rejected");
  check(!hasValidPngChunks(emptyData),"empty pixel stream rejected");
  check(!hasValidPngChunks(duplicate),"duplicate IHDR rejected");
  byte[] crc=RED.clone();crc[crc.length-1]^=1;check(!hasValidPngChunks(crc),"bad CRC rejected");
  check(!hasValidPngChunks(Arrays.copyOf(RED,RED.length-2)),"truncated PNG rejected");
  check(!hasValidPngChunks(join(RED,new byte[]{1})),"trailing bytes rejected");
  CacheBoundaryProbe r=new CacheBoundaryProbe(new File(root,"mirrors"));
  prepare();reply(200,noData);reply(200,GREEN);boolean accepted=r.fetchOnlineSource("no-data",null);
  check(accepted&&connections==2,"missing pixel stream falls through to second mirror");check(content(target(r,"no-data"),GREEN),"bad first mirror never becomes persisted icon");
  prepare();reply(200,crc);reply(200,GREEN);check(r.fetchOnlineSource("crc",null)&&connections==2,"CRC error falls through to second mirror");
  prepare();reply(200,new byte[512*1024+1]);reply(200,GREEN);accepted=r.fetchOnlineSource("oversize",null);
  check(accepted&&connections==2,"oversize first mirror falls through to second mirror");check(content(target(r,"oversize"),GREEN),"valid fallback persisted after oversize reply");
  prepare();Reply type=reply(200,RED);type.type="text/html";reply(200,GREEN);check(r.fetchOnlineSource("html",null)&&connections==2,"HTML first mirror rejected");
  prepare();reply(404,new byte[0]);reply(404,new byte[0]);check(!r.fetchOnlineSource("absent",null)&&connections==2,"both 404 recorded as miss");
  prepare();reply(200,RED);check(!r.fetchOnlineSource("absent",null)&&connections==0,"persisted miss prevents immediate retry");
  prepare();reply(500,new byte[0]);reply(404,new byte[0]);check(!r.fetchOnlineSource("temporary",null),"temporary response fails without success");
  prepare();reply(200,GREEN);check(r.fetchOnlineSource("temporary",null)&&connections==1,"temporary failure never becomes one-hour miss");
  prepare();OnlineFetch before=new OnlineFetch();before.cancelled=true;check(!r.fetchOnlineSource("cancel-before",before)&&connections==0,"cancel before start makes no HTTP request");
  prepare();current=new OnlineFetch();Reply paused=reply(200,RED);paused.cancelRead=true;reply(200,GREEN);check(!r.fetchOnlineSource("cancel-read",current)&&connections==1,"cancellation after paused read never tries fallback");check(!target(r,"cancel-read").exists(),"cancelled payload not published");
  prepare();reply(200,GREEN);check(r.fetchOnlineSource("cancel-read",null)&&connections==1,"fresh request after cancellation can recover");
  check(r.saveToDiskCache("same-name",RED)&&content(target(r,"same-name"),RED),"first same-name file committed");
  check(r.saveToDiskCache("same-name",GREEN)&&content(target(r,"same-name"),GREEN),"explicit successful replacement atomically overwrites same name");
  prepare();reply(200,crc);reply(200,noData);r.fetchOnlineSource("same-name",null);check(content(target(r,"same-name"),GREEN),"invalid update preserves prior good file");
  byte[] badDeflate=join(Arrays.copyOf(RED,33),chunk("IDAT",new byte[]{1,2,3,4}),chunk("IEND",new byte[0]));
  prepare();reply(200,badDeflate);reply(200,GREEN);check(r.fetchOnlineSource("bad-deflate",null)&&connections==2,"CRC-valid undecodable pixel stream tries fallback");check(content(target(r,"bad-deflate"),GREEN),"undecodable stream never replaces valid fallback");
  File[] files=target(r,"same-name").getParentFile().listFiles((dir,name)->name.endsWith(".tmp"));check(files!=null&&files.length==0,"no temporary files left after accepted or rejected writes");
 }
 static void nativeDecodeTests()throws Exception{
  Class<?> decoder=Class.forName("android.graphics.BitmapFactory");Method decode=decoder.getMethod("decodeByteArray",byte[].class,int.class,int.class);
  Object good=decode.invoke(null,RED,0,RED.length);check(good!=null,"real Android decodes accepted RGBA fixture");if(good!=null)good.getClass().getMethod("recycle").invoke(good);
  for(byte[] legal:new byte[][]{RGBA16,ADAM7}){Object image=decode.invoke(null,legal,0,legal.length);check(image!=null,"real Android confirms legal advanced PNG fixture");if(image!=null)image.getClass().getMethod("recycle").invoke(image);}
  byte[] bad=missingData();Object invalid=decode.invoke(null,bad,0,bad.length);check(invalid==null,"real Android rejects CRC-valid PNG with no pixel stream");if(invalid!=null)invalid.getClass().getMethod("recycle").invoke(invalid);
  byte[] corrupt=join(Arrays.copyOf(RED,33),chunk("IDAT",new byte[]{1,2,3,4}),chunk("IEND",new byte[0]));Object stream=decode.invoke(null,corrupt,0,corrupt.length);System.out.println("native decoder recovered bad deflate="+(stream!=null));check(!hasValidPngChunks(corrupt),"bad deflate rejected independently of permissive native decoding");if(stream!=null)stream.getClass().getMethod("recycle").invoke(stream);
 }
 static void nativeDiskCheck(File file)throws Exception{
  Class<?> decoder;try{decoder=Class.forName("android.graphics.BitmapFactory");}catch(ClassNotFoundException plainJvm){return;}
  Object bitmap=decoder.getMethod("decodeFile",String.class).invoke(null,file.getAbsolutePath());check(bitmap!=null,"fresh Android process decodes persisted replacement");
  if(bitmap!=null)try{check(((Integer)bitmap.getClass().getMethod("getPixel",int.class,int.class).invoke(bitmap,0,0))==0x8000ff00,"fresh Android process sees replacement color and alpha");}finally{bitmap.getClass().getMethod("recycle").invoke(bitmap);}
 }
 public static void main(String[] args)throws Exception{
  URL.setURLStreamHandlerFactory(protocol->"https".equals(protocol)?new URLStreamHandler(){protected URLConnection openConnection(URL url)throws IOException{connections++;Reply r=replies.poll();if(r==null)throw new IOException("unexpected test HTTP request");return new Connection(url,r);}}:null);
  File root=new File(args[1]);root.mkdirs();
  if(args[0].equals("seed")){
   CacheBoundaryProbe r=new CacheBoundaryProbe(root);check(r.saveToDiskCache("same-name",GREEN),"cross-process source seed");prepare();reply(404,new byte[0]);reply(404,new byte[0]);check(!r.fetchOnlineSource("cross-absent",null),"cross-process miss seed");
  }else if(args[0].equals("verify")){
   CacheBoundaryProbe r=new CacheBoundaryProbe(root);check(content(target(r,"same-name"),GREEN),"fresh process sees exact replacement bytes");nativeDiskCheck(target(r,"same-name"));prepare();reply(200,RED);check(!r.fetchOnlineSource("cross-absent",null)&&connections==0,"fresh process sees persisted miss memo");
  }else {tests(root);if(args[0].equals("android"))nativeDecodeTests();}
  try{Class<?> queued=Class.forName("android.app.QueuedWork");Method wait=queued.getDeclaredMethod("waitToFinish");wait.setAccessible(true);wait.invoke(null);}catch(ClassNotFoundException hostJvm){}
  System.out.println("cache boundary mode="+args[0]+" checks="+checks+" failures="+failures);System.out.flush();System.exit(failures==0?0:1);
 }
 @METHODS@
}
'''
    fixture = fixture.replace("@RED@", base64.b64encode(png((255, 0, 0, 128))).decode()).replace("@GREEN@", base64.b64encode(png((0, 255, 0, 128))).decode()).replace("@METHODS@", methods).replace("Proxy.newProxyInstance", "java.lang.reflect.Proxy.newProxyInstance")
    fixture = fixture.replace("@RGBA16@", base64.b64encode(png((255,255,0,0,0,0,128,0),16)).decode()).replace("@ADAM7@", base64.b64encode(png((255,0,0,128),interlace=1)).decode()).replace("@BOMB@",base64.b64encode(zlib.compress(bytes(9*1024*1024+1))).decode())
    src = out / "src"; src.mkdir(exist_ok=True); classes = out / "classes"; classes.mkdir(exist_ok=True)
    java = src / "CacheBoundaryProbe.java"; java.write_text(fixture, encoding="utf-8")
    sources = [str(java)]
    if not a.serial:
        stubs = {"android/os/SystemClock.java": "package android.os;public class SystemClock {public static long uptimeMillis(){return System.nanoTime()/1000000;}}", "android/content/SharedPreferences.java": "package android.content;public interface SharedPreferences {long getLong(String k,long d);Editor edit();interface Editor {Editor putLong(String k,long v);Editor remove(String k);void apply();}}"}
        for name, body in stubs.items():
            f = src / name; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(body); sources.append(str(f))
    command = [str(a.jdk / "bin/javac.exe"), "-source", "8", "-target", "8", "-encoding", "UTF-8", "-d", str(classes)]
    android_jar = a.sdk / "platforms/android-36/android.jar"
    if a.serial: command += ["-classpath", str(android_jar)]
    subprocess.run(command + sources, check=True)
    results = []; remote = None
    if a.serial:
        jar = out / "probe.jar"; dex = out / "dex"; dex.mkdir(exist_ok=True)
        subprocess.run([str(a.jdk / "bin/jar.exe"), "cf", str(jar), "-C", str(classes), "."], check=True)
        subprocess.run([str(a.jdk / "bin/java.exe"), "-cp", str(a.sdk / "build-tools/37.0.0/lib/d8.jar"), "com.android.tools.r8.D8", "--lib", str(android_jar), "--min-api", "26", "--output", str(dex), str(jar)], check=True)
        adb = [str(a.sdk / "platform-tools/adb.exe"), "-s", a.serial]; remote = "/data/local/tmp/icon-cache-probe-" + uuid.uuid4().hex
        subprocess.run(adb + ["shell", "mkdir", remote], check=True, capture_output=True)
        subprocess.run(adb + ["push", str(dex / "classes.dex"), remote + "/probe.dex"], check=True, capture_output=True)
    try:
        run_token = uuid.uuid4().hex
        for mode in ["android" if a.serial else "test", "seed", "verify"]:
            folder = ("cross-" if mode in ["seed", "verify"] else "cases-") + run_token
            command = adb + ["shell", "env", "CLASSPATH=" + remote + "/probe.dex", "app_process", "/system/bin", "CacheBoundaryProbe", mode, remote + "/" + folder] if a.serial else [str(a.jdk / "bin/java.exe"), "-cp", str(classes), "CacheBoundaryProbe", mode, str(out / folder)]
            try:
                result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=40)
            except subprocess.TimeoutExpired as error:
                captured = (error.stdout or b"") + (error.stderr or b"")
                if isinstance(captured, bytes): captured = captured.decode("utf-8", errors="replace")
                (out / (mode + "-timeout.log")).write_text(captured, encoding="utf-8")
                raise
            (out / (mode + ".log")).write_text(result.stdout + result.stderr, encoding="utf-8"); print(result.stdout, end="")
            results.append({"mode": mode, "exitCode": result.returncode, "output": result.stdout.strip()})
        (out / "summary.json").write_text(json.dumps({"serial": a.serial, "results": results, "scope": "production mirror/chunk validation/atomic write methods; controlled HTTP and actual files; host preferences proxy, Android platform SharedPreferencesImpl in owned directory with QueuedWork flush; seed/verify separate processes; Android native decode oracle; no real mirror requests or launcher data"}, indent=2), encoding="utf-8")
        if any(v["exitCode"] for v in results): raise SystemExit(1)
    finally:
        if remote:
            assert remote.startswith("/data/local/tmp/icon-cache-probe-") and len(remote.rsplit("-", 1)[1]) == 32
            subprocess.run(adb + ["shell", "rm", "-r", remote], check=True, capture_output=True)


if __name__ == "__main__":
    main()
