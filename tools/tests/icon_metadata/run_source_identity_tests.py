"""Compare extracted production source identities and count repeated resolver work."""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def block(source, signature):
    start = source.index(signature)
    end = source.index('{', start) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--baseline', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--jdk', required=True, type=Path)
    args = ap.parse_args()
    current = (ROOT / 'launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java').read_text(encoding='utf8')
    baseline = args.baseline.read_text(encoding='utf8')
    owners = []
    for name, source in [('Before', baseline), ('After', current)]:
        type_method = block(source, 'public static String desktopIconSourceType(Object itemInfo)')
        type_method = type_method.replace('{', '{ typeCalls++;', 1)
        identity = block(source, 'public static String desktopIconSourceIdentity(Object itemInfo)')
        if name == 'After':
            identity += block(source, 'static String desktopIconSourceIdentity(Object itemInfo, String effectiveType)')
            if 'private static String desktopIconSourceIdentity(Context context, String effectiveType,' in source:
                identity += block(source, 'private static String desktopIconSourceIdentity(Context context, String effectiveType,')
        pair = ('desktopIconSourceIdentity(item, type)' if name == 'After'
                else 'desktopIconSourceIdentity(item)')
        owners.append('static class ' + name + '{' + type_method + identity
                      + 'static String pair(Object item){String type=desktopIconSourceType(item);'
                      + 'return type+":"+' + pair + ';}}')
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output / 'SourceIdentityProbe.java'
    path.write_text(PROBE.replace('OWNERS', '\n'.join(owners)), encoding='utf8')
    commands = [
        [args.jdk / 'bin/javac.exe', '-encoding', 'UTF-8', '-d', args.output, path],
        [args.jdk / 'bin/java.exe', '-cp', args.output, 'SourceIdentityProbe'],
    ]
    for index, command in enumerate(commands):
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                                encoding='utf8', errors='replace', timeout=45)
        (args.output / f'{index}.log').write_text(result.stdout + result.stderr, encoding='utf8')
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        print(result.stdout, end='')
    raster = (ROOT / 'launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java').read_text(encoding='utf8')
    assert 'desktopIconSourceIdentity(itemInfo, selectedType)' in block(raster, 'private static StaticSource resolveStaticSource(Object itemInfo, Bitmap legacyBitmap,')
    assert 'desktopIconSourceIdentity(itemInfo, sourceType)' in block(raster, 'private static String buildTextureCacheKey(')
    print('PASS both production callers reuse their immediately resolved effective type')


PROBE = r'''
import java.util.Objects;
public class SourceIdentityProbe {
 static int typeCalls, managedChecks, reads, checks, cases;
 static boolean contextPresent, available, installed;
 static Context context = new Context();
 static RedirectIconInfo redirect;
 static IconSourceManager.Selection global;
 static class Context {}
 static class RedirectIconInfo {byte[] iconData;String drawableName="pack-drawable";String mode;}
 static class RedirectIconDB {
  static final String MODE_ORIGINAL="original",MODE_CUSTOM="custom",MODE_RESOURCE="resource",MODE_PACK="pack";
  static RedirectIconInfo getRedirectIconInfo(Context c,String p,String n){reads++;return redirect;}
  static String modeOf(RedirectIconInfo r){return r==null?"auto":r.mode;}
  static String resourceNameOf(RedirectIconInfo r){return "theme-drawable";}
  static String packNameOf(RedirectIconInfo r){return "pack";}
 }
 static class IconSourceManager {
  enum Type {DEFAULT,IMPROVED,PACK}
  static class Selection {Type type;String packageName="global-pack";Selection(Type t){type=t;}}
  static boolean isInstalledIconPack(Context c,String p){return installed;}
  static Selection get(Context c){return global;}
 }
 static Context currentApplicationContext(){return contextPresent?context:null;}
 static String itemFieldValue(Object i,String f){return f.equals("packageName")?"test.app":"test.Main";}
 static boolean hasEffectiveManagedDesktopSource(Context c,String p,String n){managedChecks++;return available;}
 static void check(boolean ok,String message){checks++;if(!ok)throw new AssertionError(message);}
 static void reset(){typeCalls=managedChecks=reads=0;}
 OWNERS
 public static void main(String[] args){
  Object item = new Object();
  for(boolean hasContext:new boolean[]{false,true})
  for(Object candidate:new Object[]{null,item})
  for(String mode:new String[]{"auto","original","custom","resource","pack"})
  for(IconSourceManager.Type selection:IconSourceManager.Type.values())
  for(boolean hasSource:new boolean[]{false,true})
  for(boolean hasPack:new boolean[]{false,true})
  for(int custom:new int[]{-1,0,127}) {
   contextPresent=hasContext;available=hasSource;installed=hasPack;
   global=new IconSourceManager.Selection(selection);
   redirect=mode.equals("auto")?null:new RedirectIconInfo();
   if(redirect!=null){redirect.mode=mode;redirect.iconData=custom<0?null:new byte[custom];}
   reset();String before=Before.pair(candidate);int beforeTypes=typeCalls,beforeManaged=managedChecks,beforeReads=reads;
   reset();String after=After.pair(candidate);int afterTypes=typeCalls,afterManaged=managedChecks,afterReads=reads;
   check(Objects.equals(before,after),"identity changed: "+before+" -> "+after);
   check(afterTypes==1,"source pair must resolve effective type once");
   check(beforeTypes==((hasContext&&candidate!=null)?2:1),"negative control did not reproduce duplicate type resolution");
   check(afterManaged<=beforeManaged&&afterReads<=beforeReads,"resolver work increased");
   if(beforeManaged>0)check(beforeManaged==2*afterManaged,"managed source check was not eliminated");
   check(Objects.equals(Before.desktopIconSourceIdentity(candidate),After.desktopIconSourceIdentity(candidate)),"standalone identity API changed");
   cases++;
  }
  System.out.println("PASS "+cases+" production classification/identity combinations, "+checks+" checks; paired type resolutions 2 -> 1 with negative control");
 }
}
'''

if __name__ == '__main__':
    main()
