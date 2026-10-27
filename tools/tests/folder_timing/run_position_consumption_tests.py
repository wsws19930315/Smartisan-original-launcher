"""Execute the actual Cell placement branch and verify adapted Y is already final.

No geometry formulas are duplicated: the Java checks run production geometry helpers.
"""
from pathlib import Path
import argparse, json, re
from run_creation_gate_tests import execute, method, Obj
import run_geometry_tests as geometry

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--source', type=Path,
                        default=ROOT/'launcher/smali/com/smartisanos/launcher/view/b/M.smali')
    parser.add_argument('--jdk', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    body = method(args.source, 'protected fn()V')
    start = body.index('    iget v4, v4, Lcom/smartisanos/smengine/a/j;->y:F')
    start = body.index('\n', start) + 1
    end = body.index('    iget v6, p0, Lcom/smartisanos/launcher/view/b/M;->WG:F', start)
    actual = body[start:end] + '\n    return v4\n'
    raw, adapted = Obj('raw'), Obj('adapted')
    cases = [('adapted Folder snapshot', adapted, raw, 456., 456., 0),
             ('raw adaptation fallback', raw, raw, 123., 456., 1),
             ('ordinary page without snapshot', None, raw, 123., 123., 1),
             ('failed snapshot', None, raw, 123., 456., 1),
             ('new page snapshot after global replacement', Obj('new'), Obj('replacement'), 789., 789., 0)]
    checks = 0
    for name, snapshot, original, initial, adjusted, expected_calls in cases:
        calls = []
        def adjust(*values):
            calls.append(values)
            return adjusted
        env = {'registers': {'v14': snapshot, 'v4': initial, 'v9': 1, 'v10': 2},
               'static_fields': {('Lcom/smartisanos/launcher/data/Constants;',
                                  'pageCellCenterPoints'): original},
               'adjust_y': adjust}
        result = execute(actual, Obj('page'), None, env)
        assert result == adjusted and len(calls) == expected_calls, (name, result, len(calls))
        checks += 2
    # Use the real adapters over density, label, null-point and short-array boundaries.
    marker = 'if(copy[i]!=null){emit(copy[i].x);emit(copy[i].y);}'
    source = geometry.FIXTURES['GeometryProbe.java']
    assert source.count(marker) == 1
    geometry.FIXTURES['GeometryProbe.java'] = source.replace(marker, '''if(copy[i]!=null){
      float once=copy[i].y;
      float repeated=FolderCellPositionAdapter.adjustY(page,i/3,i%3,once);
      check(Float.floatToIntBits(once)==Float.floatToIntBits(repeated));
      emit(copy[i].x);emit(copy[i].y);
     }''')
    result = geometry.run_variant(ROOT/'launcher/tools/java/com/smartisanos/launcher/data',
                                  args.output/'geometry', args.jdk)
    java_checks = int(re.search(r'CHECKS=(\d+)', result.stderr)[1])
    summary = {'actualSmaliChecks': checks, 'productionGeometryChecks': java_checks,
               'scope': 'per-page snapshot only; raw/null fallback retained; no geometry cache added'}
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2))
    print('PASS POSITION_SNAPSHOT_REUSE ' + json.dumps(summary))


if __name__ == '__main__':
    main()
