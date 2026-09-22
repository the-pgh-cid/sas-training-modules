"""Populate CAT/CATX with reported September 21 trials; preserve fixture/prompts."""
import csv
import json
from io import BytesIO

import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

from pdf_build_support import build_paths

ROOT, SOURCE, OUTPUT = build_paths('04-cat')
for name, filename in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'),
                       ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + filename))

BG, INK, BODY, MUTED = '#F5F7F5', '#17394A', '#253D46', '#566D75'
TEAL, ORANGE, PALE, WARM, LINE = '#137E79', '#B66C32', '#E8F2EE', '#F6EDE3', '#D8E1DF'
module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
              if m['id'] == 4)
with (ROOT / 'module-04-cat/results-20260921.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
assert [r['Run'] for r in rows] == ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']
assert [r['Correctness'] for r in rows] == ['NO'] * 3 + ['YES'] * 3
assert [r['CATX_Method'] for r in rows[:3]] == [
    '+ with spaces', 'TWO approaches', 'List comp filter']
assert all(r['CATX_Method'] == 'Strip/filter/join' for r in rows[3:])


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


def numbered(c, n, y, title, body, color, max_height=70):
    c.setFillColor(HexColor(color))
    c.circle(553, 600-(y-4), 9, fill=1, stroke=0)
    text(c, 550.2, y-1, str(n), 8, 'Bold', '#FFFFFF')
    text(c, 572, y, title, 11.8, 'Bold')
    end = para(c, 572, y+18, body, 344)
    assert end <= y+max_height, (title, end)


def table(c, x, y, widths, headers, values, row_h=25, size=10):
    rect(c, x, y, sum(widths), row_h, INK)
    xx = x
    for w, h in zip(widths, headers):
        assert pdfmetrics.stringWidth(h, 'Bold', 9) <= w-18, h
        text(c, xx+9, y+16, h, 9, 'Bold', '#FFFFFF')
        xx += w
    for i, row in enumerate(values):
        yy = y + row_h*(i+1)
        rect(c, x, yy, sum(widths), row_h, '#FFFFFF' if i % 2 == 0 else '#ECF1EF')
        xx = x
        for j, (w, v) in enumerate(zip(widths, row)):
            font = 'Bold' if j == 0 else 'Body'
            assert pdfmetrics.stringWidth(v, font, size) <= w-18, v
            color = TEAL if v == 'Yes' else ORANGE if v == 'No' else BODY
            text(c, xx+9, yy+16, v, size, font, color)
            xx += w


doc = fitz.open(SOURCE)
assert len(doc) == 3 and all(p.rect == fitz.Rect(0, 0, 960, 600) for p in doc)
for i, page in enumerate(doc):
    regions = [(388, 543, 576, 562)]
    if i == 0:
        regions += [(540, 445, 920, 504)]
    elif i == 1:
        regions += [(40, 274, 521, 505), (538, 132, 920, 505), (58, 175, 506, 257)]
    else:
        regions += [(538, 132, 920, 505), (58, 175, 506, 489)]
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
        c.line(62, 157, 496, 157)
        label(c, 62, 460, 'REPORTED TEST SETUP / 21 SEP 2026', TEAL)
        text(c, 62, 478, 'Claude Sonnet 4.5 / AWS Bedrock GovCloud', 10.5)
        text(c, 62, 494, 'Claude Code 2.1.278 / effortLevel=high / prompt v0.1.0', 9, color=MUTED)
        rect(c, 540, 445, 380, 59, BG)
        rect(c, 544, 463, 372, 41, PALE, 9)
        label(c, 558, 477, 'REPORTED FULL-REQUIREMENT MATCHES', TEAL, 8.5)
        text(c, 558, 496, 'Prompt A 0/3 | Prompt B 3/3', 12, 'Bold', INK)
        text(c, 544, 520, 'Reference values checked in Python; SAS execution pending.', 8.3, color=MUTED)
    elif i == 1:
        rect(c, 58, 175, 448, 82, '#FFFFFF')
        for y, s in [(191, 'Convert this SAS code to Python.'),
                     (221, 'Show code in this response. Do not create or run files,'),
                     (237, 'or read existing Python files.')]:
            text(c, 62, y, s, 11.1, 'Mono')
        rect(c, 40, 274, 481, 231, BG)
        label(c, 44, 291, 'REPORTED TRIAL RESULTS / 21 SEP 2026', ORANGE)
        text(c, 44, 316, 'Readable names can hide missing spaces', 16, 'Bold', INK)
        methods = ['Join with spaces', 'Two alternatives shown', 'Filter periods + join']
        values = [[r['Run'], method, r['Correctness'].title()]
                  for r, method in zip(rows[:3], methods)]
        table(c, 44, 332, [44, 306, 120], ['Run', 'CATX approach', 'Full match'], values)
        text(c, 44, 454, 'All three used unpadded + concatenation for CAT.', 10.4)
        text(c, 44, 474, 'A3 matched readable CATX names; stored widths were missing.', 10)
        text(c, 44, 494, 'A2 offered both CATX recipes seen in A1 and A3.', 10, color=MUTED)
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY CHOICES REMAIN OPEN', ORANGE)
        numbered(c, 1, 176, 'CAT keeps the stored blanks',
                 'All A runs reportedly joined raw inputs. The + operator is valid Python, but it cannot restore omitted padding.', ORANGE)
        numbered(c, 2, 246, 'A readable name is only one check',
                 'A3 filtered the input periods and got the readable names. Both stored results still needed width 24.', ORANGE)
        numbered(c, 3, 316, 'Alternatives need a decision',
                 'A2 offered two CATX recipes. Compare each with the required behavior before accepting either.', ORANGE)
        rect(c, 544, 389, 372, 115, WARM, 9)
        label(c, 558, 408, 'ANTI-PATTERN: ACCEPTING A NEAT NAME', ORANGE, 8.4)
        para(c, 558, 431, 'Inspect visible blanks and stored widths. Ask for cleanup separately after checking the equivalent conversion.', 344, 11, 15)
        text(c, 558, 489, 'Different Python methods can preserve the same behavior.', 9.5, 'Bold', ORANGE)
        text(c, 44, 520, 'SOURCES: results-20260921.csv; trial-log-20260921.md; analysis-20260921.md', 8, color=MUTED)
    else:
        rect(c, 58, 175, 448, 314, '#FFFFFF')
        prompt = module['prompt_b'].replace(
            'Show code in this response. Do not create or run files, or read existing\nPython files.',
            'Show code in this response. Do not create or run files,\nor read existing Python files.')
        for n, line in enumerate(prompt.splitlines()):
            assert pdfmetrics.stringWidth(line, 'Mono', 10.6) <= 444, line
            text(c, 62, 190+n*14.3, line, 10.6, 'Mono')
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY THESE DETAILS HELP', TEAL)
        numbered(c, 1, 173, 'Separate CAT from CATX',
                 'CAT preserves padded fields. CATX strips ordinary spaces, skips blanks and joins with one space.', TEAL, 60)
        numbered(c, 2, 232, 'Define the stored values',
                 'Map input periods to blanks. Require input widths of 8 and result widths of 24; preserve row order.', TEAL, 60)
        numbered(c, 3, 291, 'Request a checkable result',
                 'Name exact values and widths to assert. B1-B3 report padded CAT and strip/filter/join CATX.', TEAL, 60)
        label(c, 544, 345, 'REPORTED RESULTS / THREE B RUNS', TEAL)
        values = [[r['Run'], r['Correctness'].title(), 'Passed'] for r in rows[3:]]
        table(c, 544, 357, [44, 124, 204], ['Run', 'Full match', 'Assertions'], values, row_h=22)
        rect(c, 544, 457, 372, 47, PALE, 8)
        label(c, 556, 471, 'CHECK IT YOURSELF', TEAL, 8)
        text(c, 556, 486, 'Check exact CAT spaces and widths of 8 / 24.', 10.4, 'Bold', TEAL)
        text(c, 556, 499, 'Blank middle fields must add no CATX separator.', 10)
        text(c, 228, 514, 'Reports describe six fresh parallel agents; complete transcripts and execution logs are absent.', 8.2, color=MUTED)
        text(c, 228, 526, 'Passing assertions are reported. Local reference checked; SAS run pending. Three runs do not guarantee future results.', 8.2, color=MUTED)
    c.showPage()
    c.save()
    overlay = fitz.open(stream=buf.getvalue(), filetype='pdf')
    page.show_pdf_page(page.rect, overlay, 0)

metadata = doc.metadata
metadata.update(title='Module 04 - CAT: preserve the intended spaces',
                subject='Teaching edition v0.2.0; reported trials dated 2026-09-21',
                keywords='SAS, Python, CAT, CATX, stored width, reported trials')
doc.set_metadata(metadata)
doc.save(OUTPUT, garbage=4, deflate=True)
print(OUTPUT)
