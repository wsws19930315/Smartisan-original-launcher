"""Use actual restore/journal/recovery/file owners to inject snapshot preparation failures.

Android/codec/archive/database boundaries are fixtures. Files, threads and locks are real;
no installed Launcher data is accessed. Saved pre-fix sources provide a negative control.
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
spec = importlib.util.spec_from_file_location('journal_fixtures', Path(__file__).with_name('run_tests.py'))
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
SOURCES = dict(fixtures.SOURCES)
SOURCES['android/system/Os.java'] = SOURCES['android/system/Os.java'].replace(
    'Files.move(', 'if(com.smartisanos.launcher.backup.Effects.scenario.equals("publish"))throw new java.io.IOException("injected atomic rename");Files.move(')
del SOURCES[B+'CheckpointTest.java']
SOURCES[B+'Effects.java'] = SOURCES[B+'Effects.java'].replace(
    'public static File lastArchive;', 'public static String scenario="";public static File lastArchive;').replace(
    'events.clear();', 'scenario="";events.clear();')
SOURCES[B+'DesktopBackupController.java'] = SOURCES[B+'DesktopBackupController.java'].replace(
    'exportLayoutAtDatabaseSafePoint(Context c,CancellationToken t){return new JSONObjectHolder();}',
    '''exportLayoutAtDatabaseSafePoint(Context c,CancellationToken t)throws java.io.IOException{
    if(Effects.scenario.equals("cancel-export"))t.cancel();
    if(Effects.scenario.equals("export"))throw new java.io.IOException("injected export");
    return new JSONObjectHolder();}''')
SOURCES[B+'BackupArchiveWriter.java'] = SOURCES[B+'BackupArchiveWriter.java'].replace(
    'File f=new File(d,"archive.slauncherbackup");',
    'if(Effects.scenario.equals("write"))throw new IOException("injected archive write");File f=new File(d,"archive.slauncherbackup");').replace(
    'return f;', 'if(Effects.scenario.equals("cancel-write"))c.cancel();return f;')
SOURCES[B+'BackupValidator.java'] = SOURCES[B+'BackupValidator.java'].replace(
    'validateAndExtract(File f,File d){d.mkdirs();}',
    'validateAndExtract(File f,File d)throws java.io.IOException{if(Effects.scenario.equals("validate"))throw new java.io.IOException("injected validation");d.mkdirs();}')
SOURCES['com/smartisanos/launcher/reload/LauncherColdReloadCoordinator.java'] = SOURCES['com/smartisanos/launcher/reload/LauncherColdReloadCoordinator.java'].replace(
    'return true;', 'return !com.smartisanos.launcher.backup.Effects.scenario.equals("transition");')
SOURCES[B+'UndoPreservationTest.java'] = '''package com.smartisanos.launcher.backup;
import android.content.*;import android.util.AtomicFile;import java.io.*;import java.nio.file.*;import java.lang.reflect.*;import java.util.*;
import static com.smartisanos.launcher.backup.RestoreOperationJournal.State.*;
public class UndoPreservationTest{
 static int checks,cases;static File root;
 static void check(boolean b,String s){checks++;if(!b)throw new AssertionError(s+" scenario="+Effects.scenario);}
 static void write(File f,String s)throws Exception{f.getParentFile().mkdirs();Files.writeString(f.toPath(),s);}
 static Context fresh(){Effects.clear();AtomicFile.failState="";AtomicFile.failStart=false;AtomicFile.silentFinish=false;return new Context(new File(root,"case"+(cases++)));}
 static String content(File f)throws Exception{return f.isFile()?Files.readString(f.toPath()):"MISSING";}
 static RestoreOperationJournal.Entry prepare(Context c,String scenario)throws Exception{
  write(DesktopRestoreController.rollbackArchive(c),"old-undo");String token="restore-"+cases;
  check(BackupOperationLock.acquire(token),"preparation owner acquired "+token);
  Method validate=DesktopRestoreController.class.getDeclaredMethod("validate",Context.class,android.net.Uri.class,String.class,DesktopBackupController.CancellationToken.class,DesktopRestoreController.Listener.class);
  validate.setAccessible(true);validate.invoke(null,c,new android.net.Uri(),token,new DesktopBackupController.CancellationToken(),null);
  RestoreOperationJournal journal=new RestoreOperationJournal(c);check(journal.read().state==READY,"preview ready");
  Field f=DesktopRestoreController.class.getDeclaredField("prepared");f.setAccessible(true);Object prepared=f.get(null);
  Method create=DesktopRestoreController.class.getDeclaredMethod("createRollbackAndTransition",Context.class,prepared.getClass(),DesktopBackupController.CancellationToken.class);
  create.setAccessible(true);Effects.scenario=scenario;create.invoke(null,c,prepared,new DesktopBackupController.CancellationToken());
  return journal.read();
 }
 static void finish(Context c,RestoreOperationJournal.Entry e)throws Exception{
  Method m=DesktopRestoreController.class.getDeclaredMethod("finishRestoreFiles",Context.class,RestoreOperationJournal.class,RestoreOperationJournal.Entry.class);m.setAccessible(true);
  try{m.invoke(null,c,new RestoreOperationJournal(c),e);}catch(InvocationTargetException x){throw (Exception)x.getCause();}
 }
 static void original(Context c)throws Exception{check(content(DesktopRestoreController.rollbackArchive(c)).equals("old-undo"),"old undo bytes retained");}
 public static void main(String[] args)throws Exception{root=new File(args[0]);
  check(BackupOperationLock.acquire(new String("identity")),"identity owner acquired");
  check(BackupOperationLock.owns(new String("identity")),"equal token owns operation");
  BackupOperationLock.release(new String("identity"));check(!BackupOperationLock.isBusy(),"equal decoded token releases operation");
  check(BackupOperationLock.acquire("new-owner"),"new owner acquired");BackupOperationLock.release("identity");
  check(BackupOperationLock.owns("new-owner"),"stale token cannot release new operation");BackupOperationLock.release(new String("new-owner"));
  for(String scenario:new String[]{"cancel-export","cancel-write","export","write","validate","transition"}){
   Context c=fresh();RestoreOperationJournal.Entry e=prepare(c,scenario);original(c);
   check(e.state==IDLE,"aborted preparation idle");check(!BackupOperationLock.isBusy(),"aborted owner released");
   check(!new File(c.getCacheDir(),"restore_staging/restore-"+cases).exists(),"aborted staging removed");
  }
  Context c=fresh();AtomicFile.failState="ROLLBACK_READY";RestoreOperationJournal.Entry e=prepare(c,"");original(c);
  check(e.state==CREATING_ROLLBACK,"failed checkpoint retained");check(new File(e.rollbackPath).isFile(),"new archive retained for recovery");
  check(!BackupOperationLock.isBusy(),"failed checkpoint transient owner released");AtomicFile.failState="";
  RestoreRecoveryGuard.beforeLauncherDatabaseInit(c);original(c);check(new RestoreOperationJournal(c).read().state==IDLE,"early recovery resets safely");
  check(!new File(e.rollbackPath).getParentFile().exists(),"early recovery removes only pending snapshot");

  c=fresh();e=prepare(c,"");original(c);check(e.state==WAITING_TRANSITION,"prepared handoff checkpoint");
  check(!new File(e.rollbackPath).equals(DesktopRestoreController.rollbackArchive(c)),"pending archive isolated from old undo");
  BackupOperationLock.release(e.operationToken);check(!BackupOperationLock.isBusy(),"fixture handoff releases owner");new RestoreOperationJournal(c).write(e,COMMITTED,null);
  finish(c,e);check(new RestoreOperationJournal(c).read().state==IDLE,"successful cleanup idle");
  check(content(DesktopRestoreController.rollbackArchive(c)).equals("\\u0001"),"committed restore publishes new undo");
  check(!new File(e.rollbackPath).getParentFile().exists(),"published pending snapshot cleaned");

  c=fresh();e=prepare(c,"");BackupOperationLock.release(e.operationToken);new RestoreOperationJournal(c).write(e,ROLLED_BACK,null);
  finish(c,e);original(c);check(!new File(e.rollbackPath).getParentFile().exists(),"failed restore keeps previous undo and removes pending snapshot");

  for(boolean missingSource:new boolean[]{false,true}){
   c=fresh();e=prepare(c,"");BackupOperationLock.release(e.operationToken);new RestoreOperationJournal(c).write(e,COMMITTED,null);
   Effects.scenario="publish";if(missingSource)new File(e.rollbackPath).delete();boolean failed=false;try{finish(c,e);}catch(IOException expected){failed=true;}
   check(failed,"publication failure is not success missingSource="+missingSource);original(c);check(new RestoreOperationJournal(c).read().state==COMMITTED,"publication failure retains committed checkpoint");
   check(new File(e.rollbackPath).isFile()!=missingSource,"publication failure preserves candidate state");Effects.scenario="";
   if(missingSource)write(new File(e.rollbackPath),"\\u0001");
   RestoreRecoveryGuard.beforeLauncherDatabaseInit(c);check(new RestoreOperationJournal(c).read().state==IDLE,"startup retries publication");
   check(content(DesktopRestoreController.rollbackArchive(c)).equals("\\u0001"),"startup publishes correct new undo");
  }

  c=fresh();e=prepare(c,"");BackupOperationLock.release(e.operationToken);new RestoreOperationJournal(c).write(e,COMMITTED,null);
  AtomicFile.failState="IDLE";boolean failed=false;try{finish(c,e);}catch(RestoreOperationJournal.JournalException expected){failed=true;}
  check(failed&&new RestoreOperationJournal(c).read().state==CLEANING,"reset failure keeps durable cleanup state");
  check(new File(e.rollbackPath).isFile(),"reset failure retains source");AtomicFile.failState="";
  RestoreRecoveryGuard.beforeLauncherDatabaseInit(c);check(new RestoreOperationJournal(c).read().state==IDLE,"startup completes interrupted cleanup");
  check(content(DesktopRestoreController.rollbackArchive(c)).equals("\\u0001"),"cleanup recovery preserves published undo");
  System.out.println("PASS UNDO_PRESERVATION checks="+checks+" cases="+cases);
 }
}'''


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jdk',type=Path,required=True)
    p.add_argument('--before',type=Path,help='Directory containing saved pre-fix controller/guard sources')
    args=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='undo-preservation-') as temporary:
        base=Path(temporary);files=[]
        for name,source in SOURCES.items():
            path=base/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(source,encoding='utf-8');files.append(str(path))
        for name in ['RestoreOperationJournal','DesktopRestoreController','RestoreRecoveryGuard','BackupOperationLock','BackupFileUtils','BackupRestoreResult']:
            path=ROOT/'launcher/tools/java'/B/(name+'.java')
            if args.before and name in ['DesktopRestoreController','RestoreRecoveryGuard','BackupOperationLock']:
                path=base/B/(name+'.java');path.write_bytes((args.before/(name+'.before.java')).read_bytes())
            files.append(str(path))
        subprocess.run([str(args.jdk/'bin/javac.exe'),'-encoding','UTF-8','-d',str(base),*files],check=True)
        subprocess.run([str(args.jdk/'bin/java.exe'),'-cp',str(base),'com.smartisanos.launcher.backup.UndoPreservationTest',str(base/'data')],check=True)


if __name__=='__main__':main()
