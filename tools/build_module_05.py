"""Populate ROUND with reported September 21 trials; preserve fixture/prompts."""
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

ROOT, SOURCE, OUTPUT = build_paths('05-round')
for name, filename in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'),
                       ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + filename))

BG, INK, BODY, MUTED = '#F5F7F5', '#17394A', '#253D46', '#566D75'
TEAL, ORANGE, PALE, WARM, LINE = '#137E79', '#B66C32', '#E8F2EE', '#F6EDE3', '#D8E1DF'
module = next(m for m in json.loads((ROOT / 'module-content/modules-v0.1.0.json').read_text())
              if m['id'] == 5)
with (ROOT / 'module-05-round/results-20260921.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
assert [r['Run'] for r in rows] == ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']
assert all(r['Correctness'] == 'YES' for r in rows)
assert [r['Understanding_Correct'] for r in rows[:3]] == ['NO', 'YES', 'YES']
assert all(r['Method'] == '.round(0)' for r in rows[3:])


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



CONFIG = {'name': 'ROUND: keep the promise specific',
 'keywords': 'SAS, Python, ROUND, bounded scope, reported trials',
 'note': 'Five non-halfway inputs only; numeric 2 equals 2.0.',
 'summary': 'REPORTED NUMERIC MATCHES / FIVE INPUTS',
 'a_title': 'Matching numbers, conflicting explanations',
 'a_headers': ['Run', 'Method', 'Values', 'Explanation'],
 'a_widths': [44, 86, 68, 272],
 'a_rows': [['A1', '.round()', 'Yes', 'Wrong SAS rounding claim'],
            ['A2', '.round()', 'Yes', 'Correct + alternative recipe'],
            ['A3', '.round()', 'Yes', 'Correct + scope note']],
 'a_lines': ['A1 wrongly said SAS and pandas both use ties-to-even.',
             'Correct output and correct explanation are separate checks.',
             'All A runs matched [2, 3, -1, -2, 3].'],
 'a_why': [("A1's explanation was wrong",
            'At exact halfway values, SAS ROUND rounds away from zero; pandas rounds to even. '
            'These inputs do not test that difference.'),
           ('A2 and A3 recognized the difference',
            'A2 offered a floor/ceil alternative. A3 correctly explained that this fixture has '
            'no halfway values.'),
           ('Keep the conclusion within scope',
            'Five matching outputs do not establish equivalence for all SAS ROUND inputs or '
            'other rounding units.')],
 'anti_title': 'ANTI-PATTERN: ACCEPTING OUTPUT AS PROOF',
 'anti_body': 'Review the explanation as well as the values. A correct result on this fixture '
              'cannot validate an untested general claim.',
 'anti_last': 'Expand the checks when the required scope expands.',
 'b_why': [('Choose one route',
            'Name pandas and .round(0). All three B runs report the requested method.'),
           ('Define numeric agreement',
            'Check the list [2, 3, -1, -2, 3] in order. Numeric 2 and 2.0 count as equal here.'),
           ('State the limits of the check',
            'B1-B3 reportedly included the requested scope note: halfway inputs and other '
            'rounding units were not tested.')],
 'b_headers': ['Run', 'Numeric match', 'Scope note'],
 'b_values': [['B1', 'Yes', 'Included'], ['B2', 'Yes', 'Included'], ['B3', 'Yes', 'Included']],
 'check': ['Assert all five rounded values in order.',
           'Keep inputs unchanged; record the scope of the pass.']}

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
        label(c, 160, 520, 'PYTHON REFERENCE / 2', MUTED, 8)
        text(c, 346, 514, 'Reports: six fresh parallel agents. Complete transcripts and execution logs are absent.', 8.1, color=MUTED)
        text(c, 346, 526, 'Assertions reported passed; local reference checked; SAS pending. Three runs give no guarantee.', 8.1, color=MUTED)
    c.showPage()
    c.save()
    overlay = fitz.open(stream=buf.getvalue(), filetype='pdf')
    page.show_pdf_page(page.rect, overlay, 0)

# Replace the broad legacy SAS PDF link with the precise function reference.
for link in doc[2].get_links():
    if 'support.sas.com' in link.get('uri', ''):
        link['from'] = fitz.Rect(44, 510, 120, 524)
        link['uri'] = 'https://support.sas.com/documentation/cdl/en/lefunctionsref/63354/HTML/default/p0tj6cmga7p8qln1ejh6ebevm0c9.htm'
        doc[2].update_link(link)
# Add a link for the new pandas reference label.
doc[2].insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(160, 511, 330, 523),
                        'uri': 'https://pandas.pydata.org/docs/reference/api/pandas.Series.round.html'})

metadata = doc.metadata
metadata.update(title='Module 05 - '+CONFIG['name'],
                subject='Teaching edition v0.2.0; reported trials dated 2026-09-21',
                keywords=CONFIG['keywords'])
doc.set_metadata(metadata)
doc.save(OUTPUT, garbage=4, deflate=True)
print(OUTPUT)
