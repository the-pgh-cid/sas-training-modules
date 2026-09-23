"""Run three Python and/or R acceptance tests per teaching module."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULES = json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--modules', nargs='+', type=int, default=list(range(1, 11)))
    parser.add_argument('--language', choices=['both', 'python', 'r'], default='both')
    parser.add_argument('--rscript', default='Rscript', help='Native Rscript executable')
    parser.add_argument('--webr', action='store_true', help='Use the optional Node/WebR adapter instead of Rscript')
    parser.add_argument('--report', type=Path, help='Write a complete execution report')
    args = parser.parse_args()
    if any(n not in range(1, 11) for n in args.modules):
        parser.error('Module numbers must be 1-10')
    if args.language != 'python':
        if args.webr:
            if not shutil.which('node'):
                parser.error('Node is required for --webr; see APPENDICES.md')
            r_command = ['node', str(ROOT / 'tools/run_r_webr.cjs')]
        else:
            if not shutil.which(args.rscript):
                parser.error('Rscript is unavailable. Install R, use --webr (APPENDICES.md), or select --language python.')
            r_command = [args.rscript]
    lines = ['APPENDIX ACCEPTANCE TESTS',
             'Executed UTC: '+datetime.now(timezone.utc).isoformat(timespec='seconds'),
             'Python '+platform.python_version(),
             'Reference implementations only. No SAS execution or new model trials.']
    failures, totals = [], {'python': 0, 'r': 0}
    for m in MODULES:
        if m['id'] not in args.modules:
            continue
        folder = ROOT / f"module-{m['id']:02d}-{m['slug']}" / 'appendix'
        for lang in ['python', 'r']:
            if args.language not in ['both', lang]:
                continue
            script = folder / ('test_reference.py' if lang == 'python' else 'test_reference.R')
            command = [sys.executable, str(script)] if lang == 'python' else r_command+[str(script)]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
            output = result.stdout+result.stderr
            if lang == 'python':
                count_ok = bool(re.search(r'Ran 3 tests?\b', output))
            else:
                count_ok = all(re.search(r'PASS\s+T'+str(i)+r'\b', output) for i in [1, 2, 3])
            passed = result.returncode == 0 and count_ok
            name = f"{m['id']:02d} {m['slug']} / {lang}"
            lines.extend(['', name, output.rstrip(),
                          'RESULT: '+('PASS (3 tests)' if passed else 'FAIL (exit or test-count check)')])
            print(name+': '+('PASS (3 tests)' if passed else 'FAIL'), flush=True)
            if passed:
                totals[lang] += 3
            else:
                failures.append(name)
    lines.extend(['', f"PASSED: Python {totals['python']}; R {totals['r']}",
                  'SAS checks supplied but not executed.',
                  'OVERALL: '+('FAIL' if failures else 'PASS')])
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text('\n'.join(lines)+'\n')
    if failures:
        print('\n'.join(lines), file=sys.stderr)
        return 1
    print(lines[-3]+'; '+lines[-1])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
