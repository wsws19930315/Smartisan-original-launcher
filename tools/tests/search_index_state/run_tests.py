"""Run production scheduling methods with a deterministic serial executor.

Android/model/snapshot construction are controlled boundaries. This tests task
liveness, rather than matching source strings or claiming end-to-end search UI.
"""
import argparse
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]


def method(source, signature):
    start = source.index(signature)
    pos = source.index('{', start)
    depth = 1
    end = pos + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


PREFIX = '''import java.util.*;
public class SearchIndexRepository {
 enum State { EMPTY, BUILDING, DIRTY, READY, FAILED }
 final Object stateLock=new Object(); State state=State.READY;
 boolean fullRebuildRequested; int pendingIncrementalCount, builds;
 Snapshot currentSnapshot=new Snapshot(); static class Snapshot {long generation=1;}
 static class QueueExecutor {final Queue<Runnable> queue=new ArrayDeque<>();
  void execute(Runnable r){queue.add(r);} void drain(){while(!queue.isEmpty())queue.remove().run();}}
 final QueueExecutor executor=new QueueExecutor();
 void buildSnapshot(long generation,String reason){builds++;currentSnapshot.generation=generation;state=State.READY;}
 static void check(boolean value,String message){if(!value)throw new AssertionError(message);}
'''
TEST = '''
 public static void main(String[] args) {
  int checks=0;
  if(args.length>0) for(boolean failed:new boolean[]{false,true}) for(int pending:new int[]{1,2,5}) {
   SearchIndexRepository r=new SearchIndexRepository();r.state=State.DIRTY;r.pendingIncrementalCount=pending;
   for(int i=0;i<10;i++)r.rebuildAsync("settings");
   check(r.executor.queue.isEmpty(),"rebuild must wait for current incremental tasks");checks++;
   for(int i=0;i<pending;i++) {
    r.finishIncremental(failed);
    if(i<pending-1){check(r.executor.queue.isEmpty(),"no early rebuild");checks++;}
   }
   check(r.executor.queue.size()==1,"last incremental must schedule exactly one full rebuild");checks++;
   r.executor.drain();check(r.state==State.READY && r.builds==1,"eventual READY after dirty request");checks++;
   check(!r.fullRebuildRequested && r.pendingIncrementalCount==0,"request consumed");checks++;
  }
  for(boolean failed:new boolean[]{false,true}) {
   SearchIndexRepository r=new SearchIndexRepository();r.state=State.DIRTY;r.pendingIncrementalCount=1;
   r.finishIncremental(failed);
   check(r.state==(failed?State.FAILED:State.READY),"ordinary completion state preserved");checks++;
   check(r.executor.queue.isEmpty(),"no unrequested full rebuild");checks++;
  }
  SearchIndexRepository r=new SearchIndexRepository();r.rebuildAsync("idle");
  check(r.state==State.BUILDING && r.executor.queue.size()==1,"ordinary full rebuild preserved");checks++;
  r.executor.drain();check(r.state==State.READY && r.currentSnapshot.generation==2,"generation advances");checks++;
  System.out.println("PASS SEARCH_INDEX_STATE_CHECKS="+checks);
 }
}
'''


def main():
    ap = argparse.ArgumentParser(__doc__)
    ap.add_argument('--jdk', required=True, type=Path)
    ap.add_argument('--probe-deferred-api', action='store_true', help='Known API-only liveness gap; no current production caller demonstrated. Expected to fail on the current owner.')
    ap.add_argument('--owner', type=Path, default=ROOT / 'launcher/tools/java/com/smartisanos/launcher/quicksearch/SearchIndexRepository.java')
    args = ap.parse_args()
    source = args.owner.read_text(encoding='utf-8')
    methods = '\n'.join(method(source, sig) for sig in (
        '    public void rebuildAsync(', '    private void finishIncremental('))
    with tempfile.TemporaryDirectory(prefix='search-index-state-') as tmp:
        tmp = Path(tmp)
        java = tmp / 'SearchIndexRepository.java'
        java.write_text(PREFIX + methods + TEST, encoding='utf-8')
        subprocess.run([str(args.jdk / 'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(tmp), str(java)], check=True)
        subprocess.run([str(args.jdk / 'bin/java.exe'), '-cp', str(tmp), 'SearchIndexRepository', *(['probe'] if args.probe_deferred_api else [])], check=True)


if __name__ == '__main__':
    main()
