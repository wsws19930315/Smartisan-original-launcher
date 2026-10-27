package com.smartisanos.launcher.quickdesktop;

import android.graphics.Bitmap;
import android.os.Looper;
import android.os.Handler;
import java.lang.reflect.Field;
import java.util.concurrent.ExecutorService;

/** Production capture handoff: cancellation while readPixels runs must retain the new owner. */
public final class QuickDesktopCaptureGenerationProbe {
    private static int checks;
    private static void check(boolean ok, String why) {
        if (!ok) throw new AssertionError(why);
        checks++;
    }
    private static Field field(String name) throws Exception {
        Field f = QuickDesktopBackgroundCapture.class.getDeclaredField(name);
        f.setAccessible(true);
        return f;
    }
    private static void publish(int generation, Object host) throws Exception {
        field("generation").setInt(null, generation);
        field("pendingGeneration").setInt(null, generation);
        field("pendingHost").set(null, host);
        field("glCaptureRequested").setBoolean(null, true);
    }

    private static void controller(String name, Object value) throws Exception {
        Field field = QuickDesktopController.class.getDeclaredField(name);
        field.setAccessible(true);
        field.set(null, value);
    }

    private static Object controller(String name) throws Exception {
        Field field = QuickDesktopController.class.getDeclaredField(name);
        field.setAccessible(true);
        return field.get(null);
    }

    private static void arm(QuickDesktopHostView host, int generation) throws Exception {
        controller("hostView", host);
        controller("captureStartedForGesture", true);
        controller("backgroundReadyForGesture", false);
        controller("openAfterBackgroundReady", true);
        controller("rootGestureCancelled", true);
        host.setOpenProgress(.001f, "probe-deferred-open");
        publish(generation, host);
    }

    private static void closed(QuickDesktopHostView host) throws Exception {
        check(host.getOpenProgress() == 0, "failed capture retained deferred opening");
        check(!((Boolean) controller("captureStartedForGesture")), "failed capture retained request");
        check(!((Boolean) controller("openAfterBackgroundReady")), "failed capture retained open target");
        check(!((Boolean) controller("backgroundReadyForGesture")), "failed capture marked ready");
        check(QuickDesktopController.hasCancelledRootGesture(), "failure lost cancelled GL target guard");
    }

    private static void fail(Throwable error) {
        error.printStackTrace(); System.exit(1);
    }

    private static void failureChecks(final QuickDesktopHostView host) throws Exception {
        arm(host, 20);
        QuickDesktopBackgroundCapture.onGlFrame(null, QuickDesktopBackgroundCapture.takeGlCaptureGeneration());
        new Handler(Looper.getMainLooper()).post(new Runnable() {
            @Override public void run() { try {
                closed(host);
                arm(host, 22);
                QuickDesktopBackgroundCapture.onGlFrame(null, QuickDesktopBackgroundCapture.takeGlCaptureGeneration());
                arm(host, 24); // Failure 22 is queued on MAIN while a newer request takes ownership.
                new Handler(Looper.getMainLooper()).post(new Runnable() {
                    @Override public void run() { try {
                        check(host.getOpenProgress() > 0, "old null failure closed new gesture");
                        check((Boolean) controller("captureStartedForGesture"), "old failure cleared new request");
                        final Bitmap blank = Bitmap.createBitmap(8, 8, Bitmap.Config.ARGB_8888);
                        QuickDesktopBackgroundCapture.onGlFrame(blank,
                                QuickDesktopBackgroundCapture.takeGlCaptureGeneration());
                        // The existing serial worker posts failure before this barrier posts its assertion.
                        ((ExecutorService) field("WORKER").get(null)).execute(new Runnable() {
                            @Override public void run() {
                                new Handler(Looper.getMainLooper()).post(new Runnable() {
                                    @Override public void run() { try {
                                        check(blank.isRecycled(), "blank frame not released");
                                        closed(host);
                                        arm(host, 26);
                                        final Bitmap staleBlank = Bitmap.createBitmap(8, 8, Bitmap.Config.ARGB_8888);
                                        QuickDesktopBackgroundCapture.onGlFrame(staleBlank,
                                                QuickDesktopBackgroundCapture.takeGlCaptureGeneration());
                                        QuickDesktopBackgroundCapture.cancel("probe-new-gesture");
                                        arm(host, 28);
                                        ((ExecutorService) field("WORKER").get(null)).execute(new Runnable() {
                                            @Override public void run() {
                                                new Handler(Looper.getMainLooper()).post(new Runnable() {
                                                    @Override public void run() { try {
                                                        check(staleBlank.isRecycled(), "stale blank not released");
                                                        check(host.getOpenProgress() > 0, "stale blank closed new gesture");
                                                        check((Boolean) controller("openAfterBackgroundReady"), "stale blank cleared new target");
                                                        QuickDesktopController.onHomeIntent();
                                                        check(host.getOpenProgress() == 0, "HOME failed after capture failure");
                                                        System.out.println("PASS CAPTURE_GENERATION checks=" + checks);
                                                        System.exit(0);
                                                    } catch (Throwable error) { fail(error); } }
                                                });
                                            }
                                        });
                                    } catch (Throwable error) { fail(error); } }
                                });
                            }
                        });
                    } catch (Throwable error) { fail(error); } }
                });
            } catch (Throwable error) { fail(error); } }
        });
        Looper.loop();
    }
    public static void main(String[] args) {
        try {
            if (Looper.myLooper() == null) Looper.prepareMainLooper();
            Class<?> type = Class.forName("sun.misc.Unsafe");
            Field f = type.getDeclaredField("theUnsafe");
            f.setAccessible(true);
            Object host = type.getMethod("allocateInstance", Class.class)
                    .invoke(f.get(null), QuickDesktopHostView.class);
            publish(10, host);
            int old = QuickDesktopBackgroundCapture.takeGlCaptureGeneration();
            check(old == 10, "wrong first claim");
            check(QuickDesktopBackgroundCapture.isGlCaptureCurrent(old), "valid claim skipped before readback");
            check(!QuickDesktopBackgroundCapture.isGlCaptureCurrent(0), "zero claim allowed readback");
            check(QuickDesktopBackgroundCapture.takeGlCaptureGeneration() == 0, "duplicate claim");
            check(QuickDesktopBackgroundCapture.isGlCaptureCurrent(old), "claim flag consumed valid readback");
            QuickDesktopBackgroundCapture.cancel("probe-cancel-in-read");
            check(!QuickDesktopBackgroundCapture.isGlCaptureCurrent(old), "cancel during scene update allowed readback");
            publish(12, host);
            check(!QuickDesktopBackgroundCapture.isGlCaptureCurrent(old), "replacement allowed stale readback");
            check(QuickDesktopBackgroundCapture.isGlCaptureCurrent(12), "replacement lost valid readback");
            Bitmap oldFrame = Bitmap.createBitmap(8, 8, Bitmap.Config.ARGB_8888);
            QuickDesktopBackgroundCapture.onGlFrame(oldFrame, old);
            check(oldFrame.isRecycled(), "cancelled read not discarded");
            check(field("pendingHost").get(null) == host, "old read stole new host");
            check(QuickDesktopBackgroundCapture.takeGlCaptureGeneration() == 12, "new request lost");
            QuickDesktopBackgroundCapture.cancel("probe-cancel-after-claim");
            Bitmap lateFrame = Bitmap.createBitmap(8, 8, Bitmap.Config.ARGB_8888);
            QuickDesktopBackgroundCapture.onGlFrame(lateFrame, 12);
            check(lateFrame.isRecycled(), "late completion retained");
            check(QuickDesktopBackgroundCapture.takeGlCaptureGeneration() == 0, "cancel still requested");
            publish(14, host);
            int valid = QuickDesktopBackgroundCapture.takeGlCaptureGeneration();
            QuickDesktopBackgroundCapture.onGlFrame(null, valid);
            check(!QuickDesktopBackgroundCapture.isGlCaptureCurrent(valid), "completed claim allowed another readback");
            check(field("pendingHost").get(null) == null, "empty result retained host");
            check(QuickDesktopBackgroundCapture.takeGlCaptureGeneration() == 0, "empty result retried");
            failureChecks((QuickDesktopHostView) host);
        } catch (Throwable error) { error.printStackTrace(); System.exit(1); }
    }
}
