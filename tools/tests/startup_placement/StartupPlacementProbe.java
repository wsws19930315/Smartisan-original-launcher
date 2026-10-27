import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteTransactionListener;

/** Android runtime probe; load the built launcher APK alongside this class. */
public final class StartupPlacementProbe {
    public static void main(String[] args) throws Exception {
        Class<?> guard = Class.forName(
                "com.smartisanos.launcher.model.LauncherModelRepository$StartupPlacementCommit");
        int checks = 0;
        for (int mode = 0; mode < 3; mode++) {
            SQLiteDatabase db = SQLiteDatabase.create(null);
            try {
                db.execSQL("CREATE TABLE probe(id INTEGER PRIMARY KEY)");
                Object listener = guard.getConstructor().newInstance();
                db.beginTransactionWithListener((SQLiteTransactionListener) listener);
                db.beginTransaction();
                db.execSQL("INSERT INTO probe VALUES(1)");
                if (mode != 1) db.setTransactionSuccessful();
                db.endTransaction();
                if (mode != 2) db.setTransactionSuccessful();
                db.endTransaction();
                boolean accepted = true;
                try {
                    guard.getMethod("requireCommitted").invoke(listener);
                } catch (java.lang.reflect.InvocationTargetException expected) {
                    if (!(expected.getCause() instanceof IllegalStateException)) throw expected;
                    accepted = false;
                }
                if (accepted != (mode == 0)) throw new AssertionError("commit guard " + mode);
                checks++;
                Cursor cursor = db.rawQuery("SELECT count(*) FROM probe", null);
                try {
                    cursor.moveToFirst();
                    if (cursor.getInt(0) != (mode == 0 ? 1 : 0)) {
                        throw new AssertionError("atomic rows " + mode);
                    }
                    checks++;
                } finally {
                    cursor.close();
                }
                if (db.inTransaction()) throw new AssertionError("leaked transaction " + mode);
                checks++;
            } finally {
                db.close();
            }
        }
        System.out.println("STARTUP_PLACEMENT_PASS checks=" + checks);
    }
}
