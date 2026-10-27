"""Inject theme preference persistence failures into the production restore controller.

Journal, controller, locks and files are real; Android/DB/archive/codec boundaries
reuse the checkpoint suite's doubles. No installed Launcher data is accessed.
"""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
B = 'com/smartisanos/launcher/backup/'
spec = importlib.util.spec_from_file_location('checkpoint_fixtures', Path(__file__).with_name('run_tests.py'))
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
SOURCES = dict(fixtures.SOURCES)
del SOURCES[B + 'CheckpointTest.java']
SOURCES['android/content/Context.java'] = SOURCES['android/content/Context.java'].replace(
    'public boolean commit(){return true;}',
    '''public int failThemeCommits,themeCommits;public boolean commit(){
    if(themePending){themePending=false;themeCommits++;
      if(failThemeCommits>0){failThemeCommits--;return false;}}
    return true;}''').replace(
    'public Editor edit(){return this;}',
    'boolean themePending;public Editor edit(){themePending=false;return this;}').replace(
    'values.put(k,v);return this;',
    'values.put(k,v);themePending="launcher_theme".equals(k);return this;')
SOURCES[B + 'ThemeBackupCodec.java'] = '''package com.smartisanos.launcher.backup;
import android.content.*;import org.json.*;public class ThemeBackupCodec{
 public static boolean available;
 public static JSONObject encode(Context c,java.io.File f,DesktopBackupController.CancellationToken t){return new JSONObject();}
 public static void restoreWallpaper(Context c,JSONObject j,java.io.File f){Effects.events.add("WALLPAPER");}
 public static boolean isThemePackageAvailable(Context c,String p){return available;}
}'''
SOURCES[B + 'PreferenceBackupCodec.java'] = '''package com.smartisanos.launcher.backup;
import android.content.*;import org.json.*;public class PreferenceBackupCodec{
 public static JSONObject encode(Context c){return new JSONObject();}
 public static void restore(Context c,JSONObject j){Effects.events.add("PREF");
  c.prefs.values.put("launcher_theme",Effects.lastArchive.getName().startsWith("source")?"unavailable-theme":"old-theme");}
}'''
SOURCES[B + 'ThemeFallbackTest.java'] = '''package com.smartisanos.launcher.backup;
import android.content.*;import java.io.*;import java.nio.file.*;import java.util.*;
import static com.smartisanos.launcher.backup.RestoreOperationJournal.State.*;
public class ThemeFallbackTest{
 static int checks,cases;static File root;
 static void check(boolean b,String s){checks++;if(!b)throw new AssertionError(s+" events="+Effects.events);}
 static Context fresh(){Effects.clear();ThemeBackupCodec.available=false;Context c=new Context(new File(root,"case"+(cases++)));
  c.prefs.values.put("launcher_theme","old-theme");return c;}
 static RestoreOperationJournal.Entry prepare(Context c,boolean undo)throws Exception{
  RestoreOperationJournal.Entry e=new RestoreOperationJournal.Entry();e.operationToken="test-token";
  e.stagingPath=new File(c.getCacheDir(),"restore_staging/test-token").getAbsolutePath();
  e.rollbackPath=DesktopRestoreController.rollbackArchive(c).getAbsolutePath();e.undo=undo;
  for(File f:new File[]{new File(e.stagingPath,"source.slauncherbackup"),new File(e.rollbackPath)}){
   f.getParentFile().mkdirs();Files.writeString(f.toPath(),"fixture");}
  new RestoreOperationJournal(c).write(e,WAITING_TRANSITION,null);return e;}
 static boolean apply(Context c,RestoreOperationJournal.Entry e){return DesktopRestoreController.applyPreparedAfterOldProcessExit(
  c,e.operationToken,e.undo?"BACKUP_RESTORE_ROLLBACK":"BACKUP_RESTORE");}
 static void retained(RestoreOperationJournal.Entry e){check(new File(e.rollbackPath).isFile(),"rollback retained");
  check(new File(e.stagingPath,"source.slauncherbackup").isFile(),"source retained");}
 public static void main(String[] args)throws Exception{root=new File(args[0]);
  Context c=fresh();RestoreOperationJournal.Entry e=prepare(c,false);check(apply(c,e),"successful missing-theme fallback");
  check(new RestoreOperationJournal(c).read().state==COMMITTED,"successful restore committed");
  check("old-theme".equals(c.prefs.getString("launcher_theme","")),"original theme retained");
  check(c.prefs.themeCommits==1,"one fallback write");check(Effects.events.contains("ICONS"),"icons applied after persisted fallback");

  c=fresh();e=prepare(c,false);c.prefs.failThemeCommits=1;check(apply(c,e),"failed fallback rolls back");
  check(new RestoreOperationJournal(c).read().state==ROLLED_BACK,"failed fallback must not commit incoming restore");
  check(Effects.lastArchive.equals(new File(e.rollbackPath)),"failure uses rollback archive");
  check(Effects.events.equals(Arrays.asList("DB","PREF","DB","PREF","ICONS","PORTABLE","RECONCILE","WALLPAPER","VERIFY")),"no forward icons/wallpaper after failed fallback");
  check(c.prefs.themeCommits==2,"rollback fallback persisted");retained(e);

  c=fresh();e=prepare(c,false);c.prefs.failThemeCommits=2;check(!apply(c,e),"persistent failure does not report success");
  check(new RestoreOperationJournal(c).read().state==ROLLING_BACK,"rollback remains recoverable");
  check(!Effects.events.contains("ICONS")&&!Effects.events.contains("VERIFY"),"no later phase after either failed write");
  check("RESTORE_ROLLBACK_FAILED".equals(c.prefs.getString("pending_restore_toast","")),"specific failure notice");retained(e);
  Effects.clear();check(apply(c,e),"retry succeeds when storage recovers");
  check(new RestoreOperationJournal(c).read().state==ROLLED_BACK,"retry rolls back rather than applies incoming backup");
  check(Effects.lastArchive.equals(new File(e.rollbackPath)),"retry source remains rollback");

  c=fresh();e=prepare(c,true);c.prefs.failThemeCommits=1;check(!apply(c,e),"undo storage failure is not success");
  check(new RestoreOperationJournal(c).read().state==FAILED_ROLLBACK_PENDING,"undo retains failed checkpoint");retained(e);
  Effects.clear();check(apply(c,e),"undo retry after recovery");check(new RestoreOperationJournal(c).read().state==COMMITTED,"undo retry complete");
  check(Effects.lastArchive.equals(new File(e.rollbackPath)),"undo retry correct source");

  c=fresh();e=prepare(c,false);ThemeBackupCodec.available=true;c.prefs.failThemeCommits=1;
  check(apply(c,e),"available theme unaffected");check(c.prefs.themeCommits==0,"available theme no fallback write");
  check("unavailable-theme".equals(c.prefs.getString("launcher_theme","")),"available theme keeps restored preference");
  System.out.println("PASS production theme fallback checks="+checks+" cases="+cases);
 }
}'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jdk', type=Path, required=True)
    parser.add_argument('--controller', type=Path, help='Optional saved pre-fix source for a negative control')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='restore-theme-fallback-') as temporary:
        base = Path(temporary)
        files = []
        for name, source in SOURCES.items():
            path = base / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source, encoding='utf-8')
            files.append(str(path))
        for name in ['RestoreOperationJournal', 'DesktopRestoreController', 'RestoreRecoveryGuard',
                     'BackupOperationLock', 'BackupFileUtils', 'BackupRestoreResult']:
            path = ROOT / 'launcher/tools/java' / B / (name + '.java')
            if name == 'DesktopRestoreController' and args.controller:
                path = base / B / (name + '.java')
                path.write_bytes(args.controller.read_bytes())
            files.append(str(path))
        classes = base / 'classes'
        classes.mkdir()
        subprocess.run([str(args.jdk / 'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(classes), *files], check=True)
        subprocess.run([str(args.jdk / 'bin/java.exe'), '-cp', str(classes),
                        'com.smartisanos.launcher.backup.ThemeFallbackTest', str(base / 'data')], check=True)


if __name__ == '__main__':
    main()
