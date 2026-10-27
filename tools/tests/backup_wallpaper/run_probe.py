"""Run production archive/codec and extracted owner IO on an isolated Android fixture."""
import argparse,subprocess,os,uuid,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--serial',required=True);ap.add_argument('--jdk',type=Path,required=True);ap.add_argument('--sdk',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 def run(cmd):
  r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60)
  if r.returncode:raise RuntimeError(r.stdout+r.stderr)
  return r.stdout
 java=ROOT/'launcher/tools/java';src=a.out/'src';classes=a.out/'classes';dex=a.out/'dex';classes.mkdir(exist_ok=True);dex.mkdir(exist_ok=True)
 def write(name,text):
  p=src/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');return p
 host=(java/'com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java').read_text(encoding='utf-8')
 def extract(first,last):return host[host.index(first):host.index(last,host.index(first))]
 members=''
 import re
 for key in ['WALLPAPER_PREFS','PREF_WALLPAPER_URI','PREF_WALLPAPER_THUMB','PREF_WALLPAPER_READY','PREF_WALLPAPER_REFRESH_PENDING']:
  members+=re.search(r'    private static final String '+key+r'\s*=\s*"[^";]*";',host).group()+'\n'
 helper=(Path(__file__).with_name('OwnerFixture.java.txt')).read_text(encoding='utf-8').replace('// FIELDS',members).replace('// PRODUCTION',extract('    public static String wallpaperBackupPreviousTheme(', '    public static String currentLauncherWallpaperUri(')+extract('    private static String saveLauncherWallpaperCopy(', '    private static void syncLauncherWallpaperUri(')+extract('    private static void cleanupOldWallpaperCopies(', '    public static Bitmap decodeLauncherWallpaperBitmap('))
 files=[write('com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java',helper)]
 recon=(java/'com/smartisanos/launcher/backup/RestoreIconSourceReconciler.java').read_text(encoding='utf-8')
 methods=recon[recon.index('    public static JSONObject encodePortableSources('):recon.index('    /** Atomically overlays')]+recon[recon.index('    public static void restorePortableSources('):recon.index('    public static void setPendingReconcile(')]+recon[recon.index('    private static void copyExistingSources('):recon.index('    private static SharedPreferences prefs(')]
 files+=[write('com/smartisanos/launcher/backup/RestoreIconSourceReconciler.java','package com.smartisanos.launcher.backup; import android.content.*;import android.graphics.*;import android.util.Log;import org.json.*;import java.io.*;import java.util.*;import com.smartisanos.launcher.data.redirectIcon.RedirectIconDB;import com.smartisanos.launcher.theme.MaintainedLauncherSettingsHost;public class RestoreIconSourceReconciler {static final String TAG="fixture",CACHE_DIR="online_icon_cache_v4";static final long MAX_SOURCE_BYTES=512L*1024L;'+methods+'}')]
 stubs={'com/smartisanos/launcher/data/redirectIcon/RedirectIconDB.java':'''package com.smartisanos.launcher.data.redirectIcon;public class RedirectIconDB {public static final String MODE_RESOURCE="resource",MODE_PACK="pack",MODE_CUSTOM="custom",MODE_AUTO="auto",MODE_ORIGINAL="original";public static final java.util.List<RedirectIconInfo> infos=new java.util.ArrayList<>();public static java.util.List<RedirectIconInfo> listAllInfo(android.content.Context c){return infos;}public static RedirectIconInfo getRedirectIconInfo(android.content.Context c,String p,String a){for(RedirectIconInfo i:infos)if(p.equals(i.packageName)&&a.equals(i.componentName))return i;return null;}public static String modeOf(RedirectIconInfo i){if(i==null||i.drawableName==null)return MODE_AUTO;return i.drawableName.split(":")[0];}public static void invalidateCaches(){}}''', 'com/smartisanos/launcher/backup/DesktopBackupController.java':'package com.smartisanos.launcher.backup;public class DesktopBackupController {public static class CancellationToken {public boolean cancelled;public void throwIfCancelled() throws java.io.IOException {if(cancelled)throw new java.io.IOException("cancelled");}}}', 'com/smartisanos/launcher/backup/LayoutSnapshotExporter.java':'package com.smartisanos.launcher.backup;public class LayoutSnapshotExporter {public static void validate(org.json.JSONObject j)throws Exception{j.getJSONArray("items");j.getJSONArray("pages");}}', 'com/smartisanos/launcher/backup/ShortcutIconBackupCodec.java':'package com.smartisanos.launcher.backup;public class ShortcutIconBackupCodec {public static org.json.JSONObject empty()throws Exception{return new org.json.JSONObject().put("records",new org.json.JSONArray());}public static void validate(org.json.JSONObject a,org.json.JSONObject b,java.io.File c){}}'}
 files += [write(k,v) for k,v in stubs.items()]
 files += [java/('com/smartisanos/launcher/backup/'+n+'.java') for n in ['ThemeBackupCodec','BackupFileUtils','BackupManifest','BackupArchiveWriter','BackupArchiveReader','BackupValidator']]
 files += [java/'com/smartisanos/launcher/backup/IconBackupCodec.java',java/'com/smartisanos/launcher/data/redirectIcon/RedirectIconInfo.java',Path(__file__).with_name('WallpaperBackupProbe.java')]
 run([a.jdk/'bin/javac.exe','-encoding','UTF-8','-source','8','-target','8','-classpath',a.sdk/'platforms/android-36/android.jar','-d',classes,*files]);run([a.jdk/'bin/jar.exe','cf',a.out/'probe.jar','-C',classes,'.']);os.environ['JAVA_HOME']=str(a.jdk);run([a.sdk/'build-tools/36.0.0/d8.bat','--min-api','26','--output',dex,a.out/'probe.jar'])
 adb=a.sdk/'platform-tools/adb.exe'
 def device(*c):return run([adb,'-s',a.serial,*c])
 remote='/data/local/tmp/wallpaper-backup-'+uuid.uuid4().hex;device('shell','mkdir',remote);device('push',dex/'classes.dex',remote+'/probe.dex')
 evidence=ROOT/'build/backup-wallpaper-20261014'
 device('push',evidence/'2026-10-03 22-22.slauncherbackup',remote+'/old.slauncherbackup');device('push',evidence/'2026-10-09 16-20.slauncherbackup',remote+'/new.slauncherbackup')
 before=device('shell','pidof','com.smartisanos.launcher').strip();result=device('shell',f'CLASSPATH={remote}/probe.dex app_process /system/bin com.smartisanos.launcher.backup.WallpaperBackupProbe {remote}');after=device('shell','pidof','com.smartisanos.launcher').strip();assert 'PASS WALLPAPER_BACKUP_CHECKS=' in result,result
 device('pull',remote+'/filtered.slauncherbackup',a.out/'filtered.slauncherbackup');report={'serial':a.serial,'result':result,'pid_before':before,'pid_after':after,'remote_fixture':remote,'scope':'real Android bitmap/URI/JSON/ZIP/checksums and extracted production file methods; controlled preferences and scene boundary; launcher/phone data untouched'};(a.out/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(result);print('Launcher PID',before,'->',after)
if __name__=='__main__':main()
