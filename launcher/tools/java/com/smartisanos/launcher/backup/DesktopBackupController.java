package com.smartisanos.launcher.backup;

import android.content.ContentResolver;
import android.content.Context;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.os.Handler;
import android.os.Looper;
import android.os.ParcelFileDescriptor;
import android.provider.DocumentsContract;
import android.util.Log;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.Field;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public final class DesktopBackupController {
    public static final String PREFS = "launcher_backup_settings";
    public static final String KEY_TREE_URI = "backup_tree_uri";
    public static final String KEY_TREE_DISPLAY_NAME = "backup_tree_display_name";
    public static final String KEY_LAST_BACKUP_TIME = "last_backup_time";
    public static final String KEY_LAST_BACKUP_FILE_NAME = "last_backup_file_name";
    public static final String KEY_LAST_BACKUP_DOCUMENT_URI = "last_backup_document_uri";
    public static final String KEY_LAST_RESTORE_DOCUMENT_URI = "last_restore_document_uri";
    private static final String TAG = "DesktopBackup";
    private static final long EXTERNAL_COPY_LIMIT = BackupValidator.MAX_ARCHIVE_BYTES;
    private static final Handler MAIN = new Handler(Looper.getMainLooper());
    private static volatile RunningOperation running;
    private static volatile PreparedBackup preparedBackup;

    public interface Listener {
        void onState(String state, boolean cancellable);
        void onComplete(BackupRestoreResult result);
    }

    public interface PreviewListener extends Listener {
        void onPreview(BackupArchiveReader.ValidatedBackup backup,
                RestoreMergePlanner.Plan plan, String suggestedName);
    }

    public static final class CancellationToken {
        private volatile boolean cancelled;
        public void cancel() { cancelled = true; }
        public boolean isCancelled() { return cancelled; }
        public void throwIfCancelled() throws BackupCancelledException {
            if (cancelled) throw new BackupCancelledException();
        }
    }

    static final class BackupCancelledException extends IOException {
        BackupCancelledException() { super("Backup cancelled"); }
    }

    private static final class RunningOperation {
        final String token;
        final CancellationToken cancellation = new CancellationToken();
        volatile Listener listener;
        RunningOperation(String token, Listener listener) { this.token = token; this.listener = listener; }
    }

    private static final class PreparedBackup {
        final String token;
        final Context context;
        final File staging;
        final File archive;
        final Uri treeUri;
        final BackupArchiveReader.ValidatedBackup backup;
        volatile boolean saving;
        PreparedBackup(String token, Context context, File staging, File archive, Uri treeUri,
                BackupArchiveReader.ValidatedBackup backup) {
            this.token = token; this.context = context; this.staging = staging; this.archive = archive;
            this.treeUri = treeUri; this.backup = backup;
        }
    }

    private DesktopBackupController() {}

    public static boolean hasRunningBackup() { return running != null; }

    /** Builds and validates the exact archive that will later be copied after confirmation. */
    public static void prepareBackupPreview(Context context, Uri treeUri, PreviewListener listener) {
        if (context == null || treeUri == null || listener == null) return;
        discardPreparedBackupPreview(context);
        if (running != null || BackupOperationLock.isBusy()) {
            complete(listener, BackupRestoreResult.error("BACKUP_OPERATION_BUSY",
                    "桌面正在执行其他设置，请稍后再试。"));
            return;
        }
        final Context app = context.getApplicationContext() == null ? context : context.getApplicationContext();
        final RunningOperation operation = new RunningOperation(UUID.randomUUID().toString(), listener);
        if (!BackupOperationLock.acquire(operation.token)) {
            complete(listener, BackupRestoreResult.error("BACKUP_OPERATION_BUSY",
                    "桌面正在执行其他设置，请稍后再试。"));
            return;
        }
        running = operation;
        final Uri targetTree = treeUri;
        new Thread(new Runnable() {
            public void run() {
                if (clearInterruptedBackupBeforeStart(app, operation)) preparePreview(app, targetTree, operation);
            }
        }, "DesktopBackupPreview").start();
    }

    /** Releases an unconfirmed preview and its staged archive. */
    public static void discardPreparedBackupPreview(Context context) {
        PreparedBackup current = preparedBackup;
        if (current == null) return;
        if (current.saving) return;
        preparedBackup = null;
        RunningOperation operation = running;
        if (operation != null && current.token.equals(operation.token)) {
            operation.cancellation.cancel();
            running = null;
        }
        BackupFileUtils.deleteRecursively(current.staging);
        if (context != null) new BackupOperationJournal(context).reset();
        BackupOperationLock.release(current.token);
    }

    /** Copies the already-previewed archive; it does not take a second desktop snapshot. */
    public static synchronized void startPreparedBackup(Context context, String fileName, boolean overwrite,
            Listener listener) {
        final PreparedBackup current = preparedBackup;
        final RunningOperation operation = running;
        final String normalized = normalizeBackupFileName(fileName);
        if (current == null || operation == null || !current.token.equals(operation.token)
                || normalized.length() == 0) {
            complete(listener, BackupRestoreResult.error("BACKUP_EXPORT_FAILED",
                    "备份预览已失效，请重新开始。"));
            return;
        }
        if (current.saving) return;
        current.saving = true;
        operation.listener = listener;
        new Thread(new Runnable() {
            public void run() { copyPreparedArchive(current, normalized, overwrite, operation); }
        }, "DesktopBackupSave").start();
    }

    public static void attachListener(Listener listener) {
        RunningOperation operation = running;
        if (operation != null) operation.listener = listener;
    }

    public static void detachListener(Listener listener) {
        RunningOperation operation = running;
        if (operation != null && operation.listener == listener) operation.listener = null;
    }

    public static boolean cancelRunningBackup() {
        RunningOperation operation = running;
        if (operation == null) return false;
        operation.cancellation.cancel();
        return true;
    }

    public static String directoryDisplayName(Context context, Uri uri) {
        if (context == null || uri == null) return "尚未选择";
        Cursor cursor = null;
        try {
            cursor = context.getContentResolver().query(uri,
                    new String[] {DocumentsContract.Document.COLUMN_DISPLAY_NAME}, null, null, null);
            if (cursor != null && cursor.moveToFirst()) {
                String value = cursor.getString(0);
                if (value != null && value.length() != 0) return value;
            }
        } catch (Throwable ignored) {
        } finally { if (cursor != null) cursor.close(); }
        return "已选择目录";
    }

    public static String documentDisplayName(Context context, Uri uri) {
        if (context == null || uri == null) return "";
        Cursor cursor = null;
        try {
            cursor = context.getContentResolver().query(uri,
                    new String[] {DocumentsContract.Document.COLUMN_DISPLAY_NAME}, null, null, null);
            if (cursor != null && cursor.moveToFirst()) {
                String value = cursor.getString(0);
                if (value != null) return value;
            }
        } catch (Throwable ignored) {
        } finally { if (cursor != null) cursor.close(); }
        return uri.getLastPathSegment() == null ? "" : uri.getLastPathSegment();
    }

    /**
     * A SAF tree is not a filesystem path.  Show its stable document-id path
     * instead of a generic "folder selected" label, without assuming that the
     * provider exposes a local filesystem path.
     */
    public static String directoryDisplayPath(Context context, Uri uri) {
        if (uri != null) {
            try {
                String documentId = DocumentsContract.getTreeDocumentId(uri);
                if (documentId != null && documentId.length() != 0) {
                    int separator = documentId.indexOf(':');
                    if (separator >= 0) {
                        String volume = documentId.substring(0, separator);
                        String relative = documentId.substring(separator + 1);
                        if ("primary".equalsIgnoreCase(volume)) {
                            return relative.length() == 0 ? "/" : "/" + relative;
                        }
                        return relative.length() == 0 ? volume : volume + "/" + relative;
                    }
                    return documentId;
                }
            } catch (Throwable ignored) {
            }
        }
        return directoryDisplayName(context, uri);
    }

    public static boolean persistTreePermission(Context context, Uri uri, int flags) {
        if (context == null || uri == null) return false;
        int persist = flags & (android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION
                | android.content.Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
        if ((persist & android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION) == 0
                || (persist & android.content.Intent.FLAG_GRANT_WRITE_URI_PERMISSION) == 0) return false;
        try {
            context.getContentResolver().takePersistableUriPermission(uri, persist);
            String name = directoryDisplayPath(context, uri);
            return context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit()
                    .putString(KEY_TREE_URI, uri.toString()).putString(KEY_TREE_DISPLAY_NAME, name).commit();
        } catch (Throwable error) {
            Log.w(TAG, "BACKUP_LOCATION_PERMISSION_LOST", error);
            return false;
        }
    }

    public static String normalizeBackupFileName(String value) {
        String name = value == null ? "" : value.trim();
        name = name.replaceAll("[\\\\/:*?\"<>|]", "_").trim();
        if (name.length() == 0) return "";
        String extension = ".slauncherbackup";
        if (name.toLowerCase(Locale.US).endsWith(extension)) {
            name = name.substring(0, name.length() - extension.length()).trim();
        }
        if (name.length() == 0) return "";
        if (name.length() > 96) name = name.substring(0, 96).trim();
        return name.length() == 0 ? "" : name + extension;
    }

    public static Uri findTreeBackup(Context context, Uri treeUri, String fileName) {
        try { return findTreeBackupChecked(context, treeUri, fileName); }
        catch (Exception error) {
            Log.w(TAG, "BACKUP_TREE_LIST_FAILED", error);
            return null;
        }
    }

    private static Uri findTreeBackupChecked(Context context, Uri treeUri, String fileName)
            throws Exception {
        if (context == null || treeUri == null || fileName == null) {
            throw coded("BACKUP_LOCATION_PERMISSION_LOST");
        }
        Cursor cursor = null;
        try {
            Uri children = DocumentsContract.buildChildDocumentsUriUsingTree(treeUri,
                    DocumentsContract.getTreeDocumentId(treeUri));
            cursor = context.getContentResolver().query(children, new String[] {
                    DocumentsContract.Document.COLUMN_DOCUMENT_ID,
                    DocumentsContract.Document.COLUMN_DISPLAY_NAME }, null, null, null);
            if (cursor == null) throw coded("BACKUP_TREE_LIST_FAILED");
            while (cursor.moveToNext()) {
                if (fileName.equals(cursor.getString(1))) {
                    return DocumentsContract.buildDocumentUriUsingTree(treeUri, cursor.getString(0));
                }
            }
        } finally { if (cursor != null) cursor.close(); }
        return null;
    }

    public static void startBackupToTree(Context context, Uri treeUri, String fileName,
            boolean overwrite, Listener listener) {
        start(context, treeUri, fileName, overwrite, listener);
    }

    private static synchronized void start(Context context, Uri treeUri, String fileName,
            boolean overwrite, Listener listener) {
        if (running != null || BackupOperationLock.isBusy()) {
            complete(listener, BackupRestoreResult.error("BACKUP_EXPORT_FAILED",
                    "桌面正在执行其他设置，请稍后再试。"));
            return;
        }
        final Context app = context.getApplicationContext() == null ? context : context.getApplicationContext();
        final RunningOperation operation = new RunningOperation(UUID.randomUUID().toString(), listener);
        if (!BackupOperationLock.acquire(operation.token)) {
            complete(listener, BackupRestoreResult.error("BACKUP_EXPORT_FAILED",
                    "桌面正在执行其他设置，请稍后再试。"));
            return;
        }
        running = operation;
        final Uri targetTree = treeUri;
        final String targetName = normalizeBackupFileName(fileName);
        final boolean replaceExisting = overwrite;
        new Thread(new Runnable() {
            public void run() {
                if (clearInterruptedBackupBeforeStart(app, operation)) {
                    execute(app, targetTree, targetName, replaceExisting, operation);
                }
            }
        }, "DesktopBackup").start();
    }

    private static void execute(Context context, Uri treeUri, String requestedName, boolean overwrite,
            RunningOperation operation) {
        long begin = System.currentTimeMillis();
        BackupOperationJournal journal = new BackupOperationJournal(context);
        BackupOperationJournal.Entry entry = new BackupOperationJournal.Entry();
        entry.token = operation.token;
        File staging = new File(new File(context.getCacheDir(), "backup_staging"), operation.token);
        entry.stagingPath = staging.getAbsolutePath();
        Uri partial = null;
        boolean finalizing = false;
        try {
            state(operation, journal, entry, BackupOperationJournal.State.VALIDATING_LOCATION,
                    "VALIDATING_LOCATION", true);
            if (treeUri == null)
                throw coded("BACKUP_LOCATION_NOT_SELECTED");
            operation.cancellation.throwIfCancelled();
            BackupFileUtils.deleteRecursively(staging);
            BackupFileUtils.ensureDirectory(new File(staging, "icons/custom"));

            JSONObjectHolder layout = createCurrentArchive(context, staging, operation, journal, entry);
            File archive = new File(staging, "archive.slauncherbackup");
            operation.cancellation.throwIfCancelled();
            String baseName = requestedName;
            if (baseName.length() == 0) {
                baseName = "SmartisanLauncher_" + new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US)
                        .format(new Date()) + ".slauncherbackup";
            }
            state(operation, journal, entry, BackupOperationJournal.State.COPYING_TO_DESTINATION,
                    "COPYING_TO_DESTINATION", true);
            Uri finalUri;
            finalUri = writeToTree(context, treeUri, archive, baseName, overwrite, operation, journal,
                    entry, staging);
            partial = finalUri;
            operation.cancellation.throwIfCancelled();
            finalizing = true;
            completeBackup(context, baseName, journal, entry);
            Log.i(TAG, "BACKUP_COPY_COMPLETE token=" + safeToken(operation.token)
                    + " itemCount=" + layout.itemCount + " durationMs="
                    + (System.currentTimeMillis() - begin));
            notifyComplete(operation, BackupRestoreResult.ok("桌面备份已完成", layout.itemCount, 0, 0));
        } catch (BackupCancelledException cancelled) {
            if (!finalizing) {
                deleteDocumentQuietly(context, partial);
                journal.write(entry, BackupOperationJournal.State.CANCELLED, "BACKUP_CANCELLED");
            }
            notifyComplete(operation, BackupRestoreResult.error("BACKUP_CANCELLED", "已取消本次备份"));
        } catch (Throwable error) {
            if (!finalizing) deleteDocumentQuietly(context, partial);
            String code = error instanceof CodedIOException ? ((CodedIOException) error).code
                    : (isNoSpace(error) ? "BACKUP_NO_SPACE"
                    : (error instanceof java.io.FileNotFoundException ? "BACKUP_LOCATION_PERMISSION_LOST"
                    : "BACKUP_EXPORT_FAILED"));
            if (!finalizing) journal.write(entry, BackupOperationJournal.State.FAILED, code);
            Log.w(TAG, "BACKUP_FAILED token=" + safeToken(operation.token) + " errorCode=" + code, error);
            notifyComplete(operation, BackupRestoreResult.error(code, userMessage(code)));
        } finally {
            BackupFileUtils.deleteRecursively(staging);
            BackupOperationLock.release(operation.token);
            if (running == operation) running = null;
        }
    }

    private static void preparePreview(Context context, Uri treeUri, RunningOperation operation) {
        BackupOperationJournal journal = new BackupOperationJournal(context);
        BackupOperationJournal.Entry entry = new BackupOperationJournal.Entry();
        entry.token = operation.token;
        File staging = new File(new File(context.getCacheDir(), "backup_preview"), operation.token);
        entry.stagingPath = staging.getAbsolutePath();
        boolean ready = false;
        try {
            state(operation, journal, entry, BackupOperationJournal.State.VALIDATING_LOCATION,
                    "VALIDATING_LOCATION", true);
            if (!hasPersistedTreePermission(context, treeUri)) throw coded("BACKUP_LOCATION_PERMISSION_LOST");
            BackupFileUtils.deleteRecursively(staging);
            BackupFileUtils.ensureDirectory(new File(staging, "icons/custom"));
            createCurrentArchive(context, staging, operation, journal, entry);
            File archive = new File(staging, "archive.slauncherbackup");
            operation.cancellation.throwIfCancelled();
            BackupArchiveReader.ValidatedBackup backup = BackupArchiveReader.read(archive,
                    new File(staging, "preview_extracted"));
            backup.sourceName = suggestedBackupName();
            RestoreMergePlanner.Plan plan = RestoreMergePlanner.plan(context, backup);
            operation.cancellation.throwIfCancelled();
            if (!journal.write(entry, BackupOperationJournal.State.PREVIEW_READY, null)) throw coded("BACKUP_COPY_FAILED");
            preparedBackup = new PreparedBackup(operation.token, context, staging, archive, treeUri, backup);
            ready = true;
            notifyPreview(operation, backup, plan, backup.sourceName);
        } catch (BackupCancelledException cancelled) {
            journal.write(entry, BackupOperationJournal.State.CANCELLED, "BACKUP_CANCELLED");
            notifyComplete(operation, BackupRestoreResult.error("BACKUP_CANCELLED", "已取消本次备份"));
        } catch (Throwable error) {
            String code = error instanceof CodedIOException ? ((CodedIOException) error).code
                    : (isNoSpace(error) ? "BACKUP_NO_SPACE" : "BACKUP_EXPORT_FAILED");
            journal.write(entry, BackupOperationJournal.State.FAILED, code);
            Log.w(TAG, "BACKUP_PREVIEW_FAILED token=" + safeToken(operation.token)
                    + " errorCode=" + code, error);
            notifyComplete(operation, BackupRestoreResult.error(code, userMessage(code)));
        } finally {
            if (!ready) {
                BackupFileUtils.deleteRecursively(staging);
                BackupOperationLock.release(operation.token);
                if (running == operation) running = null;
            }
        }
    }

    private static JSONObjectHolder createCurrentArchive(Context context, File staging,
            RunningOperation operation, BackupOperationJournal journal,
            BackupOperationJournal.Entry entry) throws Exception {
        state(operation, journal, entry, BackupOperationJournal.State.WAITING_DATABASE,
                "WAITING_DATABASE", true);
        final JSONObjectHolder layout = exportLayoutAtDatabaseSafePoint(context, operation.cancellation);
        operation.cancellation.throwIfCancelled();
        state(operation, journal, entry, BackupOperationJournal.State.EXPORTING_LAYOUT,
                "EXPORTING_LAYOUT", true);
        BackupManifest manifest = BackupManifest.create(context, readGridMode(context));
        Log.i(TAG, "BACKUP_SCHEMA formatVersion=" + manifest.formatVersion
                + " iconSourceSchemaVersion=" + manifest.iconSourceSchemaVersion
                + " shortcutSourceSchemaVersion=" + manifest.shortcutSourceSchemaVersion
                + " profileIdentitySchemaVersion=" + manifest.profileIdentitySchemaVersion);
        // Resolve legacy icon-pack preferences through their existing owner before snapshotting.
        com.smartisanos.home.settings.icons.IconSourceManager.get(context);
        org.json.JSONObject settings = PreferenceBackupCodec.encode(context);
        org.json.JSONObject theme = ThemeBackupCodec.encode(context, staging, operation.cancellation);
        org.json.JSONObject icons = IconBackupCodec.encode(context, new File(staging, "icons/custom"));
        org.json.JSONObject shortcutIcons = ShortcutIconBackupCodec.encode(context, layout.value,
                new File(staging, "icons/shortcuts"));
        org.json.JSONObject portableSources = RestoreIconSourceReconciler.encodePortableSources(
                context, new File(staging, "icons/sources"), layout.value, icons);
        state(operation, journal, entry, BackupOperationJournal.State.BUILDING_ARCHIVE,
                "正在构建压缩包", true);
        BackupArchiveWriter.write(staging, manifest, layout.value, settings, theme, icons,
                shortcutIcons, portableSources, operation.cancellation);
        operation.cancellation.throwIfCancelled();
        return layout;
    }

    private static boolean hasPersistedTreePermission(Context context, Uri treeUri) {
        try {
            for (android.content.UriPermission permission
                    : context.getContentResolver().getPersistedUriPermissions()) {
                if (treeUri.equals(permission.getUri()) && permission.isReadPermission()
                        && permission.isWritePermission()) return true;
            }
        } catch (Throwable ignored) {
        }
        return false;
    }

    public static String suggestedBackupName() {
        return new SimpleDateFormat("yyyy-MM-dd HH-mm", Locale.getDefault()).format(new Date());
    }

    private static void notifyPreview(final RunningOperation operation,
            final BackupArchiveReader.ValidatedBackup backup, final RestoreMergePlanner.Plan plan,
            final String suggestedName) {
        MAIN.post(new Runnable() {
            public void run() {
                Listener target = operation.listener;
                if (target instanceof PreviewListener) {
                    ((PreviewListener) target).onPreview(backup, plan, suggestedName);
                }
            }
        });
    }

    private static void copyPreparedArchive(PreparedBackup prepared, String fileName,
            boolean overwrite, RunningOperation operation) {
        Context context = prepared.context;
        BackupOperationJournal journal = new BackupOperationJournal(context);
        Uri partial = null;
        boolean finalizing = false;
        try {
            BackupOperationJournal.Entry entry = journal.read();
            state(operation, journal, entry, BackupOperationJournal.State.COPYING_TO_DESTINATION,
                    "COPYING_TO_DESTINATION", true);
            Uri finalUri = writeToTree(context, prepared.treeUri, prepared.archive, fileName,
                    overwrite, operation, journal, entry, prepared.staging);
            partial = finalUri;
            operation.cancellation.throwIfCancelled();
            finalizing = true;
            completeBackup(context, fileName, journal, entry);
            notifyComplete(operation, BackupRestoreResult.ok("桌面备份已完成",
                    prepared.backup.itemCount(), 0, 0));
        } catch (Throwable error) {
            if (!finalizing && context != null) deleteDocumentQuietly(context, partial);
            String code = error instanceof BackupOperationJournal.JournalException
                    ? ((BackupOperationJournal.JournalException) error).errorCode
                    : error instanceof BackupCancelledException ? "BACKUP_CANCELLED"
                    : error instanceof CodedIOException ? ((CodedIOException) error).code
                    : (isNoSpace(error) ? "BACKUP_NO_SPACE"
                    : (error instanceof java.io.FileNotFoundException
                    ? "BACKUP_LOCATION_PERMISSION_LOST" : "BACKUP_COPY_FAILED"));
            if (!finalizing && context != null) {
                try {
                    journal.write(journal.read(), error instanceof BackupCancelledException
                            ? BackupOperationJournal.State.CANCELLED : BackupOperationJournal.State.FAILED, code);
                } catch (BackupOperationJournal.JournalException journalError) {
                    Log.w(TAG, journalError.errorCode, journalError);
                }
            }
            notifyComplete(operation, BackupRestoreResult.error(code, userMessage(code)));
        } finally {
            BackupFileUtils.deleteRecursively(prepared.staging);
            preparedBackup = null;
            BackupOperationLock.release(operation.token);
            if (running == operation) running = null;
        }
    }

    private static void completeBackup(Context context, String fileName,
            BackupOperationJournal journal, BackupOperationJournal.Entry entry) throws IOException {
        // COMPLETE is the commit point. Once attempted, leave the file and journal
        // for recovery: a failed readback can still follow a successful publication.
        entry.completedFileName = fileName;
        if (!journal.write(entry, BackupOperationJournal.State.COMPLETE, null)) throw coded("BACKUP_COPY_FAILED");
        if (!publishCompletedBackupMetadata(context, entry)) throw coded("BACKUP_METADATA_PENDING");
    }

    private static boolean publishCompletedBackupMetadata(Context context, BackupOperationJournal.Entry entry) {
        if (entry.partialUri.length() == 0 || entry.completedFileName.length() == 0) return false;
        return context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit()
                .putLong(KEY_LAST_BACKUP_TIME, entry.updatedAt)
                .putString(KEY_LAST_BACKUP_FILE_NAME, entry.completedFileName)
                .putString(KEY_LAST_BACKUP_DOCUMENT_URI, entry.partialUri)
                .putBoolean("last_backup_incomplete", false).commit();
    }

    static JSONObjectHolder exportLayoutAtDatabaseSafePoint(final Context context,
            final CancellationToken token)
            throws Exception {
        final JSONObjectHolder holder = new JSONObjectHolder();
        final CountDownLatch latch = new CountDownLatch(1);
        Class<?> handlerClass = Class.forName("com.smartisanos.launcher.data.A");
        Field field = handlerClass.getDeclaredField("mWorker");
        field.setAccessible(true);
        android.os.Handler worker = (android.os.Handler) field.get(null);
        if (worker == null) throw coded("BACKUP_EXPORT_FAILED");
        if (!worker.post(new Runnable() {
            public void run() {
                try {
                    token.throwIfCancelled();
                    holder.value = LayoutSnapshotExporter.exportStableSnapshot(context);
                    holder.itemCount = holder.value.getJSONArray("items").length();
                } catch (Throwable error) { holder.error = error; }
                finally { latch.countDown(); }
            }
        })) throw coded("BACKUP_EXPORT_FAILED");
        while (!latch.await(250, TimeUnit.MILLISECONDS)) token.throwIfCancelled();
        if (holder.error != null) throw new Exception(holder.error);
        return holder;
    }

    private static Uri writeToTree(Context context, Uri tree, File archive, String finalName,
            boolean overwrite, RunningOperation operation, BackupOperationJournal journal,
            BackupOperationJournal.Entry entry, File staging) throws Exception {
        Uri partial = null;
        Uri finalUri = null;
        try {
            ContentResolver resolver = context.getContentResolver();
            String treeId = DocumentsContract.getTreeDocumentId(tree);
            Uri parent = DocumentsContract.buildDocumentUriUsingTree(tree, treeId);
            Uri existing = findTreeBackupChecked(context, tree, finalName);
            // SAF has no provider-independent atomic replacement. Keep the existing
            // archive intact, including when an older caller requested overwrite.
            if (existing != null) throw coded("BACKUP_NAME_EXISTS");
            String partialName = finalName + ".partial";
            partial = DocumentsContract.createDocument(resolver, parent, "application/zip", partialName);
            if (partial == null) throw coded("BACKUP_LOCATION_READ_ONLY");
            entry.partialUri = partial.toString();
            entry.destinationUri = "";
            requireExportCheckpoint(journal, entry);
            copyToUriAndVerify(context, archive, partial, operation.cancellation, staging);
            operation.cancellation.throwIfCancelled();
            try { finalUri = DocumentsContract.renameDocument(resolver, partial, finalName); }
            catch (Exception unsupportedRename) {
                // A revoked grant is not an unsupported rename: do not create
                // a second target after the provider has denied access.
                if (hasDirectoryPermissionFailure(unsupportedRename)) throw unsupportedRename;
                // Retain the existing copy fallback for other rename failures.
            }
            if (finalUri != null) {
                entry.partialUri = finalUri.toString();
                requireExportCheckpoint(journal, entry);
                operation.cancellation.throwIfCancelled();
                return finalUri;
            }
            finalUri = DocumentsContract.createDocument(resolver, parent, "application/zip", finalName);
            if (finalUri == null) throw coded("BACKUP_COPY_FAILED");
            // Both documents exist during fallback copying. Recovery must know
            // both URIs if this process exits before either can be removed.
            entry.destinationUri = finalUri.toString();
            requireExportCheckpoint(journal, entry);
            copyToUriAndVerify(context, archive, finalUri, operation.cancellation, staging);
            operation.cancellation.throwIfCancelled();
            // Keep both recovery URIs until the temporary document is confirmed gone.
            if (!deletePendingDocument(context, partial)) throw coded("BACKUP_CLEANUP_PENDING");
            entry.partialUri = finalUri.toString();
            entry.destinationUri = "";
            requireExportCheckpoint(journal, entry);
            return finalUri;
        } catch (Throwable error) {
            deleteDocumentQuietly(context, finalUri);
            deleteDocumentQuietly(context, partial);
            if (hasDirectoryPermissionFailure(error)) {
                CodedIOException denied = coded("BACKUP_LOCATION_PERMISSION_LOST");
                denied.initCause(error);
                throw denied;
            }
            throw error;
        }
    }

    private static boolean hasDirectoryPermissionFailure(Throwable error) {
        // Used only at the SAF export boundary, never for local snapshot/database errors.
        for (Throwable current = error; current != null; current = current.getCause()) {
            if (current instanceof SecurityException) return true;
        }
        return false;
    }

    private static void requireExportCheckpoint(BackupOperationJournal journal,
            BackupOperationJournal.Entry entry) throws IOException {
        if (!journal.write(entry, BackupOperationJournal.State.COPYING_TO_DESTINATION, null)) {
            throw coded("BACKUP_COPY_FAILED");
        }
    }

    private static void copyToUriAndVerify(Context context, File archive, Uri destination,
            CancellationToken cancellation, File staging) throws Exception {
        ParcelFileDescriptor descriptor = null;
        OutputStream output = null;
        FileInputStream input = null;
        try {
            descriptor = context.getContentResolver().openFileDescriptor(destination, "w");
            if (descriptor == null) throw coded("BACKUP_LOCATION_READ_ONLY");
            output = new FileOutputStream(descriptor.getFileDescriptor());
            input = new FileInputStream(archive);
            BackupFileUtils.copy(input, output, EXTERNAL_COPY_LIMIT, cancellation);
            output.flush();
            try { descriptor.getFileDescriptor().sync(); } catch (Throwable ignored) {}
        } finally {
            BackupFileUtils.closeQuietly(input);
            BackupFileUtils.closeQuietly(output);
            BackupFileUtils.closeQuietly(descriptor);
        }
        cancellation.throwIfCancelled();
        File verify = new File(staging, "external_verify.slauncherbackup");
        InputStream verifyInput = context.getContentResolver().openInputStream(destination);
        if (verifyInput == null) throw coded("BACKUP_VERIFY_FAILED");
        FileOutputStream verifyOutput = new FileOutputStream(verify);
        try { BackupFileUtils.copy(verifyInput, verifyOutput, EXTERNAL_COPY_LIMIT, cancellation); }
        finally { verifyInput.close(); verifyOutput.close(); }
        if (verify.length() != archive.length()) throw coded("BACKUP_VERIFY_FAILED");
        BackupValidator.validateAndExtract(verify, new File(staging, "external_verified"));
        BackupFileUtils.deleteRecursively(new File(staging, "external_verified"));
        verify.delete();
    }


    public static void cleanupInterruptedBackup(Context context) {
        if (context == null) return;
        final String token = UUID.randomUUID().toString();
        // Startup cleanup only owns disposable backup output, never the desktop database.
        // Keep the existing operation gate until the old journal is handled so a new
        // backup/restore cannot reuse its staging or be mistaken for interrupted work.
        if (!BackupOperationLock.acquire(token)) return;
        final Context app = context.getApplicationContext() == null ? context : context.getApplicationContext();
        try {
            new Thread(new Runnable() {
                public void run() {
                    try { cleanupInterruptedBackupNow(app); }
                    catch (RuntimeException error) { Log.e(TAG, "BACKUP_STARTUP_CLEANUP_FAILED", error); }
                    finally { BackupOperationLock.release(token); }
                }
            }, "DesktopBackupCleanup").start();
        } catch (RuntimeException error) {
            BackupOperationLock.release(token);
            Log.e(TAG, "BACKUP_STARTUP_CLEANUP_START_FAILED", error);
        }
    }

    private static boolean clearInterruptedBackupBeforeStart(Context context, RunningOperation operation) {
        String code = "BACKUP_CLEANUP_PENDING";
        try {
            if (cleanupInterruptedBackupNow(context)) return true;
            if (new BackupOperationJournal(context).read().state == BackupOperationJournal.State.COMPLETE) {
                code = "BACKUP_METADATA_PENDING";
            }
        } catch (BackupOperationJournal.JournalException error) {
            code = error.errorCode;
        } catch (RuntimeException error) {
            Log.w(TAG, "BACKUP_STARTUP_CLEANUP_FAILED", error);
        }
        // Do not overwrite the previous operation's unresolved document URIs.
        BackupOperationLock.release(operation.token);
        if (running == operation) running = null;
        notifyComplete(operation, BackupRestoreResult.error(code, userMessage(code)));
        return false;
    }

    private static boolean cleanupInterruptedBackupNow(Context context) {
        BackupOperationJournal journal = new BackupOperationJournal(context);
        BackupOperationJournal.Entry entry = journal.read();
        if (entry.state == BackupOperationJournal.State.IDLE) return true;
        if (entry.state == BackupOperationJournal.State.COMPLETE) {
            // Older COMPLETE records have no metadata candidate; retain their
            // established behavior without guessing a display name from a URI.
            return entry.completedFileName.length() == 0 || publishCompletedBackupMetadata(context, entry);
        }
        if (entry.stagingPath.length() != 0) {
            File staging = new File(entry.stagingPath);
            BackupFileUtils.deleteRecursively(staging);
            if (!staging.exists()) entry.stagingPath = "";
        }
        String partial = entry.partialUri;
        if (partial.length() != 0 && deletePendingDocument(context, Uri.parse(partial))) {
            entry.partialUri = "";
            if (partial.equals(entry.destinationUri)) entry.destinationUri = "";
        }
        if (entry.destinationUri.length() != 0 && !entry.destinationUri.equals(partial)
                && deletePendingDocument(context, Uri.parse(entry.destinationUri))) {
            entry.destinationUri = "";
        }
        boolean pending = entry.stagingPath.length() != 0 || entry.partialUri.length() != 0
                || entry.destinationUri.length() != 0;
        boolean preferencesSaved = entry.state == BackupOperationJournal.State.PREVIEW_READY
                || context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit()
                        .putBoolean("last_backup_incomplete", true).commit();
        if (pending || !preferencesSaved) {
            // Keep the original nonterminal state and only unresolved resources.
            // A later startup or explicit backup attempt can retry once.
            journal.write(entry, entry.state, "BACKUP_CLEANUP_PENDING");
            Log.w(TAG, "BACKUP_CLEANUP_PENDING");
            return false;
        }
        return journal.write(new BackupOperationJournal.Entry(), BackupOperationJournal.State.IDLE, null);
    }

    private static boolean deletePendingDocument(Context context, Uri uri) {
        try {
            if (DocumentsContract.deleteDocument(context.getContentResolver(), uri)) return true;
        } catch (Exception error) {
            Log.w(TAG, "BACKUP_DOCUMENT_DELETE_FAILED", error);
        }
        // A prior delete may have succeeded before its checkpoint failed. Only
        // a successful empty query confirms absence; null/denied queries do not.
        Cursor cursor = null;
        try {
            cursor = context.getContentResolver().query(uri,
                    new String[] {DocumentsContract.Document.COLUMN_DOCUMENT_ID}, null, null, null);
            return cursor != null && !cursor.moveToNext();
        } catch (Exception error) {
            Log.w(TAG, "BACKUP_DOCUMENT_QUERY_FAILED", error);
            return false;
        } finally { if (cursor != null) cursor.close(); }
    }

    private static void state(RunningOperation operation, BackupOperationJournal journal,
            BackupOperationJournal.Entry entry, BackupOperationJournal.State state,
            String display, boolean cancellable) throws BackupCancelledException, IOException {
        operation.cancellation.throwIfCancelled();
        if (!journal.write(entry, state, null)) throw coded("BACKUP_COPY_FAILED");
        Listener listener = operation.listener;
        if (listener != null) MAIN.post(new StateCallback(listener, display, cancellable));
    }

    private static int readGridMode(Context context) {
        int mode = context.getSharedPreferences("com.smartisanos.launcher_prefs", 0)
                .getInt("prefs_key_launcher_mode", 12);
        return mode == 20 ? 20 : 12;
    }

    private static void deleteDocumentQuietly(Context context, Uri uri) {
        if (context == null || uri == null) return;
        try { DocumentsContract.deleteDocument(context.getContentResolver(), uri); } catch (Throwable ignored) {}
    }

    private static String userMessage(String code) {
        if ("BACKUP_METADATA_PENDING".equals(code)) return "备份文件已保存，但完成记录尚未更新，请稍后重试。";
        if ("BACKUP_JOURNAL_CORRUPT".equals(code)) return "备份记录已损坏，已停止备份并保留原记录，请联系开发者处理。";
        if ("BACKUP_JOURNAL_READ_FAILED".equals(code)) return "无法读取备份记录，已停止备份，请检查存储状态后重试。";
        if ("BACKUP_CLEANUP_PENDING".equals(code)) return "上次备份尚未清理完成，请恢复原目录访问权限后重试。";
        if ("BACKUP_NAME_EXISTS".equals(code)) return "已保留同名备份，请更换名称后保存。";
        if ("BACKUP_TREE_LIST_FAILED".equals(code)) return "无法确认目录内已有备份，请重新选择目录后重试。";
        if ("BACKUP_CANCELLED".equals(code)) return "已取消本次备份";
        if ("BACKUP_LOCATION_PERMISSION_LOST".equals(code)) return "备份目录授权已失效，请重新选择。";
        if ("BACKUP_LOCATION_READ_ONLY".equals(code)) return "所选目录不可写，请重新选择或使用每次另存。";
        if ("BACKUP_NO_SPACE".equals(code)) return "存储空间不足，无法完成备份。";
        if ("BACKUP_VERIFY_FAILED".equals(code)) return "备份文件校验失败。";
        return "桌面备份失败，请稍后重试。";
    }

    private static CodedIOException coded(String code) { return new CodedIOException(code); }
    private static boolean isNoSpace(Throwable error) {
        for (Throwable current = error; current != null; current = current.getCause()) {
            String message = String.valueOf(current.getMessage());
            if (message.contains("ENOSPC") || message.toLowerCase(Locale.US).contains("no space left"))
                return true;
        }
        return false;
    }
    private static final class CodedIOException extends IOException {
        final String code; CodedIOException(String code) { super(code); this.code = code; }
    }
    static final class JSONObjectHolder {
        org.json.JSONObject value; Throwable error; int itemCount;
    }
    private static final class StateCallback implements Runnable {
        final Listener listener; final String state; final boolean cancellable;
        StateCallback(Listener listener, String state, boolean cancellable) {
            this.listener = listener; this.state = state; this.cancellable = cancellable;
        }
        public void run() { listener.onState(state, cancellable); }
    }
    private static void notifyComplete(RunningOperation operation, BackupRestoreResult result) {
        Listener listener = operation.listener;
        if (listener != null) complete(listener, result);
    }
    private static void complete(final Listener listener, final BackupRestoreResult result) {
        if (listener == null) return;
        MAIN.post(new Runnable() { public void run() { listener.onComplete(result); } });
    }
    private static String safeToken(String token) {
        return token == null ? "none" : token.substring(0, Math.min(8, token.length()));
    }
}
