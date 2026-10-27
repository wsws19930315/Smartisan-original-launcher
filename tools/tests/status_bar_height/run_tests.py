"""Run the production height calculation without Android dependencies."""
from pathlib import Path
import subprocess, uuid

root=Path(__file__).resolve().parents[3]
source=root/'launcher/tools/java/com/smartisanos/launcher/compat/StatusBarHeightCompat.java'
text=source.read_text(encoding='utf8')
start=text.index('    public static int calculate(')
end=text.index('    private static void captureLiveInsets',start)
out=root/'build'/('status-bar-height-test-'+uuid.uuid4().hex[:8]);out.mkdir(parents=True)
java='''public class HeightTest {
static int checks;
static void eq(int a,int b){checks++;if(a!=b)throw new AssertionError(a+" != "+b);}
static int legacy(int system,int cutout,boolean has,int gap,int extra,boolean auto,int max){
 system=Math.max(0,system);cutout=has?Math.max(0,cutout):0;int floor=Math.max(system,cutout);
 int base=auto&&has?Math.max(system,cutout+Math.max(0,gap)):system;
 long request=(long)base+extra;request=auto?Math.max(request,floor):Math.max(0L,request);
 return (int)Math.min(request,Math.max(floor,system+Math.max(0,max)));
}
public static void main(String[] args){
 eq(calculate(63,145,true,5,0,true,42),150);
 eq(calculate(145,145,true,5,0,true,42),150);
 for(int system:new int[]{0,24,63,100,145})for(int cutout:new int[]{0,30,80,145,200})
 for(int gap:new int[]{0,2,5})for(int extra:new int[]{-12,0,16,48}){
  eq(calculate(system,cutout,false,gap,extra,true,42),legacy(system,cutout,false,gap,extra,true,42));
  eq(calculate(system,cutout,true,gap,extra,false,42),legacy(system,cutout,true,gap,extra,false,42));
  int height=calculate(system,cutout,true,gap,0,true,42);
  eq(height,Math.max(system,cutout+gap));
 }
 System.out.println("Production status bar height checks passed: "+checks);
}
'''+text[start:end]+'}\n'
(out/'HeightTest.java').write_text(java,encoding='utf8')
jdk=Path(r'E:\Program Files\Android\Android Studio\jbr')
subprocess.run([str(jdk/'bin/javac.exe'),'-encoding','UTF-8','-d',str(out),str(out/'HeightTest.java')],check=True)
subprocess.run([str(jdk/'bin/java.exe'),'-cp',str(out),'HeightTest'],check=True)
