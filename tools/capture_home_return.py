"""Collect HOME lifecycle, compositor and video evidence without changing app data.

Example: python tools/capture_home_return.py --serial SERIAL --label after --method key
Experiment settings are restored, including absent keys, in finally. No default-HOME changes.
"""
import argparse
import json
import re
import shlex
import subprocess
import time
from pathlib import Path

ADB_DEFAULT = r'D:\sdk\platform-tools\adb.exe'
KEYS = ('launcher_home_diagnostics_enabled', 'launcher_home_surface_attachment_experiment',
        'launcher_home_opaque_wallpaper_experiment')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--serial', required=True)
    ap.add_argument('--label', required=True)
    ap.add_argument('--method', choices=['key', 'gesture', 'back', 'recents', 'wake'], default='key')
    ap.add_argument('--gesture-duration-ms', type=int, default=200,
                    help='ADB swipe duration for controlled gesture A/B')
    ap.add_argument('--rounds', type=int, default=3)
    ap.add_argument('--settle-seconds', type=float, default=.8,
                    help='Measurement-only settling before sampling/next launch; no app delay')
    ap.add_argument('--attachment', action='store_true')
    ap.add_argument('--opaque-wallpaper-off', action='store_true')
    ap.add_argument('--diagnostics', action='store_true')
    ap.add_argument('--window-trace', action='store_true',
                    help='API 35+: collect WM/Shell/transaction evidence; adds tracing overhead')
    ap.add_argument('--host-layer', choices=['surface', 'window'], default='surface',
                    help='Expected HOME layer for measurement setup; not a visual readiness proof')
    ap.add_argument('--adb', default=ADB_DEFAULT)
    ap.add_argument('--out', type=Path, default=Path('build/home-unified-20261011'))
    args = ap.parse_args()
    if not .8 <= args.settle_seconds <= 5:
        ap.error('--settle-seconds must be between 0.8 and 5')
    if not 50 <= args.gesture_duration_ms <= 1000:
        ap.error('--gesture-duration-ms must be between 50 and 1000')
    if not re.fullmatch(r'[\w-]+', args.label): ap.error('label must be a safe filename')
    out = args.out / args.label
    out.mkdir(parents=True, exist_ok=True)
    base = [args.adb, '-s', args.serial]
    def run(*cmd, check=True):
        return subprocess.run(base + list(cmd), capture_output=True, text=True,
                              encoding='utf-8', errors='replace', check=check, timeout=30).stdout
    def binary_file(path, *cmd):
        result = subprocess.run(base + list(cmd), capture_output=True, check=True, timeout=30)
        path.write_bytes(result.stdout)
    previous = {k: run('shell', 'settings', 'get', 'global', k).strip() for k in KEYS}
    sdk = int(run('shell', 'getprop', 'ro.build.version.sdk').strip())
    if args.window_trace and sdk < 35:
        ap.error('--window-trace requires Android 15 or newer')
    wm = run('shell', 'wm', 'size')
    width, height = map(int, re.findall(r'(\d+)x(\d+)', wm)[-1])
    info = dict(serial=args.serial, sdk=sdk, wm=wm, method=args.method,
                navigation_mode=run('shell', 'settings', 'get', 'secure', 'navigation_mode').strip(),
                previous_settings=previous, attachment=args.attachment,
                opaque_wallpaper_off=args.opaque_wallpaper_off,
                window_trace=args.window_trace, host_layer=args.host_layer, samples=[])
    info['settle_seconds'] = args.settle_seconds
    info['gesture_duration_ms'] = args.gesture_duration_ms
    trace = None
    recording = None
    log_stream = None
    log_file = None
    trace_path = '/data/misc/perfetto-traces/home-unified-' + args.label + '.pftrace'
    record_path = '/sdcard/home-unified-' + args.label + '.mp4'
    def sample(label):
        layers = run('shell', 'dumpsys', 'SurfaceFlinger', '--list')
        windows = run('shell', 'dumpsys', 'window', 'windows')
        # Limit saved WindowManager state to the Launcher and wallpaper windows.
        blocks = re.split(r'(?=\s*Window #\d+)', windows)
        windows = '\n'.join(b for b in blocks if re.search(r'Window #\d+[^\n]*(smt_launcher|Wallpaper|launcher)', b))
        (out / (label + '-windows.txt')).write_text(windows, encoding='utf-8')
        (out / (label + '-layers.txt')).write_text(layers, encoding='utf-8')
        for i, layer in enumerate(s for s in layers.splitlines()
                                  if 'SurfaceView' in s and 'smt_launcher' in s and 'Background' not in s):
            # Older SurfaceFlinger exposes latency rows; newer --list output can
            # be a diagnostic wrapper, for which Perfetto remains the evidence.
            if layer.startswith('RequestedLayerState{'): continue
            latency = run('shell', 'dumpsys SurfaceFlinger --latency ' + shlex.quote(layer), check=False)
            (out / (label + '-latency-' + str(i) + '.txt')).write_text(latency, encoding='utf-8')
        top = [s.strip() for s in run('shell', 'dumpsys', 'activity', 'activities').splitlines()
               if re.search(r'(?:topResumedActivity=|mResumedActivity:|ResumedActivity:|Resumed:)', s)]
        info['samples'].append(dict(label=label, host_monotonic=time.monotonic(),
                                    pid=run('shell', 'pidof', 'com.smartisanos.launcher').strip(),
                                    top=top, layers=[s for s in layers.splitlines() if 'smt_launcher' in s]))
    def wait_home_surface():
        # Measurement setup only: do not count a cold install as a hot return.
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline:
            layers = run('shell', 'dumpsys', 'SurfaceFlinger', '--list')
            if args.host_layer == 'window':
                if any('smt_launcher#' in s and 'SurfaceView' not in s and 'Bounds' not in s
                       for s in layers.splitlines()): return
            elif any('SurfaceView' in s and 'smt_launcher' in s and 'Background' not in s
                     for s in layers.splitlines()): return
            time.sleep(.2)
        raise RuntimeError('Launcher Surface was not ready; this is not a valid hot-return sample')
    try:
        log_file = (out / 'timing.log').open('wb')
        log_stream = subprocess.Popen(base + ['logcat', '-v', 'monotonic', '-T', '1',
                   'SmartisanHome:I', 'HomeTextureHost:I', 'MaintainedSettings:I',
                   'LauncherStartup:I', 'UnlockAnimation:I',
                   'AndroidRuntime:E', 'DEBUG:F', '*:S'], stdout=log_file, stderr=subprocess.DEVNULL)
        desired = (int(args.diagnostics), int(args.attachment), int(args.opaque_wallpaper_off))
        for key, value in zip(KEYS, desired): run('shell', 'settings', 'put', 'global', key, str(value))
        run('shell', 'input', 'keyevent', 'KEYCODE_WAKEUP')
        policy = run('shell', 'dumpsys', 'window', 'policy')
        info['keyguard'] = [s.strip() for s in policy.splitlines()
                            if re.search(r'\b(showing|inputRestricted)=', s)]
        if re.search(r'\b(?:showing|inputRestricted)=true', policy):
            raise RuntimeError('Please unlock the device; HOME is currently blocked by Keyguard')
        run('shell', 'input', 'keyevent', 'KEYCODE_HOME')
        wait_home_surface()
        time.sleep(1)
        sample('before')
        binary_file(out / 'before.png', 'exec-out', 'screencap', '-p')
        run('shell', 'am', 'start', '-W', '-a', 'android.settings.SETTINGS')
        time.sleep(.5)
        duration = max(12, int(args.rounds * (args.settle_seconds + 3.2) + 4))
        if sdk >= 29:
            config = '''buffers { size_kb: 16384 fill_policy: RING_BUFFER }
buffers { size_kb: 8192 fill_policy: RING_BUFFER }
duration_ms: DURATION
write_into_file: true
file_write_period_ms: 1000
data_sources { config { name: "android.surfaceflinger.layers"
surfaceflinger_layers_config { mode: MODE_ACTIVE trace_flags: TRACE_FLAG_COMPOSITION
trace_flags: TRACE_FLAG_BUFFERS trace_flags: TRACE_FLAG_EXTRA } } }
data_sources { config { name: "android.surfaceflinger.frametimeline" target_buffer: 1 } }
data_sources { config { name: "linux.process_stats" target_buffer: 1 process_stats_config { scan_all_processes_on_start: true record_thread_names: true proc_stats_poll_ms: 1000 } } }
data_sources { config { name: "linux.ftrace" target_buffer: 1 ftrace_config {
ftrace_events: "ftrace/print"
atrace_categories: "wm" atrace_categories: "am" atrace_categories: "view"
atrace_categories: "gfx" atrace_categories: "input" atrace_apps: "com.smartisanos.launcher" } } }
'''.replace('DURATION', str(duration * 1000))
            if args.window_trace:
                # One trace clock for draw readiness, transition ownership and visibility.
                # No persistent system logging flags or stack trace collection.
                config += '''
data_sources { config { name: "android.windowmanager"
windowmanager_config { log_level: LOG_LEVEL_VERBOSE log_frequency: LOG_FREQUENCY_TRANSACTION } } }
data_sources { config { name: "com.android.wm.shell.transition" } }
data_sources { config { name: "android.surfaceflinger.transactions"
surfaceflinger_transactions_config { mode: MODE_ACTIVE } } }
data_sources { config { name: "android.protolog" target_buffer: 1
protolog_config { tracing_mode: DEFAULT
group_overrides { group_name: "WM_DEBUG_DRAW" log_from: PROTOLOG_LEVEL_DEBUG }
group_overrides { group_name: "WM_DEBUG_APP_TRANSITIONS" log_from: PROTOLOG_LEVEL_DEBUG }
group_overrides { group_name: "WM_DEBUG_WINDOW_TRANSITIONS" log_from: PROTOLOG_LEVEL_DEBUG }
group_overrides { group_name: "WM_DEBUG_SYNC_ENGINE" log_from: PROTOLOG_LEVEL_DEBUG }
group_overrides { group_name: "WM_SHOW_TRANSACTIONS" log_from: PROTOLOG_LEVEL_DEBUG }
group_overrides { group_name: "WM_SHELL_TRANSITIONS" log_from: PROTOLOG_LEVEL_DEBUG }
group_overrides { group_name: "WM_SHELL_RECENTS_TRANSITION" log_from: PROTOLOG_LEVEL_DEBUG }
} } }
'''
            (out / 'trace-config.txt').write_text(config, encoding='utf-8')
            trace = subprocess.Popen(base + ['shell', 'perfetto', '--txt', '-c', '-', '-o', trace_path],
                                     stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            trace.stdin.write(config.encode())
            trace.stdin.close()
        else:
            run('shell', 'atrace', '--async_start', '-c', '-b', '4096', '-a',
                'com.smartisanos.launcher', 'gfx', 'view', 'wm', 'am', 'input', check=False)
        recording = subprocess.Popen(base + ['shell', 'screenrecord', '--size', '540x1200',
                  '--bit-rate', '4000000', '--time-limit', str(duration), record_path],
                  stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        time.sleep(1)
        for i in range(args.rounds):
            if i:
                run('shell', 'am', 'start', '-W', '-a', 'android.settings.SETTINGS')
                time.sleep(.5)
            info.setdefault('actions', []).append(dict(round=i, host_monotonic=time.monotonic()))
            if args.method == 'gesture':
                run('shell', 'input', 'swipe', str(width//2), str(height-2), str(width//2), str(height//2),
                    str(args.gesture_duration_ms))
            elif args.method == 'wake':
                run('shell', 'input', 'keyevent', 'KEYCODE_SLEEP')
                time.sleep(.5)
                run('shell', 'input', 'keyevent', 'KEYCODE_WAKEUP')
                run('shell', 'wm', 'dismiss-keyguard', check=False)
                run('shell', 'input', 'keyevent', 'KEYCODE_HOME')
            elif args.method == 'recents':
                run('shell', 'input', 'keyevent', 'KEYCODE_APP_SWITCH')
                time.sleep(.5)
                run('shell', 'input', 'keyevent', 'KEYCODE_HOME')
            else: run('shell', 'input', 'keyevent', 'KEYCODE_' + ('BACK' if args.method == 'back' else 'HOME'))
            time.sleep(args.settle_seconds)
            sample('return-' + str(i))
        binary_file(out / 'after.png', 'exec-out', 'screencap', '-p')
        info['memory'] = run('shell', 'dumpsys', 'meminfo', 'com.smartisanos.launcher')
        info['process_stat'] = run('shell', 'pidof', 'com.smartisanos.launcher').strip()
        if sdk < 29:
            binary_file(out / 'trace.atrace', 'exec-out', 'atrace', '--async_stop', '-b', '4096',
                        '-a', 'com.smartisanos.launcher', 'gfx', 'view', 'wm', 'am', 'input')
        if recording:
            recording.wait(timeout=duration+15)
            (out / 'record.stderr').write_bytes(recording.stderr.read())
            run('pull', record_path, str(out / 'video.mp4'), check=False)
        if trace:
            trace.wait(timeout=duration+15)
            (out / 'trace.stderr').write_bytes(trace.stderr.read())
            run('pull', trace_path, str(out / 'trace.pftrace'), check=False)
    finally:
        for proc in (recording, trace):
            if proc is not None and proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=5)
        if log_stream:
            log_stream.terminate()
            log_stream.wait(timeout=5)
        if log_file: log_file.close()
        for key, value in previous.items():
            if value == 'null': run('shell', 'settings', 'delete', 'global', key, check=False)
            else: run('shell', 'settings', 'put', 'global', key, value, check=False)
        (out / 'samples.json').write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(out=str(out), samples=info['samples']), ensure_ascii=False))

if __name__ == '__main__': main()
