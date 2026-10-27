"""Exercise actual SAF write/verify/prepared-copy/cleanup method bodies with provider fixtures.

Streams, file descriptors, journals, locks and staging files are real JVM IO.
Android provider/UI/archive-validation boundaries are controlled doubles; no user backup is accessed.
"""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT=Path(__file__).resolve().parents[3]
B='com/smartisanos/launcher/backup/'
spec=importlib.util.spec_from_file_location('journal_fixtures',Path(__file__).parent.parent/'restore_journal/run_tests.py')
fixtures=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixtures)


def block(source, marker):
    start=source.index(marker);end=source.index('{',start)+1;depth=1
    while depth:
        depth+=(source[end]=='{')-(source[end]=='}');end+=1
    return source[start:end]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jdk',type=Path,required=True)
    p.add_argument('--before',type=Path)
    args=p.parse_args()
    owner=ROOT/'launcher/tools/java'/B/'DesktopBackupController.java'
    src=(args.before/'DesktopBackupController.before.java' if args.before else owner).read_text(encoding='utf-8')
    markers=['public interface Listener {','public static final class CancellationToken {',
      'static final class BackupCancelledException','private static final class RunningOperation',
      'private static final class PreparedBackup','private static void copyPreparedArchive(',
      'private static void preparePreview(', 'private static void execute(',
      'private static Uri writeToTree(','private static void copyToUriAndVerify(',
      ('private static boolean cleanupInterruptedBackupNow(' if 'private static boolean cleanupInterruptedBackupNow(' in src else 'private static void cleanupInterruptedBackupNow('),'private static void state(',
      'private static void deleteDocumentQuietly(','private static String userMessage(',
      'private static CodedIOException coded(','private static boolean isNoSpace(',
      'private static final class CodedIOException','private static final class StateCallback',
      'private static void notifyComplete(','private static void complete(']
    if 'private static void requireExportCheckpoint(' in src:markers.append('private static void requireExportCheckpoint(')
    if 'private static Uri findTreeBackupChecked(' in src:markers.append('private static Uri findTreeBackupChecked(')
    for extra in ['private static boolean deletePendingDocument(', 'private static boolean clearInterruptedBackupBeforeStart(', 'private static void completeBackup(', 'private static boolean publishCompletedBackupMetadata(', 'private static boolean hasDirectoryPermissionFailure(']:
        if extra in src:markers.append(extra)
    methods='\n'.join(block(src,m) for m in markers)
    sources={k:v for k,v in fixtures.SOURCES.items() if k.startswith('org/json/') or k in ['android/util/AtomicFile.java','android/os/Handler.java','android/os/Looper.java','android/util/Log.java']}
    atomic=sources['android/util/AtomicFile.java']
    atomic=atomic.replace('public static boolean failStart', 'public static String silentState="",readFailureState="",mismatchState="";public static boolean failCleanup;public static boolean failStart')
    atomic=atomic.replace('public void finishWrite(FileOutputStream s){try{s.close();if(!silentFinish)Files.move(new File(base+".new").toPath(),base.toPath(),StandardCopyOption.REPLACE_EXISTING);}', 'public void finishWrite(FileOutputStream s){try{s.close();File candidate=new File(base+".new");String state=new JSONObject(new String(Files.readAllBytes(candidate.toPath()),java.nio.charset.StandardCharsets.UTF_8)).getString("state");if(!silentFinish&&!state.equals(silentState))Files.move(candidate.toPath(),base.toPath(),StandardCopyOption.REPLACE_EXISTING);if(state.equals(mismatchState))Files.write(base.toPath(),new byte[]{32},StandardOpenOption.APPEND);if(state.equals(readFailureState))failRead=true;}')
    atomic=atomic.replace('public void failWrite(FileOutputStream s){', 'public void failWrite(FileOutputStream s){if(failCleanup)throw new IllegalStateException("injected cleanup");')
    sources['android/util/AtomicFile.java']=atomic
    sources['android/util/Log.java']=sources['android/util/Log.java'].replace('public class Log {','public class Log {public static int w(String t,String s){return 0;}')
    sources['android/database/Cursor.java']='''package android.database;public interface Cursor{boolean moveToNext();String getString(int i);void close();}'''
    sources['android/content/SharedPreferences.java']='''package android.content;public interface SharedPreferences{Editor edit();interface Editor{Editor putString(String k,String v);Editor putLong(String k,long v);Editor putBoolean(String k,boolean v);boolean commit();}}'''
    sources['android/content/Context.java']='''package android.content;import java.io.*;import java.util.*;public class Context{
 public static final int MODE_PRIVATE=0;public final File root;public final Prefs prefs=new Prefs();public Context(File r){root=r;r.mkdirs();}
 public File getFilesDir(){File f=new File(root,"files");f.mkdirs();return f;}public File getCacheDir(){File f=new File(root,"cache");f.mkdirs();return f;}
 public ContentResolver getContentResolver(){return new ContentResolver(this);}public SharedPreferences getSharedPreferences(String n,int m){return prefs;}public static class Prefs implements SharedPreferences,SharedPreferences.Editor{
 public final Map<String,Object> values=new HashMap<>();public boolean fail;public Editor edit(){return this;}
 public Editor putString(String k,String v){values.put(k,v);return this;}public Editor putLong(String k,long v){values.put(k,v);return this;}
 public Editor putBoolean(String k,boolean v){values.put(k,v);return this;}public boolean commit(){return !fail;}}}'''
    sources['android/net/Uri.java']='''package android.net;public class Uri{final String s;private Uri(String s){this.s=s;}public static Uri parse(String s){return new Uri(s);}public String toString(){return s;}public boolean equals(Object o){return o instanceof Uri&&s.equals(o.toString());}public int hashCode(){return s.hashCode();}}'''
    sources['android/os/ParcelFileDescriptor.java']='''package android.os;import java.io.*;public class ParcelFileDescriptor implements Closeable{
 final FileOutputStream out;public ParcelFileDescriptor(File f)throws Exception{out=new FileOutputStream(f);}public FileDescriptor getFileDescriptor()throws IOException{return out.getFD();}public void close()throws IOException{out.close();}}'''
    sources['android/content/ContentResolver.java']='''package android.content;import android.net.*;import android.os.*;import java.io.*;import com.smartisanos.launcher.backup.FakeDocuments;
public class ContentResolver{public final Context context;public ContentResolver(Context c){context=c;}
public ParcelFileDescriptor openFileDescriptor(Uri u,String m)throws Exception{return FakeDocuments.open(u);}
public InputStream openInputStream(Uri u)throws Exception{return FakeDocuments.read(u);}
public android.database.Cursor query(Uri u,String[] columns,String selection,String[] args,String order)throws Exception{
 if(FakeDocuments.revoked)throw new SecurityException("fixture grant revoked");
 if(FakeDocuments.scenario.equals("permission-query"))throw new SecurityException("fixture tree access revoked");
 if(FakeDocuments.scenario.equals("list-null")||(u.toString().startsWith("doc://")&&FakeDocuments.scenario.equals("fallback-delete-query-null")))return null;if(FakeDocuments.scenario.equals("list-throw")||(u.toString().startsWith("doc://")&&FakeDocuments.scenario.equals("fallback-delete-query-throw")))throw new IOException("directory unavailable");
 java.util.Map<Uri,String> visible=new java.util.HashMap<>(FakeDocuments.names);
 if(u.toString().startsWith("doc://"))visible.keySet().retainAll(java.util.Collections.singleton(u));
 final java.util.Iterator<java.util.Map.Entry<Uri,String>> iterator=visible.entrySet().iterator();
 return new android.database.Cursor(){java.util.Map.Entry<Uri,String> row;public boolean moveToNext(){if(!iterator.hasNext())return false;row=iterator.next();return true;}
 public String getString(int i){return i==0?row.getKey().toString():row.getValue();}public void close(){FakeDocuments.closed++;}};
}}'''
    sources['android/provider/DocumentsContract.java']='''package android.provider;import android.content.*;import android.net.*;import com.smartisanos.launcher.backup.FakeDocuments;
public class DocumentsContract{public static String getTreeDocumentId(Uri u){return "tree";}public static Uri buildDocumentUriUsingTree(Uri t,String i){return i.startsWith("doc://")?Uri.parse(i):t;}
public static Uri buildChildDocumentsUriUsingTree(Uri t,String i){return t;}
public static class Document{public static final String COLUMN_DOCUMENT_ID="id",COLUMN_DISPLAY_NAME="name";}
public static Uri createDocument(ContentResolver r,Uri p,String mime,String n)throws Exception{return FakeDocuments.create(n);}
public static Uri renameDocument(ContentResolver r,Uri u,String n)throws Exception{return FakeDocuments.rename(u,n);}
public static boolean deleteDocument(ContentResolver r,Uri u){return FakeDocuments.delete(u);}}'''
    sources[B+'BackupArchiveReader.java']='''package com.smartisanos.launcher.backup;public class BackupArchiveReader{public static ValidatedBackup read(java.io.File f,java.io.File d){return new ValidatedBackup();}public static class ValidatedBackup{public String sourceName;public int itemCount(){return 1;}}}'''
    sources[B+'RestoreMergePlanner.java']='''package com.smartisanos.launcher.backup;public class RestoreMergePlanner{public static class Plan{}public static Plan plan(android.content.Context c,BackupArchiveReader.ValidatedBackup b){return new Plan();}}'''
    sources[B+'BackupValidator.java']='''package com.smartisanos.launcher.backup;import java.io.*;import java.nio.file.*;import java.util.*;
public class BackupValidator{public static final long MAX_ARCHIVE_BYTES=1048576;
public static void validateAndExtract(File f,File d)throws Exception{if(!Arrays.equals(Files.readAllBytes(f.toPath()),FakeDocuments.PAYLOAD))throw new IOException("fixture archive checksum mismatch");d.mkdirs();}}'''
    sources[B+'FakeDocuments.java']='''package com.smartisanos.launcher.backup;import android.net.*;import android.os.*;import java.io.*;import java.nio.file.*;import java.util.*;
public class FakeDocuments{
 public static final byte[] PAYLOAD="fixture-archive-with-checksums".getBytes(java.nio.charset.StandardCharsets.UTF_8);
 public static File root;public static String scenario;public static int ids,closed;public static Uri deniedUri;public static boolean fallback,revoked;
 public static DesktopBackupController.CancellationToken cancel;public static final Map<Uri,File> files=new HashMap<>();public static final Map<Uri,String> names=new HashMap<>();
 public static void reset(File r,String s){root=r;root.mkdirs();scenario=s;ids=0;closed=0;deniedUri=null;revoked=false;fallback=s.startsWith("final-")||s.startsWith("fallback");files.clear();names.clear();}
 public static Uri create(String n)throws Exception{if(scenario.equals("permission-create")||(!n.endsWith(".partial")&&scenario.equals("final-permission-create")))throw new SecurityException("fixture create denied");if(scenario.equals("create-null"))return null;Uri u=Uri.parse("doc://"+(++ids));File f=new File(root,"doc"+ids);Files.write(f.toPath(),new byte[0]);files.put(u,f);names.put(u,n);return u;}
 public static Uri find(String n){for(Map.Entry<Uri,String> e:names.entrySet())if(e.getValue().equals(n))return e.getKey();return null;}
 public static boolean delete(Uri u){if(revoked)throw new SecurityException("fixture cleanup access revoked");
 if(names.get(u)!=null&&names.get(u).endsWith(".partial")){
  if(scenario.equals("fallback-delete-throw"))throw new SecurityException("partial delete denied");
  if(scenario.equals("fallback-delete-denied")||scenario.startsWith("fallback-delete-query-"))return false;
 }
if(scenario.equals("delete-denied")||scenario.equals("fallback-delete-all-denied")||u.equals(deniedUri))return false;if(scenario.equals("delete-throw"))throw new SecurityException("fixture denial");File f=files.get(u);if(f==null||!f.delete())return false;files.remove(u);names.remove(u);if(scenario.equals("fallback-cleanup-checkpoint"))android.util.AtomicFile.failState="COPYING_TO_DESTINATION";return !scenario.equals("fallback-delete-false-absent");}
 public static Uri rename(Uri u,String n)throws Exception{if(scenario.equals("permission-rename"))throw new SecurityException("fixture rename denied");if(scenario.equals("permission-wrapped"))throw new IOException("wrapped provider denial",new SecurityException("fixture grant"));if(fallback){if(scenario.equals("fallback-throw"))throw new IOException("rename unsupported");return null;}
  File f=files.remove(u);names.remove(u);Uri v=scenario.equals("rename-same")?u:Uri.parse("doc://renamed"+(++ids));files.put(v,f);names.put(v,n);if(scenario.equals("rename-checkpoint"))android.util.AtomicFile.failState="COPYING_TO_DESTINATION";return v;}
 public static ParcelFileDescriptor open(Uri u)throws Exception{boolean temp=names.get(u).endsWith(".partial");if((temp&&scenario.equals("permission-open"))||(!temp&&scenario.equals("final-permission-open")))throw new SecurityException("fixture open denied");
  if((temp&&scenario.equals("cancel"))||(!temp&&scenario.equals("final-cancel")))cancel.cancel();
  if((temp&&scenario.equals("write"))||(!temp&&scenario.equals("final-write")))throw new IOException("provider write failed");
  if(scenario.equals("open-null"))return null;return new ParcelFileDescriptor(files.get(u));}
 public static InputStream read(Uri u)throws Exception{boolean temp=names.get(u).endsWith(".partial");if(scenario.equals("permission-revoked")){revoked=true;throw new SecurityException("fixture access revoked during copy");}if((temp&&scenario.equals("permission-read"))||(!temp&&scenario.equals("final-permission-read")))throw new SecurityException("fixture read denied");if(scenario.equals("plain-io"))throw new IOException("fixture provider IO failure");
  if((temp&&scenario.equals("read"))||(!temp&&scenario.equals("final-read")))throw new IOException("read permission lost");
  byte[] b=Files.readAllBytes(files.get(u).toPath());if(scenario.equals("length"))b=Arrays.copyOf(b,b.length-1);if(scenario.equals("checksum"))b[0]^=1;
  return new ByteArrayInputStream(b);}
}'''
    java='''package com.smartisanos.launcher.backup;
import android.database.*;import android.content.*;import android.net.*;import android.os.*;import android.provider.*;import android.util.*;
import java.io.*;import java.util.*;import java.text.SimpleDateFormat;
public final class DesktopBackupController{
 static final String PREFS="backup",TAG="test",KEY_LAST_BACKUP_TIME="last-time",KEY_LAST_BACKUP_FILE_NAME="last-name",KEY_LAST_BACKUP_DOCUMENT_URI="last-uri";
 static final long EXTERNAL_COPY_LIMIT=BackupValidator.MAX_ARCHIVE_BYTES;static final Handler MAIN=new Handler(Looper.getMainLooper());
 static RunningOperation running;static PreparedBackup preparedBackup;static int previews;
 static boolean hasPersistedTreePermission(Context c,Uri u){return true;}static String suggestedBackupName(){return "fixture";}static String safeToken(String t){return t;}
 static class JSONObjectHolder{int itemCount=1;}
 static JSONObjectHolder createCurrentArchive(Context c,File stage,RunningOperation op,BackupOperationJournal journal,BackupOperationJournal.Entry e)throws Exception{if(FakeDocuments.scenario.equals("local-security"))throw new SecurityException("fixture local snapshot denied");java.nio.file.Files.write(new File(stage,"archive.slauncherbackup").toPath(),FakeDocuments.PAYLOAD);return new JSONObjectHolder();}
 static void notifyPreview(RunningOperation op,BackupArchiveReader.ValidatedBackup b,RestoreMergePlanner.Plan plan,String name){previews++;}
 static Uri findTreeBackup(Context c,Uri tree,String n){return FakeDocuments.find(n);}
 METHODS
 public static class Probe{
  static int checks,cases;static File root;static BackupRestoreResult result;static boolean overwrite,direct;
  static void check(boolean b,String label){checks++;if(!b)throw new AssertionError(label+" scenario="+FakeDocuments.scenario+" documents="+FakeDocuments.names);}
  static Context context(String scenario)throws Exception{Context c=new Context(new File(root,"case"+(cases++)));FakeDocuments.reset(new File(c.root,"documents"),scenario);return c;}
  static void execute(Context c,String scenario)throws Exception{
   String token="saf-test";check(BackupOperationLock.acquire(token),"operation owner acquired");
   File stage=direct?new File(new File(c.getCacheDir(),"backup_staging"),token):new File(c.getCacheDir(),"staging");stage.mkdirs();File archive=new File(stage,"archive.slauncherbackup");java.nio.file.Files.write(archive.toPath(),FakeDocuments.PAYLOAD);
   BackupOperationJournal.Entry e=new BackupOperationJournal.Entry();e.token=token;e.stagingPath=stage.getAbsolutePath();new BackupOperationJournal(c).write(e,BackupOperationJournal.State.PREVIEW_READY,null);
   RunningOperation operation=new RunningOperation(token,new Listener(){public void onState(String s,boolean x){}public void onComplete(BackupRestoreResult r){result=r;}});
   FakeDocuments.cancel=operation.cancellation;running=operation;
   PreparedBackup prepared=new PreparedBackup(token,c,stage,archive,Uri.parse("tree://fixture"),new BackupArchiveReader.ValidatedBackup());preparedBackup=direct?null:prepared;
   c.prefs.fail=scenario.endsWith("prefs");if(scenario.equals("checkpoint"))AtomicFile.failState="COPYING_TO_DESTINATION";if(scenario.equals("complete"))AtomicFile.failState="COMPLETE";
   if(scenario.equals("save-read-fail"))AtomicFile.failRead=true;
   if(scenario.equals("complete-silent"))AtomicFile.silentState="COMPLETE";
   if(scenario.equals("complete-readback"))AtomicFile.readFailureState="COMPLETE";
   if(scenario.equals("complete-sync"))AtomicFile.failSyncState="COMPLETE";
   result=null;if(direct)DesktopBackupController.execute(c,Uri.parse("tree://fixture"),"backup.slauncherbackup",overwrite,operation);else copyPreparedArchive(prepared,"backup.slauncherbackup",overwrite,operation);AtomicFile.failState="";AtomicFile.failRead=false;AtomicFile.silentState="";AtomicFile.readFailureState="";AtomicFile.failSyncState="";
   check(!BackupOperationLock.isBusy()&&running==null&&preparedBackup==null,"finished attempt releases operation and preview");check(!stage.exists(),"staging cleaned");check(result!=null,"completion delivered");
  }
  public static void main(String[] args)throws Exception{root=new File(args[0]);
   for(boolean directPath:new boolean[]{false,true})for(String mode:new String[]{"permission-query","permission-create","permission-open","permission-read","permission-rename","permission-wrapped","final-permission-create","final-permission-open","final-permission-read"}){
    Context c2=context(mode);direct=directPath;execute(c2,mode);direct=false;
    check(!result.success&&"BACKUP_LOCATION_PERMISSION_LOST".equals(result.errorCode),"SAF permission denial must report lost directory access");check(FakeDocuments.files.isEmpty()&&!c2.prefs.values.containsKey(KEY_LAST_BACKUP_DOCUMENT_URI),"denied export cleans candidate and does not publish metadata");
    if(mode.equals("permission-query")||mode.equals("permission-create"))check(FakeDocuments.ids==0,"denied listing or creation does not allocate documents");
    if(mode.equals("permission-rename")||mode.equals("permission-wrapped"))check(FakeDocuments.ids==1,"rename permission denial cannot start fallback creation");
   }
   for(boolean directPath:new boolean[]{false,true}){
    Context c2=context("permission-revoked");Uri previous=FakeDocuments.create("previous.backup");byte[] old="previous-good".getBytes(java.nio.charset.StandardCharsets.UTF_8);java.nio.file.Files.write(FakeDocuments.files.get(previous).toPath(),old);c2.prefs.values.put(KEY_LAST_BACKUP_DOCUMENT_URI,previous.toString());
    direct=directPath;execute(c2,"permission-revoked");direct=false;BackupOperationJournal j=new BackupOperationJournal(c2);String pending=j.read().partialUri;
    check(!result.success&&"BACKUP_LOCATION_PERMISSION_LOST".equals(result.errorCode)&&FakeDocuments.files.size()==2,"revoked grant preserves unremovable candidate and reports permission loss");
    cleanupInterruptedBackupNow(c2);check(j.read().state!=BackupOperationJournal.State.IDLE&&j.read().partialUri.equals(pending),"revoked cleanup preserves original recovery URI");
    FakeDocuments.revoked=false;FakeDocuments.scenario="retry";cleanupInterruptedBackupNow(c2);check(j.read().state==BackupOperationJournal.State.IDLE&&FakeDocuments.files.size()==1&&Arrays.equals(old,java.nio.file.Files.readAllBytes(FakeDocuments.files.get(previous).toPath()))&&c2.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI).equals(previous.toString()),"restored access clears only failed candidate and preserves previous backup metadata");
   }
   for(boolean directPath:new boolean[]{false,true}){
    Context c2=context("plain-io");direct=directPath;execute(c2,"plain-io");direct=false;check(!result.success&&(directPath?"BACKUP_EXPORT_FAILED":"BACKUP_COPY_FAILED").equals(result.errorCode),"plain IO failure is not labeled permission loss");
   }
   {Context c2=context("local-security");direct=true;execute(c2,"local-security");direct=false;check(!result.success&&"BACKUP_EXPORT_FAILED".equals(result.errorCode)&&FakeDocuments.ids==0,"local snapshot SecurityException is not labeled directory permission loss");}
   {Context c2=context("complete");c2.prefs.values.put(KEY_LAST_BACKUP_TIME,Long.valueOf(123));c2.prefs.values.put(KEY_LAST_BACKUP_FILE_NAME,"previous.slauncherbackup");c2.prefs.values.put(KEY_LAST_BACKUP_DOCUMENT_URI,"doc://previous");execute(c2,"complete");
    check(c2.prefs.values.get(KEY_LAST_BACKUP_TIME).equals(Long.valueOf(123))&&c2.prefs.values.get(KEY_LAST_BACKUP_FILE_NAME).equals("previous.slauncherbackup")&&c2.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI).equals("doc://previous"),"failed completion must preserve previous backup metadata");}
   for(boolean directPath:new boolean[]{false,true})for(String mode:new String[]{"complete","complete-silent","complete-sync","complete-readback","prefs","final-prefs","success"}){
    Context c2=context(mode);Uri old=FakeDocuments.create("previous.slauncherbackup");byte[] oldBytes="previous-good-backup".getBytes(java.nio.charset.StandardCharsets.UTF_8);java.nio.file.Files.write(FakeDocuments.files.get(old).toPath(),oldBytes);
    c2.prefs.values.put(KEY_LAST_BACKUP_TIME,Long.valueOf(123));c2.prefs.values.put(KEY_LAST_BACKUP_FILE_NAME,"previous.slauncherbackup");c2.prefs.values.put(KEY_LAST_BACKUP_DOCUMENT_URI,old.toString());
    direct=directPath;execute(c2,mode);direct=false;BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=j.read();
    if(mode.startsWith("complete")){
     check(!result.success&&c2.prefs.values.get(KEY_LAST_BACKUP_TIME).equals(Long.valueOf(123))&&c2.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI).equals(old.toString())&&c2.prefs.values.get(KEY_LAST_BACKUP_FILE_NAME).equals("previous.slauncherbackup"),"both save paths keep previous metadata until confirmed COMPLETE");
     check(FakeDocuments.files.size()==2&&FakeDocuments.files.containsKey(Uri.parse(e2.partialUri)),"completion attempt retains owned candidate and previous good archive");
     cleanupInterruptedBackupNow(c2);
     if(mode.equals("complete-readback")){
      check(j.read().state==BackupOperationJournal.State.COMPLETE&&FakeDocuments.files.size()==2,"physically published COMPLETE survives failed readback recovery");
      check(c2.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI).equals(e2.partialUri)&&c2.prefs.values.get(KEY_LAST_BACKUP_TIME).equals(Long.valueOf(e2.updatedAt)),"recovery publishes actual committed URI and stable completion time");
     }else check(j.read().state==BackupOperationJournal.State.IDLE&&FakeDocuments.files.size()==1&&c2.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI).equals(old.toString()),"uncommitted completion recovery removes only candidate and retains old metadata");
    }else if(mode.endsWith("prefs")){
     check(!result.success&&"BACKUP_METADATA_PENDING".equals(result.errorCode)&&e2.state==BackupOperationJournal.State.COMPLETE,"metadata failure reports saved file with pending record");
     check(FakeDocuments.files.size()==2&&FakeDocuments.files.containsKey(Uri.parse((String)c2.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI))),"metadata commit false never leaves dangling URI");
     RunningOperation blocked=new RunningOperation("new-metadata",new Listener(){public void onState(String x,boolean y){}public void onComplete(BackupRestoreResult r){result=r;}});check(BackupOperationLock.acquire(blocked.token),"metadata retry owns transient gate");running=blocked;
     boolean start=(Boolean)DesktopBackupController.class.getDeclaredMethod("clearInterruptedBackupBeforeStart",Context.class,RunningOperation.class).invoke(null,c2,blocked);
     check(!start&&running==null&&!BackupOperationLock.isBusy()&&"BACKUP_METADATA_PENDING".equals(result.errorCode)&&j.read().token.equals(e2.token),"pending metadata blocks new journal without leaking transient owner");
     c2.prefs.fail=false;cleanupInterruptedBackupNow(c2);c2.prefs.values.put(KEY_LAST_BACKUP_TIME,Long.valueOf(0));cleanupInterruptedBackupNow(c2);
     check(FakeDocuments.files.size()==2&&j.read().state==BackupOperationJournal.State.COMPLETE&&c2.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI).equals(e2.partialUri)&&c2.prefs.values.get(KEY_LAST_BACKUP_TIME).equals(Long.valueOf(e2.updatedAt)),"metadata retry is idempotent and preserves committed file and timestamp");
    }else{
     check(result.success&&e2.state==BackupOperationJournal.State.COMPLETE&&FakeDocuments.files.size()==2,"both save paths complete normally");
     check(c2.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI).equals(e2.partialUri)&&c2.prefs.values.get(KEY_LAST_BACKUP_TIME).equals(Long.valueOf(e2.updatedAt))&&c2.prefs.values.get(KEY_LAST_BACKUP_FILE_NAME).equals("backup.slauncherbackup")&&Boolean.FALSE.equals(c2.prefs.values.get("last_backup_incomplete")),"published metadata uses confirmed checkpoint and actual URI");
    }
    check(FakeDocuments.files.containsKey(old)&&Arrays.equals(oldBytes,java.nio.file.Files.readAllBytes(FakeDocuments.files.get(old).toPath())),"previous backup bytes survive publication and recovery");
   }
   {Context c2=context("complete-before-prefs");Uri output=FakeDocuments.create("confirmed.slauncherbackup");java.nio.file.Files.write(FakeDocuments.files.get(output).toPath(),FakeDocuments.PAYLOAD);BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry committed=new BackupOperationJournal.Entry();committed.token="committed-owner";committed.partialUri=output.toString();BackupOperationJournal.Entry.class.getField("completedFileName").set(committed,"confirmed.slauncherbackup");
    check(j.write(committed,BackupOperationJournal.State.COMPLETE,null),"committed journal contains recovery metadata before preference publication");Context reconstructed=new Context(c2.root);cleanupInterruptedBackupNow(reconstructed);
    check(reconstructed.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI).equals(output.toString())&&reconstructed.prefs.values.get(KEY_LAST_BACKUP_FILE_NAME).equals("confirmed.slauncherbackup")&&reconstructed.prefs.values.get(KEY_LAST_BACKUP_TIME).equals(Long.valueOf(committed.updatedAt)),"fresh context reconstructs last backup metadata from saved journal");check(FakeDocuments.files.containsKey(output)&&j.read().state==BackupOperationJournal.State.COMPLETE,"metadata reconstruction preserves completed archive and checkpoint");}
   {Context c2=context("legacy-complete");BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.partialUri=FakeDocuments.create("legacy.backup").toString();e2.state=BackupOperationJournal.State.COMPLETE;String q=String.valueOf((char)34);String legacy=e2.toJson().toString().replace(","+q+"completedFileName"+q+":"+q+q,"");
    java.nio.file.Files.write(new File(c2.getFilesDir(),"backup_restore/backup_operation_journal.json").toPath(),legacy.getBytes(java.nio.charset.StandardCharsets.UTF_8));cleanupInterruptedBackupNow(c2);check(j.read().state==BackupOperationJournal.State.COMPLETE&&FakeDocuments.files.size()==1&&c2.prefs.values.isEmpty(),"legacy COMPLETE without candidate metadata stays valid and does not guess a name");}
   for(String failure:new String[]{"silent-finish","sync-failed"}){
    Context c2=context(failure);BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.token="durable-owner";
    check(j.write(e2,BackupOperationJournal.State.PREVIEW_READY,null),"baseline checkpoint written");File f=new File(c2.getFilesDir(),"backup_restore/backup_operation_journal.json");byte[] before=java.nio.file.Files.readAllBytes(f.toPath());
    long started=e2.startedAt,updated=e2.updatedAt;String code=e2.errorCode;
    AtomicFile.silentFinish=failure.equals("silent-finish");if(failure.equals("sync-failed"))AtomicFile.failSyncState="COPYING_TO_DESTINATION";
    boolean saved=j.write(e2,BackupOperationJournal.State.COPYING_TO_DESTINATION,"candidate-code");AtomicFile.silentFinish=false;AtomicFile.failSyncState="";
    check(!saved,"unpublished or unsynced checkpoint must not report success");check(Arrays.equals(before,java.nio.file.Files.readAllBytes(f.toPath())),"write failure keeps previous checkpoint bytes");
    check(e2.state==BackupOperationJournal.State.PREVIEW_READY&&e2.startedAt==started&&e2.updatedAt==updated&&e2.errorCode.equals(code),"failed write does not publish candidate into live entry");
    check(j.write(e2,BackupOperationJournal.State.COPYING_TO_DESTINATION,null)&&j.read().state==BackupOperationJournal.State.COPYING_TO_DESTINATION,"retry publishes confirmed checkpoint");
   }
   for(String mode:new String[]{"readback-io","readback-mismatch","fail-cleanup"}){
    Context c2=context(mode);BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.token="verify-owner";check(j.write(e2,BackupOperationJournal.State.PREVIEW_READY,null),"readback baseline checkpoint");long before=e2.updatedAt;
    if(mode.equals("readback-io"))AtomicFile.readFailureState="COPYING_TO_DESTINATION";
    if(mode.equals("readback-mismatch"))AtomicFile.mismatchState="COPYING_TO_DESTINATION";
    if(mode.equals("fail-cleanup")){AtomicFile.failState="COPYING_TO_DESTINATION";AtomicFile.failCleanup=true;}
    check(!j.write(e2,BackupOperationJournal.State.COPYING_TO_DESTINATION,null),"failed checkpoint verification or rollback reports false");
    check(e2.state==BackupOperationJournal.State.PREVIEW_READY&&e2.updatedAt==before,"post-finish failure leaves live entry unchanged");
    AtomicFile.failRead=false;AtomicFile.readFailureState="";AtomicFile.mismatchState="";AtomicFile.failState="";AtomicFile.failCleanup=false;
    check(j.write(e2,BackupOperationJournal.State.COPYING_TO_DESTINATION,null)&&j.read().state==BackupOperationJournal.State.COPYING_TO_DESTINATION,"readback or rollback failure permits later confirmed retry");
   }
   {Context c2=context("oversized-candidate");BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.token="bounded";check(j.write(e2,BackupOperationJournal.State.PREVIEW_READY,null),"bounded baseline checkpoint");
    File f=new File(c2.getFilesDir(),"backup_restore/backup_operation_journal.json");byte[] before=java.nio.file.Files.readAllBytes(f.toPath());char[] large=new char[128*1024];Arrays.fill(large,'x');e2.partialUri=new String(large);
    check(!j.write(e2,BackupOperationJournal.State.COPYING_TO_DESTINATION,null),"oversized candidate refused before replacing readable journal");check(Arrays.equals(before,java.nio.file.Files.readAllBytes(f.toPath()))&&j.read().state==BackupOperationJournal.State.PREVIEW_READY,"oversized candidate preserves old readable bytes");}
   {Context c2=context("complete-silent");execute(c2,"complete-silent");check(!result.success&&FakeDocuments.files.size()==1,"silent COMPLETE failure retains owned candidate until recovery");check(new BackupOperationJournal(c2).read().state==BackupOperationJournal.State.COPYING_TO_DESTINATION,"silent COMPLETE failure does not overwrite journal authority");cleanupInterruptedBackupNow(c2);check(FakeDocuments.files.isEmpty(),"uncommitted silent completion output removed by recovery");}
   {Context c2=context("reset-silent");BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.token="reset-owner";e2.partialUri=FakeDocuments.create("pending.partial").toString();j.write(e2,BackupOperationJournal.State.COPYING_TO_DESTINATION,null);
    RunningOperation op=new RunningOperation("new-reset",new Listener(){public void onState(String s,boolean b){}public void onComplete(BackupRestoreResult r){result=r;}});check(BackupOperationLock.acquire(op.token),"silent reset test owns transient gate");running=op;AtomicFile.silentState="IDLE";
    boolean start=(Boolean)DesktopBackupController.class.getDeclaredMethod("clearInterruptedBackupBeforeStart",Context.class,RunningOperation.class).invoke(null,c2,op);AtomicFile.silentState="";
    check(!start&&running==null&&!BackupOperationLock.isBusy(),"silent reset failure blocks new operation and releases transient gate");check(j.read().state==BackupOperationJournal.State.COPYING_TO_DESTINATION,"silent reset keeps old pending checkpoint");cleanupInterruptedBackupNow(c2);check(j.read().state==BackupOperationJournal.State.IDLE,"silent reset failure retries using confirmed absent document");}
   {Context c2=context("first-write-silent");BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.token="first-owner";AtomicFile.silentState="VALIDATING_LOCATION";
    check(!j.write(e2,BackupOperationJournal.State.VALIDATING_LOCATION,null),"silent first publication cannot report success");AtomicFile.silentState="";
    check(e2.state==BackupOperationJournal.State.IDLE&&e2.startedAt==0&&e2.updatedAt==0,"failed first write preserves initial live entry");
    File sidecar=new File(c2.getFilesDir(),"backup_restore/backup_operation_journal.json.new");check(sidecar.isFile(),"unpublished first checkpoint retained as evidence");boolean blocked=false;try{j.read();}catch(RuntimeException error){blocked=true;}
    check(blocked&&!j.write(new BackupOperationJournal.Entry(),BackupOperationJournal.State.IDLE,null),"unpublished first checkpoint blocks unsafe reset");}
   for(String bad:new String[]{"", "{", "{}", new org.json.JSONObject().put("state","IDLE").toString(), new org.json.JSONObject().put("token","x").put("state","BOGUS").put("stagingPath","").put("partialUri","").toString(), new BackupOperationJournal.Entry().toJson().put("partialUri","doc://pending").toString()}){
    Context c2=context("corrupt-journal");BackupOperationJournal j=new BackupOperationJournal(c2);
    File f=new File(c2.getFilesDir(),"backup_restore/backup_operation_journal.json");byte[] original=bad.getBytes(java.nio.charset.StandardCharsets.UTF_8);java.nio.file.Files.write(f.toPath(),original);
    boolean blocked=false;try{j.read();}catch(RuntimeException e){blocked=true;}
    check(blocked,"corrupt backup journal must not appear idle");
    check(!j.write(new BackupOperationJournal.Entry(),BackupOperationJournal.State.IDLE,null),"write refuses corrupt journal replacement");j.reset();
    check(Arrays.equals(java.nio.file.Files.readAllBytes(f.toPath()),original),"corrupt evidence survives write and reset");
    Uri untouched=FakeDocuments.create("untouched.backup");RunningOperation blockedOperation=new RunningOperation("blocked-corrupt",new Listener(){public void onState(String x,boolean y){}public void onComplete(BackupRestoreResult r){result=r;}});
    check(BackupOperationLock.acquire(blockedOperation.token),"corrupt test acquires transient gate");running=blockedOperation;result=null;
    boolean proceed=(Boolean)DesktopBackupController.class.getDeclaredMethod("clearInterruptedBackupBeforeStart",Context.class,RunningOperation.class).invoke(null,c2,blockedOperation);
    check(!proceed&&running==null&&!BackupOperationLock.isBusy(),"corrupt journal blocks backup and releases transient gate");
    check(result!=null&&"BACKUP_JOURNAL_CORRUPT".equals(result.errorCode),"corrupt journal failure reaches UI explicitly");
    check(FakeDocuments.files.containsKey(untouched)&&FakeDocuments.ids==1&&Arrays.equals(java.nio.file.Files.readAllBytes(f.toPath()),original),"corrupt gate does not delete documents or overwrite evidence");

   }
   {Context c2=context("read-failure");BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.token="old";j.write(e2,BackupOperationJournal.State.PREVIEW_READY,null);
    File f=new File(c2.getFilesDir(),"backup_restore/backup_operation_journal.json");byte[] original=java.nio.file.Files.readAllBytes(f.toPath());AtomicFile.failRead=true;
    boolean failed=false;try{j.read();}catch(RuntimeException error){failed="BACKUP_JOURNAL_READ_FAILED".equals(error.getClass().getField("errorCode").get(error));}
    check(failed,"existing unreadable journal not treated as absent");check(!j.write(new BackupOperationJournal.Entry(),BackupOperationJournal.State.IDLE,null),"read failure blocks replacement");j.reset();AtomicFile.failRead=false;
    check(Arrays.equals(original,java.nio.file.Files.readAllBytes(f.toPath()))&&j.read().state==BackupOperationJournal.State.PREVIEW_READY,"read failure preserves bytes and normal reads recover");}
   {Context c2=context("save-read-fail");execute(c2,"save-read-fail");check(result!=null&&"BACKUP_JOURNAL_READ_FAILED".equals(result.errorCode),"prepared save reports read failure even when error journaling also fails");
    check(FakeDocuments.files.isEmpty()&&new BackupOperationJournal(c2).read().state==BackupOperationJournal.State.PREVIEW_READY,"failed save does not create documents or replace unreadable prior checkpoint");}
   {Context c2=context("truly-missing");BackupOperationJournal j=new BackupOperationJournal(c2);check(j.read().state==BackupOperationJournal.State.IDLE,"readable directory without journal is idle");check(j.write(new BackupOperationJournal.Entry(),BackupOperationJournal.State.IDLE,null),"fresh journal remains writable");}
   {Context c2=context("new-sidecar");BackupOperationJournal j=new BackupOperationJournal(c2);File f=new File(c2.getFilesDir(),"backup_restore/backup_operation_journal.json.new");byte[] bytes="interrupted-write".getBytes(java.nio.charset.StandardCharsets.UTF_8);java.nio.file.Files.write(f.toPath(),bytes);
    boolean blocked=false;try{j.read();}catch(RuntimeException error){blocked="BACKUP_JOURNAL_READ_FAILED".equals(error.getClass().getField("errorCode").get(error));}
    check(blocked&&!j.write(new BackupOperationJournal.Entry(),BackupOperationJournal.State.IDLE,null),"orphan new sidecar cannot be treated as fresh journal");check(Arrays.equals(bytes,java.nio.file.Files.readAllBytes(f.toPath())),"orphan sidecar preserved");}
   {Context c2=context("backup-sidecar");BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.token="recovered";e2.state=BackupOperationJournal.State.PREVIEW_READY;File f=new File(c2.getFilesDir(),"backup_restore/backup_operation_journal.json.bak");java.nio.file.Files.write(f.toPath(),e2.toJson().toString().getBytes(java.nio.charset.StandardCharsets.UTF_8));check(j.read().token.equals("recovered")&&j.read().state==BackupOperationJournal.State.PREVIEW_READY,"AtomicFile backup sidecar recovery remains supported");}
   {Context c2=context("oversized");BackupOperationJournal j=new BackupOperationJournal(c2);File f=new File(c2.getFilesDir(),"backup_restore/backup_operation_journal.json");byte[] bytes=new byte[128*1024+1];Arrays.fill(bytes,(byte)'x');java.nio.file.Files.write(f.toPath(),bytes);boolean blocked=false;try{j.read();}catch(RuntimeException error){blocked=true;}check(blocked&&!j.write(new BackupOperationJournal.Entry(),BackupOperationJournal.State.IDLE,null),"oversized journal blocks read and overwrite");check(f.length()==bytes.length,"oversized evidence retained");}
   for(String failState:new String[]{"VALIDATING_LOCATION","PREVIEW_READY","silent-preview",""}){
    Context c2=context("preview-checkpoint");RunningOperation op=new RunningOperation("preview-token",new Listener(){public void onState(String s,boolean b){}public void onComplete(BackupRestoreResult r){result=r;}});check(BackupOperationLock.acquire(op.token),"preview owns operation gate");running=op;preparedBackup=null;previews=0;result=null;
    if(failState.equals("silent-preview"))AtomicFile.silentState="PREVIEW_READY";
    AtomicFile.failState=failState;preparePreview(c2,Uri.parse("tree://fixture"),op);AtomicFile.failState="";AtomicFile.silentState="";
    if(failState.isEmpty()){
     check(previews==1&&preparedBackup!=null&&BackupOperationLock.isBusy(),"durable preview is published and keeps owner for confirmation");check(new BackupOperationJournal(c2).read().state==BackupOperationJournal.State.PREVIEW_READY,"successful preview checkpoint retained");
     BackupFileUtils.deleteRecursively(preparedBackup.staging);preparedBackup=null;running=null;BackupOperationLock.release(op.token);
    }else{
     check(previews==0&&preparedBackup==null&&running==null&&!BackupOperationLock.isBusy(),"failed preview checkpoint cannot publish preview or leave owner");check(result!=null&&!result.success,"failed preview checkpoint reports failure");
    }
   }
   for(String scenario:new String[]{"cancel"}){
    Context c=context(scenario);String saved=FakeDocuments.scenario;FakeDocuments.scenario="seed";
    Uri old=FakeDocuments.create("backup.slauncherbackup");byte[] bytes="existing-backup-sentinel".getBytes(java.nio.charset.StandardCharsets.UTF_8);
    java.nio.file.Files.write(FakeDocuments.files.get(old).toPath(),bytes);FakeDocuments.scenario=saved;
    overwrite=true;execute(c,scenario);overwrite=false;
    check(FakeDocuments.files.containsKey(old),"same-name attempt preserves old document");
    check(Arrays.equals(java.nio.file.Files.readAllBytes(FakeDocuments.files.get(old).toPath()),bytes),"old backup bytes unchanged");
    check(FakeDocuments.files.size()==1,"same-name rejection creates no output");check(!result.success&&"BACKUP_NAME_EXISTS".equals(result.errorCode),"same-name safety block explicit");
    check(userMessage(result.errorCode).contains("名称"),"same-name error explains rename");
   }
   for(String scenario:new String[]{"list-null","list-throw"}){
    Context c=context(scenario);execute(c,scenario);check(!result.success,"directory failure not reported successful");
    check(FakeDocuments.ids==0&&FakeDocuments.files.isEmpty(),"directory query failure blocks all document mutations");
   }
   {Context c=context("name-conflict");Uri old=FakeDocuments.create("backup.slauncherbackup");execute(c,"name-conflict");
    check(!result.success&&"BACKUP_NAME_EXISTS".equals(result.errorCode),"non-overwrite conflict remains explicit");check(FakeDocuments.files.containsKey(old)&&FakeDocuments.ids==1,"non-overwrite leaves old document alone");}
   for(String scenario:new String[]{"cancel","write","read","length","checksum","open-null","create-null","final-cancel","final-write","final-read","prefs","final-prefs","checkpoint","rename-checkpoint","complete"}){
    Context c=context(scenario);execute(c,scenario);
    if(scenario.endsWith("prefs")){
     check(FakeDocuments.files.size()==1&&new BackupOperationJournal(c).read().state==BackupOperationJournal.State.COMPLETE,"metadata failure preserves completed file and journal");
     check("BACKUP_METADATA_PENDING".equals(result.errorCode)&&FakeDocuments.files.containsKey(Uri.parse((String)c.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI))),"failed preference commit never points at deleted output");
     c.prefs.fail=false;cleanupInterruptedBackupNow(c);check(FakeDocuments.files.size()==1,"metadata recovery never deletes complete file");
    }else if(scenario.equals("complete")){
     check(FakeDocuments.files.size()==1&&!c.prefs.values.containsKey(KEY_LAST_BACKUP_DOCUMENT_URI),"unconfirmed completion leaves previous metadata untouched and retains owned candidate");
     cleanupInterruptedBackupNow(c);check(FakeDocuments.files.isEmpty(),"recovery removes uncommitted completion candidate");
    }else check(FakeDocuments.files.isEmpty(),"failed/cancelled precommit export leaves no new documents");
    check(!result.success,"failed/cancelled export not reported successful");
    if(scenario.contains("cancel")){check("BACKUP_CANCELLED".equals(result.errorCode),"prepared export reports cancellation accurately");check(new BackupOperationJournal(c).read().state==BackupOperationJournal.State.CANCELLED,"cancelled journal state");}
   }
   for(String scenario:new String[]{"success","rename-same","fallback","fallback-throw"}){
    Context c=context(scenario);execute(c,scenario);check(result.success,"complete export successful");check(FakeDocuments.files.size()==1,"only final document retained");
    Uri uri=Uri.parse((String)c.prefs.values.get(KEY_LAST_BACKUP_DOCUMENT_URI));check(FakeDocuments.files.containsKey(uri),"published URI is actual provider URI");
    check(new BackupOperationJournal(c).read().partialUri.equals(uri.toString()),"journal follows actual renamed/fallback URI");
    check(Arrays.equals(java.nio.file.Files.readAllBytes(FakeDocuments.files.get(uri).toPath()),FakeDocuments.PAYLOAD),"published bytes match verified archive");
   }
   for(String scenario:new String[]{"fallback-delete-denied","fallback-delete-throw","fallback-delete-query-null","fallback-delete-query-throw","fallback-delete-all-denied"}){
    Context c2=context(scenario);execute(c2,scenario);
    check(!result.success&&"BACKUP_CLEANUP_PENDING".equals(result.errorCode),"fallback cannot complete with unremoved partial");
    BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry pending=j.read();Uri partialUri=Uri.parse(pending.partialUri);
    check(FakeDocuments.files.size()==(scenario.equals("fallback-delete-all-denied")?2:1)&&FakeDocuments.files.containsKey(partialUri),"all remaining fallback documents stay tracked after cleanup refusal");
    check(pending.state==BackupOperationJournal.State.FAILED&&pending.destinationUri.length()!=0,"failure retains both fallback recovery URIs");
    check(!c2.prefs.values.containsKey(KEY_LAST_BACKUP_DOCUMENT_URI),"failed fallback does not publish success metadata");
    cleanupInterruptedBackupNow(c2);check(j.read().state!=BackupOperationJournal.State.IDLE&&j.read().partialUri.equals(partialUri.toString()),"refused startup cleanup preserves fallback partial");
    FakeDocuments.scenario="retry";cleanupInterruptedBackupNow(c2);check(FakeDocuments.files.isEmpty()&&j.read().state==BackupOperationJournal.State.IDLE,"fallback residual recovers after provider permits deletion");
   }
   {Context c2=context("fallback-cleanup-checkpoint");execute(c2,"fallback-cleanup-checkpoint");
    check(!result.success&&FakeDocuments.files.isEmpty(),"checkpoint failure after partial removal rolls back new output");
    BackupOperationJournal j=new BackupOperationJournal(c2);check(j.read().state==BackupOperationJournal.State.FAILED&&j.read().destinationUri.length()!=0,"checkpoint failure retains prior fallback recovery URIs");
    FakeDocuments.scenario="retry";cleanupInterruptedBackupNow(c2);check(j.read().state==BackupOperationJournal.State.IDLE,"cleanup checkpoint failure recovers using confirmed missing URIs");}
   {Context c2=context("fallback-delete-false-absent");execute(c2,"fallback-delete-false-absent");
    check(result.success&&FakeDocuments.files.size()==1,"successful empty query confirms partial gone despite delete false");
    check(new BackupOperationJournal(c2).read().state==BackupOperationJournal.State.COMPLETE,"confirmed fallback cleanup allows completion");}
   for(String scenario:new String[]{"delete-denied","delete-throw"}){
    Context failed=context(scenario);Uri pending=FakeDocuments.create("pending.partial");BackupOperationJournal j=new BackupOperationJournal(failed);
    BackupOperationJournal.Entry interrupted=new BackupOperationJournal.Entry();interrupted.partialUri=pending.toString();interrupted.token="pending-owner";
    j.write(interrupted,BackupOperationJournal.State.COPYING_TO_DESTINATION,null);cleanupInterruptedBackupNow(failed);
    check(FakeDocuments.files.containsKey(pending),"denied cleanup document retained");
    check(j.read().partialUri.equals(pending.toString())&&j.read().state!=BackupOperationJournal.State.IDLE,"denied cleanup preserves journal URI and state");
    RunningOperation blocked=new RunningOperation("new-attempt",new Listener(){public void onState(String x,boolean y){}public void onComplete(BackupRestoreResult r){result=r;}});
    check(BackupOperationLock.acquire(blocked.token),"new attempt owns operation gate");running=blocked;result=null;
    boolean proceed=(Boolean)DesktopBackupController.class.getDeclaredMethod("clearInterruptedBackupBeforeStart",Context.class,RunningOperation.class).invoke(null,failed,blocked);
    check(!proceed&&!BackupOperationLock.isBusy()&&running==null,"pending cleanup blocks new work and releases transient gate");
    check(result!=null&&"BACKUP_CLEANUP_PENDING".equals(result.errorCode)&&j.read().partialUri.equals(pending.toString()),"blocked attempt reports pending and preserves previous journal");
    FakeDocuments.scenario="retry";cleanupInterruptedBackupNow(failed);
    check(FakeDocuments.files.isEmpty()&&j.read().state==BackupOperationJournal.State.IDLE,"later cleanup removes pending document and resets journal");
   }
   for(boolean checkpointFailure:new boolean[]{false,true}){
    Context c2=context("partial-cleanup");Uri first=FakeDocuments.create("one.partial"),secondUri=FakeDocuments.create("two.partial");FakeDocuments.deniedUri=secondUri;
    BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.partialUri=first.toString();e2.destinationUri=secondUri.toString();j.write(e2,BackupOperationJournal.State.COPYING_TO_DESTINATION,null);
    if(checkpointFailure)AtomicFile.failState="COPYING_TO_DESTINATION";cleanupInterruptedBackupNow(c2);AtomicFile.failState="";
    check(!FakeDocuments.files.containsKey(first)&&FakeDocuments.files.containsKey(secondUri),"partial cleanup removes only deletable target");
    check(j.read().destinationUri.equals(secondUri.toString())&&j.read().state!=BackupOperationJournal.State.IDLE,"pending second URI survives checkpoint failure");
    if(!checkpointFailure)check(j.read().partialUri.isEmpty(),"successful first delete recorded separately");
    FakeDocuments.deniedUri=null;cleanupInterruptedBackupNow(c2);check(FakeDocuments.files.isEmpty()&&j.read().state==BackupOperationJournal.State.IDLE,"retry handles absent first URI and finishes second");
   }
   {Context c2=context("reset-failure");Uri u=FakeDocuments.create("reset.partial");BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.partialUri=u.toString();j.write(e2,BackupOperationJournal.State.COPYING_TO_DESTINATION,null);
    AtomicFile.failState="IDLE";cleanupInterruptedBackupNow(c2);AtomicFile.failState="";check(j.read().state!=BackupOperationJournal.State.IDLE&&FakeDocuments.files.isEmpty(),"failed reset retains prior journal after document deletion");
    cleanupInterruptedBackupNow(c2);check(j.read().state==BackupOperationJournal.State.IDLE,"empty successful query allows retry after reset failure");}
   for(String query:new String[]{"list-null","list-throw"}){
    Context c2=context(query);BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.partialUri="doc://missing";j.write(e2,BackupOperationJournal.State.COPYING_TO_DESTINATION,null);cleanupInterruptedBackupNow(c2);
    check(j.read().partialUri.equals("doc://missing")&&j.read().state!=BackupOperationJournal.State.IDLE,"null or failed query cannot prove document absence");
   }
   {Context c2=context("completed-preserve");Uri u=FakeDocuments.create("complete.backup");BackupOperationJournal j=new BackupOperationJournal(c2);BackupOperationJournal.Entry e2=new BackupOperationJournal.Entry();e2.partialUri=u.toString();j.write(e2,BackupOperationJournal.State.COMPLETE,null);cleanupInterruptedBackupNow(c2);
    check(FakeDocuments.files.containsKey(u)&&j.read().state==BackupOperationJournal.State.COMPLETE,"completed archive never treated as interrupted output");}
   Context c=context("startup");Uri partial=FakeDocuments.create("backup.partial"),destination=FakeDocuments.create("backup.final");
   BackupOperationJournal.Entry e=new BackupOperationJournal.Entry();e.token="interrupted";e.partialUri=partial.toString();e.stagingPath=new File(c.getCacheDir(),"staging").getAbsolutePath();new File(e.stagingPath).mkdirs();
   java.lang.reflect.Field second=BackupOperationJournal.Entry.class.getField("destinationUri");second.set(e,destination.toString());
   new BackupOperationJournal(c).write(e,BackupOperationJournal.State.COPYING_TO_DESTINATION,null);cleanupInterruptedBackupNow(c);
   check(FakeDocuments.files.isEmpty(),"startup removes both partial and interrupted fallback target");check(new BackupOperationJournal(c).read().state==BackupOperationJournal.State.IDLE,"startup resets interrupted operation");
   String legacy=e.toJson().toString().replace(",\\\"destinationUri\\\":\\\""+destination.toString()+"\\\"","");
   File journalFile=new File(c.getFilesDir(),"backup_restore/backup_operation_journal.json");java.nio.file.Files.write(journalFile.toPath(),legacy.getBytes(java.nio.charset.StandardCharsets.UTF_8));
   BackupOperationJournal.Entry legacyRead=new BackupOperationJournal(c).read();
   check(legacyRead.token.equals("interrupted")&&legacyRead.state==BackupOperationJournal.State.COPYING_TO_DESTINATION
    &&BackupOperationJournal.Entry.class.getField("destinationUri").get(legacyRead).equals(""),"legacy journal without second URI remains readable");
   System.out.println("PASS SAF_EXPORT_CHECKS="+checks+" cases="+cases);
  }
 }
}'''.replace('\n METHODS\n','\n'+methods+'\n')
    host=(ROOT/'launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java').read_text(encoding='utf-8')
    ui_probe='private static void showBackupFailureDialog(' in host
    if ui_probe:
        sources['android/app/Activity.java']='package android.app;public class Activity{}'
        sources['android/content/res/Resources.java']='package android.content.res;public class Resources{}'
        sources['android/view/View.java']='package android.view;public class View{public interface OnClickListener{void onClick(View v);}}'
        ui_methods=block(host,'private static void showBackupFailureDialog(')+'\n'+block(host,'private static String backupResultMessage(')
        sources[B+'BackupPermissionUiProbe.java']='''package com.smartisanos.launcher.backup;
import android.app.Activity;import android.content.res.Resources;import android.view.View;
public final class BackupPermissionUiProbe{
 static int choices,infos,pickers,checks;static boolean pending;static String title,message,positive;static View.OnClickListener yes,no;
 static String getString(Resources r,String key,String fallback){return fallback;}
 static void showChoiceDialog(Activity a,String t,String m,String cancel,String accept,View.OnClickListener negative,View.OnClickListener affirmative){choices++;title=t;message=m;positive=accept;no=negative;yes=affirmative;}
 static void showInfoDialog(Activity a,String t,String m){infos++;title=t;message=m;}
 static void openBackupTree(Activity a,boolean continuePreview){pickers++;pending=continuePreview;}
 static void reset(){choices=infos=pickers=0;yes=no=null;positive=title=message="";pending=true;}
 static void check(boolean ok,String label){checks++;if(!ok)throw new AssertionError(label);}
 METHODS
 public static void main(String[] args){Activity a=new Activity();Resources r=new Resources();reset();showBackupFailureDialog(a,r,BackupRestoreResult.error("BACKUP_LOCATION_PERMISSION_LOST",""));
  check(choices==1&&infos==0&&pickers==0,"permission dialog cannot launch picker automatically");check(positive.equals("重新选择目录")&&message.contains("授权"),"permission loss presents explicit reselect action");check(no==null,"cancel leaves authorization untouched");yes.onClick(new View());check(pickers==1&&!pending,"reselect uses existing picker without restarting failed preview");
  reset();showBackupFailureDialog(a,r,BackupRestoreResult.error("BACKUP_LOCATION_READ_ONLY",""));check(infos==1&&choices==0&&title.equals("备份位置不可用"),"read-only result preserves informational behavior");
  reset();showBackupFailureDialog(a,r,BackupRestoreResult.error("BACKUP_COPY_FAILED",""));check(infos==1&&choices==0&&pickers==0,"ordinary copy failure does not request reauthorization");
  reset();showBackupFailureDialog(a,r,BackupRestoreResult.error("BACKUP_METADATA_PENDING",""));check(infos==1&&choices==0&&message.contains("已保存"),"metadata pending remains file-saved information");
  reset();showBackupFailureDialog(a,r,BackupRestoreResult.error("BACKUP_JOURNAL_CORRUPT",""));check(infos==1&&choices==0&&message.contains("损坏"),"journal failure is not mislabeled as directory loss");
  System.out.println("PASS BACKUP_FAILURE_UI_CHECKS="+checks);
 }
}'''.replace('\n METHODS\n','\n'+ui_methods+'\n')
    sources[B+'DesktopBackupController.java']=java
    with tempfile.TemporaryDirectory(prefix='saf-export-') as temporary:
        base=Path(temporary);files=[]
        for name,source in sources.items():
            path=base/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(source,encoding='utf-8');files.append(str(path))
        for name in ['BackupOperationJournal','BackupOperationLock','BackupFileUtils','BackupRestoreResult']:
            path=ROOT/'launcher/tools/java'/B/(name+'.java')
            if args.before and name=='BackupOperationJournal':
                path=base/B/(name+'.java');path.write_bytes((args.before/(name+'.before.java')).read_bytes())
            files.append(str(path))
        subprocess.run([str(args.jdk/'bin/javac.exe'),'-encoding','UTF-8','-d',str(base),*files],check=True)
        subprocess.run([str(args.jdk/'bin/java.exe'),'-cp',str(base),'com.smartisanos.launcher.backup.DesktopBackupController$Probe',str(base/'data')],check=True)
        if ui_probe:subprocess.run([str(args.jdk/'bin/java.exe'),'-cp',str(base),'com.smartisanos.launcher.backup.BackupPermissionUiProbe'],check=True)


if __name__=='__main__':main()
