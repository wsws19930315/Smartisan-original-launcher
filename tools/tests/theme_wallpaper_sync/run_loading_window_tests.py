"""Run actual loading-window policy with controlled Window fixtures, not OEM SystemUI."""
from pathlib import Path
import argparse,subprocess,sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'prepared_icon_source'))
from run_device_tests import block,ROOT

def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--baseline',required=True,type=Path);ap.add_argument('--source',type=Path,default=ROOT/'launcher/tools/java/com/smartisanos/launcher/reload/OriginalLoadingContentFactory.java');ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
 stubs={
 'android/content/Context.java':'package android.content; public class Context {}',
 'android/app/Activity.java':'package android.app; public class Activity extends android.content.Context {}',
 'com/smartisanos/launcher/Launcher.java':'package com.smartisanos.launcher; public class Launcher extends android.app.Activity {}',
 'android/os/Build.java':'package android.os; public class Build {public static class VERSION {public static int SDK_INT;}}',
 'android/graphics/Color.java':'package android.graphics; public class Color {public static final int TRANSPARENT=0;}',
 'android/view/View.java':'''package android.view; public class View {public static final int SYSTEM_UI_FLAG_LAYOUT_STABLE=0x100,SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN=0x400,SYSTEM_UI_FLAG_FULLSCREEN=4,SYSTEM_UI_FLAG_LIGHT_STATUS_BAR=0x2000;public int flags;public int getSystemUiVisibility(){return flags;}public void setSystemUiVisibility(int f){flags=f;}}''',
 'android/view/WindowManager.java':'''package android.view; public class WindowManager {public static class LayoutParams {public static final int LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES=1,FLAG_FULLSCREEN=0x400,FLAG_TRANSLUCENT_STATUS=0x4000000,FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS=0x80000000;public int flags,layoutInDisplayCutoutMode;}}''',
 'android/view/Window.java':'''package android.view; public class Window {public WindowManager.LayoutParams attrs=new WindowManager.LayoutParams();public View decor=new View();public int color=0xff123456,nav=0xff654321,animations=123;public WindowManager.LayoutParams getAttributes(){return attrs;}public void setAttributes(WindowManager.LayoutParams a){attrs=a;}public View getDecorView(){return decor;}public void clearFlags(int f){attrs.flags&=~f;}public void addFlags(int f){attrs.flags|=f;}public void setStatusBarColor(int c){color=c;}}''',
 'com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java':'''package com.smartisanos.launcher.theme; public class MaintainedLauncherSettingsHost {public static boolean isThemeChangingMessage(android.content.Context c,String s){return c!=null&&"theme".equals(s);}}'''}
 getter=block((ROOT/'launcher/tools/java/com/smartisanos/launcher/reload/LauncherColdReloadCoordinator.java').read_text(encoding='utf8'),'    static boolean ownsInitializationLoadingWindow()')
 owners=[]
 for name,path in [('Before',args.baseline),('After',args.source)]:owners.append('static class '+name+'{'+block(path.read_text(encoding='utf8'),'    public static void coverLoadingWindow(')+'}')
 java='''package com.smartisanos.launcher.reload;
import android.content.Context;import android.view.*;import android.os.Build;
import com.smartisanos.launcher.theme.MaintainedLauncherSettingsHost;
class LauncherColdReloadCoordinator {static boolean sInitialLoadingWindowApplied; GETTER}
public class LoadingWindowProbe {
 OWNERS
 static int cases,checks;
 static void check(boolean v,String m){checks++;if(!v)throw new AssertionError(m);}
 public static void main(String[] ignored){
  for(int api:new int[]{23,24,26,28,29,30,36})for(int kind=0;kind<4;kind++)for(String message:new String[]{"","theme","initializing","other",null})for(boolean reload:new boolean[]{false,true})for(int extra:new int[]{0,0x4000000,0x1000000})for(int ui:new int[]{0,0x2000,0x1706}){
   Build.VERSION.SDK_INT=api;LauncherColdReloadCoordinator.sInitialLoadingWindowApplied=reload;
   check(LauncherColdReloadCoordinator.ownsInitializationLoadingWindow()==reload,"existing reload owner");
   Context context=kind==0?new com.smartisanos.launcher.Launcher():kind==1?new android.app.Activity():kind==2?new Context():null;
   Window before=new Window(),after=new Window();before.attrs.flags=after.attrs.flags=0x400|extra;before.decor.flags=after.decor.flags=ui;
   Before.coverLoadingWindow(before,context,message);After.coverLoadingWindow(after,context,message);
   boolean cold=kind==0&&"".equals(message)&&!reload;
   if(cold){
    check((after.attrs.flags&0x80000000)!=0,"cold startup must own transparent bar backing");
    check((after.attrs.flags&0x4000000)==0&&after.color==0,"cold backing transparent");
    check((after.attrs.flags&0x400)!=0,"original fullscreen retained");
    check((after.attrs.flags&~0x84000000)==(before.attrs.flags&~0x84000000),"unrelated flags preserved");
   }else check(after.attrs.flags==before.attrs.flags&&after.color==before.color,"theme/generic/reload unchanged");
   check(after.decor.flags==before.decor.flags,"same visibility and navigation flags");
   check(after.attrs.layoutInDisplayCutoutMode==before.attrs.layoutInDisplayCutoutMode,"same cutout geometry");
   check(after.nav==before.nav&&after.animations==before.animations,"navigation and animations unchanged");cases++;
  }
  After.coverLoadingWindow(null,null,null);checks++;
  System.out.println("RESULT {\\"cases\\":"+cases+",\\"checks\\":"+checks+",\\"scope\\":\\"actual coverLoadingWindow and reload getter with controlled Window fixtures; not OEM visual acceptance\\"}");
 }
}'''.replace('GETTER',getter).replace('OWNERS','\n'.join(owners))
 stubs['com/smartisanos/launcher/reload/LoadingWindowProbe.java']=java
 files=[]
 for name,text in stubs.items():f=out/'src'/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text,encoding='utf8');files.append(str(f))
 jdk=Path('E:/Program Files/Android/Android Studio/jbr/bin');classes=out/'classes';classes.mkdir(exist_ok=True)
 def run(cmd,name):
  r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf8',errors='replace',timeout=90);(out/name).write_text(r.stdout+r.stderr,encoding='utf8');print(r.stdout+r.stderr,end='');return r
 run([jdk/'javac.exe','-encoding','UTF-8','-d',classes,*files],'compile.log').check_returncode()
 r=run([jdk/'java.exe','-cp',classes,'com.smartisanos.launcher.reload.LoadingWindowProbe'],'test.log');r.check_returncode();row=json.loads(next(s[7:]for s in r.stdout.splitlines()if s.startswith('RESULT ')));(out/'summary.json').write_text(json.dumps(row,indent=2))

if __name__=='__main__':main()
