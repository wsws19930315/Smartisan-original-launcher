package com.smartisanos.launcher.gesture;

import android.app.Activity;
import android.app.KeyguardManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.opengl.GLSurfaceView;
import android.os.Build;
import android.os.Bundle;
import android.os.Message;
import android.os.PowerManager;
import android.os.Process;
import android.os.SystemClock;
import android.os.Trace;
import android.provider.Settings;
import android.util.Log;
import android.view.SurfaceView;
import android.view.View;
import android.view.WindowManager;
import com.smartisanos.launcher.theme.LauncherSettingBridge;
import java.lang.ref.WeakReference;
import java.util.concurrent.atomic.AtomicInteger;

/** Reuses the original HOME scene; optional markers never imply display presentation. */
public final class LauncherHomeCompat {
    private static final String TAG = "SmartisanHome";
    private static final String EXTRA_FROM_HOME_KEY = "android.intent.extra.FROM_HOME_KEY";
    private static final String DIAGNOSTICS = "launcher_home_diagnostics_enabled";
    private static final String ATTACHMENT = "launcher_home_surface_attachment_experiment";
    private static final String WALLPAPER = "launcher_home_opaque_wallpaper_experiment";
    private static volatile boolean diagnostics;
    private static volatile int resume;
    private static volatile int surfaceGeneration;
    private static volatile int contextGeneration;
    private static volatile int sceneIdentity;
    private static volatile int frameIndex;
    private static final AtomicInteger FRAMES = new AtomicInteger();
    private static final AtomicInteger REDRAW_IDS = new AtomicInteger();
    private static WeakReference<GLSurfaceView> surfaceRef;
    private static WeakReference<Activity> activityRef;
    private static boolean originalWallpaper;
    private static boolean wallpaperCaptured;
    private static boolean wallpaperAdjusted;
    private static int lifecycleStrategy;
    private static boolean experimentPaused;

    private LauncherHomeCompat() { }

    /** Returns true when the alias has handed off; it never initializes an original scene. */
    public static boolean redirectLauncherAlias(Activity activity) {
        if (activity == null || activity.getComponentName() == null
                || !"com.smartisanos.launcher.LauncherAlias".equals(
                        activity.getComponentName().getClassName())) return false;
        Intent home = createLauncherHomeIntent(activity);
        if (home.getComponent() != null) return false;
        if (activity.getIntent() != null) home.putExtras(activity.getIntent());
        home.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP
                | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        // Mark the alias finishing before task lookup, or singleTask can deliver
        // the HOME intent back to this alias and finish the intended destination.
        activity.finish();
        try {
            activity.startActivity(home);
            Log.i(TAG, "HOME_ENTRY_REDIRECTED alias=LauncherAlias target=Launcher");
        } catch (android.content.ActivityNotFoundException | SecurityException error) {
            Log.w(TAG, "HOME_ENTRY_REDIRECT_FAILED", error);
        }
        return true;
    }

    /** Shared by entry, settings and coordinated reload; callers retain their own flags/extras. */
    public static Intent createLauncherHomeIntent(Context context) {
        Intent home = new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_HOME);
        // Pie treats an app-specified component as a standard task. A package
        // restriction still resolves our single HOME entry without changing HOME.
        if (isCurrentDefaultHome(context)) home.setPackage(context.getPackageName());
        else home.setClassName(context.getPackageName(), "com.smartisanos.launcher.Launcher");
        return home;
    }

    private static int setting(Context context, String key) {
        try { return Settings.Global.getInt(context.getContentResolver(), key, 0); }
        catch (SecurityException error) { return 0; }
    }

    private static boolean diagnosticsEnabled(Context context) {
        return Log.isLoggable(TAG, Log.DEBUG) || setting(context, DIAGNOSTICS) != 0;
    }

    public static void onLauncherCreated(Activity activity) {
        activityRef = new WeakReference<Activity>(activity);
        wallpaperCaptured = false;
        wallpaperAdjusted = false;
        diagnostics = diagnosticsEnabled(activity);
        mark("ACTIVITY_CREATE");
        inspectGestureContract(activity.getIntent(), "CREATE");
    }

    public static void bindSurface(GLSurfaceView surface) {
        surfaceRef = new WeakReference<GLSurfaceView>(surface);
        diagnostics = diagnosticsEnabled(surface.getContext());
        lifecycleStrategy = 0;
        experimentPaused = false;
        applySurfaceExperiment(surface);
        mark("SURFACE_BIND");
    }

    private static void applySurfaceExperiment(GLSurfaceView surface) {
        // The default path keeps the original platform lifecycle. The API-34
        // experiment is isolated and changes no EGL, format, z-order or engine code.
        if (Build.VERSION.SDK_INT < 34) return;
        int requested = diagnostics && setting(surface.getContext(), ATTACHMENT) != 0 ? 2 : 0;
        if (requested == lifecycleStrategy) return;
        Api34.apply(surface, requested);
        lifecycleStrategy = requested;
        mark("SURFACE_LIFECYCLE strategy=" + requested);
    }

    private static final class Api34 {
        static void apply(SurfaceView surface, int strategy) {
            surface.setSurfaceLifecycle(strategy == 2
                    ? SurfaceView.SURFACE_LIFECYCLE_FOLLOWS_ATTACHMENT
                    : SurfaceView.SURFACE_LIFECYCLE_DEFAULT);
        }
    }

    public static void onLauncherResuming(Activity activity) {
        diagnostics = diagnosticsEnabled(activity);
        resume++;
        frameIndex = 0;
        FRAMES.set(diagnostics ? 4 : 0);
        GLSurfaceView surface = surface();
        if (surface != null) {
            if (experimentPaused) {
                surface.onResume();
                experimentPaused = false;
                mark("EXPERIMENT_GL_RESUME");
            }
            applySurfaceExperiment(surface);
        }
        applyWallpaperExperiment(activity);
        window(activity, "RESUME_BEGIN");
    }

    public static void onLauncherResumed(Activity activity) {
        // J/Eb already restore their existing scene and request an engine update.
        // Do not hide/show a valid Surface, re-layout it, or recreate its textures.
        window(activity, "RESUME_END");
    }

    private static void applyWallpaperExperiment(Activity activity) {
        boolean experiment = diagnostics && setting(activity, WALLPAPER) != 0;
        if (!experiment && !wallpaperAdjusted) return;
        int flag = WindowManager.LayoutParams.FLAG_SHOW_WALLPAPER;
        if (!wallpaperCaptured) {
            originalWallpaper = (activity.getWindow().getAttributes().flags & flag) != 0;
            wallpaperCaptured = true;
        }
        String theme = LauncherSettingBridge.readString(activity, "launcher_theme", "smartisan_theme_black");
        boolean wallpaperTheme = LauncherSettingBridge.readTransparentMode(activity)
                || "smartisan_theme_aero".equals(theme) || "smartisan_theme_trans".equals(theme);
        boolean show = originalWallpaper;
        if (!wallpaperTheme && experiment) show = false;
        boolean current = (activity.getWindow().getAttributes().flags & flag) != 0;
        if (current != show) {
            if (show) activity.getWindow().addFlags(flag);
            else activity.getWindow().clearFlags(flag);
            mark("WALLPAPER_AB show=" + show + " theme=" + theme);
        }
        wallpaperAdjusted = show != originalWallpaper;
    }

    public static void onLauncherPaused(Activity activity) { window(activity, "PAUSE"); }
    public static void onLauncherStopped(Activity activity) {
        window(activity, "STOP");
        // A retained Surface must not keep scheduling engine updates
        // running behind another app. The experiment alone uses the existing
        // GLSurfaceView pause/resume API; the default lifecycle is unchanged.
        GLSurfaceView surface = surface();
        if (lifecycleStrategy == 2 && surface != null && !experimentPaused) {
            surface.onPause();
            experimentPaused = true;
            mark("EXPERIMENT_GL_PAUSE");
        }
    }
    public static void onLauncherFocusChanged(Activity activity, boolean focused) {
        window(activity, "FOCUS value=" + focused);
    }
    public static void onHomeIntent(Activity activity, Intent intent) {
        inspectGestureContract(intent, "NEW_INTENT");
        if (isStandardAndroidHome(intent)) window(activity, "HOME_INTENT");
    }
    private static void inspectGestureContract(Intent intent, String source) {
        if (!diagnostics || !isStandardAndroidHome(intent)) return;
        try {
            Bundle contract = intent.getBundleExtra("gesture_nav_contract_v1");
            Message callback = contract == null ? null :
                    (Message) contract.getParcelable("android.intent.extra.REMOTE_CALLBACK");
            mark("GESTURE_CONTRACT source=" + source + " present=" + (contract != null)
                    + " callback=" + (callback != null && callback.replyTo != null));
        } catch (android.os.BadParcelableException | ClassCastException error) {
            mark("GESTURE_CONTRACT malformed=" + error.getClass().getSimpleName());
        }
    }

    public static void onLauncherDestroyed(Activity activity) {
        window(activity, "ACTIVITY_DESTROY");
        Activity current = activityRef == null ? null : activityRef.get();
        if (current == activity) {
            activityRef = null;
            surfaceRef = null;
            FRAMES.set(0);
        }
    }

    public static void onSurfaceAttached(GLSurfaceView surface) { surfaceEvent(surface, "ATTACH"); }
    public static void onSurfaceDetached(GLSurfaceView surface) { surfaceEvent(surface, "DETACH"); }
    public static void onWindowVisibilityChanged(GLSurfaceView surface, int visibility) {
        surfaceEvent(surface, "WINDOW_VISIBLE value=" + visibility);
    }
    public static void onSurfaceCreated(GLSurfaceView surface) {
        surfaceGeneration++;
        surfaceEvent(surface, "SURFACE_CREATE");
    }
    public static void onSurfaceDestroyed(GLSurfaceView surface) {
        surfaceEvent(surface, "SURFACE_DESTROY");
    }
    public static void onSurfaceSizeChanged(GLSurfaceView surface, int width, int height) {
        surfaceEvent(surface, "SURFACE_SIZE width=" + width + " height=" + height);
    }

    /** Observe the actual platform callback without changing its thread or ordering. */
    public static Runnable traceSurfaceRedraw(GLSurfaceView view, final Runnable finishDrawing) {
        if (!diagnostics) return finishDrawing;
        final int id = REDRAW_IDS.incrementAndGet();
        mark("SURFACE_REDRAW_REQUEST id=" + id + " view=" + System.identityHashCode(view));
        return new Runnable() {
            @Override public void run() {
                mark("SURFACE_REDRAW_CALLBACK_BEGIN id=" + id + " presented=unknown");
                try {
                    finishDrawing.run();
                } finally {
                    mark("SURFACE_REDRAW_CALLBACK_END id=" + id + " presented=unknown");
                }
            }
        };
    }
    public static void onEglContextCreated() {
        contextGeneration++;
        mark("EGL_CONTEXT_CREATE");
    }
    public static int getEglContextGeneration() {
        return contextGeneration;
    }
    public static void onRendererSizeChanged(int width, int height) {
        mark("GL_SURFACE_SIZE width=" + width + " height=" + height);
    }
    public static void onSceneCreate(Object scene) {
        sceneIdentity = System.identityHashCode(scene);
        mark("SCENE_CREATE");
    }

    /** Before GLSurfaceView performs EGL swap; this is not a first-present signal. */
    public static void onRendererFrameComplete() {
        if (!diagnostics || FRAMES.get() <= 0) return;
        int left = FRAMES.getAndDecrement();
        if (left <= 0) return;
        final int session = resume;
        final int generation = surfaceGeneration;
        final int index = ++frameIndex;
        mark("GL_DRAW_COMPLETE frame=" + index + " presented=unknown");
        GLSurfaceView surface = surface();
        if (surface == null) return;
        surface.queueEvent(new Runnable() {
            @Override public void run() {
                if (diagnostics && resume == session && surfaceGeneration == generation) {
                    // The next GL loop follows the swap attempt. It gives neither
                    // a swap return code nor a compositor/display present fence.
                    mark("GL_LOOP_AFTER_SWAP_ATTEMPT frame=" + index + " presented=unknown");
                }
            }
        });
    }

    private static GLSurfaceView surface() { return surfaceRef == null ? null : surfaceRef.get(); }

    private static void surfaceEvent(GLSurfaceView surface, String event) {
        if (!diagnostics) return;
        mark(event + " view=" + System.identityHashCode(surface)
                + " valid=" + surface.getHolder().getSurface().isValid()
                + " attached=" + surface.isAttachedToWindow()
                + " visibility=" + surface.getVisibility()
                + " windowVisibility=" + surface.getWindowVisibility());
    }

    private static void window(Activity activity, String event) {
        if (!diagnostics) return;
        KeyguardManager keyguard = (KeyguardManager) activity.getSystemService(Context.KEYGUARD_SERVICE);
        PowerManager power = (PowerManager) activity.getSystemService(Context.POWER_SERVICE);
        View decor = activity.getWindow().getDecorView();
        GLSurfaceView surface = surface();
        mark(event + " activity=" + System.identityHashCode(activity)
                + " focus=" + activity.hasWindowFocus()
                + " decorVisibility=" + decor.getWindowVisibility()
                + " flags=" + Integer.toHexString(activity.getWindow().getAttributes().flags)
                + " surfaceValid=" + (surface != null && surface.getHolder().getSurface().isValid())
                + " interactive=" + (power != null && power.isInteractive())
                + " locked=" + (keyguard != null && keyguard.isKeyguardLocked()));
    }

    public static void mark(String event) {
        if (!diagnostics) return;
        Log.i(TAG, "HOME_TIMING " + event + " elapsed_ns=" + SystemClock.elapsedRealtimeNanos()
                + " monotonic_ns=" + System.nanoTime() + " pid=" + Process.myPid()
                + " resume=" + resume + " surfaceGen=" + surfaceGeneration
                + " contextGen=" + contextGeneration + " scene=" + sceneIdentity
                + " thread=" + Thread.currentThread().getName());
        String trace = "HOME:" + event;
        Trace.beginSection(trace.length() > 120 ? trace.substring(0, 120) : trace);
        Trace.endSection();
    }


    public static void logHomeIntentReceived(Intent intent) {
        if (intent == null) {
            return;
        }
        Log.i(TAG, "HOME_INTENT_RECEIVED action=" + intent.getAction()
                + " categories=" + intent.getCategories()
                + " flags=0x" + Integer.toHexString(intent.getFlags())
                + " FROM_HOME_KEY=" + intent.getBooleanExtra(EXTRA_FROM_HOME_KEY, false));
    }

    public static boolean isStandardAndroidHome(Intent intent) {
        return intent != null
                && Intent.ACTION_MAIN.equals(intent.getAction())
                && intent.hasCategory(Intent.CATEGORY_HOME);
    }

    public static boolean isCurrentDefaultHome(Context context) {
        if (context == null) {
            return false;
        }
        try {
            Intent home = new Intent(Intent.ACTION_MAIN);
            home.addCategory(Intent.CATEGORY_HOME);
            ResolveInfo resolved = context.getPackageManager().resolveActivity(
                    home, PackageManager.MATCH_DEFAULT_ONLY);
            return resolved != null
                    && resolved.activityInfo != null
                    && context.getPackageName().equals(resolved.activityInfo.packageName);
        } catch (Throwable error) {
            Log.w(TAG, "HOME_GATE_DEFAULT_HOME query_failed", error);
            return false;
        }
    }

    public static void logHomeGateFlags(int flags) {
        boolean broughtToFront = (flags & 0x00400000) == 0x00400000;
        Log.i(TAG, "HOME_FLAGS_HEX flags=0x" + Integer.toHexString(flags));
        Log.i(TAG, "HOME_GATE_FLAGS flags=0x" + Integer.toHexString(flags));
        Log.i(TAG, "HOME_BROUGHT_TO_FRONT " + broughtToFront);
        Log.i(TAG, "HOME_GATE_BROUGHT_TO_FRONT " + broughtToFront);
        Log.i(TAG, "HOME_ALREADY_ON_HOME " + !broughtToFront);
        Log.i(TAG, "HOME_GATE_ALREADY_ON_HOME " + !broughtToFront);
    }

    public static void logHomeGate(String gate, boolean value) {
        Log.i(TAG, gate + " " + value);
    }

    public static void logHomeGateEvent(String event) {
        Log.i(TAG, event);
    }

    public static void logPageViewNotReady() {
        logHomeGateEvent("HOME_GATE_PAGE_VIEW_NOT_READY");
    }

    public static void logOriginalHomeNoOp() {
        logHomeGateEvent("HOME_ALREADY_ON_FIRST_PAGE reason=original_noop_or_debounced");
    }

    public static void logOriginalHomeAnimationRequested() {
        logHomeGateEvent("HOME_CREATE_SCROLL_EVENT_SENT");
        logHomeGateEvent("HOME_RETURN_TO_FIRST_PAGE original_animation_requested=true");
    }
}
