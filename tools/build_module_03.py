"""Populate LENGTH with the reported September 21 trials; preserve both prompts."""
import csv
import json
from io import BytesIO

import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

from pdf_build_support import build_paths

ROOT, SOURCE, OUTPUT = build_paths('03-length')
for name, filename in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'),
                       ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + filename))

BG, INK, BODY, MUTED = '#F5F7F5', '#17394A', '#253D46', '#566D75'
TEAL, ORANGE, PALE, WARM, LINE = '#137E79', '#B66C32', '#E8F2EE', '#F6EDE3', '#D8E1DF'
module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
              if m['id'] == 3)
with (ROOT / 'module-03-length/results-20260921.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
assert [r['Run'] for r in rows] == ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']
assert [r['Numeric_Match'] for r in rows] == ['YES'] * 6
assert [r['Semantic_Correct'] for r in rows] == ['NO'] * 3 + ['YES'] * 3


def text(c, x, y, s, size=11, font='Body', color=BODY):
    assert x + pdfmetrics.stringWidth(s, font, size) <= 924, s
    c.setFillColor(HexColor(color))
    c.setFont(font, size)
    c.drawString(x, 600-y, s)


def rect(c, x, y, w, h, color, radius=0):
    c.setFillColor(HexColor(color))
    if radius:
        c.roundRect(x, 600-y-h, w, h, radius, stroke=0, fill=1)
    else:
        c.rect(x, 600-y-h, w, h, stroke=0, fill=1)


def label(c, x, y, s, color=INK, size=8.7):
    text(c, x, y, s, size, 'Bold', color)


def para(c, x, y, s, width, size=10.5, leading=13.5, color=BODY):
    line = ''
    for word in s.split():
        candidate = (line + ' ' + word).strip()
        if pdfmetrics.stringWidth(candidate, 'Body', size) > width and line:
            text(c, x, y, line, size, color=color)
            y += leading
            line = word
        else:
            line = candidate
    if line:
        text(c, x, y, line, size, color=color)
        y += leading
    return y


def numbered(c, n, y, title, body, color):
    c.setFillColor(HexColor(color))
    c.circle(553, 600-(y-4), 9, fill=1, stroke=0)
    text(c, 550.2, y-1, str(n), 8, 'Bold', '#FFFFFF')
    text(c, 572, y, title, 11.8, 'Bold')
    end = para(c, 572, y+18, body, 344)
    assert end <= y+60, (title, end)


def table(c, x, y, widths, headers, values, row_h=23, size=10):
    rect(c, x, y, sum(widths), row_h, INK)
    xx = x
    for w, h in zip(widths, headers):
        assert pdfmetrics.stringWidth(h, 'Bold', 9) <= w-18, h
        text(c, xx+9, y+15, h, 9, 'Bold', '#FFFFFF')
        xx += w
    for i, row in enumerate(values):
        yy = y + row_h*(i+1)
        rect(c, x, yy, sum(widths), row_h, '#FFFFFF' if i % 2 == 0 else '#ECF1EF')
        xx = x
        for j, (w, v) in enumerate(zip(widths, row)):
            font = 'Bold' if j == 0 else 'Body'
            assert pdfmetrics.stringWidth(v, font, size) <= w-18, v
            color = TEAL if v == 'Yes' else ORANGE if v == 'No' else BODY
            text(c, xx+9, yy+15, v, size, font, color)
            xx += w


def results(c, x, y, variant, widths):
    selected = [r for r in rows if r['Run'].startswith(variant)]
    values = [[r['Run'], r['Numeric_Match'].title(), r['Semantic_Correct'].title()]
              for r in selected]
    table(c, x, y, widths, ['Run', 'Numeric values', 'Required behavior'], values)


doc = fitz.open(SOURCE)
assert len(doc) == 3 and all(p.rect == fitz.Rect(0, 0, 960, 600) for p in doc)
for i, page in enumerate(doc):
    regions = [(388, 543, 576, 562)]
    if i == 0:
        regions += [(540, 270, 920, 504)]
    elif i == 1:
        regions += [(40, 274, 521, 505), (538, 132, 920, 505), (58, 175, 506, 257)]
    else:
        regions += [(538, 132, 920, 505), (58, 175, 506, 425)]
    for r in regions:
        page.add_redact_annot(fitz.Rect(r), fill=False)
    page.apply_redactions(images=0, graphics=0)
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(960, 600))
    rect(c, 388, 543, 188, 20, BG)
    footer = 'Teaching edition v0.2.0  |  22 Sep 2026'
    text(c, 480-pdfmetrics.stringWidth(footer, 'Body', 8)/2, 555, footer, 8, color=MUTED)
    if i == 0:
        c.setStrokeColor(HexColor(LINE))
        c.setLineWidth(.6)
        c.line(62, 154, 496, 154)
        label(c, 62, 462, 'REPORTED TEST SETUP / 21 SEP 2026', TEAL)
        text(c, 62, 479, 'Claude Sonnet 4.5 / AWS Bedrock GovCloud', 10.5)
        text(c, 62, 494, 'Claude Code 2.1.278 / effortLevel=high / prompt v0.1.0', 9, color=MUTED)
        rect(c, 540, 270, 380, 234, BG)
        label(c, 544, 282, 'EXPECTED RESULT')
        table(c, 544, 292, [98, 164, 110], ['Row', 'Stored width', 'len'],
              module['expected_rows'], row_h=21)
        text(c, 544, 433, 'Both ABC rows contain seven padding spaces.', 9.3)
        text(c, 544, 448, 'Final row: ten spaces; LENGTH returns 1.', 9.3)
        rect(c, 544, 460, 372, 43, PALE, 9)
        label(c, 558, 476, 'REPORTED NUMERIC MATCHES: A 3/3 | B 3/3', TEAL, 8.5)
        text(c, 558, 494, 'Required behavior: A 0/3 | B 3/3', 12, 'Bold', INK)
        text(c, 544, 520, 'Reference values checked in Python; SAS execution pending.', 8.3, color=MUTED)
    elif i == 1:
        rect(c, 58, 175, 448, 82, '#FFFFFF')
        for y, s in [(191, 'Convert this SAS code to Python.'),
                     (221, 'Show code in this response. Do not create or run files,'),
                     (237, 'or read existing Python files.')]:
            text(c, 62, y, s, 11.1, 'Mono')
        rect(c, 40, 274, 481, 231, BG)
        label(c, 44, 291, 'REPORTED TRIAL RESULTS / 21 SEP 2026', ORANGE)
        text(c, 44, 316, 'Matching numbers; missing behavior', 17, 'Bold', INK)
        results(c, 44, 332, 'A', [50, 180, 240])
        text(c, 44, 445, 'All three used pandas .str.len() directly.', 10.5)
        text(c, 44, 463, "Reported: no padding; final period kept as literal '.'.", 10.2)
        para(c, 44, 484, 'The numeric vector [3, 3, 10, 1, 1] matched, but stored text and missing-value interpretation did not.', 470, 10, 13)
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY CHOICES REMAIN OPEN', ORANGE)
        numbered(c, 1, 176, 'The numbers can agree', "Literal '.' has length 1, which matches the expected blank result by coincidence.", ORANGE)
        numbered(c, 2, 236, 'Storage still differs', 'This fixture requires width 10. Correct numeric values alone do not establish stored-text equivalence.', ORANGE)
        numbered(c, 3, 296, 'Name the spaces to ignore', 'For these ASCII strings, ignore trailing ordinary spaces in the calculation; preserve the stored text.', ORANGE)
        label(c, 544, 355, 'COUNTEREXAMPLES / LOCALLY CHECKED', ORANGE, 8.5)
        table(c, 544, 367, [134, 99, 139], ['Python value', 'Direct len', 'Expected LENGTH'],
              [["'ABC   '", '6', '3'], ["''", '0', '1'], ["' ABC '", '5', '4']], row_h=19, size=9.5)
        label(c, 544, 465, 'ANTI-PATTERN: CHECKING ONLY THE NUMBERS', ORANGE, 8.4)
        para(c, 544, 484, 'Inspect stored values, missing input and trailing spaces, even when the numeric results agree.', 372, 10.2, 13)
        text(c, 44, 520, 'SOURCES: results-20260921.csv; trial-log-20260921.md; analysis-20260921.md', 8, color=MUTED)
    else:
        rect(c, 58, 175, 448, 252, '#FFFFFF')
        prompt = module['prompt_b'].replace(
            'Show code in this response. Do not create or run files, or read existing\nPython files.',
            'Show code in this response. Do not create or run files,\nor read existing Python files.')
        for n, line in enumerate(prompt.splitlines()):
            assert pdfmetrics.stringWidth(line, 'Mono', 10.4) <= 444, line
            text(c, 62, 190+n*14.2, line, 10.4, 'Mono')
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY THESE DETAILS HELP', TEAL)
        numbered(c, 1, 173, 'Make the stored value visible', 'Right-pad to width 10 and inspect repr(text). Interpret the final input period as character missing.', TEAL)
        numbered(c, 2, 228, 'Preserve the counting rule', "Use rstrip(' ') for the calculation only. Keep leading spaces; set the all-blank result to 1.", TEAL)
        numbered(c, 3, 283, 'Verify the requested behavior', 'B1-B3 report width and value assertions passing. Correct padding can use different methods.', TEAL)
        label(c, 544, 335, 'REPORTED RESULTS / THREE B RUNS', TEAL)
        results(c, 544, 348, 'B', [42, 144, 186])
        rect(c, 544, 453, 372, 51, PALE, 8)
        label(c, 556, 467, 'CHECK IT YOURSELF', TEAL, 8)
        text(c, 556, 483, 'Confirm all widths = 10 and the five len values.', 10, 'Bold', TEAL)
        text(c, 556, 498, "Final stored value: ten spaces, not a literal '.'.", 10)
        text(c, 228, 514, 'Reports describe six fresh parallel agents; complete transcripts are absent from this repository.', 8.2, color=MUTED)
        text(c, 228, 526, 'Passing assertions are reported. Local reference checked; SAS run pending. Three runs do not guarantee future results.', 8.2, color=MUTED)
    c.showPage()
    c.save()
    overlay = fitz.open(stream=buf.getvalue(), filetype='pdf')
    page.show_pdf_page(page.rect, overlay, 0)

metadata = doc.metadata
metadata.update(title='Module 03 - LENGTH: say which spaces count',
                subject='Teaching edition v0.2.0; reported trials dated 2026-09-21',
                keywords='SAS, Python, LENGTH, stored width, reported trials')
doc.set_metadata(metadata)
doc.save(OUTPUT, garbage=4, deflate=True)
print(OUTPUT)
