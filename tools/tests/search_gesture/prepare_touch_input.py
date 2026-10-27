"""Prepare a shell-only stable-downTime gesture producer for device regression.

Usage after preparation:
  adb -s SERIAL shell 'CLASSPATH=/data/local/tmp/smartisan-touch-input.dex app_process /system/bin TouchInput swipe X1 Y1 X2 Y2 MS'
Use cancel instead of swipe to finish the same stream with ACTION_CANCEL.
Use multi-cancel-2/3/4 to pause at the endpoint for 2.5 seconds, add fingers,
and cancel the stream when auditing Quick Desktop ownership transfer.
No APK installation or app settings changes are performed.
"""
import argparse
import os
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--jdk', required=True, type=Path)
    parser.add_argument('--sdk', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    classes, dex = args.output / 'classes', args.output / 'dex'
    classes.mkdir(exist_ok=True)
    dex.mkdir(exist_ok=True)

    def run(command, log):
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                                encoding='utf8', errors='replace', timeout=90)
        (args.output / log).write_text(result.stdout + result.stderr, encoding='utf8')
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)

    run([args.jdk / 'bin/javac.exe', '-source', '8', '-target', '8',
         '-bootclasspath', args.sdk / 'platforms/android-36/android.jar', '-d', classes,
         Path(__file__).with_name('TouchInput.java')], 'compile.log')
    jar = args.output / 'touch.jar'
    run([args.jdk / 'bin/jar.exe', 'cf', jar, '-C', classes, '.'], 'jar.log')
    os.environ['JAVA_HOME'] = str(args.jdk)
    run([args.sdk / 'build-tools/37.0.0/d8.bat', '--min-api', '23', '--output', dex, jar], 'dex.log')
    run([args.sdk / 'platform-tools/adb.exe', '-s', args.serial, 'push', dex / 'classes.dex',
         '/data/local/tmp/smartisan-touch-input.dex'], 'push.log')
    print('Prepared /data/local/tmp/smartisan-touch-input.dex; preserves one downTime per gesture')


if __name__ == '__main__':
    main()
