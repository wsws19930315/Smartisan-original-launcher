"""Check exact ELF patch bytes and exercise real native array writes on an arm64 device."""
import argparse
import importlib.util
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--ndk', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--negative-library', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('batch_patch', ROOT / 'tools/patch_native_batch_capacity.py')
    patch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(patch)
    library = ROOT / 'launcher/lib/arm64-v8a/liblauncher_opt.so'
    assert patch.patch(library.read_bytes()) == library.read_bytes(), 'production ELF is not patched'
    constants = (ROOT / 'launcher/smali/com/smartisanos/launcher/data/Constants.smali').read_text()
    method = constants.split('.method public static getCellNumByMode(I)I')[1].split('.end method')[0]
    counts = [int(value, 16) for value in re.findall(r'const/16 p0, 0x([0-9a-f]+)', method)]
    assert max(counts) <= patch.CAPACITY, 'a configured grid exceeds the verified native capacity'
    writers = set()
    for source in (ROOT / 'launcher/smali').rglob('*.smali'):
        text = source.read_text('utf-8')
        if re.search(r'->(?:calculateMVPMatrixArrayData(?:WithChildZ)?|calculateModeSpaceLightDirArrayData)\(', text):
            writers.add(re.search(r'^\.class .* (L[^;]+;)', text).group(1))
    expected = {'Lcom/smartisanos/launcher/view/b;', 'Lcom/smartisanos/launcher/view/c;',
                'Lcom/smartisanos/launcher/view/b/ka;'}
    assert writers == expected, ('batch allocation owners changed', writers)
    scene = (ROOT / 'launcher/smali/com/smartisanos/smengine/SceneNode.smali').read_text()
    for owner in expected:
        assert 'instance-of v0, p0, ' + owner in scene
    assert '->create(Z)J' in scene and ':native_node_allocated' in scene
    print('PASS ALL_NATIVE_BATCH_WRITER_OWNERS=3')
    adb = [str(args.sdk / 'platform-tools/adb.exe'), '-s', args.serial]

    def run(command):
        result = subprocess.run([str(v) for v in command], capture_output=True, timeout=45)
        if result.returncode:
            raise RuntimeError(result.stdout.decode(errors='replace') + result.stderr.decode(errors='replace'))
        return result.stdout.decode(errors='replace')

    clang = args.ndk / 'toolchains/llvm/prebuilt/windows-x86_64/bin/aarch64-linux-android26-clang++.cmd'
    executable = args.output / 'bounds-probe'
    run([clang, Path(__file__).with_name('NativeBatchBoundsProbe.cpp'), '-static-libstdc++',
         '-ldl', '-o', executable])
    remote = '/data/local/tmp/smartisan-native-batch-probe'
    try:
        run(adb + ['push', executable, remote])
        run(adb + ['shell', 'chmod', '755', remote])
        run(adb + ['push', ROOT / 'launcher/lib/arm64-v8a/liblauncher_batch_compat.so', remote + '-bridge.so'])
        for name, path, size in [('fixed', library, patch.NODE_SIZE),
                                 ('negative', args.negative_library, 0x818)]:
            if path is None:
                continue
            run(adb + ['push', path, remote + '.so'])
            command = adb + ['shell', remote, remote + '.so', hex(size)]
            if name == 'fixed':
                command.append(remote + '-bridge.so')
            output = run(command)
            (args.output / (name + '.txt')).write_text(output)
            if name == 'fixed':
                assert 'PASS ORDINARY_NODE_ORIGINAL_SIZE' in output
                assert 'PASS ARRAY_ZERO_INITIALIZATION' in output
                assert 'PASS CREATE_RELEASE_CYCLES=10000' in output
                assert output.count('outside_object_changed_bytes=0') == patch.CAPACITY
                assert output.count('legacy_fields_changed=0 outside=0') == patch.CAPACITY
                print('PASS REAL_NATIVE_ARRAY_WRITES=%d' % (patch.CAPACITY * 2))
            else:
                assert 'index=16 outside_object_changed_bytes=12' in output
                assert 'matrix_index=80 legacy_fields_changed=0 outside=64' in output
                print('PASS NEGATIVE_ORIGINAL_OVERFLOW_REPRODUCED')
    finally:
        run(adb + ['shell', 'rm', '-f', remote, remote + '.so', remote + '-bridge.so'])
    print('PASS EXACT_ELF_PATCH_AND_GRID_COVERAGE')


if __name__ == '__main__':
    main()
