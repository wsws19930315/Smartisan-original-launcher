package com.smartisanos.launcher.quickdesktop;

import com.smartisanos.launcher.view.Eb;
import java.lang.reflect.Method;

/** Exercises the UI/GL ownership boundary with the production controller. */
public final class QuickDesktopWorkspaceSnapshotProbe {
    private static int checks;
    private static void check(boolean value, String message) {
        checks++;
        if (!value) throw new AssertionError(message);
    }
    private static int mode() throws Exception {
        Method method = QuickDesktopController.class.getDeclaredMethod("workspaceMode");
        method.setAccessible(true);
        return (Integer) method.invoke(null);
    }
    private static void publish(Object page, int index, int mode) throws Exception {
        QuickDesktopController.class.getMethod("publishWorkspaceState", Object.class,
                int.class, int.class).invoke(null, page, index, mode);
    }
    public static void main(String[] args) {
        try {
            android.os.Looper.prepareMainLooper();
            int initial = mode();
            check(Eb.geometryReads == 0, "UI read engine geometry before a GL snapshot");
            check(initial == 0, "unpublished workspace was eligible");
            for (int value : new int[]{12, 9, 13, 10}) {
                publish(Eb.page(), 0, value);
                check(mode() == value, "first-page mode lost");
                publish(Eb.page(), 1, value);
                check(mode() == 0, "another page was eligible");
            }
            for (int value : new int[]{-1, 0, 8, 20, 80}) {
                publish(Eb.page(), 0, value);
                check(mode() == 0, "unsupported mode was eligible");
            }
            publish(Eb.page(), 0, 12);
            Eb.replacePage();
            check(mode() == 0, "old page snapshot authorized its replacement");
            publish(Eb.page(), 0, 12);
            check(mode() == 12, "replacement page did not recover");
            Eb.editing = true;
            check(mode() == 0, "editing retained ownership");
            Eb.editing = false;
            QuickDesktopController.onLauncherStopped();
            check(mode() == 0, "stop retained snapshot");
            publish(Eb.page(), 0, 12);
            QuickDesktopController.onLauncherDestroyed();
            check(mode() == 0, "destroy retained snapshot");
            publish(null, 0, 12);
            check(mode() == 0, "null page retained snapshot");
            Thread producer = new Thread(new Runnable() { public void run() {
                for (int i = 0; i < 10000; i++) {
                    Eb.pageIndex = i & 1;
                    Eb.publishProbeFrame();
                }
            }}, "GL-snapshot-producer");
            producer.start();
            for (int i = 0; i < 10000; i++) {
                int value = mode();
                check(value == 0 || value == 12, "torn snapshot");
            }
            producer.join();
            check(Eb.geometryReads == 0, "UI entered native geometry after publication");
            System.out.println("PASS WORKSPACE_SNAPSHOT=" + checks);
        } catch (Throwable error) {
            error.printStackTrace();
            System.exit(1);
        }
    }
}
