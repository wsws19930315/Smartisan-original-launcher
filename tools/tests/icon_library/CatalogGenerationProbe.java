package com.smartisanos.home.settings.icons;

import android.content.Context;
import android.os.Looper;
import android.os.OperationCanceledException;
import java.lang.reflect.Constructor;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/** Actual catalog on ART; only a snapshot barrier and one synthetic label are injected. */
public final class CatalogGenerationProbe {
    static int checks;
    static final AtomicInteger snapshots=new AtomicInteger();
    static final AtomicInteger closes=new AtomicInteger();
    static volatile String label="Old audit label";
    static volatile CountDownLatch captured,release;
    static void check(boolean value,String message) {
        if(!value)throw new AssertionError(message); checks++;
    }
    public static java.io.InputStream stream(java.io.InputStream input) {
        return new java.io.FilterInputStream(input) {
            public void close()throws java.io.IOException {try{super.close();}finally{closes.incrementAndGet();}}
        };
    }
    public static <T> Map<String,T> snapshot(Map<String,T> original)throws Exception {
        snapshots.incrementAndGet();
        Map<String,T> result=new HashMap<String,T>(original);
        Class<?> type=Class.forName(IconLibraryCatalog.class.getName()+"$InstalledLabel");
        Constructor<?> constructor=type.getDeclaredConstructor(String.class,String.class);
        constructor.setAccessible(true);
        @SuppressWarnings("unchecked") T item=(T)constructor.newInstance(label,"tools");
        result.put("fixture.audit.target",item);
        CountDownLatch gate=release,seen=captured;
        if(gate!=null) {
            seen.countDown();
            if(!gate.await(15,TimeUnit.SECONDS))throw new AssertionError("snapshot barrier timed out");
        }
        return result;
    }
    static final class Load extends Thread {
        final Context context; IconLibraryCatalog result; Throwable failure;
        Load(Context context){super("catalog-generation-probe");this.context=context;}
        public void run(){try{result=IconLibraryCatalog.load(context);}catch(Throwable e){failure=e;}}
    }
    static void finish(Load task)throws Exception {
        task.join(20000);check(!task.isAlive(),"loader terminates");
    }
    static void run(Context context)throws Exception {
        try {IconLibraryCatalog.load(context);throw new AssertionError("main IO accepted");}
        catch(IllegalStateException expected){checks++;}
        for(int invalidations:new int[]{1,3}) {
            IconLibraryCatalog.invalidateInstalledLabels();
            label="Old audit label";captured=new CountDownLatch(1);release=new CountDownLatch(1);
            int before=snapshots.get();Load first=new Load(context);first.start();
            check(captured.await(15,TimeUnit.SECONDS),"old package snapshot captured");
            CountDownLatch gate=release;
            try {
                label="New audit label";
                for(int i=0;i<invalidations;i++)IconLibraryCatalog.invalidateInstalledLabels();
                check(first.isAlive(),"MAIN invalidation did not await background build");
                check(IconLibraryCatalog.peek()==null,"invalidation clears ready catalog");
                release=null;
            } finally {gate.countDown();}
            finish(first);
            check(IconLibraryCatalog.peek()==null,"invalidated build must not republish old snapshot");
            check(first.result==null && first.failure instanceof OperationCanceledException,
                    "invalidated caller receives explicit cancellation");
            check(closes.get()==before+1,"discarded build closes its asset stream");
            Load second=new Load(context),third=new Load(context);second.start();third.start();
            finish(second);finish(third);
            check(second.failure==null && third.failure==null,"next callers can rebuild");
            check(second.result==third.result && second.result==IconLibraryCatalog.peek(),"one shared publication");
            check(snapshots.get()==before+2,"one discarded build plus one rebuild; no hidden retry");
            check(closes.get()==before+2,"successful rebuild closes its asset stream");
            check(second.result.metadataForTarget("fixture.audit.target").name.equals("New audit label"),
                    "new snapshot provides current labels");
            check(IconLibraryCatalog.load(context)==second.result,"MAIN cached read remains nonblocking");
        }
        System.out.println("PASS CATALOG_GENERATION_ANDROID checks="+checks+" snapshots="+snapshots.get());
    }
    public static void main(String[] args)throws Exception {
        try {
            Looper.prepareMainLooper();Class<?> type=Class.forName("android.app.ActivityThread");
            Object thread=type.getMethod("systemMain").invoke(null);
            Context system=(Context)type.getMethod("getSystemContext").invoke(thread);
            run(system.createPackageContext("com.smartisanos.launcher",0));
        } catch(Throwable error) {error.printStackTrace(System.out);System.exit(1);}
    }
}
