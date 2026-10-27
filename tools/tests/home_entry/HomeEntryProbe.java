package com.smartisanos.launcher.gesture;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ComponentName;
import android.content.Intent;
import android.os.Looper;

/** Executes the built entry helper without Launcher data or framework Activity launches. */
public final class HomeEntryProbe {
    private static int checks;
    private static final String PACKAGE = "com.smartisanos.launcher";
    private static android.content.pm.PackageManager packageManager;

    private static void check(boolean condition) {
        checks++;
        if (!condition) throw new AssertionError("check " + checks);
    }

    private static final class Entry extends Activity {
        ComponentName component;
        Intent incoming;
        Intent started;
        RuntimeException failure;
        int starts;
        int finishes;
        String packageName = PACKAGE;

        Entry(String name) {
            component = name == null ? null : new ComponentName(PACKAGE, PACKAGE + '.' + name);
            incoming = new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER);
            if (component != null) incoming.setComponent(component);
        }

        @Override public ComponentName getComponentName() { return component; }
        @Override public String getPackageName() { return packageName; }
        @Override public android.content.pm.PackageManager getPackageManager() { return packageManager; }
        @Override public Intent getIntent() { return incoming; }
        @Override public void startActivity(Intent intent) {
            check(finishes == 1);
            starts++;
            if (failure != null) throw failure;
            started = intent;
        }
        @Override public void finish() { finishes++; }
    }

    public static void main(String[] args) throws Exception {
        Looper.prepareMainLooper();
        Class<?> thread = Class.forName("android.app.ActivityThread");
        Object main = thread.getMethod("systemMain").invoke(null);
        android.content.Context system = (android.content.Context)
                thread.getMethod("getSystemContext").invoke(main);
        packageManager = system.getPackageManager();
        check(!LauncherHomeCompat.redirectLauncherAlias(null));
        Entry canonical = new Entry("Launcher");
        check(!LauncherHomeCompat.redirectLauncherAlias(canonical));
        check(canonical.starts == 0 && canonical.finishes == 0);
        canonical.incoming.setComponent(new ComponentName(PACKAGE, PACKAGE + ".LauncherAlias"));
        check(!LauncherHomeCompat.redirectLauncherAlias(canonical));
        check(canonical.starts == 0);
        check(!LauncherHomeCompat.redirectLauncherAlias(new Entry(null)));
        Entry notDefault = new Entry("LauncherAlias");
        notDefault.packageName = "fixture.other.launcher";
        check(!LauncherHomeCompat.redirectLauncherAlias(notDefault));
        check(notDefault.starts == 0 && notDefault.finishes == 0);
        Intent fallback = LauncherHomeCompat.createLauncherHomeIntent(notDefault);
        check(fallback.getComponent() != null
                && (PACKAGE + ".Launcher").equals(fallback.getComponent().getClassName()));

        Entry alias = new Entry("LauncherAlias");
        Intent base = LauncherHomeCompat.createLauncherHomeIntent(alias);
        check(base.getComponent() == null && PACKAGE.equals(base.getPackage()));
        check(base.getFlags() == 0 && base.getExtras() == null);
        check(base.getCategories().size() == 1 && base.hasCategory(Intent.CATEGORY_HOME));
        alias.incoming.putExtra("test_reload_token", "fixture-token");
        alias.incoming.putExtra("test_grid", 20);
        alias.incoming.addFlags(Intent.FLAG_ACTIVITY_MULTIPLE_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        Intent original = new Intent(alias.incoming);
        check(LauncherHomeCompat.redirectLauncherAlias(alias));
        check(alias.starts == 1 && alias.finishes == 1);
        check(Intent.ACTION_MAIN.equals(alias.started.getAction()));
        check(alias.started.hasCategory(Intent.CATEGORY_HOME));
        check(!alias.started.hasCategory(Intent.CATEGORY_LAUNCHER));
        check(alias.started.getComponent() == null);
        check(PACKAGE.equals(alias.started.getPackage()));
        android.content.pm.ResolveInfo target = packageManager.resolveActivity(
                alias.started, android.content.pm.PackageManager.MATCH_DEFAULT_ONLY);
        check(target != null && target.activityInfo != null
                && (PACKAGE + ".Launcher").equals(target.activityInfo.name));
        check(alias.started.getFlags() == (Intent.FLAG_ACTIVITY_NEW_TASK
                | Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP));
        check("fixture-token".equals(alias.started.getStringExtra("test_reload_token")));
        check(alias.started.getIntExtra("test_grid", -1) == 20);
        check(alias.incoming.filterEquals(original) && alias.incoming.getFlags() == original.getFlags());
        alias.started.putExtra("test_grid", 12);
        check(alias.incoming.getIntExtra("test_grid", -1) == 20);

        Entry noIntent = new Entry("LauncherAlias");
        noIntent.incoming = null;
        check(LauncherHomeCompat.redirectLauncherAlias(noIntent));
        for (RuntimeException failure : new RuntimeException[] {
                new ActivityNotFoundException("fixture"), new SecurityException("fixture")}) {
            Entry rejected = new Entry("LauncherAlias");
            rejected.failure = failure;
            check(LauncherHomeCompat.redirectLauncherAlias(rejected));
            check(rejected.starts == 1 && rejected.started == null && rejected.finishes == 1);
        }
        System.out.println("PASS HOME_ENTRY checks=" + checks);
    }
}
