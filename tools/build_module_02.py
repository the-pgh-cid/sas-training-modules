from pathlib import Path
from io import BytesIO
import csv, re
import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

from pdf_build_support import build_paths
ROOT, SOURCE, OUT = build_paths('02-substr')
SRC = ROOT / 'module-02-substr'
OUT.parent.mkdir(parents=True, exist_ok=True)
for name, file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/'+file))

BG = '#F5F7F5'
INK = '#17394A'
BODY = '#253D46'
MUTED = '#566D75'
TEAL = '#137E79'
ORANGE = '#B66C32'
PALE = '#E8F2EE'
WARM = '#F6EDE3'
LINE = '#D8E1DF'
H = 600

rows = list(csv.DictReader((SRC/'results-20260921.csv').open()))
counts = {p: sum(r['Overall_Match']=='YES' for r in rows if r['Run'].startswith(p)) for p in ('A','B')}
assert counts == {'A':0,'B':3}
assert [sum(r[k]=='YES' for k in ('Row1_Correct','Row2_Correct','Row3_Correct')) for r in rows] == [2,1,1,3,3,3]

def text(c,x,y,s,size=11,font='Body',color=BODY):
    c.setFillColor(HexColor(color)); c.setFont(font,size)
    c.drawString(x,H-y,s)

def para(c,x,y,s,width,size=10.7,leading=14,font='Body',color=BODY):
    # Top input is the first baseline. Assert widths instead of silently shrinking text.
    for source_line in s.split('\n'):
        line = ''
        for word in source_line.split():
            candidate=(line+' '+word).strip()
            if pdfmetrics.stringWidth(candidate,font,size)>width and line:
                text(c,x,y,line,size,font,color); y+=leading; line=word
            else: line=candidate
        if line: text(c,x,y,line,size,font,color); y+=leading
    return y

def rect(c,x,y,w,h,color,r=0):
    c.setFillColor(HexColor(color))
    if r: c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=0)
    else: c.rect(x,H-y-h,w,h,fill=1,stroke=0)

def rule(c,x,y,w):
    c.setStrokeColor(HexColor(LINE));c.setLineWidth(.6)
    c.line(x,H-y,x+w,H-y)

def label(c,x,y,s,color=INK,size=9): text(c,x,y,s,size,'Bold',color)

def numbered(c,n,y,title,body,color,height=49):
    c.setFillColor(HexColor(color));c.circle(553,H-(y-4),9,fill=1,stroke=0)
    text(c,550.2,y-1,str(n),8,'Bold','#FFFFFF')
    text(c,572,y,title,11.8,'Bold')
    end=para(c,572,y+18,body,344,10.6,13.5)
    assert end<=y+height+3, (title,end)

def result_table(c,x,y,group):
    widths=[52,72,72,72,202] if group=='A' else [46,55,55,55,161]
    heads=['Run','Row 1','Row 2','Row 3','Full match']
    row_h=23
    rect(c,x,y,sum(widths),row_h,INK)
    off=x
    for w,h in zip(widths,heads):
        text(c,off+9,y+15,h,9.2,'Bold','#FFFFFF');off+=w
    for i,r in enumerate(r for r in rows if r['Run'].startswith(group)):
        yy=y+row_h*(i+1)
        rect(c,x,yy,sum(widths),row_h,'#FFFFFF' if i%2==0 else '#ECF1EF')
        vals=[r['Run']]+['Yes' if r[k]=='YES' else 'No' for k in ('Row1_Correct','Row2_Correct','Row3_Correct')]+['Yes' if r['Overall_Match']=='YES' else 'No']
        off=x
        for j,(w,v) in enumerate(zip(widths,vals)):
            text(c,off+9,yy+15,v,10,'Bold' if j in (0,4) else 'Body', TEAL if v=='Yes' else ORANGE if v=='No' else BODY);off+=w

doc=fitz.open(SOURCE)
bg=tuple(int(BG[i:i+2],16)/255 for i in (1,3,5))
for i,page in enumerate(doc):
    regions=[(388,543,576,562)]
    if i==1: regions += [(40,274,521,505),(538,132,920,505),(58,175,506,257)]
    if i==2: regions += [(538,132,920,505),(58,390,506,440)]
    for r in regions:
        page.add_redact_annot(fitz.Rect(r),fill=False)
    page.apply_redactions(images=0,graphics=0)
    buffer=BytesIO();c=canvas.Canvas(buffer,pagesize=(960,600))
    rect(c,388,543,188,20,BG)
    footer='Teaching edition v0.2.0  |  22 Sep 2026'
    text(c,480-pdfmetrics.stringWidth(footer,'Body',8)/2,555,footer,8,'Body',MUTED)
    if i==0:
        rule(c,62,446,434)
        label(c,62,462,'REPORTED TEST SETUP / 21 SEP 2026',TEAL,8.7)
        text(c,62,479,'Claude Sonnet 4.5 / AWS Bedrock GovCloud',10.5)
        text(c,62,494,'Claude Code 2.1.278 / effortLevel=high / prompt v0.1.0',9,'Body',MUTED)
        rect(c,544,460,372,43,PALE,9)
        label(c,558,475,'REPORTED FULL MATCHES',TEAL,8)
        text(c,558,493,'Prompt A: 0/3     Prompt B: 3/3',14,'Bold',INK)
    elif i==1:
        rect(c,58,175,448,82,'#FFFFFF')
        for yy,ss in [(191,'Convert this SAS code to Python.'),(221,'Show code in this response. Do not create or run files,'),(237,'or read existing Python files.')]:
            text(c,62,yy,ss,11.1,'Mono')
        rect(c,40,274,481,231,BG)
        label(c,44,291,'REPORTED TRIAL RESULTS / 21 SEP 2026',ORANGE)
        text(c,44,316,'0/3 runs matched every expected row',17,'Bold',INK)
        result_table(c,44,332,'A')
        text(c,44,443,'All three chose pandas bracket slicing (.str[start:stop]).',10.5)
        text(c,44,459,'No right-padding or assertions were reported.',10.5)
        para(c,44,482,'A1: CSV row flags show 2/3 rows matched; the narrative summary says 1/3. This table follows the CSV.',468,9,12,color=MUTED)

        rect(c,538,132,382,373,BG)
        label(c,544,147,'WHY CHOICES REMAIN OPEN',ORANGE)
        numbered(c,1,176,'The code has the rule','Start positions and lengths are in the SAS source. The model still has to translate them correctly.',ORANGE)
        numbered(c,2,235,'The method is open','Bracket slices and .str.slice() can both be correct. A shared method does not prove shared behavior.',ORANGE)
        numbered(c,3,294,'Appearance is a weak check','All A runs matched row 1. Checking only ABC would miss the reported failures elsewhere.',ORANGE)
        label(c,544,346,'SAME INPUT, DIFFERENT REPORTED VALUES',ORANGE,8.7)
        text(c,544,365,'SAS-to-Python / middle / expected: to-P',10.2,'Mono')
        rect(c,544,376,372,51,WARM,8)
        label(c,558,393,'RUN A2',ORANGE,8)
        text(c,558,415,'-to-',15,'Mono')
        label(c,735,393,'RUN A3',ORANGE,8)
        text(c,735,415,'o-Py',15,'Mono')
        label(c,544,449,'ANTI-PATTERN: ACCEPTING A PLAUSIBLE TABLE',ORANGE,8.4)
        para(c,544,467,'Execute the returned code and compare every value. Right-padding preserves widths; it does not fix a shifted start position.',372,10.5,14)
        text(c,44,519,'SOURCES: results-20260921.csv; trial-log-20260921.md; analysis-20260921.md',8,'Body',MUTED)
    else:
        # Preserve the full Prompt B wording; repair an awkward inherited wrap.
        rect(c,58,390,448,52,'#FFFFFF')
        text(c,62,404,'Show code in this response. Do not create or run files,',10.8,'Mono')
        text(c,62,419,'or read existing Python files.',10.8,'Mono')
        rect(c,538,132,382,373,BG)
        label(c,544,147,'WHY THESE DETAILS HELP',TEAL)
        numbered(c,1,173,'Translate the rule','SAS start - 1 = Python start. Add the requested length to get the exclusive stop.',TEAL)
        numbered(c,2,226,'Separate value and display','Preserve stored widths 20, 3, 4, 14. Trim trailing spaces only in the printed view.',TEAL)
        numbered(c,3,279,'Check every slice','Assert all nine visible strings and column widths. B1-B3 report padding and passing assertions.',TEAL)
        label(c,544,330,'REPORTED RESULTS / 3 OF 3 FULL MATCHES',TEAL,8.7)
        result_table(c,544,343,'B')
        text(c,544,449,'All three used pandas .str.slice().',10.5)
        rect(c,544,459,372,45,PALE,8)
        label(c,556,472,'CHECK IT YOURSELF',TEAL,8)
        text(c,556,486,'Execute the code; verify values and widths.',10,'Bold',TEAL)
        text(c,556,498,'3/3 agreement is not a guarantee of determinism.',9.4,'Body',MUTED)
        text(c,228,514,'Evidence: six fresh parallel subagents, three per prompt; raw transcripts were not supplied.',8.2,'Body',MUTED)
        text(c,228,526,'Assertions passing is reported, not independently rerun here. Python reference checked; SAS run pending.',8.2,'Body',MUTED)
    c.showPage();c.save();buffer.seek(0)
    overlay=fitz.open(stream=buffer.getvalue(),filetype='pdf')
    page.show_pdf_page(page.rect,overlay,0)

meta=doc.metadata
meta.update(title='Module 02 - SUBSTR: specify the positions',subject='Teaching edition v0.2.0; populated from reported trials dated 2026-09-21',keywords='SAS, Python, SUBSTR, prompt constraints, reported trials')
doc.set_metadata(meta)
doc.save(OUT,garbage=4,deflate=True)
print(OUT)
