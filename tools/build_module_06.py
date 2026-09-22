"""Populate INTCK with reported September 21 trials; preserve fixture/prompts."""
import csv
import json
import textwrap
from io import BytesIO

import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

from pdf_build_support import build_paths

ROOT, SOURCE, OUTPUT = build_paths('06-intck')
for name, filename in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'),
                       ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + filename))

BG, INK, BODY, MUTED = '#F5F7F5', '#17394A', '#253D46', '#566D75'
TEAL, ORANGE, PALE, WARM, LINE = '#137E79', '#B66C32', '#E8F2EE', '#F6EDE3', '#D8E1DF'
module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
              if m['id'] == 6)
with (ROOT / 'module-06-intck/results-20260921.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
assert [r['Run'] for r in rows] == ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']
assert all(r['Correctness'] == 'YES' for r in rows)
assert [r['Method'] for r in rows[:3]] == ['Custom functions', 'Vectorized inline', 'Vectorized inline']
assert all(r['Assertions'] == 'Yes' for r in rows[3:])


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



CONFIG = {'name': 'INTCK: say exactly what you are counting',
 'keywords': 'SAS, Python, INTCK, discrete boundaries, reported trials',
 'note': 'Last two rows test boundaries rather than elapsed periods.',
 'summary': 'REPORTED MATCHES / ALL THREE COLUMNS',
 'a_title': 'Two methods, the same boundary counts',
 'a_headers': ['Run', 'Implementation', 'Values match'],
 'a_widths': [44, 306, 120],
 'a_rows': [['A1', 'Custom functions + .apply()', 'Yes'],
            ['A2', 'Vectorized inline', 'Yes'],
            ['A3', 'Vectorized inline', 'Yes']],
 'a_lines': ['A1 used functions; A2/A3 used direct Series formulas.',
             'All explained boundary counting; A runs had no assertions.',
             'A shared result does not require identical code.'],
 'a_why': [('Same rule, different structure',
            'A1 put the date arithmetic in functions. A2 and A3 wrote it inline. Both structures '
            'matched the six supplied rows.'),
           ('The one-day rows test the meaning',
            'January 31 to February 1 crosses a month. December 31 to January 1 crosses both a '
            'month and a year.'),
           ('Compare behavior before style',
            'Different code is not automatically a failed conversion. Check the three columns '
            'and input order before choosing a method.')],
 'anti_title': 'ANTI-PATTERN: "MONTHS BETWEEN DATES"',
 'anti_body': 'Completed months and crossed month boundaries answer different questions. State '
              'the counting rule and include a one-day boundary example.',
 'anti_last': 'Dividing elapsed days by 30 does not count boundaries.',
 'b_why': [('Define the meaning',
            'Default discrete INTCK counts boundaries. Keep this exercise scoped to ordinary '
            'day, month and year date intervals.'),
           ('Choose the route',
            'Specify pandas, date parsing and formulas. All three B runs report vectorized '
            'inline calculations.'),
           ('Make success visible',
            'Assert every result column. B1-B3 report the expected lists and explain why one day '
            'can cross a month or year.')],
 'b_headers': ['Run', 'Values match', 'Assertions'],
 'b_values': [['B1', 'Yes', 'Passed'], ['B2', 'Yes', 'Passed'], ['B3', 'Yes', 'Passed']],
 'check': ['Check every row in days, months and years.',
           'One day can cross one month and one year.']}

def prompt_lines(value, width=67):
    result = []
    reflowed = value.replace('existing\nPython files.', 'existing Python files.')
    for line in reflowed.splitlines():
        result.extend(textwrap.wrap(line, width=width, replace_whitespace=False,
                                    drop_whitespace=True, break_long_words=False,
                                    break_on_hyphens=False) or [''])
    assert ' '.join(' '.join(result).split()) == ' '.join(value.split())
    return result


doc = fitz.open(SOURCE)
assert len(doc) == 3 and all(p.rect == fitz.Rect(0, 0, 960, 600) for p in doc)
for i, page in enumerate(doc):
    regions = [(388, 543, 576, 562)]
    if i == 0:
        regions += [(540, 449, 920, 505)]
    elif i == 1:
        regions += [(40, 157, 521, 505), (538, 132, 920, 505)]
    else:
        regions += [(538, 132, 920, 505), (58, 175, 506, 489)]
    for region in regions:
        page.add_redact_annot(fitz.Rect(region), fill=False)
    page.apply_redactions(images=0, graphics=0)
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(960, 600))
    rect(c, 388, 543, 188, 20, BG)
    footer = 'Teaching edition v0.2.0  |  22 Sep 2026'
    text(c, 480-pdfmetrics.stringWidth(footer, 'Body', 8)/2, 555, footer, 8, color=MUTED)
    if i == 0:
        label(c, 62, 460, 'REPORTED TEST SETUP / 21 SEP 2026', TEAL)
        text(c, 62, 478, 'Claude Sonnet 4.5 / AWS Bedrock GovCloud', 10.5)
        text(c, 62, 494, 'Claude Code 2.1.278 / effortLevel=high / prompt v0.1.0', 9, color=MUTED)
        rect(c, 540, 449, 380, 56, BG)
        text(c, 544, 460, CONFIG['note'], 9, color=MUTED)
        rect(c, 544, 469, 372, 35, PALE, 8)
        label(c, 558, 482, CONFIG['summary'], TEAL, 8)
        text(c, 558, 498, 'Prompt A 3/3 | Prompt B 3/3', 12, 'Bold', INK)
        text(c, 544, 520, 'Reference values checked in Python; SAS execution pending.', 8.3, color=MUTED)
    elif i == 1:
        rect(c, 40, 157, 481, 348, BG)
        rect(c, 44, 161, 470, 103, '#FFFFFF', 10)
        for n, line in enumerate(prompt_lines(module['prompt_a'], 65)):
            assert pdfmetrics.stringWidth(line, 'Mono', 11.1) <= 434, line
            text(c, 62, 190+n*15, line, 11.1, 'Mono')
        label(c, 44, 290, 'REPORTED TRIAL RESULTS / 21 SEP 2026', ORANGE)
        text(c, 44, 316, CONFIG['a_title'], 16, 'Bold', INK)
        table(c, 44, 332, CONFIG['a_widths'], CONFIG['a_headers'], CONFIG['a_rows'], size=9.8)
        for y, line in zip([455, 475, 495], CONFIG['a_lines']):
            text(c, 44, y, line, 10.2, color=MUTED if y==495 else BODY)
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY CHOICES REMAIN OPEN', ORANGE)
        for n, (title, body) in enumerate(CONFIG['a_why']):
            numbered(c, n+1, 176+n*70, title, body, ORANGE)
        rect(c, 544, 389, 372, 115, WARM, 9)
        label(c, 558, 408, CONFIG['anti_title'], ORANGE, 8.1)
        end=para(c, 558, 430, CONFIG['anti_body'], 344, 10.8, 14.5)
        assert end <= 480, end
        text(c, 558, 490, CONFIG['anti_last'], 9.3, 'Bold', ORANGE)
        text(c, 44, 520, 'SOURCES: results-20260921.csv; trial-log-20260921.md; analysis-20260921.md', 8, color=MUTED)
    else:
        rect(c, 58, 175, 448, 314, '#FFFFFF')
        for n, line in enumerate(prompt_lines(module['prompt_b'])):
            assert pdfmetrics.stringWidth(line, 'Mono', 10.6) <= 434, line
            text(c, 62, 190+n*14.3, line, 10.6, 'Mono')
        rect(c, 538, 132, 382, 373, BG)
        label(c, 544, 147, 'WHY THESE DETAILS HELP', TEAL)
        for n, (title, body) in enumerate(CONFIG['b_why']):
            numbered(c, n+1, 173+n*59, title, body, TEAL, 60)
        label(c, 544, 345, 'REPORTED RESULTS / THREE B RUNS', TEAL)
        table(c, 544, 357, [44, 152, 176], CONFIG['b_headers'], CONFIG['b_values'], row_h=22)
        rect(c, 544, 457, 372, 47, PALE, 8)
        label(c, 556, 471, 'CHECK IT YOURSELF', TEAL, 8)
        text(c, 556, 486, CONFIG['check'][0], 10.4, 'Bold', TEAL)
        text(c, 556, 499, CONFIG['check'][1], 9.5)
        text(c, 346, 514, 'Reports: six fresh parallel agents. Complete transcripts and execution logs are absent.', 8.1, color=MUTED)
        text(c, 346, 526, 'Assertions reported passed; local reference checked; SAS pending. Three runs give no guarantee.', 8.1, color=MUTED)
    c.showPage()
    c.save()
    overlay = fitz.open(stream=buf.getvalue(), filetype='pdf')
    page.show_pdf_page(page.rect, overlay, 0)

# Tight reference hitboxes avoid covering the adjacent evidence footer.
for link in doc[2].get_links():
    if 'support.sas.com' in link.get('uri', ''):
        link['from'] = fitz.Rect(44, 510, 120, 524)
    elif 'pandas.pydata.org' in link.get('uri', ''):
        link['from'] = fitz.Rect(224, 510, 332, 524)
    doc[2].update_link(link)

metadata = doc.metadata
metadata.update(title='Module 06 - '+CONFIG['name'],
                subject='Teaching edition v0.2.0; reported trials dated 2026-09-21',
                keywords=CONFIG['keywords'])
doc.set_metadata(metadata)
doc.save(OUTPUT, garbage=4, deflate=True)
print(OUTPUT)
