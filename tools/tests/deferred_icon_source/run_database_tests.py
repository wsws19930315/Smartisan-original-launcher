"""Run the actual icon DB transaction Smali against isolated Android SQLite files.

No installed Launcher state is accessed. Two app_process instances verify a real
write/read round trip; constraint failures and missing rows exercise result flags.
"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[3]

ASSEMBLER = r'''
import java.io.File;
import brut.androlib.smali.SmaliBuilder;
import com.android.tools.smali.dexlib2.Opcodes;
import com.android.tools.smali.dexlib2.writer.builder.DexBuilder;
import com.android.tools.smali.dexlib2.writer.io.FileDataStore;
public class AssembleIconDatabaseProbe {
 public static void main(String[] args) throws Exception {
  DexBuilder dex = new DexBuilder(new Opcodes(28));
  SmaliBuilder builder = new SmaliBuilder(28);
  for (int i = 1; i < args.length; i++)
   if (!builder.buildFile(new File(args[i]), dex)) throw new AssertionError(args[i]);
  FileDataStore output = new FileDataStore(new File(args[0]));
  try { dex.writeTo(output); } finally { output.raf.close(); }
 }
}
'''

PROBE = r'''
package com.smartisanos.launcher.audit;
import android.content.ContentValues;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.content.pm.ResolveInfo;
import android.content.pm.ActivityInfo;
import java.lang.reflect.Constructor;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
public class IconDatabaseProbe {
 static int checks, falsePositives;
 static boolean fixed;
 public static ContentValues prepared;
 public static SQLiteDatabase active;
 public static int writes;
 public static List<ResolveInfo> resolves() {
  ResolveInfo info = new ResolveInfo(); info.activityInfo = new ActivityInfo();
  info.activityInfo.name = "Main"; return Collections.singletonList(info);
 }
 public static boolean persist(ContentValues values) {
  writes++;
  try { return write(active, false, 1, values); }
  catch (Exception error) { throw new AssertionError(error); }
 }
 static void check(boolean ok, String message) {
  checks++; if (!ok) throw new AssertionError(message);
 }
 static ContentValues icon(long owner, byte... bytes) {
  ContentValues values = new ContentValues();
  values.put("owner", owner); values.put("light_icon", bytes); return values;
 }
 static boolean write(SQLiteDatabase db, boolean exists, long id, ContentValues values) throws Exception {
  Class<?> type = Class.forName("com.smartisanos.launcher.data.a.e");
  Constructor<?> ctor = type.getDeclaredConstructor(SQLiteDatabase.class, boolean.class,
    long.class, ContentValues.class); ctor.setAccessible(true);
  Object task = ctor.newInstance(db, exists, id, values);
  Object result = type.getMethod("execute").invoke(task);
  return result.getClass().getField("b").getBoolean(result);
 }
 static void failed(boolean reported, String operation) {
  if (reported) falsePositives++;
  if (fixed) check(!reported, operation + " reported success without writing a row");
 }
 static void read(SQLiteDatabase db) {
  Cursor c = db.rawQuery("SELECT owner, light_icon FROM table_icons", null);
  try {
   check(c.getCount() == 1, "failed writes changed row count");
   check(c.moveToFirst() && c.getLong(0) == 1, "owner changed");
   check(Arrays.equals(c.getBlob(1), new byte[]{9, 8}), "committed bytes did not survive");
  } finally { c.close(); }
 }
 public static void main(String[] args) throws Exception {
  String mode = args[0], path = args[1];
  System.out.println("PROBE_PID=" + android.os.Process.myPid());
  if (!path.startsWith("/data/local/tmp/smartisan-icon-db-")) throw new AssertionError("test path");
  fixed = Boolean.parseBoolean(args[2]);
  if (mode.equals("read")) {
   SQLiteDatabase db = SQLiteDatabase.openDatabase(path, null, SQLiteDatabase.OPEN_READONLY);
   try { read(db); } finally { db.close(); }
   System.out.println("PASS fresh-process SQLite read checks=" + checks); return;
  }
  SQLiteDatabase db = SQLiteDatabase.openOrCreateDatabase(path, null);
  try {
   db.execSQL("CREATE TABLE table_icons(owner INTEGER UNIQUE NOT NULL, light_icon BLOB)");
   check(write(db, false, 1, icon(1, (byte)1)), "valid insert failed");
   failed(write(db, false, 1, icon(1, (byte)2)), "constraint insert");
   failed(write(db, true, 99, icon(99, (byte)3)), "missing owner update");
   ContentValues bad = icon(2, (byte)4); bad.put("missing_column", 1);
   failed(write(db, false, 2, bad), "invalid insert");
   db.execSQL("CREATE TRIGGER ignore_update BEFORE UPDATE ON table_icons BEGIN SELECT RAISE(IGNORE); END");
   failed(write(db, true, 1, icon(1, (byte)5)), "ignored update");
   db.execSQL("DROP TRIGGER ignore_update");
   check(!write(db, true, 1, bad), "SQL exception must fail transaction");
   check(write(db, true, 1, icon(1, (byte)9, (byte)8)), "valid update failed");
   read(db);
   // Execute the unchanged production byte-returning bridge, with only PM/generator fixtures.
   active = db; prepared = icon(1, (byte)7);
   com.smartisanos.launcher.data.ItemInfo item = new com.smartisanos.launcher.data.ItemInfo();
   byte[] bytes = (byte[])Class.forName("com.smartisanos.launcher.e.s")
     .getMethod("a", item.getClass(), boolean.class).invoke(null, item, true);
   check(Arrays.equals(bytes, new byte[]{7}) && writes == 1,
     "failed persistence must retain usable in-memory bytes");
   bytes = (byte[])Class.forName("com.smartisanos.launcher.e.s")
     .getMethod("a", item.getClass(), boolean.class).invoke(null, item, false);
   check(Arrays.equals(bytes, new byte[]{7}) && writes == 1, "non-persisting caller wrote DB");
   prepared = null; item.iconRawData = new byte[]{6};
   bytes = (byte[])Class.forName("com.smartisanos.launcher.e.s")
     .getMethod("a", item.getClass(), boolean.class).invoke(null, item, true);
   check(Arrays.equals(bytes, new byte[]{6}) && writes == 1, "unchanged-cache return changed");
   read(db);
  } finally { db.close(); }
  if (!fixed) check(falsePositives == 4, "baseline failure controls changed");
  System.out.println("PASS isolated SQLite checks=" + checks + " falsePositives=" + falsePositives
    + " expectFixed=" + fixed + " boundary=actual-e-V-U-smali");
 }
}
'''


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--serial', required=True)
    ap.add_argument('--jdk', type=Path, required=True)
    ap.add_argument('--sdk', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--source', type=Path,
                    default=ROOT / 'launcher/smali/com/smartisanos/launcher/data/a/e.smali')
    ap.add_argument('--caller-source', type=Path,
                    default=ROOT / 'launcher/smali/com/smartisanos/launcher/e/s.smali')
    ap.add_argument('--expect-fixed', action='store_true')
    args = ap.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    classes, dex = out / 'classes', out / 'dex'
    classes.mkdir(exist_ok=True)
    dex.mkdir(exist_ok=True)
    jar = ROOT / 'tools/apktool.jar'
    java = args.jdk / 'bin/java.exe'
    javac = args.jdk / 'bin/javac.exe'
    android = args.sdk / 'platforms/android-36/android.jar'
    adb = [str(args.sdk / 'platform-tools/adb.exe'), '-s', args.serial]

    def run(command):
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=90)
        print(result.stdout, end='', flush=True)
        print(result.stderr, end='', flush=True)
        pid = re.search(r'PROBE_PID=(\d+)', result.stdout)
        if pid:
            scoped = subprocess.check_output(
                [*adb, 'logcat', '-d', '--pid=' + pid[1], '-s',
                 'AndroidRuntime:E', 'LauncherIconRaster:I'], timeout=20)
            mode = str(command[-3])
            (out / (mode + '-android-runtime.log')).write_bytes(scoped)
            if result.returncode == 0 and mode == 'write' and args.expect_fixed:
                assert scoped.count(b'ICON_SOURCE_DATABASE_WRITE_FAILED') == 1, \
                    'failed-persistence bridge did not log exactly one database failure'
        result.check_returncode()

    assembler = out / 'AssembleIconDatabaseProbe.java'
    assembler.write_text(ASSEMBLER, encoding='utf-8')
    run([javac, '-cp', jar, '-d', classes, assembler])
    smali = []
    for source in (args.source, ROOT / 'launcher/smali/com/smartisanos/launcher/data/V.smali',
                   ROOT / 'launcher/smali/com/smartisanos/launcher/data/U.smali'):
        target = out / source.name
        shutil.copyfile(source, target)
        smali.append(target)
    caller = args.caller_source.read_text(encoding='utf-8')
    start = caller.index('.method public static a(Lcom/smartisanos/launcher/data/ItemInfo;Z)[B')
    end = caller.index('.end method', start) + len('.end method')
    bridge = out / 's.smali'
    bridge.write_text('''.class public Lcom/smartisanos/launcher/e/s;
.super Ljava/lang/Object;
''' + caller[start:end] + '''
.method public static l(Landroid/content/Context;Ljava/lang/String;)Ljava/util/List;
 .locals 1
 invoke-static {}, Lcom/smartisanos/launcher/audit/IconDatabaseProbe;->resolves()Ljava/util/List;
 move-result-object v0
 return-object v0
.end method
.method public static ra(Ljava/lang/String;)Z
 .locals 1
 const/4 v0, 0x0
 return v0
.end method
.method public static rg()Ljava/lang/String;
 .locals 1
 const-string v0, "light_icon"
 return-object v0
.end method
''', encoding='utf-8')
    smali.append(bridge)
    assembled = out / 'database.dex'
    run([java, '-cp', str(classes) + ';' + str(jar), 'AssembleIconDatabaseProbe', assembled, *smali])
    probe = out / 'IconDatabaseProbe.java'
    probe.write_text(PROBE, encoding='utf-8')
    fixtures = {
        'ItemInfo.java': '''package com.smartisanos.launcher.data;
public class ItemInfo {public long id=1; public String packageName="example.app",componentName="Main";
public boolean isSystemApp; public byte[] iconRawData;}''',
        'Aa.java': '''package com.smartisanos.launcher;
public class Aa {public static android.content.ContentValues a(com.smartisanos.launcher.data.ItemInfo i,
android.content.pm.ResolveInfo r,android.content.Context c){return com.smartisanos.launcher.audit.IconDatabaseProbe.prepared;}}''',
        'ja.java': '''package com.smartisanos.launcher; public class ja {
public static ja getInstance(){return new ja();}public android.app.Application getApplication(){return null;}}''',
        'h.java': '''package com.smartisanos.launcher.data.a; public class h {
public static boolean a(android.content.ContentValues v){return com.smartisanos.launcher.audit.IconDatabaseProbe.persist(v);}}''',
    }
    for name, content in fixtures.items():
        (out / name).write_text(content, encoding='utf-8')
    run([javac, '-source', '8', '-target', '8', '-cp', android, '-d', classes,
         probe, *(out / name for name in fixtures)])
    program_classes = [f for f in classes.rglob('*.class') if f.name != 'AssembleIconDatabaseProbe.class']
    run([java, '-cp', args.sdk / 'build-tools/37.0.0/lib/d8.jar', 'com.android.tools.r8.D8',
         '--min-api', '28', '--lib', android, '--output', dex, assembled,
         *program_classes])
    remote = '/data/local/tmp/smartisan-icon-db-' + uuid.uuid4().hex
    run([*adb, 'push', dex / 'classes.dex', remote + '.dex'])
    try:
        for mode in ('write', 'read'):
            run([*adb, 'shell', 'env', 'CLASSPATH=' + remote + '.dex', 'app_process',
                 '/system/bin', 'com.smartisanos.launcher.audit.IconDatabaseProbe', mode,
                 remote + '.db', str(args.expect_fixed).lower()])
    finally:
        run([*adb, 'shell', 'rm', '-f', remote + '.dex', remote + '.db',
             remote + '.db-journal', remote + '.db-wal', remote + '.db-shm'])


if __name__ == '__main__':
    main()
