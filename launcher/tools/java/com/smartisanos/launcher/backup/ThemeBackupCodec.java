package com.smartisanos.launcher.backup;

import android.content.Context;

import org.json.JSONObject;
import java.io.File;
import android.graphics.BitmapFactory;
import com.smartisanos.launcher.theme.MaintainedLauncherSettingsHost;

public final class ThemeBackupCodec {
    private ThemeBackupCodec() {}

    public static JSONObject encode(Context context) throws Exception {
        JSONObject root = new JSONObject();
        android.content.SharedPreferences settings = context.getSharedPreferences("launcher_settings", 0);
        android.content.SharedPreferences launcher = context.getSharedPreferences("com.smartisanos.launcher_prefs", 0);
        root.put("themeId", first(settings.getString("launcher_theme", null),
                launcher.getString("launcher_theme", "")));
        root.put("themePackage", first(settings.getString("launcher_theme_package", null),
                launcher.getString("launcher_theme_package", "")));
        root.put("transparent", readBoolean(settings, launcher, "launcher_grid_theme", false));
        root.put("aero", readBoolean(settings, launcher, "launcher_aero_theme", false));
        return root;
    }

    public static JSONObject encode(Context context, File staging,
            DesktopBackupController.CancellationToken cancellation) throws Exception {
        JSONObject root = encode(context);
        File file = new File(staging, "wallpaper/selected-image");
        boolean selected = MaintainedLauncherSettingsHost.exportWallpaperSourceForBackup(context, file, cancellation);
        JSONObject wallpaper = new JSONObject().put("version", 1)
                .put("source", selected ? "selected" : "default")
                .put("previousTheme", MaintainedLauncherSettingsHost.wallpaperBackupPreviousTheme(context));
        if (selected) wallpaper.put("file", "wallpaper/selected-image");
        root.put("wallpaper", wallpaper);
        validateWallpaper(root, staging);
        return root;
    }

    public static void validateWallpaper(JSONObject theme, File extractedRoot) throws Exception {
        if (!theme.has("wallpaper")) return; // Historical archives retain the current wallpaper.
        JSONObject wallpaper = theme.getJSONObject("wallpaper");
        if (wallpaper.getInt("version") != 1) throw new IllegalArgumentException("Unsupported wallpaper backup version");
        String previous = wallpaper.optString("previousTheme", "");
        if (previous.length() > 256 || "smartisan_theme_trans".equals(previous)) {
            throw new IllegalArgumentException("Invalid underlying wallpaper theme");
        }
        String source = wallpaper.getString("source");
        if ("default".equals(source)) {
            if (wallpaper.has("file")) throw new IllegalArgumentException("Default wallpaper contains an image reference");
            return;
        }
        if (!"selected".equals(source) || !"wallpaper/selected-image".equals(wallpaper.optString("file", ""))) {
            throw new IllegalArgumentException("Invalid wallpaper backup source");
        }
        File file = new File(extractedRoot, "wallpaper/selected-image");
        if (!file.isFile() || file.length() <= 0 || file.length() > 20L * 1024L * 1024L) {
            throw new IllegalArgumentException("Invalid wallpaper backup image size");
        }
        BitmapFactory.Options bounds = new BitmapFactory.Options();
        bounds.inJustDecodeBounds = true;
        BitmapFactory.decodeFile(file.getAbsolutePath(), bounds);
        if (bounds.outWidth <= 0 || bounds.outHeight <= 0
                || (long) bounds.outWidth * bounds.outHeight > 100000000L) {
            throw new IllegalArgumentException("Invalid wallpaper backup image");
        }
    }

    public static void restoreWallpaper(Context context, JSONObject theme, File extractedRoot) throws Exception {
        validateWallpaper(theme, extractedRoot);
        JSONObject wallpaper = theme.optJSONObject("wallpaper");
        if (wallpaper == null) return;
        File source = "selected".equals(wallpaper.getString("source"))
                ? new File(extractedRoot, "wallpaper/selected-image") : null;
        MaintainedLauncherSettingsHost.restoreWallpaperSourceFromBackup(context, source,
                wallpaper.optString("previousTheme", ""));
    }

    public static boolean isThemePackageAvailable(Context context, String packageName) {
        if (packageName == null || packageName.length() == 0) return true;
        try { context.getPackageManager().getPackageInfo(packageName, 0); return true; }
        catch (Throwable ignored) { return false; }
    }

    private static boolean readBoolean(android.content.SharedPreferences first,
            android.content.SharedPreferences second, String key, boolean fallback) {
        if (first.contains(key)) {
            Object value = first.getAll().get(key);
            if (value instanceof Boolean) return ((Boolean) value).booleanValue();
            if (value instanceof Integer) return ((Integer) value).intValue() != 0;
        }
        if (second.contains(key)) {
            Object value = second.getAll().get(key);
            if (value instanceof Boolean) return ((Boolean) value).booleanValue();
            if (value instanceof Integer) return ((Integer) value).intValue() != 0;
        }
        return fallback;
    }

    private static String first(String first, String second) {
        return first != null && first.length() != 0 ? first : (second == null ? "" : second);
    }
}
