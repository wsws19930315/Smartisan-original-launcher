package com.smartisanos.launcher.theme;

import android.graphics.Paint;
import java.util.HashMap;

/** Exercise the built admission helper without creating a second texture owner. */
public final class FolderLabelTextureProbe {
    private static int checks;
    public static class Texture {
        float width = 118, height = 35;
        int generation = com.smartisanos.launcher.gesture.LauncherHomeCompat.getEglContextGeneration();
        public int getContextGeneration() { return generation; }
        public float getWidth() { return width; }
        public float getHeight() { return height; }
    }
    public static class Registry {
        final HashMap<String, Texture> textures = new HashMap<>();
        public Texture bb(String key) { return textures.get(key); }
    }
    private static void check(boolean value, String message) {
        checks++; if (!value) throw new AssertionError(message);
    }
    private static boolean keep(Registry registry, Paint paint, Paint owner, int h, int w) {
        return LauncherSettingBridge.retainFolderLabelTexture("label", paint, h, w, registry, owner);
    }
    public static void main(String[] args) {
        try {
            Paint owner = new Paint(); Registry registry = new Registry(); Texture original = new Texture();
            check(!keep(registry, owner, owner, 35, 118), "missing descriptor follows original rebuild");
            registry.textures.put("label", original);
            for (int i = 0; i < 500; i++) {
                check(keep(registry, owner, owner, 35, 118), "same folder generation and dimensions retained");
            }
            check(registry.textures.get("label") == original && registry.textures.size() == 1,
                    "engine descriptor and owner unchanged");
            com.smartisanos.launcher.gesture.LauncherHomeCompat.onEglContextCreated();
            check(!keep(registry, owner, owner, 35, 118), "old EGL descriptor excluded despite same key/size");
            original.generation = com.smartisanos.launcher.gesture.LauncherHomeCompat.getEglContextGeneration();
            check(keep(registry, owner, owner, 35, 118), "newly uploaded current-context descriptor retained");
            check(!keep(registry, new Paint(owner), owner, 35, 118),
                    "other paint identity excluded even when appearance matches");
            Paint next = new Paint(owner);
            check(!keep(registry, owner, next, 35, 118), "previous generation excluded after owner rebuild");
            registry.textures.clear();
            check(!keep(registry, next, next, 35, 118), "theme/context reset remains a cache miss");
            registry.textures.put("label", original);
            original.width = 119;
            check(!keep(registry, owner, owner, 35, 118), "current descriptor width reread");
            original.width = 118; original.height = 36;
            check(!keep(registry, owner, owner, 35, 118), "current descriptor height reread");
            original.height = 35;
            check(!keep(registry, owner, owner, 70, 236), "physical/large-screen size mismatch rebuilds");
            for (int size : new int[] {0, -1}) {
                check(!keep(registry, owner, owner, size, 118), "invalid height excluded");
                check(!keep(registry, owner, owner, 35, size), "invalid width excluded");
            }
            check(!keep(registry, null, null, 35, 118), "null paint excluded");
            check(!keep(null, owner, owner, 35, 118), "missing owner excluded");
            check(!LauncherSettingBridge.retainFolderLabelTexture(
                    "renamed", owner, 35, 118, registry, owner), "new label key rebuilds");
            registry.textures.remove("label");
            check(!keep(registry, owner, owner, 35, 118), "explicit texture release remains authoritative");
            System.out.println("PASS FOLDER_LABEL_TEXTURE checks=" + checks);
        } catch (Throwable failure) { failure.printStackTrace(); System.exit(1); }
    }
}
