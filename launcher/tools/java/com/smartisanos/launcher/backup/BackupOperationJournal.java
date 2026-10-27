package com.smartisanos.launcher.backup;

import android.content.Context;
import android.util.AtomicFile;
import android.util.Log;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Arrays;

public final class BackupOperationJournal {
    private static final String TAG = "BackupJournal";
    private static final long MAX_JOURNAL_BYTES = 128 * 1024L;

    public static final class JournalException extends IllegalStateException {
        public final String errorCode;
        JournalException(String code, Throwable cause) { super(code, cause); errorCode = code; }
    }
    public enum State {
        IDLE, VALIDATING_LOCATION, WAITING_DATABASE, EXPORTING_LAYOUT,
        BUILDING_ARCHIVE, PREVIEW_READY, COPYING_TO_DESTINATION, COMPLETE, CANCELLED, FAILED
    }

    public static final class Entry {
        public String token = "";
        public State state = State.IDLE;
        public String stagingPath = "";
        public String partialUri = "";
        public String destinationUri = "";
        public String completedFileName = "";
        public String errorCode = "";
        public long startedAt;
        public long updatedAt;

        JSONObject toJson() throws Exception {
            JSONObject json = new JSONObject();
            json.put("token", token);
            json.put("state", state.name());
            json.put("stagingPath", stagingPath);
            json.put("partialUri", partialUri);
            json.put("destinationUri", destinationUri);
            json.put("completedFileName", completedFileName);
            json.put("errorCode", errorCode);
            json.put("startedAt", startedAt);
            json.put("updatedAt", updatedAt);
            return json;
        }

        static Entry fromJson(JSONObject json) throws Exception {
            Entry entry = new Entry();
            entry.token = json.getString("token");
            entry.state = State.valueOf(json.getString("state"));
            entry.stagingPath = json.getString("stagingPath");
            entry.partialUri = json.getString("partialUri");
            entry.destinationUri = json.optString("destinationUri", "");
            entry.completedFileName = json.optString("completedFileName", "");
            entry.errorCode = json.optString("errorCode", "");
            entry.startedAt = json.optLong("startedAt", 0L);
            entry.updatedAt = json.optLong("updatedAt", 0L);
            if (entry.state == State.IDLE && (entry.stagingPath.length() != 0
                    || entry.partialUri.length() != 0 || entry.destinationUri.length() != 0)) {
                throw new IOException("Idle backup journal retains pending resources");
            }
            return entry;
        }
    }

    private final AtomicFile file;

    public BackupOperationJournal(Context context) {
        File directory = new File(context.getFilesDir(), "backup_restore");
        if (!directory.exists()) directory.mkdirs();
        file = new AtomicFile(new File(directory, "backup_operation_journal.json"));
    }

    public synchronized Entry read() {
        byte[] data;
        boolean existed = true;
        try {
            existed = hasJournalFiles();
            data = readBytes();
        } catch (FileNotFoundException missing) {
            File parent = file.getBaseFile().getParentFile();
            if (!existed && !hasJournalFiles() && parent.isDirectory()
                    && parent.canRead() && parent.canExecute()) return new Entry();
            throw failure("BACKUP_JOURNAL_READ_FAILED", missing);
        } catch (IOException error) {
            throw failure("BACKUP_JOURNAL_READ_FAILED", error);
        } catch (RuntimeException error) {
            throw failure("BACKUP_JOURNAL_READ_FAILED", error);
        }
        try {
            return Entry.fromJson(new JSONObject(new String(data, BackupFileUtils.UTF_8)));
        } catch (Exception error) {
            throw failure("BACKUP_JOURNAL_CORRUPT", error);
        }
    }

    private boolean hasJournalFiles() {
        File base = file.getBaseFile();
        return base.exists() || new File(base.getPath() + ".bak").exists()
                || new File(base.getPath() + ".new").exists();
    }

    private byte[] readBytes() throws IOException {
        FileInputStream input = null;
        try {
            input = file.openRead();
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            BackupFileUtils.copy(input, output, MAX_JOURNAL_BYTES, null);
            return output.toByteArray();
        } finally {
            BackupFileUtils.closeQuietly(input);
        }
    }

    private static JournalException failure(String code, Throwable error) {
        Log.e(TAG, code, error);
        return new JournalException(code, error);
    }

    public synchronized boolean write(Entry entry, State state, String errorCode) {
        FileOutputStream output = null;
        try {
            // Retain corrupt/unreadable evidence instead of replacing it with
            // a new operation, error state or IDLE reset.
            read();
            long now = System.currentTimeMillis();
            long startedAt = entry.startedAt == 0L ? now : entry.startedAt;
            String code = errorCode == null ? "" : errorCode;
            JSONObject json = entry.toJson();
            json.put("startedAt", startedAt).put("updatedAt", now)
                    .put("state", state.name()).put("errorCode", code);
            Entry.fromJson(json);
            byte[] data = json.toString().getBytes(BackupFileUtils.UTF_8);
            if (data.length > MAX_JOURNAL_BYTES) throw new IOException("Backup journal too large");
            output = file.startWrite();
            output.write(data);
            output.getFD().sync();
            file.finishWrite(output);
            output = null;
            // AtomicFile may log publication failures without throwing. Confirm
            // the exact checkpoint before publishing it into the live entry.
            if (!Arrays.equals(data, readBytes())) throw new IOException("Checkpoint verification failed");
            entry.startedAt = startedAt;
            entry.updatedAt = now;
            entry.state = state;
            entry.errorCode = code;
            return true;
        } catch (Exception error) {
            if (output != null) {
                try { file.failWrite(output); }
                catch (RuntimeException cleanupError) { error.addSuppressed(cleanupError); }
            }
            Log.e(TAG, "BACKUP_JOURNAL_WRITE_FAILED", error);
            return false;
        }
    }

    public synchronized void reset() {
        write(new Entry(), State.IDLE, null);
    }
}
