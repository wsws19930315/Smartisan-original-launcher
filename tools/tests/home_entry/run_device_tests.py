"""Run the built HOME entry helper on ART without touching installed Launcher data."""
import argparse
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(__doc__)
    for key in ('serial', 'jdk', 'sdk', 'output'):
        parser.add_argument('--' + key, required=True)
    args = parser.parse_args()
    out, jdk, sdk = Path(args.output), Path(args.jdk), Path(args.sdk)
    out.mkdir(parents=True, exist_ok=True)
    classes, dex = out/'classes', out/'dex'
    classes.mkdir(exist_ok=True); dex.mkdir(exist_ok=True)

    def run(command, log):
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=90)
        (out/log).write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        return result.stdout

    run([jdk/'bin/javac.exe', '-encoding', 'UTF-8', '-source', '8', '-target', '8',
         '-bootclasspath', sdk/'platforms/android-36/android.jar',
         '-classpath', ROOT/'build/scratch/classes', '-d', classes,
         Path(__file__).with_name('HomeEntryProbe.java')], 'compile.log')
    run([jdk/'bin/jar.exe', 'cf', out/'probe.jar', '-C', classes, '.'], 'jar.log')
    os.environ['JAVA_HOME'] = str(jdk)
    run([sdk/'build-tools/37.0.0/d8.bat', '--min-api', '23', '--output', dex,
         out/'probe.jar'], 'dex.log')
    adb = sdk/'platform-tools/adb.exe'
    remote = '/data/local/tmp/smartisan-home-entry'
    try:
        run([adb, '-s', args.serial, 'push', dex/'classes.dex', remote+'-probe.dex'], 'push.log')
        run([adb, '-s', args.serial, 'push', ROOT/'build/scratch/dex/classes2.dex',
             remote+'-helper.dex'], 'push-helper.log')
        result = run([adb, '-s', args.serial, 'shell',
                      f'CLASSPATH={remote}-probe.dex:{remote}-helper.dex '
                      'app_process /system/bin com.smartisanos.launcher.gesture.HomeEntryProbe'],
                     'device.log')
        assert 'PASS HOME_ENTRY' in result, result
        print(result)
    finally:
        run([adb, '-s', args.serial, 'shell', 'rm', '-f', remote+'-probe.dex',
             remote+'-helper.dex'], 'cleanup.log')


if __name__ == '__main__':
    main()
