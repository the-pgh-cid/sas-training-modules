"""Populate the original teaching PDF with reported trials; preserve fixture/prompts."""
import csv
import json
from io import BytesIO
import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from pdf_build_support import build_paths

SLUG = '08-input'
MODULE_ID = 8
ROOT, SOURCE, OUTPUT = build_paths(SLUG)
for name, filename in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'),
                       ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + filename))
BG, INK, BODY, MUTED = '#F5F7F5', '#17394A', '#253D46', '#566D75'
TEAL, ORANGE, PALE, WARM, LINE = '#137E79', '#B66C32', '#E8F2EE', '#F6EDE3', '#D8E1DF'
module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
              if m['id'] == MODULE_ID)
with (ROOT / f'module-{SLUG}/results-20260921.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
assert [r['Run'] for r in rows] == ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']

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


assert all(r['Correctness'] == 'YES' for r in rows)
assert all(r['Method'] == 'pd.to_numeric + pd.to_datetime' for r in rows)
assert [r['Assertions'] for r in rows] == ['No'] * 3 + ['Yes'] * 3
doc = fitz.open(SOURCE)
assert len(doc) == 3 and all(p.rect == fitz.Rect(0, 0, 960, 600) for p in doc)
for i, page in enumerate(doc):
    regions = [(388, 543, 576, 562)]
    if i == 0:
        regions += [(540, 458, 920, 505)]
    elif i == 1:
        regions += [(40, 242, 521, 505), (538, 132, 920, 505)]
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
        rect(c, 540, 458, 380, 47, BG)
        rect(c, 544, 458, 372, 46, PALE, 9)
        label(c, 558, 474, 'REPORTED EXPECTED-VALUE MATCHES', TEAL, 8.5)
        text(c, 558, 494, 'Prompt A 3/3 | Prompt B 3/3', 12, 'Bold', INK)
        text(c, 544, 520, 'Reference values checked in Python; SAS execution pending.', 8.3, color=MUTED)
    elif i == 1:
        rect(c, 40, 242, 481, 263, BG)
        label(c, 44, 260, 'REPORTED TRIAL RESULTS / 21 SEP 2026', ORANGE)
        text(c, 44, 284, 'All three A runs matched the valid inputs', 15.5, 'Bold', INK)
        values = [[r['Run'], r['Correctness'].title(), 'None reported'] for r in rows[:3]]
        table(c, 44, 301, [44, 162, 264], ['Run', 'Values match', 'Assertions'], values)
        label(c, 44, 425, 'SHARED REPORTED CONVERSION METHODS', ORANGE)
        text(c, 44, 447, 'pd.to_numeric + pd.to_datetime', 11, 'Mono')
        text(c, 44, 468, "Date parsing used format='%d%b%Y'.", 10.7)
        text(c, 44, 490, 'Shared methods do not establish identical full responses.', 9.8, color=MUTED)
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY CHOICES REMAIN OPEN', ORANGE)
        numbered(c, 1, 176, 'Agreement is useful evidence',
                 'All six runs reportedly used the same two conversion functions. The three valid rows matched in both groups.', ORANGE)
        numbered(c, 2, 247, 'Representation still matters',
                 'A date string can display the right day without being a datetime. Numeric and date types need their own checks.', ORANGE)
        numbered(c, 3, 318, 'Keep the conclusion in scope',
                 'Three clean inputs do not test invalid values, missing data or other informats. The report cannot establish future reliability.', ORANGE)
        rect(c, 544, 389, 372, 115, WARM, 9)
        label(c, 558, 408, 'ANTI-PATTERN: "MAKE IT LOOK THE SAME"', ORANGE, 8.3)
        para(c, 558, 431, 'Request numeric values and datetime values, then check both meaning and type. Preserve the source strings for comparison.', 344, 11, 15)
        text(c, 558, 489, 'Correct-looking text does not prove a correct data type.', 9.2, 'Bold', ORANGE)
        text(c, 44, 520, 'SOURCES: results-20260921.csv; trial-log-20260921.md; analysis-20260921.md', 8, color=MUTED)
    else:
        rect(c, 58, 175, 448, 314, '#FFFFFF')
        for n, line in enumerate(module['prompt_b'].splitlines()):
            assert pdfmetrics.stringWidth(line, 'Mono', 10.6) <= 444, line
            text(c, 62, 190+n*14.3, line, 10.6, 'Mono')
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY THESE DETAILS HELP', TEAL)
        numbered(c, 1, 173, 'Keep sources and results distinct',
                 'Keep char_num and char_date as strings. Add numeric and datetime columns; preserve the original row order.', TEAL, 60)
        numbered(c, 2, 232, 'State the date interpretation',
                 '%d%b%Y means day, month abbreviation and year. The prompt specifies English months and calendar-date comparison.', TEAL, 60)
        numbered(c, 3, 291, 'Ask for value and type checks',
                 'B1-B3 reportedly include both kinds of assertions and pass them. The checks cover these three valid inputs.', TEAL, 60)
        label(c, 544, 345, 'REPORTED RESULTS / THREE B RUNS', TEAL)
        values = [[r['Run'], r['Correctness'].title(), 'Passed: values + types'] for r in rows[3:]]
        table(c, 544, 357, [44, 124, 204], ['Run', 'Values match', 'Assertions'], values, row_h=22)
        rect(c, 544, 457, 372, 47, PALE, 8)
        label(c, 556, 471, 'CHECK IT YOURSELF', TEAL, 8)
        text(c, 556, 486, 'Compare every value, then inspect both types.', 10.2, 'Bold', TEAL)
        text(c, 556, 499, 'Use formatted dates for checking; retain datetime data.', 9.5)
        text(c, 346, 514, 'Reports: six fresh parallel agents. Complete transcripts and execution logs are absent.', 8.2, color=MUTED)
        text(c, 346, 526, 'Assertions reported passed; local reference checked; SAS pending. Three runs give no guarantee.', 8.2, color=MUTED)
    c.showPage()
    c.save()
    overlay = fitz.open(stream=buf.getvalue(), filetype='pdf')
    page.show_pdf_page(page.rect, overlay, 0)

metadata = doc.metadata
metadata.update(title='Module 08 - INPUT: tell the model how to read the values',
                subject='Teaching edition v0.2.0; reported trials dated 2026-09-21',
                keywords='SAS, Python, INPUT, date parsing, data types, reported trials')
doc.set_metadata(metadata)
doc.save(OUTPUT, garbage=4, deflate=True)
print(OUTPUT)
