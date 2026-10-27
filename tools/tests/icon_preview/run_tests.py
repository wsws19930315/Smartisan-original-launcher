"""Exercise production request/session/worker methods with deterministic worker barriers."""
import argparse
import json
import pathlib
import subprocess
import tempfile
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[3]


def block(source, marker):
    start = source.index(marker)
    end = source.index("{", start) + 1
    depth = 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[start:end]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jdk", type=pathlib.Path, required=True)
    parser.add_argument("--serial")
    parser.add_argument("--source", type=pathlib.Path, default=ROOT / "launcher/tools/java/com/smartisanos/home/settings/icons/IconPreviewRepository.java")
    parser.add_argument("--sdk", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()
    source = args.source.read_text(encoding="utf-8")
    declarations = source[source.index("    public interface Callback"):source.index("    public static final class ImprovedCandidate")]
    declarations += block(source, "    public static final class IconRenderKey")
    declarations += block(source, "    public static final class RequestSession")
    declarations += block(source, "    public static final class PendingCallback")
    methods = source[source.index("    public RequestSession openSession"):source.index("    public Bitmap getCachedOfficialIcon")]
    methods += block(source, "    public static void logPerf")
    methods += source[source.index("    public void request(final IconRenderKey"):source.index("    public Drawable cachedDrawable")]
    methods += source[source.index("    private final class RenderTask"):source.index("    private IconRenderKey defaultKey")]
    methods += block(source, "    public void prefetchLocal(")
    methods += block(source, "    private void enqueueOnline(")
    methods += block(source, "    private final class OnlineFetch")
    methods += block(source, "    private final class IoOperation")
    methods += block(source, "    public boolean scheduleIo(")
    methods += block(source, "    private void purgeMetadataWork(")
    methods += block(source, "    public boolean scheduleMetadata(")
    methods += block(source, "    public boolean scheduleIndex(")
    methods += block(source, "    private boolean scheduleMetadataOn(")
    # Include the actual constructor submission, not a hand-written replacement.
    start = source.index('        indexPool = metadataExecutor("icon-directory", 4);')
    start = source.index('\n', start) + 1
    end = source.index('        app.registerComponentCallbacks(this);', start)
    methods += "void catalogPrewarmFromConstructor() {" + source[start:end] + "}\n"
    # Pause only the extracted test copy at an eviction boundary, never the APK.
    methods = methods.replace("if(evicted!=null && !decodePool.getQueue().remove(evicted))", "if(evicted!=null) evictionGate();\n                if(evicted!=null && !decodePool.getQueue().remove(evicted))")
    methods = methods.replace("if (decodePool.getQueue().remove(candidateToEvict))", "evictionGate();\n                    if (decodePool.getQueue().remove(candidateToEvict))")
    methods = methods.replace("com.smartisanos.launcher.theme.MaintainedLauncherSettingsHost.onPreviewLibrarySourceDownloaded", "Host.onPreviewLibrarySourceDownloaded")
    fields = source[source.index("    private static final int MAX_SESSION_QUEUE_SIZE"):source.index("    private IconPreviewRepository(Context")]
    fields = fields.replace("private static volatile IconPreviewRepository sInstance;", "")
    fields = fields.replace("private final Context app;", "")
    fields = fields.replace("private final Handler main = new Handler(Looper.getMainLooper());", "private final Handler main = new Handler();")
    fixture = r'''
    static class Bitmap { final int id; boolean recycled; Bitmap(int i){id=i;} void recycle(){recycled=true;} }
    static class Drawable { final int id; Drawable(int i){id=i;} }
    static class LruCache<K,V> extends java.util.concurrent.ConcurrentHashMap<K,V> {
        LruCache(int size){} protected void entryRemoved(boolean e,K k,V a,V b){}
    }
    static class Handler {
        final java.util.concurrent.ConcurrentLinkedQueue<Runnable> work = new java.util.concurrent.ConcurrentLinkedQueue<>();
        void post(Runnable r){work.add(r);}
        void drain(){Runnable r; while((r=work.poll())!=null)r.run();}
    }
    IconPreviewRepository() {
        cache=new LruCache<>(1000);
        onlinePool=new ThreadPoolExecutor(2,2,15L,TimeUnit.SECONDS,new ArrayBlockingQueue<Runnable>(24),job->new Thread(job,"probe-io"));
        decodePool=new ThreadPoolExecutor(2,2,15L,TimeUnit.SECONDS,new PriorityBlockingQueue<Runnable>(),job->new Thread(job,"probe-render"));
        metadataPool=new ThreadPoolExecutor(1,1,15L,TimeUnit.SECONDS,new ArrayBlockingQueue<Runnable>(16));
        indexPool=new ThreadPoolExecutor(1,1,15L,TimeUnit.SECONDS,new ArrayBlockingQueue<Runnable>(4),job->new Thread(job,"probe-directory"));
    }
    static class IconLibraryCatalog {
        static volatile CountDownLatch entered, release;
        static volatile String threadName;
        static final AtomicInteger loads=new AtomicInteger();
        static void load(Object app)throws Exception {
            loads.incrementAndGet();threadName=Thread.currentThread().getName();
            CountDownLatch e=entered,r=release;if(e!=null)e.countDown();if(r!=null)r.await();
        }
    }
    final Object app = new Object();
    final Map<RequestSession,Runnable> candidateRefresh=new HashMap<>();
    final Map<RequestSession,Long> candidateRequests=new HashMap<>();
    static class Host { static void onPreviewLibrarySourceDownloaded(Object app,String source,String pkg,String component){} }
    CountDownLatch ioEntered, ioRelease;
    boolean fetchOnlineSource(String source, OnlineFetch fetch) {
        check(Thread.currentThread().getName().startsWith("probe-io"),"HTTP isolated from preview workers");
        if(ioEntered!=null)ioEntered.countDown();
        try { if(ioRelease!=null)await(ioRelease); } catch(Exception e){throw new RuntimeException(e);}
        return !fetch.cancelled;
    }
    static Bitmap drawableToBitmap(Drawable d,int size){return d==null?null:new Bitmap(d.id);}
    static IconRenderKey key(int i){return new IconRenderKey("pkg"+i,"Activity",0,"DEFAULT","",1,52,320,1);}
    static int checks, failures;
    static void check(boolean ok,String message){checks++;if(!ok){failures++;System.out.println("FAIL "+message);}}
    static void await(CountDownLatch latch)throws Exception{if(!latch.await(3,TimeUnit.SECONDS))throw new AssertionError("worker timeout");}
    static void idle(IconPreviewRepository r)throws Exception {
        long end=System.nanoTime()+TimeUnit.SECONDS.toNanos(3);
        // A worker's first task can be assigned before it becomes active or enters the queue.
        while((r.decodePool.getActiveCount()!=0||!r.decodePool.getQueue().isEmpty()
                ||r.decodePool.getTaskCount()!=r.decodePool.getCompletedTaskCount())&&System.nanoTime()<end)Thread.sleep(2);
        check(r.decodePool.getActiveCount()==0&&r.decodePool.getQueue().isEmpty(),"workers drained");r.main.drain();
    }
    static void prefetch()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();
        try {
            r.request(key(1),Priority.P1_ADJACENT,()->new Drawable(7),null);idle(r);
            check(r.cache.get(key(1))!=null,"callback-free prefetch populates cache");
            AtomicInteger operations=new AtomicInteger();
            r.schedule(Priority.P2_IDLE,()->operations.incrementAndGet());idle(r);
            check(operations.get()==1,"metadata operation runs once");
            int beforePause=operations.get();r.pauseP2=true;r.schedule(Priority.P2_IDLE,()->operations.incrementAndGet());idle(r);
            check(operations.get()==beforePause,"memory-pressure metadata stays paused");
            check(r.pendingCount()==0,"prefetch releases pending marker");
        }finally{r.decodePool.shutdownNow();}
    }
    static void localPrefetchAndDedup()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();
        CountDownLatch entered=new CountDownLatch(1),release=new CountDownLatch(1);
        try {
            RequestSession s=r.openSession("warm");IconRenderKey shared=key(800);
            r.prefetchLocal(s,shared,()->{entered.countDown();await(release);return null;});
            await(entered);
            check(r.pendingCount()==0,"local miss never reserves a visible pending slot");
            AtomicInteger visible=new AtomicInteger();
            r.request(s,shared,Priority.P0_VISIBLE,()->new Drawable(88),(k,b)->visible.set(b==null?-1:b.id));
            release.countDown();idle(r);
            check(visible.get()==88,"visible decode independent of local-only miss");
            final CountDownLatch blocked=new CountDownLatch(1),gate=new CountDownLatch(1);
            IconRenderKey key=key(801);
            r.request(s,key,Priority.P0_VISIBLE,()->{blocked.countDown();await(gate);return new Drawable(1);},null);
            await(blocked);
            for(int i=0;i<100;i++)r.request(s,key,Priority.P0_VISIBLE,()->new Drawable(1),null);
            check(r.pending.get(key).size()==1,"scroll prefetch subscriptions deduplicated per session");
            gate.countDown();idle(r);r.cancelSession(s);
        }finally{release.countDown();r.decodePool.shutdownNow();r.onlinePool.shutdownNow();}
    }
    static void eviction()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch entered=new CountDownLatch(2),release=new CountDownLatch(1);
        try {
            for(int i=0;i<2;i++)r.request(key(20+i),Priority.P0_VISIBLE,()->{entered.countDown();await(release);return new Drawable(1);},(k,b)->{});
            await(entered);RequestSession s=r.openSession("queue");
            AtomicInteger results=new AtomicInteger();
            for(int i=0;i<110;i++)r.request(s,key(100+i),Priority.P2_IDLE,()->new Drawable(2),(k,b)->results.incrementAndGet());
            check(r.decodePool.getQueue().size()<=96,"low-priority session queue stays bounded");
            IconRenderKey evicted=null;
            for(int i=0;i<110;i++)if(!r.pending.containsKey(key(100+i))){evicted=key(100+i);break;}
            check(evicted!=null,"evicted batch detached before UI delivery");
            AtomicInteger retried=new AtomicInteger();
            if(evicted!=null)r.request(s,evicted,Priority.P0_VISIBLE,()->new Drawable(99),(k,b)->retried.set(b==null?-1:b.id));
            r.main.drain();release.countDown();idle(r);
            check(results.get()==110,"evicted requests complete and release callbacks");
            check(retried.get()==99,"visible retry decodes after low-priority eviction");
            check(r.pendingCount()==0,"queue trimming leaves no pending entries");
            r.cancelSession(s);check(r.activeSessions.isEmpty(),"cancel releases session");
        }finally{release.countDown();r.decodePool.shutdownNow();}
    }
    static void staleCompletion()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch oldStarted=new CountDownLatch(1),oldRelease=new CountDownLatch(1),newStarted=new CountDownLatch(1),newRelease=new CountDownLatch(1);
        try {
            IconRenderKey k=key(4);RequestSession old=r.openSession("old");AtomicInteger oldResults=new AtomicInteger(),newResult=new AtomicInteger();
            r.request(old,k,Priority.P0_VISIBLE,()->{oldStarted.countDown();await(oldRelease);return new Drawable(10);},(name,b)->oldResults.incrementAndGet());
            await(oldStarted);r.cancelSession(old);RequestSession fresh=r.openSession("new");
            r.request(fresh,k,Priority.P0_VISIBLE,()->{newStarted.countDown();await(newRelease);return new Drawable(20);},(name,b)->newResult.set(b==null?-1:b.id));
            await(newStarted);oldRelease.countDown();
            long end=System.nanoTime()+TimeUnit.SECONDS.toNanos(3);
            while(r.decodePool.getActiveCount()>1&&System.nanoTime()<end)Thread.sleep(2);
            r.main.drain();
            check(oldResults.get()==0,"cancelled callback not delivered");
            check(newResult.get()==0,"old task cannot consume new request callback");
            check(r.cache.get(k)==null,"cancelled task cannot refill cache");
            newRelease.countDown();idle(r);
            check(newResult.get()==20,"fresh request receives fresh bitmap");
            r.cancelSession(fresh);
        }finally{oldRelease.countDown();newRelease.countDown();r.decodePool.shutdownNow();}
    }
    static void sharedConsumers()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch entered=new CountDownLatch(1),release=new CountDownLatch(1);
        try {
            RequestSession one=r.openSession("one"),two=r.openSession("two");AtomicInteger calls=new AtomicInteger(),loads=new AtomicInteger();
            DrawableLoader load=()->{loads.incrementAndGet();entered.countDown();await(release);return new Drawable(30);};
            r.request(one,key(8),Priority.P0_VISIBLE,load,(k,b)->calls.addAndGet(100));await(entered);
            r.request(two,key(8),Priority.P0_VISIBLE,load,(k,b)->calls.incrementAndGet());
            r.cancelSession(one);release.countDown();idle(r);
            check(calls.get()==1,"one cancelled consumer preserves other callback");
            check(loads.get()==1,"shared key only decoded once");
            check(r.pendingCount()==0,"shared request completed");r.cancelSession(two);
        }finally{release.countDown();r.decodePool.shutdownNow();}
    }
    static void cancelledPreparation()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch entered=new CountDownLatch(2),release=new CountDownLatch(1);
        try {
            for(int i=0;i<2;i++)r.request(key(50+i),Priority.P0_VISIBLE,()->{entered.countDown();await(release);return new Drawable(1);},(k,b)->{});
            await(entered);RequestSession s=r.openSession("prepare");AtomicInteger calls=new AtomicInteger();
            r.schedule(s,Priority.P2_IDLE,()->calls.incrementAndGet());
            r.request(s,key(60),Priority.P1_ADJACENT,()->{calls.incrementAndGet();return new Drawable(2);},null);
            r.cancelSession(s);
            check(r.decodePool.getQueue().isEmpty(),"cancel removes queued metadata and prefetch");
            release.countDown();idle(r);check(calls.get()==0,"cancelled metadata never executes");
            check(r.pendingCount()==0,"cancelled prefetch releases marker");
        }finally{release.countDown();r.decodePool.shutdownNow();}
    }
    static void memoryPressure()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch entered=new CountDownLatch(2),release=new CountDownLatch(1);
        try {
            for(int i=0;i<2;i++)r.request(key(70+i),Priority.P0_VISIBLE,()->{entered.countDown();await(release);return new Drawable(1);},(k,b)->{});
            await(entered);AtomicInteger idleLoads=new AtomicInteger(),visibleLoads=new AtomicInteger();
            r.request(key(72),Priority.P2_IDLE,()->{idleLoads.incrementAndGet();return new Drawable(2);},null);
            r.schedule(Priority.P2_IDLE,()->idleLoads.incrementAndGet());r.pauseP2=true;
            release.countDown();idle(r);
            check(idleLoads.get()==0,"queued idle work stops on memory pressure");
            r.request(key(73),Priority.P0_VISIBLE,()->{visibleLoads.incrementAndGet();return new Drawable(3);},null);idle(r);
            check(visibleLoads.get()==1,"visible work resumes after memory pressure");
            check(r.pendingCount()==0,"pressure leaves no pending entries");
        }finally{release.countDown();r.decodePool.shutdownNow();}
    }
    static void networkIsolation()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();
        r.ioEntered=new CountDownLatch(2); r.ioRelease=new CountDownLatch(1);
        RequestSession s=r.openSession("library");
        try {
            DrawableLoader deferred=()->{RenderTask task=CURRENT_RENDER.get();if(!task.onlineAttempted){task.requiredOnlineSource=task.key.sourceId;return null;}return new Drawable(99);};
            for(int i=0;i<2;i++)r.request(s,new IconRenderKey("pkg","Activity",0,"RESOURCE","source"+i,1,72,320,1),Priority.P0_VISIBLE,deferred,(k,b)->{});
            await(r.ioEntered);
            CountDownLatch prepared=new CountDownLatch(1);
            r.schedule(s,Priority.P0_VISIBLE,()->prepared.countDown());await(prepared);
            AtomicInteger other=new AtomicInteger();r.request(key(1000),Priority.P0_VISIBLE,()->new Drawable(42),(k,b)->other.set(b.id));idle(r);
            check(other.get()==42,"another page renders while both HTTP workers are blocked");
            for(int i=2;i<40;i++)r.request(s,new IconRenderKey("pkg","Activity",0,"RESOURCE","source"+i,1,72,320,1),Priority.P0_VISIBLE,deferred,(k,b)->{});
            idle(r);
            check(r.onlinePool.getQueue().size()<=24,"IO queue hard bound");
            check(r.online.size()<=26,"IO dedup/inflight map hard bound");
            r.cancelSession(s);
            check(r.onlinePool.getQueue().isEmpty()&&r.online.isEmpty(),"exit purges all queued IO and callbacks");
            check(r.pendingCount()==0,"exit releases pending image ownership");
            r.ioRelease.countDown();r.onlinePool.shutdown();r.onlinePool.awaitTermination(3,TimeUnit.SECONDS);idle(r);
            check(r.activeSessions.isEmpty(),"no leaked page sessions");
        } finally {r.ioRelease.countDown();r.decodePool.shutdownNow();r.onlinePool.shutdownNow();}
    }
    static void metadataIsolation()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();
        RequestSession directory=r.openSession("directory"),query=r.openSession("query");
        CountDownLatch entered=new CountDownLatch(1),release=new CountDownLatch(1),finished=new CountDownLatch(1);
        try {
            check(r.scheduleIndex(directory,()->{entered.countDown();try{await(release);}catch(Exception e){throw new RuntimeException(e);}}),"index task queued");
            await(entered);
            check(r.scheduleMetadata(query,finished::countDown),"query queued separately");await(finished);
            check(r.indexPool.getActiveCount()==1,"query completes while directory worker is blocked");
            java.util.concurrent.atomic.AtomicInteger stale=new java.util.concurrent.atomic.AtomicInteger();
            check(r.scheduleIndex(query,stale::incrementAndGet),"queued directory consumer");
            r.cancelSession(query);
            check(r.indexPool.getQueue().isEmpty(),"cancel removes queued metadata consumer");
            release.countDown();r.indexPool.shutdown();r.indexPool.awaitTermination(3,TimeUnit.SECONDS);
            check(stale.get()==0,"cancelled metadata never runs");
            check(r.metadataPool.getQueue().isEmpty(),"query queue drains");
        } finally {release.countDown();r.cancelSession(directory);r.metadataPool.shutdownNow();r.indexPool.shutdownNow();r.decodePool.shutdownNow();r.onlinePool.shutdownNow();}
    }
    static void visibleJoinSessionTrim(int mode)throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch entered=new CountDownLatch(2),release=new CountDownLatch(1);
        RequestSession prefetch=r.openSession("adjacent"),visible=mode==0?prefetch:r.openSession("visible");
        try {
            for(int i=0;i<2;i++)r.request(key(10000+i),Priority.P0_VISIBLE,()->{entered.countDown();await(release);return new Drawable(1);},null);
            await(entered);IconRenderKey shared=key(11000);AtomicInteger result=new AtomicInteger(),loads=new AtomicInteger();
            r.request(prefetch,shared,Priority.P1_ADJACENT,()->{loads.incrementAndGet();return new Drawable(77);},null);
            Callback consumer=(k,b)->result.set(b==null?-1:b.id);
            r.request(visible,shared,Priority.P0_VISIBLE,()->new Drawable(99),consumer);
            if(mode==2)r.cancelRequest(visible,shared,consumer);
            for(int i=0;i<96;i++)r.request(prefetch,key(12000+i),Priority.P1_ADJACENT,()->new Drawable(2),null);
            check(r.decodePool.getQueue().size()<=96,"adjacent session trim retains its bound");
            check(r.pending.containsKey(shared)==(mode!=2),"visible join protected, recycled-only subscription evictable mode="+mode);
            release.countDown();idle(r);
            check(result.get()==(mode==2?0:77),"visible join receives bitmap, not trim-null mode="+mode);
            check(loads.get()==(mode==2?0:1),"shared queued loader executes at most once mode="+mode);
            check(r.pendingCount()==0,"visible join pressure drains pending ownership");
        } finally {release.countDown();r.cancelSession(prefetch);r.cancelSession(visible);r.decodePool.shutdownNow();r.onlinePool.shutdownNow();r.metadataPool.shutdownNow();r.indexPool.shutdownNow();}
    }
    static void visibleBurstCancellation()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch entered=new CountDownLatch(2),release=new CountDownLatch(1);
        RequestSession[] sessions=new RequestSession[80];AtomicInteger callbacks=new AtomicInteger(),stale=new AtomicInteger(),cancelledLoads=new AtomicInteger(),preparation=new AtomicInteger();
        try {
            for(int i=0;i<2;i++)r.request(key(20000+i),Priority.P0_VISIBLE,()->{entered.countDown();await(release);return new Drawable(1);},null);
            await(entered);
            for(int i=0;i<sessions.length;i++){
                sessions[i]=r.openSession("burst-"+i);final boolean cancel=(i%2)==0;
                for(int j=0;j<10;j++)r.request(sessions[i],key(21000+i*10+j),Priority.P0_VISIBLE,()->{if(cancel)cancelledLoads.incrementAndGet();return new Drawable(3);},(k,b)->{if(cancel)stale.incrementAndGet();else callbacks.incrementAndGet();});
            }
            for(int i=0;i<8;i++)r.schedule(Priority.P0_VISIBLE,preparation::incrementAndGet);
            check(r.decodePool.getQueue().size()<=MAX_RENDER_QUEUE_SIZE,"800 visible requests and metadata reserve obey global bound");
            check(r.pendingCount()<=MAX_RENDER_QUEUE_SIZE+2,"visible overflow releases pending ownership before delivery");
            for(int i=0;i<sessions.length;i+=2)r.cancelSession(sessions[i]);
            release.countDown();idle(r);
            check(stale.get()==0,"cancelled visible sessions receive no queued or rejected callback");
            check(cancelledLoads.get()==0,"cancelled burst loaders never execute");
            check(callbacks.get()==400,"remaining burst consumers each receive one completion including explicit rejection");
            check(preparation.get()==8,"metadata reserve survives image saturation");
            check(r.pendingCount()==0,"visible burst and cancellation fully drain");
        } finally {release.countDown();for(RequestSession session:sessions)r.cancelSession(session);r.decodePool.shutdownNow();r.onlinePool.shutdownNow();r.metadataPool.shutdownNow();r.indexPool.shutdownNow();}
    }
    static volatile CountDownLatch evictionEntered,evictionRelease;
    static final AtomicBoolean evictionOnce=new AtomicBoolean();
    static void evictionGate(){
        if(evictionEntered==null||!evictionOnce.compareAndSet(false,true))return;
        evictionEntered.countDown();try{await(evictionRelease);}catch(Exception e){throw new RuntimeException(e);}
    }
    static void concurrentVisibleJoin(boolean global)throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch entered=new CountDownLatch(2),release=new CountDownLatch(1);
        RequestSession owner=global?null:r.openSession("trim-owner"),visible=r.openSession("racing-visible");AtomicInteger result=new AtomicInteger();
        Thread evictor=null,joiner=null;
        try {
            for(int i=0;i<2;i++)r.request(key(40000+i),Priority.P0_VISIBLE,()->{entered.countDown();await(release);return new Drawable(1);},null);
            await(entered);IconRenderKey shared=key(41000);
            r.request(owner,shared,Priority.P1_ADJACENT,()->new Drawable(77),null);
            int limit=global?MAX_RENDER_QUEUE_SIZE-8:MAX_SESSION_QUEUE_SIZE;
            for(int i=1;i<limit;i++)r.request(owner,key(42000+i),Priority.P1_ADJACENT,()->new Drawable(2),null);
            evictionEntered=new CountDownLatch(1);evictionRelease=new CountDownLatch(1);evictionOnce.set(false);
            evictor=new Thread(()->r.request(owner,key(43000),global?Priority.P0_VISIBLE:Priority.P1_ADJACENT,()->new Drawable(3),null));evictor.start();await(evictionEntered);
            joiner=new Thread(()->r.request(visible,shared,Priority.P0_VISIBLE,()->new Drawable(99),(k,b)->result.set(b==null?-1:b.id)));joiner.start();
            long end=System.nanoTime()+TimeUnit.SECONDS.toNanos(3);
            while(joiner.getState()!=Thread.State.BLOCKED&&joiner.isAlive()&&System.nanoTime()<end)Thread.sleep(1);
            evictionRelease.countDown();evictor.join(3000);joiner.join(3000);
            check(!evictor.isAlive()&&!joiner.isAlive(),"join and eviction lock order terminates global="+global);
            release.countDown();idle(r);
            check(result.get()==99,"racing visible join gets fresh batch instead of evicted null global="+global);
            check(r.pendingCount()==0,"racing join leaves no stale pending batch global="+global);
        } finally {if(evictionRelease!=null)evictionRelease.countDown();evictionEntered=null;release.countDown();r.cancelSession(owner);r.cancelSession(visible);r.decodePool.shutdownNow();r.onlinePool.shutdownNow();r.metadataPool.shutdownNow();r.indexPool.shutdownNow();}
    }
    static void postedCallbacksAfterCancel()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();AtomicInteger stale=new AtomicInteger(),fresh=new AtomicInteger();
        try {
            for(int i=0;i<32;i++){
                RequestSession old=r.openSession("posted-old");CountDownLatch loaded=new CountDownLatch(1);
                r.request(old,key(30000+i),Priority.P0_VISIBLE,()->{loaded.countDown();return new Drawable(1);},(k,b)->stale.incrementAndGet());await(loaded);
                long deadline=System.nanoTime()+TimeUnit.SECONDS.toNanos(3);
                while(r.pendingCount()!=0&&System.nanoTime()<deadline)Thread.sleep(1);
                check(r.pendingCount()==0,"completion detached before delayed MAIN delivery");r.cancelSession(old);
                RequestSession current=r.openSession("posted-new");
                r.request(current,key(31000+i),Priority.P0_VISIBLE,()->new Drawable(2),(k,b)->fresh.incrementAndGet());idle(r);r.cancelSession(current);
            }
            check(stale.get()==0,"32 cancelled generations dropped after completion was posted");
            check(fresh.get()==32,"32 replacement generations receive their own callbacks");
        } finally {r.decodePool.shutdownNow();r.onlinePool.shutdownNow();r.metadataPool.shutdownNow();r.indexPool.shutdownNow();}
    }
    static void globalQueueBound()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch entered=new CountDownLatch(2),release=new CountDownLatch(1);
        try {
            for(int i=0;i<2;i++)r.request(key(2000+i),Priority.P0_VISIBLE,()->{entered.countDown();await(release);return new Drawable(1);},null);
            await(entered);
            for(int i=0;i<MAX_RENDER_QUEUE_SIZE+32;i++)r.request(key(3000+i),Priority.P2_IDLE,()->new Drawable(2),null);
            check(r.decodePool.getQueue().size()<=MAX_RENDER_QUEUE_SIZE,"sessionless requests obey global render bound");
            check(r.pendingCount()<=MAX_RENDER_QUEUE_SIZE+2,"rejection releases pending consumers");
            AtomicInteger visible=new AtomicInteger();r.request(key(9000),Priority.P0_VISIBLE,()->new Drawable(9),(k,b)->visible.set(b==null?0:b.id));
            check(r.decodePool.getQueue().size()<=MAX_RENDER_QUEUE_SIZE,"visible admission replaces idle work within bound");
            release.countDown();idle(r);check(visible.get()==9,"visible icon completes despite an idle backlog");
            check(r.pendingCount()==0,"bounded backlog fully drains");
        } finally {release.countDown();r.decodePool.shutdownNow();r.onlinePool.shutdownNow();r.metadataPool.shutdownNow();r.indexPool.shutdownNow();}
    }
    static void catalogPrewarmIsolation()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();
        CountDownLatch entered=new CountDownLatch(1),release=new CountDownLatch(1);
        CountDownLatch otherEntered=new CountDownLatch(1),visibleStarted=new CountDownLatch(1);
        IconLibraryCatalog.entered=entered;IconLibraryCatalog.release=release;IconLibraryCatalog.loads.set(0);
        try {
            r.catalogPrewarmFromConstructor();await(entered);
            r.request(key(51001),Priority.P0_VISIBLE,()->{otherEntered.countDown();await(release);return new Drawable(1);},null);
            await(otherEntered);
            r.request(key(51002),Priority.P0_VISIBLE,()->{visibleStarted.countDown();return new Drawable(2);},null);
            boolean started=visibleStarted.await(2,TimeUnit.SECONDS);
            System.out.println("CATALOG_PREWARM owner="+IconLibraryCatalog.threadName+" renderActive="+r.decodePool.getActiveCount()+" directoryActive="+r.indexPool.getActiveCount()+" visibleWhileBlocked="+started);
            check(started,"visible icon starts while catalogue and one unrelated decoder remain blocked");
            check("probe-directory".equals(IconLibraryCatalog.threadName),"catalogue uses existing directory owner");
            check(IconLibraryCatalog.loads.get()==1,"constructor preload still runs once");
            release.countDown();idle(r);
        } finally {
            release.countDown();IconLibraryCatalog.entered=IconLibraryCatalog.release=null;
            r.decodePool.shutdownNow();r.onlinePool.shutdownNow();r.metadataPool.shutdownNow();r.indexPool.shutdownNow();
        }
    }
    static void queuedCatalogPrewarmRespectsTrim()throws Exception {
        IconPreviewRepository r=new IconPreviewRepository();CountDownLatch release=new CountDownLatch(1),entered=new CountDownLatch(3);
        IconLibraryCatalog.entered=null;IconLibraryCatalog.release=null;IconLibraryCatalog.loads.set(0);
        try {
            r.indexPool.execute(()->{entered.countDown();try{await(release);}catch(Exception e){throw new RuntimeException(e);}});
            for(int i=0;i<2;i++)r.request(key(52000+i),Priority.P0_VISIBLE,()->{entered.countDown();await(release);return new Drawable(1);},null);
            await(entered);r.catalogPrewarmFromConstructor();r.pauseP2=true;release.countDown();
            r.indexPool.submit(()->{}).get(3,TimeUnit.SECONDS);idle(r);
            check(IconLibraryCatalog.loads.get()==0,"queued preload retains low-memory pause gate");
        } finally {release.countDown();r.decodePool.shutdownNow();r.onlinePool.shutdownNow();r.metadataPool.shutdownNow();r.indexPool.shutdownNow();}
    }
    public static void main(String[] args)throws Exception {
        catalogPrewarmIsolation();queuedCatalogPrewarmRespectsTrim();
        visibleJoinSessionTrim(0);visibleJoinSessionTrim(1);visibleJoinSessionTrim(2);
        visibleBurstCancellation();postedCallbacksAfterCancel();
        concurrentVisibleJoin(false);concurrentVisibleJoin(true);
        globalQueueBound();
        metadataIsolation();
        networkIsolation();prefetch();localPrefetchAndDedup();eviction();staleCompletion();sharedConsumers();cancelledPreparation();memoryPressure();
        System.out.println("production preview checks="+checks+" failures="+failures);
        if(failures!=0)System.exit(1);
    }
'''
    if args.serial:
        if not args.sdk or not args.output:
            parser.error("--serial requires --sdk and --output")
        args.output.mkdir(parents=True, exist_ok=True)
        fixture = fixture.replace(block(fixture, "    static class Handler"), r'''
    static class Handler {
        final java.util.concurrent.ConcurrentLinkedQueue<Runnable> work = new java.util.concurrent.ConcurrentLinkedQueue<>();
        void post(Runnable r){work.add(r);}
        void drain(){
            CountDownLatch delivered=new CountDownLatch(1);
            new android.os.Handler(android.os.Looper.getMainLooper()).post(()->{
                try {Runnable r;while((r=work.poll())!=null)r.run();}
                finally {delivered.countDown();}
            });
            try {await(delivered);}catch(Exception e){throw new RuntimeException(e);}
        }
    }
''')
        fixture = fixture.replace("public static void main(String[] args)throws Exception {", "static void runChecks()throws Exception {")
        fixture += r'''
    public static void main(String[] args)throws Exception {
        android.os.Looper.prepareMainLooper();
        new Thread(()->{
            try {runChecks();}
            catch(Throwable error){error.printStackTrace();failures++;}
            finally {System.out.flush();System.err.flush();System.exit(failures==0?0:1);}
        },"preview-test-driver").start();
        android.os.Looper.loop();
        if(failures!=0)System.exit(1);
    }
'''
    with tempfile.TemporaryDirectory(prefix="icon-preview-") as temporary:
        base = pathlib.Path(temporary)
        java = base / "IconPreviewRepository.java"
        java.write_text("import java.util.*;import java.util.concurrent.*;import java.util.concurrent.atomic.*;\npublic class IconPreviewRepository {\n" + declarations + fields + methods + fixture + "\n}", encoding="utf-8")
        log = base / "android/util/Log.java"
        log.parent.mkdir(parents=True)
        log.write_text("package android.util;public class Log {public static int d(String t,String s){return 0;}public static int w(String t,String s){return 0;}public static int w(String t,String s,Throwable e){return 0;}}")
        clock = base / "android/os/SystemClock.java"
        clock.parent.mkdir(parents=True)
        clock.write_text("package android.os;public class SystemClock {public static long elapsedRealtime(){return System.nanoTime()/1000000;}}")
        if args.serial:
            android_jar = args.sdk / "platforms/android-36/android.jar"
            subprocess.run([str(args.jdk / "bin/javac.exe"), "-source", "8", "-target", "8", "-encoding", "UTF-8", "-classpath", str(android_jar), "-d", str(base), str(java)], check=True)
            jar = base / "probe.jar"
            subprocess.run([str(args.jdk / "bin/jar.exe"), "cf", str(jar), "-C", str(base), "."], check=True)
            dex = base / "dex"; dex.mkdir()
            subprocess.run([str(args.jdk / "bin/java.exe"), "-cp", str(args.sdk / "build-tools/37.0.0/lib/d8.jar"), "com.android.tools.r8.D8", "--lib", str(android_jar), "--min-api", "26", "--output", str(dex), str(jar)], check=True)
            remote = "/data/local/tmp/preview-queue-" + uuid.uuid4().hex + ".dex"
            adb = [str(args.sdk / "platform-tools/adb.exe"), "-s", args.serial]
            subprocess.run(adb + ["push", str(dex / "classes.dex"), remote], check=True, capture_output=True)
            try:
                result = subprocess.run(adb + ["shell", "env", "CLASSPATH=" + remote, "app_process", "/system/bin", "IconPreviewRepository"], text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=60)
                (args.output / "device.log").write_text(result.stdout + result.stderr, encoding="utf-8")
                print(result.stdout, end="")
                if result.returncode: raise RuntimeError(result.stderr + result.stdout)
                (args.output / "summary.json").write_text(json.dumps({"serial": args.serial, "scope": "extracted production queue/session methods; real ART executors and MAIN Looper, controlled delivery barrier; bitmap/drawable/cache/network are doubles; no APK installed or user data accessed", "result": result.stdout.strip()}, indent=2), encoding="utf-8")
            finally:
                subprocess.run(adb + ["shell", "rm", remote], check=True, capture_output=True)
        else:
            subprocess.run([str(args.jdk / "bin/javac.exe"), "-encoding", "UTF-8", "-d", str(base), str(java), str(log), str(clock)], check=True)
            subprocess.run([str(args.jdk / "bin/java.exe"), "-cp", str(base), "IconPreviewRepository"], check=True)
    host = (ROOT / "launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java").read_text(encoding="utf-8")
    adapter = block(host, "    private static final class AppIconAdapter")
    assert "previews.request(sCurrentIconPageSession" not in adapter
    assert "previews.schedule(requestSession," in adapter
    assert "sCurrentIconPageOwner.get() == activity" in block(host, "    public static void onSettingsHostDestroyed")
    print("PASS adapter session identity, metadata cancellation and destroyed-owner wiring")


if __name__ == "__main__":
    main()
