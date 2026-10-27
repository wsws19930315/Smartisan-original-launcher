package com.smartisanos.launcher.quickdesktop;

import android.content.Context;
import android.os.Looper;
import android.os.SystemClock;
import android.view.MotionEvent;
import android.view.View;
import java.lang.reflect.Field;

/** Real production Host/MotionEvent with controlled external actions and controller callbacks. */
public final class QuickDesktopTouchTerminalProbe {
    private static int checks;

    private static void check(boolean value, String message) {
        checks++;
        if (!value) throw new AssertionError(message);
    }

    private static Object field(Object target, String name) throws Exception {
        Field field = target.getClass().getDeclaredField(name);
        field.setAccessible(true);
        return field.get(target);
    }

    private static boolean send(QuickDesktopHostView host, long down, int action, float x) {
        MotionEvent event = MotionEvent.obtain(down, SystemClock.uptimeMillis(), action, x, 600, 0);
        try { return host.onTouchEvent(event); }
        finally { event.recycle(); }
    }

    private static void assertClosed(QuickDesktopHostView host) throws Exception {
        check(host.getOpenProgress() == 0, "zero progress after terminal");
        check(host.getVisibility() == View.GONE, "closed host must be GONE");
        check(!((Boolean) field(host, "touchSequenceActive")), "terminal releases touch sequence");
        check(field(host, "velocityTracker") == null, "terminal releases velocity tracker");
        check(QuickDesktopController.closed == 1, "terminal calls controller cleanup once");
    }

    public static void main(String[] args) {
        try {
            if (Looper.myLooper() == null) Looper.prepareMainLooper();
            Class<?> activityThread = Class.forName("android.app.ActivityThread");
            Object thread = activityThread.getMethod("systemMain").invoke(null);
            Context system = (Context) activityThread.getMethod("getSystemContext").invoke(thread);
            Context context = system.createPackageContext("com.smartisanos.launcher",
                    Context.CONTEXT_IGNORE_SECURITY);
            QuickDesktopHostView host = new QuickDesktopHostView(
                    new android.view.ContextThemeWrapper(context, android.R.style.Theme_DeviceDefault));
            host.measure(View.MeasureSpec.makeMeasureSpec(1000, View.MeasureSpec.EXACTLY),
                    View.MeasureSpec.makeMeasureSpec(2000, View.MeasureSpec.EXACTLY));
            host.layout(0, 0, 1000, 2000);
            for (int round = 0; round < 20; round++) {
                for (int terminal : new int[]{MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL}) {
                    host.setOpenProgress(1, "probe-open");
                    QuickDesktopController.closed = 0;
                    long down = SystemClock.uptimeMillis();
                    check(send(host, down, MotionEvent.ACTION_DOWN, 900), "open host accepts DOWN");
                    check(send(host, down, MotionEvent.ACTION_MOVE, -200), "drag reaches zero");
                    check(host.getOpenProgress() == 0, "drag clamped at zero");
                    check(QuickDesktopController.closed == 0, "active drag waits for terminal");
                    check(send(host, down, terminal, -200), "zero-progress terminal must be consumed");
                    assertClosed(host);
                    check(!send(host, down, MotionEvent.ACTION_DOWN, 500), "closed host rejects next DOWN");
                    check(!send(host, down, MotionEvent.ACTION_MOVE, 600), "closed host rejects stray MOVE");
                    check(!send(host, down, terminal, 600), "closed host rejects duplicate terminal");
                    check(QuickDesktopController.closed == 1, "stray events do not repeat cleanup");
                }
                host.setOpenProgress(1, "probe-reverse-open");
                QuickDesktopController.closed = 0;
                long down = SystemClock.uptimeMillis();
                send(host, down, MotionEvent.ACTION_DOWN, 900);
                send(host, down, MotionEvent.ACTION_MOVE, -200);
                check(send(host, down, MotionEvent.ACTION_MOVE, 600), "zero-point reversal remains owned");
                check(host.getOpenProgress() > .69f && host.getOpenProgress() < .71f,
                        "reversal restores continuous progress");
                check(QuickDesktopController.closed == 0, "reversal does not prematurely remove host");
                send(host, down, MotionEvent.ACTION_MOVE, -200);
                check(send(host, down, MotionEvent.ACTION_CANCEL, -200), "reversal terminal consumed");
                assertClosed(host);
            }
            host.closeImmediately("probe-finish");
            System.out.println("PASS QUICKDESKTOP_TOUCH_TERMINAL checks=" + checks);
            System.exit(0);
        } catch (Throwable error) {
            error.printStackTrace();
            System.exit(1);
        }
    }
}
