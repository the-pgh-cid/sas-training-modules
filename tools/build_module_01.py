from pathlib import Path
from io import BytesIO
import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

from pdf_build_support import build_paths
ROOT, SOURCE, OUTPUT = build_paths('01-mean')
for name,fn in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+fn))

def text(c,x,y,s,size=10,font='Body',color='#253D46'):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,600-y,s)

doc=fitz.open(SOURCE)
for i,page in enumerate(doc):
    page.add_redact_annot(fitz.Rect(388,543,576,562),fill=False)
    page.apply_redactions(images=0,graphics=0)
    buf=BytesIO();c=canvas.Canvas(buf,pagesize=(960,600))
    c.setFillColor(HexColor('#F5F7F5'));c.rect(388,37,188,20,fill=1,stroke=0)
    footer='Teaching edition v0.2.0  |  22 Sep 2026'
    text(c,480-pdfmetrics.stringWidth(footer,'Body',8)/2,555,footer,8,color='#566D75')
    if i==0:
        c.setStrokeColor(HexColor('#D8E1DF'));c.setLineWidth(.6)
        c.line(62,154,496,154)
        text(c,62,462,'REPORTED TEST SETUP / ORIGINAL MEAN TRIALS',8.7,'Bold','#137E79')
        line1='Original prompts; this edition adds a response-only instruction.'
        line2='Model, client, settings and trial date: not stated in this PDF.'
        assert pdfmetrics.stringWidth(line1,'Body',9.5)<434
        text(c,62,479,line1,9.5)
        text(c,62,494,line2,9,'Body','#566D75')
        c.setFillColor(HexColor('#E8F2EE'));c.roundRect(544,97,372,43,9,fill=1,stroke=0)
        text(c,558,475,'HISTORICAL TRIAL STATUS / SEE PAGES 2-3',8,'Bold','#137E79')
        status='A: 3/3 displayed matches | B2/B3: code reuse'
        assert pdfmetrics.stringWidth(status,'Bold',11.2)<344
        text(c,558,493,status,11.2,'Bold','#17394A')
    c.showPage();c.save();buf.seek(0)
    overlay=fitz.open(stream=buf.getvalue(),filetype='pdf')
    page.show_pdf_page(page.rect,overlay,0)

metadata=doc.metadata
metadata.update(title='Module 01 - MEAN: make missing values explicit',subject='Teaching edition v0.2.0; historical test setup and evidence status added 2026-09-22')
doc.set_metadata(metadata)
doc.save(OUTPUT,garbage=4,deflate=True)
print(OUTPUT)

# Confirm the additions did not alter the source, prompts or teaching content.
updated=fitz.open(OUTPUT);original=fitz.open(SOURCE)
for i in range(3):
    region=fitz.Rect(0,0,960,534)
    before=original[i].get_text(clip=region)
    after=updated[i].get_text(clip=region)
    if i==0:
        assert after.startswith(before)
    else:
        assert after==before, ('Existing content changed',i+1)
    assert updated[i].get_links()==original[i].get_links() or [l.get('uri') for l in updated[i].get_links()]==[l.get('uri') for l in original[i].get_links()]
assert len(updated)==3
print('PASS: 3 pages; existing teaching content and prompts preserved; reference link retained.')
