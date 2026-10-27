import android.os.SystemClock;
import android.view.InputDevice;
import android.view.InputEvent;
import android.view.MotionEvent;
import java.lang.reflect.Method;

/** Shell-only gesture input with one downTime for the complete pointer stream. */
public final class TouchInput {
    private static Object manager;
    private static Method inject;

    private static void send(long down, int action, float x, float y) throws Exception {
        long eventTime = SystemClock.uptimeMillis();
        long monotonicNanos = System.nanoTime();
        MotionEvent event = MotionEvent.obtain(down, eventTime, action, x, y, 0);
        event.setSource(InputDevice.SOURCE_TOUCHSCREEN);
        try {
            if (!Boolean.TRUE.equals(inject.invoke(manager, event, 2))) {
                throw new IllegalStateException("Touch injection was rejected");
            }
            if (action != MotionEvent.ACTION_MOVE) {
                System.out.println("TOUCH_EVENT action=" + action + " eventTimeMillis=" + eventTime
                        + " monotonicNanos=" + monotonicNanos + " injectedNanos=" + System.nanoTime());
            }
        } finally {
            event.recycle();
        }
    }

    private static void cancelWithAdditionalPointers(long down, float x, float y, int count)
            throws Exception {
        // Give the controller's asynchronous capture/window a measurable half-open interval.
        System.out.println("TOUCH_MULTI_HOLD downTime=" + down);
        SystemClock.sleep(2500);
        MotionEvent.PointerProperties[] properties = new MotionEvent.PointerProperties[count];
        MotionEvent.PointerCoords[] coordinates = new MotionEvent.PointerCoords[count];
        for (int i = 0; i < count; i++) {
            properties[i] = new MotionEvent.PointerProperties();
            properties[i].id = i;
            properties[i].toolType = MotionEvent.TOOL_TYPE_FINGER;
            coordinates[i] = new MotionEvent.PointerCoords();
            coordinates[i].x = x + i * 20;
            coordinates[i].y = y + i * 20;
            coordinates[i].pressure = 1;
            coordinates[i].size = 1;
        }
        for (int pointers = 2; pointers <= count + 1; pointers++) {
            int action = pointers <= count ? MotionEvent.ACTION_POINTER_DOWN
                    | ((pointers - 1) << MotionEvent.ACTION_POINTER_INDEX_SHIFT)
                    : MotionEvent.ACTION_CANCEL;
            MotionEvent event = MotionEvent.obtain(down, SystemClock.uptimeMillis(), action,
                    Math.min(pointers, count), properties, coordinates, 0, 0, 1, 1, 0, 0,
                    InputDevice.SOURCE_TOUCHSCREEN, 0);
            try {
                if (!Boolean.TRUE.equals(inject.invoke(manager, event, 2))) {
                    throw new IllegalStateException("Multi-pointer injection was rejected");
                }
                System.out.println("TOUCH_MULTI action=" + action + " count=" + event.getPointerCount());
            } finally { event.recycle(); }
            SystemClock.sleep(30);
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 6 || !("swipe".equals(args[0]) || "cancel".equals(args[0])
                || args[0].matches("multi-cancel-[234]"))) {
            throw new IllegalArgumentException("swipe|cancel|multi-cancel-[234] x1 y1 x2 y2 durationMs");
        }
        float x1 = Float.parseFloat(args[1]), y1 = Float.parseFloat(args[2]);
        float x2 = Float.parseFloat(args[3]), y2 = Float.parseFloat(args[4]);
        long duration = Long.parseLong(args[5]);
        if (duration <= 0 || duration > 10000) throw new IllegalArgumentException("duration");
        Class<?> type = Class.forName("android.hardware.input.InputManager");
        try {
            manager = type.getMethod("getInstance").invoke(null);
        } catch (NoSuchMethodException | java.lang.reflect.InvocationTargetException unavailableLegacyAccessor) {
            // Android 16's legacy accessor requires an Application, absent in app_process.
            if (unavailableLegacyAccessor instanceof java.lang.reflect.InvocationTargetException
                    && !(unavailableLegacyAccessor.getCause() instanceof NullPointerException)) {
                throw unavailableLegacyAccessor;
            }
            // Keep permission and other service failures visible; only resolve the shell owner.
            type = Class.forName("android.hardware.input.InputManagerGlobal");
            manager = type.getMethod("getInstance").invoke(null);
        }
        inject = type.getMethod("injectInputEvent", InputEvent.class, int.class);
        long down = SystemClock.uptimeMillis();
        send(down, MotionEvent.ACTION_DOWN, x1, y1);
        long now;
        while ((now = SystemClock.uptimeMillis()) < down + duration) {
            float fraction = Math.min(1f, (now - down) / (float) duration);
            send(down, MotionEvent.ACTION_MOVE, x1 + (x2 - x1) * fraction,
                    y1 + (y2 - y1) * fraction);
            SystemClock.sleep(10);
        }
        send(down, MotionEvent.ACTION_MOVE, x2, y2);
        if (args[0].startsWith("multi-cancel-")) {
            cancelWithAdditionalPointers(down, x2, y2,
                    Integer.parseInt(args[0].substring(args[0].length() - 1)));
        } else {
            send(down, "cancel".equals(args[0]) ? MotionEvent.ACTION_CANCEL : MotionEvent.ACTION_UP,
                    x2, y2);
        }
        System.out.println("TOUCH_INPUT downTime=" + down + " mode=" + args[0]);
    }
}
