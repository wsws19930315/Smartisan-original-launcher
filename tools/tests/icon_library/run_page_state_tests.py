"""Exercise the production icon-library resume and retry handlers with fake views."""

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "launcher/tools/java/com/smartisanos/home/settings/icons/IconLibrarySearchPage.java"


def method(source, signature):
    start = source.index(signature)
    cursor = source.index("{", start) + 1
    depth = 1
    while depth:
        depth += (source[cursor] == "{") - (source[cursor] == "}")
        cursor += 1
    return source[start:cursor]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jdk", type=Path, default=Path("E:/Program Files/Android/Android Studio/jbr"))
    args = parser.parse_args()
    source = SOURCE.read_text(encoding="utf-8")
    resume = method(source, "public IconPreviewRepository.RequestSession resume()")
    pause = method(source, "public void pause()")
    error = method(source, "private void showDirectoryError()")
    body = r'''
public class IconLibrarySearchPage {
    static final int GONE=8, VISIBLE=0;
    interface OnClickListener { void onClick(View view); }
    static class View {
        int visibility=VISIBLE;
        int removals;
        OnClickListener click;
        void setVisibility(int value){visibility=value;}
        void setOnClickListener(OnClickListener value){click=value;}
        void removeCallbacks(Runnable value){removals++;}
    }
    static class TextView extends View { String text="";void setText(String value){text=value;} }
    static class Loading {
        final View root=new View();
        final View progress=new View();
        final TextView message=new TextView();
    }
    static class IconPreviewRepository {
        static class RequestSession { boolean cancelled; }
        RequestSession openSession(String name){return new RequestSession();}
        void cancelSession(RequestSession session){session.cancelled=true;}
    }
    static class IconLibraryCatalog {
        static IconLibraryCatalog current=new IconLibraryCatalog();
        static IconLibraryCatalog peek(){return current;}
    }
    static class IconPackManager {
        static boolean ready=true;
        static long searchGeneration(){return 7;}
        static boolean isSearchIndexReady(IconLibraryCatalog c){return ready&&c==IconLibraryCatalog.peek();}
    }
    IconLibraryCatalog directoryCatalog=IconLibraryCatalog.peek();
    final Loading loading=new Loading();
    final IconPreviewRepository repository=new IconPreviewRepository();
    IconPreviewRepository.RequestSession session=new IconPreviewRepository.RequestSession();
    boolean closed,paused,directoryReady,packsReady,queryPending;
    long directoryGeneration=7;
    int filterCalls,bindCalls,indexCalls;
    CancellationSignal queryCancel;
    int generation,saves,selections,releases;
    boolean bindPosted;
    final View grid=new View();final Runnable bindFrame=()->{};
    static class Handler {int removals;void removeCallbacksAndMessages(Object token){removals++;}}
    final Handler main=new Handler();
    void saveResultState(){saves++;}
    void cancelSelection(){selections++;}
    void releaseBindings(){releases++;}
    final java.util.Set<Integer> loadingPages=new java.util.HashSet<Integer>();
    static class CancellationSignal {boolean cancelled;void cancel(){cancelled=true;}}
    void bindVisible(){bindCalls++;}
    void scheduleFilter(boolean browse,boolean debounce){filterCalls++;queryPending=false;}
    void initializeDirectory(){indexCalls++;}
    static void check(boolean value,String detail){if(!value)throw new AssertionError(detail);}
    RESUME_METHOD
    PAUSE_METHOD
    ERROR_METHOD
    public static void main(String[] args){
        IconLibrarySearchPage page=new IconLibrarySearchPage();
        page.paused=true;page.directoryReady=true;page.packsReady=true;page.queryPending=true;
        page.resume();
        check(page.filterCalls==1 && page.bindCalls==0,"cancelled query must restart after resume");
        page.paused=true;page.resume();
        check(page.filterCalls==1 && page.bindCalls==1,"settled result only rebinds");
        page.paused=true;page.directoryGeneration=6;page.resume();
        check(page.indexCalls==1,"changed pack index refreshes directory");
        page.loading.message.setVisibility(GONE);
        page.showDirectoryError();
        check(page.loading.message.visibility==VISIBLE,"retry text must be visible");
        check("加载失败，点击重试".equals(page.loading.message.text),"retry text matches action");
        page.loading.root.click.onClick(new View());
        check(page.indexCalls==2,"retry click starts directory load");
        IconLibrarySearchPage pausedPage=new IconLibrarySearchPage();
        pausedPage.directoryReady=true;pausedPage.packsReady=true;pausedPage.queryPending=true;pausedPage.bindPosted=true;
        IconPreviewRepository.RequestSession old=pausedPage.session;CancellationSignal oldQuery=new CancellationSignal();pausedPage.queryCancel=oldQuery;
        pausedPage.pause();
        check(pausedPage.paused&&pausedPage.generation==1&&pausedPage.saves==1,"actual pause invalidates generation and saves state");
        check(oldQuery.cancelled&&old.cancelled,"pause cancels old query and image session");
        check(pausedPage.releases==1&&pausedPage.selections==1,"pause releases row subscriptions and pending selection");
        check(!pausedPage.bindPosted&&pausedPage.grid.removals==1&&pausedPage.main.removals==1,"pause removes queued binding and UI messages");
        pausedPage.pause();check(pausedPage.saves==1&&pausedPage.generation==1,"duplicate pause is a no-op");
        pausedPage.resume();check(!pausedPage.paused&&pausedPage.session!=old&&!pausedPage.session.cancelled,"resume allocates fresh image session");
        check(pausedPage.filterCalls==1&&pausedPage.queryCancel!=oldQuery&&!pausedPage.queryCancel.cancelled,"cancelled query restarts with fresh cancellation token");
        pausedPage.closed=true;pausedPage.pause();check(pausedPage.saves==1,"closed page ignores pause");
        IconLibrarySearchPage replaced=new IconLibrarySearchPage();
        replaced.paused=true;replaced.directoryReady=true;replaced.packsReady=true;
        IconLibraryCatalog.current=new IconLibraryCatalog();replaced.resume();
        check(replaced.indexCalls==1&&replaced.bindCalls==0,"same-generation replacement catalog must refresh on resume");
        IconLibrarySearchPage incomplete=new IconLibrarySearchPage();
        incomplete.paused=true;incomplete.directoryReady=true;incomplete.packsReady=true;IconPackManager.ready=false;incomplete.resume();
        check(incomplete.indexCalls==1&&incomplete.bindCalls==0,"resume cannot bind an index no longer ready");
        System.out.println("PASS icon library pause/resume/retry 16 checks");
    }
}
'''
    body = body.replace("RESUME_METHOD", resume.replace("new android.os.CancellationSignal()", "new CancellationSignal()"))
    body = body.replace("ERROR_METHOD", error)
    body = body.replace("PAUSE_METHOD", pause)
    with tempfile.TemporaryDirectory(prefix="icon-library-page-") as tmp:
        java = Path(tmp) / "IconLibrarySearchPage.java"
        java.write_text(body, encoding="utf-8")
        subprocess.run([str(args.jdk / "bin/javac.exe"), "-encoding", "UTF-8", str(java)], check=True)
        subprocess.run([str(args.jdk / "bin/java.exe"), "-cp", tmp, "IconLibrarySearchPage"], check=True)
    # These transitions are in larger UI methods; guard their real source wiring.
    filter_method = method(source, "private void scheduleFilter(boolean browse, boolean debounce)")
    rows_method = method(source, "private void setRows(")
    categories_method = method(source, "private void showCategories()")
    if "queryPending = true" not in filter_method or "queryPending = false" not in rows_method or "queryPending = false" not in categories_method:
        raise AssertionError("query pending state is not wired to schedule, publish and category exit")


if __name__ == "__main__":
    main()
