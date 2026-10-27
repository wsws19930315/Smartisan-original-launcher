"""Execute the real e.s texture-entry Smali prefix and production version predicate on ART.

Source resolver/cache creation is counted by a fixture; no Launcher state is read.
"""
import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'tools/tests/deferred_icon_source'))
from run_database_tests import ASSEMBLER
from run_key_source_device_tests import block


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--serial', required=True)
    ap.add_argument('--before', type=Path, required=True)
    ap.add_argument('--after', type=Path, default=ROOT/'launcher/smali/com/smartisanos/launcher/e/s.smali')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output
    (out/'classes').mkdir(parents=True, exist_ok=True)
    (out/'dex').mkdir(exist_ok=True)
    assembled = []
    signature = '.method public static a(Lcom/smartisanos/launcher/data/ItemInfo;Ljava/lang/String;ZI)Lcom/smartisanos/smengine/Da;'
    for name, path in [('Before', args.before), ('After', args.after)]:
        source = path.read_text(encoding='utf8')
        start = source.index(signature)
        end = source.index('    :cond_page_mode_key_ready\n', start)+len('    :cond_page_mode_key_ready\n')
        prefix = source[start:end].replace(signature, '.method public static gate(Lcom/smartisanos/launcher/data/ItemInfo;Ljava/lang/String;I)Ljava/lang/String;')
        prefix = prefix.replace('p3', 'p2')
        target = out/(name+'.smali')
        target.write_text('.class public Lcom/smartisanos/launcher/audit/Key'+name+';\n.super Ljava/lang/Object;\n'+prefix+'    return-object p1\n.end method\n', encoding='utf8')
        assembled.append(target)
    raster = (ROOT/'launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java').read_text(encoding='utf8')
    version = re.search(r'private static final String RASTER_CACHE_VERSION = "([^"]+)";', raster)[1]
    helper = block(raster, 'public static boolean hasCurrentTextureCacheKey(')
    fixture = out/'IconRasterDiagnostics.java'
    fixture.write_text('''package com.smartisanos.launcher.theme;
public class IconRasterDiagnostics {
 public static int builds;
 private static final String RASTER_CACHE_VERSION="'''+version+'''";
 public static boolean shouldUseHighResolutionDesktopRaster(Object item){return true;}
 public static String textureCacheKey(Object item,String key,int mode){builds++;return key+"@rebuilt:"+mode;}
'''+helper+'}', encoding='utf8')
    item = out/'ItemInfo.java'
    item.write_text('package com.smartisanos.launcher.data;public class ItemInfo{}', encoding='utf8')
    probe = out/'KeyEntryProbe.java'
    probe.write_text(PROBE.replace('VERSION', version), encoding='utf8')
    assembler = out/'AssembleIconDatabaseProbe.java'
    assembler.write_text(ASSEMBLER, encoding='utf8')
    sdk = Path('D:/sdk');jdk=Path('E:/Program Files/Android/Android Studio/jbr/bin')

    def run(command, name):
        r = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                           encoding='utf8', errors='replace', timeout=120)
        (out/name).write_text(r.stdout+r.stderr, encoding='utf8')
        if r.returncode:
            raise RuntimeError(r.stdout+r.stderr)
        return r.stdout

    run([jdk/'javac.exe','-cp',ROOT/'tools/apktool.jar','-d',out/'classes',assembler], 'javac-assembler.log')
    run([jdk/'java.exe','-cp',str(out/'classes')+';'+str(ROOT/'tools/apktool.jar'),
         'AssembleIconDatabaseProbe',out/'entry.dex',*assembled], 'assemble.log')
    run([jdk/'javac.exe','-source','8','-target','8','-d',out/'classes',fixture,item,probe], 'javac.log')
    classes=[p for p in (out/'classes').rglob('*.class') if p.name!='AssembleIconDatabaseProbe.class']
    run([jdk/'java.exe','-cp',sdk/'build-tools/37.0.0/lib/d8.jar','com.android.tools.r8.D8',
         '--min-api','28','--lib',sdk/'platforms/android-36/android.jar','--output',out/'dex',out/'entry.dex',*classes], 'd8.log')
    adb=[sdk/'platform-tools/adb.exe','-s',args.serial];remote='/data/local/tmp/smartisan-key-entry.dex'
    run([*adb,'push',out/'dex/classes.dex',remote], 'push.log')
    try:
        result=run([*adb,'shell','env','CLASSPATH='+remote,'app_process','/system/bin',
                    'com.smartisanos.launcher.audit.KeyEntryProbe'], 'result.log')
        assert 'PASS KEY_ENTRY' in result, result
        print(result)
    finally:
        run([*adb,'shell','rm','-f',remote], 'cleanup.log')


PROBE = r'''
package com.smartisanos.launcher.audit;
import com.smartisanos.launcher.theme.IconRasterDiagnostics;
import com.smartisanos.launcher.data.ItemInfo;
public class KeyEntryProbe {
 static int checks;
 static String call(String owner,ItemInfo item,String key,int mode)throws Exception{
  return (String)Class.forName("com.smartisanos.launcher.audit.Key"+owner).getMethod("gate",ItemInfo.class,String.class,int.class).invoke(null,item,key,mode);
 }
 static void check(boolean ok,String message){checks++;if(!ok)throw new AssertionError(message);}
 public static void main(String[] args){try{run();}catch(Throwable error){error.printStackTrace(System.out);System.exit(1);}}
 static void run()throws Exception {
  ItemInfo item=new ItemInfo();String current="icon#VERSION:source:grid=12:final",active=current+":active-frame:20261022";
  for(String suffix:new String[]{"",":active-frame:20261022",":folder-shared",":package-update"}){
   String key=current+suffix;IconRasterDiagnostics.builds=0;String before=call("Before",item,key,12);
   check(IconRasterDiagnostics.builds==1&&!key.equals(before),"old v18 guard redundantly rebuilds current key");
   IconRasterDiagnostics.builds=0;String after=call("After",item,key,12);
   check(IconRasterDiagnostics.builds==0&&key.equals(after),"current key reused without resolver/cache build");
  }
  for(String key:new String[]{"raw", "icon#raster:v17-old:stale", "icon#raster:v18-icon-contract:stale"}){
   IconRasterDiagnostics.builds=0;String after=call("After",item,key,12);
   check(IconRasterDiagnostics.builds==1&&after.equals(key+"@rebuilt:12"),"raw and obsolete keys build once");
  }
  for(int mode:new int[]{1,8,9,12,20}){
   IconRasterDiagnostics.builds=0;check(current.equals(call("After",item,current,mode))&&IconRasterDiagnostics.builds==0,"caller-owned current representation retained, mode="+mode);
  }
  check(call("After",null,current,12)==null&&call("After",item,null,12)==null,"null guard retained");
  check(!IconRasterDiagnostics.hasCurrentTextureCacheKey(null)&&!IconRasterDiagnostics.hasCurrentTextureCacheKey("raw"),"predicate null/raw");
  System.out.println("PASS KEY_ENTRY checks="+checks+" currentRebuildsBefore=1 after=0 obsoleteV18BuildsAfter=1 boundary=actual-entry-prefix,counted-source-fixture");
 }
}
'''

if __name__ == '__main__':
    main()
