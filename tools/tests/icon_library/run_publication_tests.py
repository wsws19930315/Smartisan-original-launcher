"""Execute production page delivery methods with explicitly drained worker/MAIN queues."""
import argparse
from pathlib import Path
import subprocess
from run_page_state_tests import method, SOURCE

def main():
    parser=argparse.ArgumentParser(__doc__)
    parser.add_argument('--source',type=Path,default=SOURCE)
    parser.add_argument('--jdk',type=Path,default=Path('E:/Program Files/Android/Android Studio/jbr'))
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    source=args.source.read_text(encoding='utf-8')
    body=Path(__file__).with_name('PublicationFixture.java.txt').read_text(encoding='utf-8')
    for marker,signature in [('INITIALIZE','private void initializeDirectory()'),
                             ('FILTER','private void scheduleFilter(boolean browse, boolean debounce)'),
                             ('PAGE','private void requestPackPage(final int offset)'),
                             ('SAVE','private void saveResultState()')]:
        body=body.replace(marker+'_METHOD',method(source,signature))
    for old,new in [('android.os.CancellationSignal','CancellationSignal'),
                    ('android.os.SystemClock','SystemClock'),('android.util.Log','Log')]:
        body=body.replace(old,new)
    java=args.output/'IconLibrarySearchPage.java';java.write_text(body,encoding='utf-8')
    result=subprocess.run([str(args.jdk/'bin/javac.exe'),'-encoding','UTF-8',str(java)],capture_output=True,text=True)
    (args.output/'compile.log').write_text(result.stdout+result.stderr,encoding='utf-8')
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    result=subprocess.run([str(args.jdk/'bin/java.exe'),'-cp',str(args.output),'IconLibrarySearchPage'],capture_output=True,text=True,timeout=30)
    (args.output/'result.log').write_text(result.stdout+result.stderr,encoding='utf-8')
    print(result.stdout,end='')
    if result.returncode:raise RuntimeError(result.stderr)

if __name__=='__main__':main()
