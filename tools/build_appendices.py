"""Append language comparisons and acceptance tests to immutable v0.2 lessons."""
import argparse
from io import BytesIO
import json
from pathlib import Path
import subprocess

import fitz
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
CORE_COMMIT = '1800819e7ecf1485dce3820046146824d5f735a5'
MODULES = json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
BG, INK, BODY, MUTED = '#F5F7F5', '#17394A', '#253D46', '#566D75'
TEAL, ORANGE, PALE, WARM, LINE = '#137E79', '#B66C32', '#E8F2EE', '#F6EDE3', '#D8E1DF'
for name, file in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'),
                   ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + file))


def text(c, x, y, value, size=10.5, font='Body', color=BODY, width=None):
    limit = width if width is not None else 916-x
    if pdfmetrics.stringWidth(value, font, size) > limit + .1:
        raise ValueError(f'Text wider than {limit}: {value!r}')
    c.setFillColor(HexColor(color))
    c.setFont(font, size)
    c.drawString(x, 600-y, value)


def para(c, x, y, value, width, size=10.5, leading=14, bottom=None, color=BODY):
    lines, line = [], ''
    for word in value.split():
        candidate = (line + ' ' + word).strip()
        if line and pdfmetrics.stringWidth(candidate, 'Body', size) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    end = y + max(0, len(lines)-1)*leading
    if bottom is not None and end > bottom:
        raise ValueError(f'Paragraph ends at {end}, below {bottom}: {value!r}')
    for i, line in enumerate(lines):
        text(c, x, y+i*leading, line, size=size, color=color, width=width)
    return end


def rect(c, x, y, w, h, color, radius=0):
    c.setFillColor(HexColor(color))
    c.roundRect(x, 600-y-h, w, h, radius, stroke=0, fill=1)


def label(c, x, y, value, color=TEAL, size=8.7):
    text(c, x, y, value, size, 'Bold', color)


def header(c, m, title, subtitle):
    rect(c, 0, 0, 960, 600, BG)
    label(c, 44, 30, 'SAS TO PYTHON / R  |  LLM COLLABORATION', INK)
    label(c, 672, 30, f"APPENDIX / MODULE {m['id']:02d}", MUTED)
    text(c, 44, 82, title, 28, 'Bold', INK)
    para(c, 44, 108, subtitle, 872, size=10.5, leading=14, bottom=125, color=MUTED)


def footer(c, m, n):
    c.setStrokeColor(HexColor(LINE))
    c.setLineWidth(.7)
    c.line(44, 600-544, 916, 600-544)
    label(c, 44, 561, f"{m['id']:02d} / {m['slug'].upper()} / APPENDIX", INK, 8)
    text(c, 370, 561, 'Appendix v0.1.0 | 23 Sep 2026', 8, color=MUTED)
    text(c, 875, 561, f'A{n}/2', 8, color=MUTED)


def comparison_page(c, m, data):
    header(c, m, 'One behavior, three implementations', data['comparison_intro'])
    for x, lang, title in [(44, 'sas', 'SAS / SOURCE BEHAVIOR'),
                           (342, 'python', 'PYTHON / PANDAS'), (640, 'r', 'R / BASE')]:
        label(c, x, 147, title)
        rect(c, x, 160, 276, 277, '#FFFFFF', 9)
        lines = data['snippets'][lang]
        if len(lines) > 17:
            raise ValueError(f"{m['id']} {lang}: more than 17 snippet lines")
        for i, line in enumerate(lines):
            text(c, x+14, 182+i*12.4, line, 9.3, 'Mono', width=248)
        c.setStrokeColor(HexColor(LINE))
        c.line(x+14, 600-397, x+262, 600-397)
        para(c, x+14, 412, data['language_notes'][lang], 248,
             size=9, leading=11, bottom=434, color=MUTED)
    for x, note in zip([44, 490], data['semantic_notes']):
        rect(c, x, 447, 426, 63, PALE, 8)
        text(c, x+13, 465, note['title'], 10.5, 'Bold', TEAL, width=400)
        para(c, x+13, 481, note['text'], 400, size=9.5, leading=12, bottom=505)
    # Full citations are retained in appendix.json and the companion README.
    for i, ref in enumerate(data.get('references', [])[:3]):
        x = 44+i*280
        title = ref['label']
        text(c, x, 531, title, 8.3, 'Bold', MUTED, width=266)
        w = pdfmetrics.stringWidth(title, 'Bold', 8.3)
        c.linkURL(ref['url'], (x, 600-534, x+w, 600-522), relative=0)
    footer(c, m, 1)
    c.showPage()


def tests_page(c, m, data):
    header(c, m, 'Three checks that earn the pass',
           'Use the same inputs and expected behavior in each language. Check the contract as well as the values.')
    tests = data['tests']
    if [t['id'] for t in tests] != ['T1', 'T2', 'T3']:
        raise ValueError('Exactly T1, T2 and T3 are required')
    for test, y in zip(tests, [147, 261, 375]):
        rect(c, 44, y, 872, 104, '#FFFFFF', 9)
        rect(c, 44, y, 5, 104, TEAL if test['id'] != 'T2' else ORANGE, 2)
        text(c, 62, y+22, test['id']+' / '+test['name'], 13, 'Bold', INK)
        for x, key, title in [(62, 'input', 'INPUT / CONDITION'),
                               (350, 'expected', 'EXPECTED'), (640, 'catches', 'WHAT THIS CATCHES')]:
            label(c, x, y+43, title, MUTED, 8)
            para(c, x, y+61, test[key], 254, size=10, leading=12.5, bottom=y+99)
    slug = f"{m['id']:02d}-{m['slug']}"
    label(c, 44, 504, f'REFERENCE CODE + TESTS: module-{slug}/appendix/', INK, 8.5)
    text(c, 44, 521, f"Run: python tools/run_appendix_tests.py --modules {m['id']:02d}", 9.2, 'Mono')
    text(c, 44, 536, 'New reference code, separate from historical trials. SAS checks await execution; scope is stated in the companion README.', 8.4, color=MUTED)
    footer(c, m, 2)
    c.showPage()


def build(m, args):
    slug = f"{m['id']:02d}-{m['slug']}"
    rel = Path(f'module-{slug}/module-{slug}.pdf')
    data = json.loads((ROOT / f'module-{slug}/appendix/appendix.json').read_text())
    if data['module_id'] != m['id'] or data['slug'] != m['slug']:
        raise ValueError('Appendix identity does not match module')
    if args.source_dir:
        source = (args.source_dir / rel.name).read_bytes()
    else:
        source = subprocess.run(['git', 'show', f'{CORE_COMMIT}:{rel.as_posix()}'],
                                cwd=ROOT, capture_output=True, check=True).stdout
    doc = fitz.open(stream=source, filetype='pdf')
    if len(doc) != 3:
        raise ValueError('Source must be the immutable three-page v0.2 core PDF')
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(960, 600), invariant=1)
    comparison_page(c, m, data)
    tests_page(c, m, data)
    c.save()
    appendix = fitz.open(stream=buf.getvalue(), filetype='pdf')
    doc.insert_pdf(appendix)
    meta = doc.metadata
    meta.update(title=f"Module {m['id']:02d} - {m['title']}",
                subject='v0.3.0 package: original v0.2 lesson plus SAS/Python/R reference and tests appendix',
                keywords='SAS, Python, R, unit tests, language comparison, appendix')
    doc.set_metadata(meta)
    output = args.output_dir / rel.name if args.output_dir else ROOT / rel
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output, garbage=4, deflate=True)
    print(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--modules', nargs='+', type=int, default=list(range(1, 11)))
    parser.add_argument('--source-dir', type=Path, help='Directory of original three-page v0.2 PDFs (flat filenames)')
    parser.add_argument('--output-dir', type=Path, help='Optional flat output directory; defaults to module folders')
    args = parser.parse_args()
    if any(i not in range(1, 11) for i in args.modules):
        parser.error('Module numbers must be 1-10')
    for m in MODULES:
        if m['id'] in args.modules:
            build(m, args)


if __name__ == '__main__':
    main()
