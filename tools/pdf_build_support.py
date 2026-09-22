"""Load immutable PDF baselines so rebuilding never stacks previous overlays."""
import argparse
import subprocess
import tempfile
from pathlib import Path

BASELINE_COMMIT = 'a17fc462c76c4148ea9563914f6f5cd95a1191b2'


def build_paths(slug):
    parser = argparse.ArgumentParser(description=f'Rebuild module {slug} from its original PDF.')
    parser.add_argument('--source', type=Path, help='Original v0.1.0 PDF; defaults to the Git baseline.')
    parser.add_argument('--output', type=Path, help='Destination PDF; defaults to the module folder.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    relative = f'module-{slug}/module-{slug}.pdf'
    if args.source:
        source = args.source.resolve()
    else:
        data = subprocess.run(
            ['git', 'show', f'{BASELINE_COMMIT}:{relative}'], cwd=root,
            check=True, capture_output=True,
        ).stdout
        # The temporary directory lives until the process exits.
        global _baseline_dir
        _baseline_dir = tempfile.TemporaryDirectory(prefix='sas-pdf-baseline-')
        source = Path(_baseline_dir.name) / f'module-{slug}.pdf'
        source.write_bytes(data)
    output = args.output.resolve() if args.output else root / relative
    if source == output:
        raise ValueError('Source and output paths must differ.')
    output.parent.mkdir(parents=True, exist_ok=True)
    return root, source, output
