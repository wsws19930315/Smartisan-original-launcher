"""Check extracted Folder-only refresh-normalized original frame progression."""
from pathlib import Path
import subprocess,argparse
ROOT=Path(__file__).resolve().parents[3]
def method(source,marker):
 start=source.index(marker);end=source.index('{',start)+1;depth=1
 while depth:
  depth+=(source[end]=='{')-(source[end]=='}');end+=1
 return source[start:end]
def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
 source=(ROOT/'launcher/tools/java/com/smartisanos/launcher/theme/LauncherSettingBridge.java').read_text()
 actual=method(source,'public static float folderAnimationFrameDelta(')
 files={
 'android/view/Display.java':'package android.view; public class Display { public float hz; public boolean fail; public Display(float h){hz=h;} public float getRefreshRate(){if(fail)throw new IllegalStateException();return hz;} }',
 'android/view/WindowManager.java':'package android.view; public interface WindowManager { Display getDefaultDisplay(); }',
 'Probe.java':'''public class Probe {
 static class Context { static final String WINDOW_SERVICE="window"; Object service; int calls; Object getSystemService(String name){calls++;return service;} }
 static class MaintainedLauncherSettingsHost { static Context context; static Context currentApplicationContext(){return context;} }
 @METHOD@
 static int checks; static void check(float actual,float expected){checks++;if(Float.floatToIntBits(actual)!=Float.floatToIntBits(expected))throw new AssertionError(actual+" != "+expected);}
 public static void main(String[] args) {
  check(folderAnimationFrameDelta(7.2f,20f),7.2f);
  Context c=new Context();MaintainedLauncherSettingsHost.context=c;check(folderAnimationFrameDelta(7.2f,20f),7.2f);
  c.service=new Object();check(folderAnimationFrameDelta(7.2f,20f),7.2f);
  android.view.Display d=new android.view.Display(60f);c.service=(android.view.WindowManager)()->d;
  for(float hz:new float[]{60f,59.94f,60.06f,30f,50f,90f,120f,144f,240f}){d.hz=hz;for(float delta:new float[]{6f,7.2f,20f,27.6f,120f})check(folderAnimationFrameDelta(delta,20f),Math.min(1200f/hz,120f));}
  for(float hz:new float[]{0f,Float.NaN,Float.POSITIVE_INFINITY,-1f}){d.hz=hz;for(float delta:new float[]{7.2f,27.6f})check(folderAnimationFrameDelta(delta,20f),delta);}
  d.hz=1f;check(folderAnimationFrameDelta(7.2f,20f),120f);
  d.hz=60f;int calls=c.calls;check(folderAnimationFrameDelta(0f,20f),0f);check(folderAnimationFrameDelta(-1f,20f),-1f);check(folderAnimationFrameDelta(Float.NaN,20f),Float.NaN);check(folderAnimationFrameDelta(7.2f,0f),7.2f);if(c.calls!=calls)throw new AssertionError("zero/resume probed display");
  d.fail=true;check(folderAnimationFrameDelta(7.2f,20f),7.2f);
  c.service=(android.view.WindowManager)()->null;check(folderAnimationFrameDelta(7.2f,20f),7.2f);
  c.service=(android.view.WindowManager)()->{throw new IllegalStateException();};check(folderAnimationFrameDelta(7.2f,20f),7.2f);
  System.out.println("PASS FOLDER_TIMING checks="+checks+" refresh-normalized original progression; resume/cap/unavailable display");
 }
}'''.replace('@METHOD@',actual)}
 for name,text in files.items():
  f=out/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text,encoding='utf8')
 jdk=Path('E:/Program Files/Android/Android Studio/jbr/bin')
 for args in [[jdk/'javac.exe','-encoding','UTF-8','-d',out,*[out/n for n in files]],[jdk/'java.exe','-cp',out,'Probe']]:
  r=subprocess.run(list(map(str,args)),capture_output=True,text=True);print(r.stdout+r.stderr);assert r.returncode==0
 # Preserve the existing global clock and restrict the new call to active Folder transitions.
 smali=(ROOT/'launcher/smali/com/smartisanos/launcher/view/Eb.smali').read_text();update=smali.split('.method public update()V\n',1)[1].split('.end method',1)[0]
 gate=update.split(':cond_held_pointer_delta_done\n',1)[1]
 assert '->Ix:' in gate and '->Zr()Z' in gate and '->Yr()Z' in gate
 assert gate.index('->Zr()Z')<gate.index('->folderAnimationFrameDelta(FF)F')<gate.index('->T(F)V')
 assert '0x3d75c28f' in update and '0x42c80000' in update
 print('PASS Folder transition gate; existing elapsed clock and held-pointer guard retained')
if __name__=='__main__':main()
