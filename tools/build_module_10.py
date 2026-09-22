"""Populate LAG with reported September 21 trials; preserve fixture/prompts."""
import csv
import json
from io import BytesIO

import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

from pdf_build_support import build_paths

ROOT, SOURCE, OUTPUT = build_paths('10-lag')
for name, filename in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'),
                       ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + filename))

BG, INK, BODY, MUTED = '#F5F7F5', '#17394A', '#253D46', '#566D75'
TEAL, ORANGE, PALE, WARM, LINE = '#137E79', '#B66C32', '#E8F2EE', '#F6EDE3', '#D8E1DF'
module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
              if m['id'] == 10)
with (ROOT / 'module-10-lag/results-20260921.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
assert [r['Run'] for r in rows] == ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']
assert all(r['Correctness'] == 'YES' for r in rows)
assert [r['Assertions'] for r in rows] == ['No'] * 3 + ['Yes'] * 3


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


assert [r['Method'] for r in rows] == ['shift(1) + shift(2)'] * 6
doc = fitz.open(SOURCE)
assert len(doc) == 3 and all(p.rect == fitz.Rect(0, 0, 960, 600) for p in doc)
for i, page in enumerate(doc):
    regions = [(388, 543, 576, 562)]
    if i == 0:
        regions += [(540, 479, 920, 505)]
    elif i == 1:
        regions += [(40, 244, 521, 505), (538, 132, 920, 505)]
    else:
        regions += [(538, 132, 920, 505)]
    for r in regions:
        page.add_redact_annot(fitz.Rect(r), fill=False)
    page.apply_redactions(images=0, graphics=0)
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(960, 600))
    rect(c, 388, 543, 188, 20, BG)
    footer = 'Teaching edition v0.2.0  |  22 Sep 2026'
    text(c, 480-pdfmetrics.stringWidth(footer, 'Body', 8)/2, 555, footer, 8, color=MUTED)
    if i == 0:
        label(c, 62, 461, 'REPORTED TEST SETUP / 21 SEP 2026', TEAL)
        text(c, 62, 479, 'Claude Sonnet 4.5 / AWS Bedrock GovCloud', 10.5)
        text(c, 62, 495, 'Claude Code 2.1.278 / effortLevel=high / prompt v0.1.0', 9, color=MUTED)
        rect(c, 540, 479, 380, 26, BG)
        rect(c, 544, 481, 372, 23, PALE, 7)
        text(c, 556, 497, 'Reported output matches: Prompt A 3/3 | Prompt B 3/3', 10.2, 'Bold', TEAL)
        text(c, 544, 520, 'Reference checked in Python; SAS execution pending.', 8.3, color=MUTED)
    elif i == 1:
        rect(c, 40, 244, 481, 261, BG)
        label(c, 44, 291, 'REPORTED TRIAL RESULTS / 21 SEP 2026', ORANGE)
        text(c, 44, 316, 'All A runs chose row shifts', 16, 'Bold', INK)
        values = [[r['Run'], r['Method'], r['Correctness'].title()] for r in rows[:3]]
        table(c, 44, 332, [44, 306, 120], ['Run', 'Method', 'Output match'], values)
        text(c, 44, 454, 'All three report matching values and missing positions.', 10.2)
        text(c, 44, 474, 'No A run reportedly included assertions.', 10.2)
        text(c, 44, 494, 'Shared method does not establish identical full responses.', 9.8, color=MUTED)
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY CHOICES REMAIN OPEN', ORANGE)
        numbered(c, 1, 176, 'A short request can succeed',
                 'All A reports describe shift(1) and shift(2). The source calls both SAS functions on every row.', ORANGE)
        numbered(c, 2, 246, 'Check meaning as well as numbers',
                 'The first prior value is unavailable. Its missing value must remain missing after subtraction.', ORANGE)
        numbered(c, 3, 316, 'Keep the sequence intact',
                 'Sorting, dropping rows or wrapping the final value into the first row changes the calculation.', ORANGE)
        rect(c, 544, 389, 372, 115, WARM, 9)
        label(c, 558, 408, 'ANTI-PATTERN: "FILL THE BLANKS"', ORANGE, 8.4)
        para(c, 558, 431, 'Replacing the first missing prior value with zero manufactures a change of 10. Missing means there was no earlier observation.', 344, 10.7, 14.5)
        text(c, 558, 489, 'Preserve missing positions and the five-row order.', 9.8, 'Bold', ORANGE)
        text(c, 44, 520, 'SOURCES: results-20260921.csv; trial-log-20260921.md; evidence-review-20260922.md', 8, color=MUTED)
    else:
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY THESE DETAILS HELP', TEAL)
        numbered(c, 1, 173, 'Protect the original sequence',
                 'Use row shifts without a frequency argument. Preserve all five ids and their order.', TEAL, 60)
        numbered(c, 2, 232, 'Limit the equivalence',
                 'Shift fits these per-row calls. Conditional SAS LAG calls advance their queue only when executed.', TEAL, 60)
        numbered(c, 3, 291, 'Make missing values checkable',
                 'B1-B3 report assertions and an explanation of the first missing change. Use pd.isna for missing positions.', TEAL, 60)
        label(c, 544, 345, 'REPORTED RESULTS / THREE B RUNS', TEAL)
        values = [[r['Run'], r['Correctness'].title(), 'Passed'] for r in rows[3:]]
        table(c, 544, 357, [44, 124, 204], ['Run', 'Output match', 'Assertions'], values, row_h=22)
        rect(c, 544, 457, 372, 47, PALE, 8)
        label(c, 556, 471, 'CHECK IT YOURSELF', TEAL, 8)
        text(c, 556, 486, 'Row 3 change = -3; the first change stays missing.', 10.2, 'Bold', TEAL)
        text(c, 556, 499, 'Compare every value, missing position and original id.', 9.5)
        text(c, 340, 514, 'Six fresh-agent runs reported; complete transcripts and execution logs are absent.', 7.9, color=MUTED)
        text(c, 340, 526, 'Assertions are reported. Local reference checked; SAS execution pending.', 7.9, color=MUTED)
    c.showPage()
    c.save()
    overlay = fitz.open(stream=buf.getvalue(), filetype='pdf')
    page.show_pdf_page(page.rect, overlay, 0)

metadata = doc.metadata
metadata.update(title='Module 10 - LAG: keep missing values and order meaningful',
                subject='Teaching edition v0.2.0; reported trials dated 2026-09-21',
                keywords='SAS, Python, LAG, shift, queue, reported trials')
doc.set_metadata(metadata)
doc.save(OUTPUT, garbage=4, deflate=True)
print(OUTPUT)
