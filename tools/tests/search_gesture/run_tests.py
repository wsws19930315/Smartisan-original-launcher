"""Compile the real direction owner; verify mirrored finish gates and Smali wiring.

Motion/Android services are doubles. Runtime gesture acceptance is separately
verified with actual input on the emulator, not inferred from these predicates.
"""
import argparse
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
STUBS = {
    'android/content/Context.java': '''package android.content;public class Context {
 public static final int MODE_PRIVATE=0;
 public boolean reversed;public android.content.res.Resources getResources(){return new android.content.res.Resources();}
 public Object getContentResolver(){return null;}
 public SharedPreferences getSharedPreferences(String n,int m){return new SharedPreferences(reversed);}}''',
    'android/content/SharedPreferences.java': '''package android.content;public class SharedPreferences {
 boolean value;SharedPreferences(boolean b){value=b;}public boolean contains(String k){return true;}
 public boolean getBoolean(String k,boolean d){return value;}}''',
    'android/content/res/Resources.java': '''package android.content.res;public class Resources {
 public android.util.DisplayMetrics getDisplayMetrics(){return new android.util.DisplayMetrics();}}''',
    'android/util/DisplayMetrics.java': 'package android.util;public class DisplayMetrics{public int heightPixels=2400;public float density=3;}',
    'android/util/Log.java': 'package android.util;public class Log{public static int i(String t,String m){return 0;}}',
    'android/provider/Settings.java': 'package android.provider;public class Settings{public static class System{public static String getString(Object r,String k){return null;}}}',
    'android/os/SystemClock.java': 'package android.os;public class SystemClock{public static long uptimeMillis(){return 5000;}}',
    'android/view/MotionEvent.java': '''package android.view;public class MotionEvent {
 public static final int ACTION_UP=1,ACTION_MOVE=2,ACTION_CANCEL=3,ACTION_POINTER_DOWN=5,ACTION_POINTER_UP=6;
 public int action=ACTION_MOVE;public float x,y;public int pointers=1;public long downTime=100;
 public long getDownTime(){return downTime;}public float getX(){return x;}public float getY(){return y;}
 public int getPointerCount(){return pointers;}public int getActionMasked(){return action;}}''',
}
TEST = '''import android.content.Context;import android.view.MotionEvent;
import com.smartisanos.launcher.gesture.VerticalGestureDirectionConfig;
public class GestureTest {
 static int checks;static void check(boolean b,String m){checks++;if(!b)throw new AssertionError(m);}
 public static void main(String[] args){Context c=new Context();
 for(boolean reversed:new boolean[]{false,true}) for(int height:new int[]{1280,1920,2400,3200}) {
  c.reversed=reversed;VerticalGestureDirectionConfig.captureForActionDown(c);
  for(float ratio:new float[]{0,.1f,.249f,.25f,.5f,.75f,.751f,.9f,1}) {
   boolean expected=reversed?ratio>=.25f:ratio<=.75f;
   check(VerticalGestureDirectionConfig.passesSearchFinishRegion(ratio*height,height)==expected,"mirrored finish "+reversed+"/"+height+"/"+ratio);
  }
 }
 c.reversed=false;MotionEvent e=new MotionEvent();e.x=700;e.y=1800;
 VerticalGestureDirectionConfig.captureForActionDown(c);
 check(VerticalGestureDirectionConfig.passesSearchStartRegion(c,2100,2280),"X21A Dock origin must be accepted at density 3");
 check(!VerticalGestureDirectionConfig.passesSearchStartRegion(c,2280,2280),"outside app surface rejected");
 check(!VerticalGestureDirectionConfig.passesSearchStartRegion(c,200,2280),"top notification region rejected");
 e.y=2250;VerticalGestureDirectionConfig.beginSearchGesture(c,e);e.y=1000;
 VerticalGestureDirectionConfig.observeSearchMotion(e);e.action=MotionEvent.ACTION_UP;
 check(VerticalGestureDirectionConfig.isSearchGestureFinalValid(e),"Dock upward sequence must reach completion");
 e.action=MotionEvent.ACTION_MOVE;e.y=1800;
 VerticalGestureDirectionConfig.beginSearchGesture(c,e);e.y=800;
 VerticalGestureDirectionConfig.observeSearchMotion(e);e.action=MotionEvent.ACTION_UP;
 check(VerticalGestureDirectionConfig.isSearchGestureFinalValid(e),"valid upward history remains valid");
 check(VerticalGestureDirectionConfig.passesSearchFinishRegion(e.y,2400),"high finish accepted");
 e.action=MotionEvent.ACTION_MOVE;e.y=1800;VerticalGestureDirectionConfig.beginSearchGesture(c,e);
 e.y=1900;VerticalGestureDirectionConfig.observeSearchMotion(e);e.action=MotionEvent.ACTION_UP;
 check(!VerticalGestureDirectionConfig.isSearchGestureFinalValid(e),"opposite direction still rejected");
 e.action=MotionEvent.ACTION_MOVE;e.y=1800;VerticalGestureDirectionConfig.beginSearchGesture(c,e);
 e.pointers=2;VerticalGestureDirectionConfig.observeSearchMotion(e);e.action=MotionEvent.ACTION_UP;
 check(!VerticalGestureDirectionConfig.isSearchGestureFinalValid(e),"multi-touch still rejected");
 e.pointers=1;e.action=MotionEvent.ACTION_MOVE;e.y=2100;VerticalGestureDirectionConfig.beginSearchGesture(c,e);
 e.downTime=101;e.y=1000;VerticalGestureDirectionConfig.observeSearchMotion(e);e.action=MotionEvent.ACTION_UP;
 check(!VerticalGestureDirectionConfig.isSearchGestureFinalValid(e),"different gesture downTime still rejected");
 System.out.println("PASS SEARCH_GESTURE_CHECKS="+checks);
 }}'''


def check_touch_input_compat(jdk, source):
    """Exercise the actual shell producer against old/new service API shapes."""
    shared = {
        'android/os/SystemClock.java': '''package android.os;public class SystemClock {
static long t=100;public static long uptimeMillis(){return ++t;}
public static void sleep(long n){t+=n;}}''',
        'android/view/InputDevice.java': 'package android.view;public class InputDevice {public static final int SOURCE_TOUCHSCREEN=4098;}',
        'android/view/InputEvent.java': 'package android.view;public class InputEvent {}',
        'android/view/MotionEvent.java': '''package android.view;public class MotionEvent extends InputEvent {
public static final int ACTION_DOWN=0,ACTION_UP=1,ACTION_MOVE=2,ACTION_CANCEL=3,
ACTION_POINTER_DOWN=5,ACTION_POINTER_INDEX_SHIFT=8,TOOL_TYPE_FINGER=1;
public static class PointerProperties {public int id,toolType;}
public static class PointerCoords {public float x,y,pressure,size;}
public long down,time;public int action,source,pointers=1;
public static MotionEvent obtain(long d,long t,int a,float x,float y,int m){MotionEvent e=new MotionEvent();e.down=d;e.time=t;e.action=a;return e;}
public static MotionEvent obtain(long d,long t,int a,int n,PointerProperties[] p,
PointerCoords[] c,int meta,int buttons,float xp,float yp,int device,int edge,int s,int flags){
if(n<1||n>p.length||n>c.length)throw new AssertionError("pointer count");
for(int i=0;i<n;i++)if(p[i].id!=i||p[i].toolType!=TOOL_TYPE_FINGER||c[i].pressure!=1)
throw new AssertionError("pointer identity");
MotionEvent e=obtain(d,t,a,0f,0f,0);e.pointers=n;e.source=s;return e;}
public int getPointerCount(){return pointers;}
public void setSource(int s){source=s;}public void recycle(){}}''',
        'fixture/State.java': '''package fixture;public class State {
public static int legacy,global,events,last,lastPointers,pointerDowns;public static long down,time;
public static boolean record(android.view.InputEvent input,int mode){
android.view.MotionEvent e=(android.view.MotionEvent)input;
if(mode!=2||e.source!=4098||e.time<time)throw new AssertionError("input contract");
if(events++==0){if(e.action!=0)throw new AssertionError("missing DOWN");down=e.down;}
if(e.down!=down)throw new AssertionError("downTime changed");
if((e.action&255)==5){
if((e.action>>8)!=e.pointers-1)throw new AssertionError("pointer action index");pointerDowns++;}
time=e.time;last=e.action;lastPointers=e.pointers;return true;}
}''',
        'TouchCompatProbe.java': '''public class TouchCompatProbe {
public static void main(String[] a)throws Exception{
String mode=a[0];
if(mode.equals("legacy")||mode.equals("global")||mode.equals("contextless")){
TouchInput.main(new String[]{"swipe","1","10","1","1","20"});
if(fixture.State.events<3||fixture.State.last!=1)throw new AssertionError("incomplete swipe");
fixture.State.events=0;
TouchInput.main(new String[]{"cancel","1","10","1","1","20"});
if(fixture.State.events<3||fixture.State.last!=3)throw new AssertionError("incomplete cancellation");
for(int count=2;count<=4;count++){
fixture.State.events=0;fixture.State.pointerDowns=0;
TouchInput.main(new String[]{"multi-cancel-"+count,"1","10","1","1","20"});
if(fixture.State.last!=3||fixture.State.lastPointers!=count||fixture.State.pointerDowns!=count-1)
throw new AssertionError("incomplete multi-pointer cancellation");
}
if(mode.equals("legacy")?(fixture.State.legacy!=5||fixture.State.global!=0):(fixture.State.global!=5||fixture.State.legacy!=0))throw new AssertionError("wrong owner");
}else{
try{TouchInput.main(new String[]{"swipe","1","10","1","1","20"});throw new AssertionError("error swallowed");}
catch(java.lang.reflect.InvocationTargetException e){if(!mode.equals("denied")||!(e.getCause() instanceof SecurityException))throw e;}
catch(ClassNotFoundException e){if(!mode.equals("missing"))throw e;}
if(fixture.State.global!=0||fixture.State.events!=0)throw new AssertionError("unsafe fallback");
}
System.out.println("PASS TOUCH_INPUT_COMPAT "+mode);
}}''',
    }
    injection = 'public boolean injectInputEvent(android.view.InputEvent e,int m){return fixture.State.record(e,m);}'
    for mode in ('legacy', 'global', 'contextless', 'denied', 'missing'):
        sources = dict(shared)
        accessor = ('public static InputManager getInstance(){fixture.State.legacy++;return new InputManager();}'
                    if mode == 'legacy' else
                    'public static InputManager getInstance(){throw new NullPointerException("fixture-context");}'
                    if mode == 'contextless' else
                    'public static InputManager getInstance(){throw new SecurityException("fixture");}'
                    if mode == 'denied' else '')
        sources['android/hardware/input/InputManager.java'] = (
            'package android.hardware.input;public class InputManager {' + accessor + injection + '}')
        if mode != 'missing':
            sources['android/hardware/input/InputManagerGlobal.java'] = (
                'package android.hardware.input;public class InputManagerGlobal {'
                'public static InputManagerGlobal getInstance(){fixture.State.global++;return new InputManagerGlobal();}'
                + injection + '}')
        with tempfile.TemporaryDirectory(prefix='touch-api-') as directory:
            base = Path(directory)
            files = [str(source)]
            for name, text in sources.items():
                path = base / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8')
                files.append(str(path))
            subprocess.run([str(jdk / 'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(base), *files], check=True)
            subprocess.run([str(jdk / 'bin/java.exe'), '-cp', str(base), 'TouchCompatProbe', mode], check=True)


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--jdk', required=True, type=Path)
    ap.add_argument('--smali', type=Path, default=ROOT / 'launcher/smali/com/smartisanos/launcher/a/a/a.smali')
    ap.add_argument('--touch-input', type=Path, default=Path(__file__).with_name('TouchInput.java'))
    args = ap.parse_args()
    smali = args.smali.read_text(encoding='utf-8')
    fling = smali.split('.method private static a(FFJFFJZZ)V', 1)[1].split('.end method', 1)[0]
    assert '0x447a0000' in fling, 'completion window must keep the documented 1000ms compatibility contract'
    assert '->passesSearchFinishRegion(FI)Z' in fling, 'end coordinates must use the finish predicate'
    assert '->passesSearchStartRegion' not in fling, 'start gate already runs at ACTION_DOWN'
    assert '->isSearchGestureFinalValid' in smali and '->canOpenSearchNow' in fling
    owner = ROOT / 'launcher/tools/java/com/smartisanos/launcher/gesture/VerticalGestureDirectionConfig.java'
    with tempfile.TemporaryDirectory(prefix='search-gesture-') as tmp:
        tmp = Path(tmp)
        files = []
        for name, text in {**STUBS, 'GestureTest.java': TEST}.items():
            p = tmp / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding='utf-8')
            files.append(str(p))
        subprocess.run([str(args.jdk / 'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(tmp), *files, str(owner)], check=True)
        subprocess.run([str(args.jdk / 'bin/java.exe'), '-cp', str(tmp), 'GestureTest'], check=True)
    check_touch_input_compat(args.jdk, args.touch_input)


if __name__ == '__main__':
    main()
