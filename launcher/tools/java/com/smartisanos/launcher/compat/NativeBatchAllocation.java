package com.smartisanos.launcher.compat;

import android.os.Build;
import android.os.Process;

/** Retains the original native constructor/destructor and scopes extra storage to batch owners. */
public final class NativeBatchAllocation {
    private static final boolean ARM64_PROCESS = Build.VERSION.SDK_INT >= 23 && Process.is64Bit();

    private NativeBatchAllocation() {}

    public static long create(boolean batchOwner) {
        // The original 32-bit library and its JNI allocation path are unchanged.
        if (!ARM64_PROCESS) return 0;
        return Arm64.allocate(batchOwner);
    }

    private static final class Arm64 {
        static {
            System.loadLibrary("launcher_opt");
            System.loadLibrary("launcher_batch_compat");
        }

        private static native long allocate(boolean batchOwner);
    }
}
