"""Build the small arm64 allocation bridge with an existing Android NDK."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--ndk', type=Path)
    args = parser.parse_args()
    candidates = [args.ndk] if args.ndk else []
    if os.environ.get('ANDROID_NDK_HOME'):
        candidates.append(Path(os.environ['ANDROID_NDK_HOME']))
    directory = args.sdk / 'ndk'
    if directory.is_dir():
        candidates.extend(sorted(directory.iterdir(), key=lambda p: tuple(
            int(v) for v in p.name.split('.') if v.isdigit()), reverse=True))
    compiler = next((p / 'toolchains/llvm/prebuilt/windows-x86_64/bin/aarch64-linux-android23-clang++.cmd'
                     for p in candidates if p is not None and (p / 'toolchains/llvm/prebuilt/windows-x86_64/bin/aarch64-linux-android23-clang++.cmd').is_file()), None)
    if compiler is None:
        raise RuntimeError('Existing Android NDK required for native batch allocation bridge; set ANDROID_NDK_HOME')
    source = ROOT / 'launcher/tools/native/launcher_batch_compat.cpp'
    target = ROOT / 'launcher/lib/arm64-v8a/liblauncher_batch_compat.so'
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='smartisan-native-batch-') as work:
        result = Path(work) / target.name
        subprocess.run([str(compiler), str(source), '-O2', '-shared', '-fPIC',
                        '-fvisibility=hidden', '-fvisibility-inlines-hidden', '-ffunction-sections',
                        '-fdata-sections', '-fno-exceptions', '-fno-rtti',
                        '-static-libstdc++', '-ldl', '-Wl,--gc-sections',
                        '-Wl,--exclude-libs,ALL', '-Wl,--strip-all',
                        '-Wl,-z,max-page-size=16384', '-Wl,-z,common-page-size=16384',
                        '-Wl,--build-id=none', '-Wl,-soname,' + target.name,
                        '-o', str(result)], check=True)
        content = result.read_bytes()
        if not target.exists() or target.read_bytes() != content:
            target.write_bytes(content)
    print('[native] Built arm64 batch allocation bridge with ' + str(compiler))


if __name__ == '__main__':
    main()
