#!/usr/bin/env python3
"""Two Circles keynote, 26 Nov 2026. Rebuilt from Leaders in Sport FINAL v9X.

    python3 build.py            -> deck.html, png/, TwoCircles.pptx, TwoCircles.pdf

Every slide carries the Two Circles sign-up QR top right
(hard-as-nails.com/two-circles -> /signup/two-circles, the two-circles cohort).
Speaker notes go into the pptx notes pane.
"""
import html, os, sys, json
from slides import SLIDES

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = r"""
:root{--black:#0A0709;--pink:#E6007E;--pink-deep:#C8006D;--acid:#E4FF3D;--paper:#F3ECEF;
--dim:#B9AAB1;--muted:#8B7C84;--line:#2A1F26}
*{box-sizing:border-box}
body{margin:0;background:#222}
.s{width:1920px;height:1080px;position:relative;overflow:hidden;margin:0 auto 30px;
 background-color:var(--black);
 background-image:radial-gradient(circle at center,rgba(230,0,126,.22) 1px,transparent 1.3px);
 background-size:7px 7px;color:var(--paper);font-family:'Archivo',sans-serif;
 padding:120px 150px 120px;display:flex;flex-direction:column;justify-content:center}
.s.pink{background:var(--pink-deep);background-image:none}
.s.photo{padding:0}
.s.photo .bg{position:absolute;inset:0;background-size:cover;background-position:center}
.s.photo .scrim{position:absolute;left:0;right:0;bottom:0;height:62%;background:var(--black);opacity:.9}
.s.photo .in{position:absolute;left:150px;right:420px;bottom:120px}
h1,h2,h3{font-family:'Archivo Black',sans-serif;font-weight:400;text-transform:uppercase;
 letter-spacing:-.02em;line-height:.95;margin:0;color:#fff}
em{font-style:normal;color:var(--pink)}
.pink em{color:var(--acid)}
.xl{font-size:190px}.l{font-size:120px}.m{font-size:88px}.sm{font-size:62px}.xs{font-size:44px}
.lab{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:24px;letter-spacing:.18em;
 text-transform:uppercase;color:var(--pink);margin:0 0 40px}
.pink .lab{color:var(--acid)}
.stat{font-family:'Archivo Black';color:var(--acid);line-height:.85;letter-spacing:-.03em;margin:0}
.body{font-size:40px;line-height:1.35;max-width:30ch;margin:28px 0 0;color:var(--paper)}
.dim{color:var(--dim)}
.src{position:absolute;left:150px;bottom:56px;font-family:'JetBrains Mono';font-size:17px;
 letter-spacing:.12em;text-transform:uppercase;color:var(--muted);max-width:1300px}
.qr{position:absolute;top:48px;right:56px;width:168px;text-align:center;z-index:5}
.qr img{width:168px;height:168px;display:block}
.qr span{display:block;font-family:'JetBrains Mono';font-weight:700;font-size:14px;letter-spacing:.14em;
 color:var(--paper);margin-top:8px;text-transform:uppercase}
.tape{position:absolute;left:0;right:0;bottom:0;height:22px;
 background:repeating-linear-gradient(-45deg,var(--acid) 0 22px,var(--black) 22px 44px)}
.rule{border-top:2px solid var(--pink);padding-top:22px;margin-top:34px}
.cols{display:grid;gap:70px;margin-top:50px}
.cols .stat{font-size:150px}
.cols p{font-size:36px;line-height:1.3;margin:18px 0 0}
.list{margin:30px 0 0;padding:0;list-style:none}
.list li{font-size:40px;line-height:1.25;padding:18px 0;border-top:1px solid var(--line)}
.list li b{font-family:'Archivo Black';font-weight:400;color:#fff;text-transform:uppercase}
.list li span{color:var(--dim);font-size:30px;display:block;margin-top:6px}
.q{font-family:'Archivo';font-weight:800;font-size:58px;line-height:1.15;color:#fff;max-width:24ch;margin:0}
.who{font-family:'JetBrains Mono';font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin-top:30px}
/* league table */
table.lg{border-collapse:collapse;width:1620px;margin-top:20px}
table.lg th{font-family:'JetBrains Mono';font-weight:700;font-size:19px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--dim);text-align:right;padding:0 0 12px 10px;vertical-align:bottom;line-height:1.3}
table.lg th small{display:block;color:var(--muted);font-weight:500}
table.lg th:first-child,table.lg td:first-child{text-align:left;width:60px}
table.lg th:nth-child(2),table.lg td:nth-child(2){text-align:left}
table.lg td{font-size:34px;padding:6px 0 6px 10px;border-top:1px solid var(--line);text-align:right}
table.lg td.pos{font-family:'Archivo Black';color:var(--pink)}
table.lg td.ind{font-family:'Archivo Black';text-transform:uppercase;font-size:30px;color:#fff}
table.lg td.n{font-family:'JetBrains Mono';font-size:20px;color:var(--muted)}
table.lg tr.hl td{color:var(--acid);border-top:2px solid var(--acid);border-bottom:2px solid var(--acid)}
table.lg tr.hl td.ind,table.lg tr.hl td.pos{color:var(--acid)}
table.lg tr.ghost td{color:var(--muted)}
/* timeline */
.tl{display:grid;grid-template-columns:repeat(5,1fr);gap:34px;margin-top:60px}
.tl div{border-top:3px solid var(--pink);padding-top:20px}
.tl b{display:block;font-family:'JetBrains Mono';font-size:28px;letter-spacing:.12em;color:var(--acid)}
.tl p{font-size:42px;line-height:1.25;margin:12px 0 0;color:#fff}
.tl .off{opacity:.12}
.tl .next{border-top-color:var(--acid)}
.logo{height:120px}
"""

HEAD = ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Hard As Nails x Two Circles</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;600;800'
        '&family=JetBrains+Mono:wght@500;700&display=swap"><style>' + CSS + '</style></head><body>')


def section(i, s):
    cls = s.get('cls', '')
    qr = '' if s.get('noqr') else '<div class="qr"><img src="qr.png"><span>Two Circles · sign up</span></div>'
    tape = '<div class="tape"></div>' if s.get('tape') else ''
    return (f'<section class="s {cls}" data-artboard data-name="{i+1:02d}">{s["html"]}{qr}{tape}</section>')


def main():
    os.chdir(HERE)
    with open('deck.html', 'w') as f:
        f.write(HEAD + ''.join(section(i, s) for i, s in enumerate(SLIDES)) + '</body></html>')
    with open('notes.json', 'w') as f:
        json.dump([s.get('notes', '') for s in SLIDES], f, indent=1, ensure_ascii=False)
    print(len(SLIDES), 'slides -> deck.html')
    if '--html' in sys.argv:
        return
    from playwright.sync_api import sync_playwright
    os.makedirs('png', exist_ok=True)
    for p in os.listdir('png'):
        os.remove(os.path.join('png', p))
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
        pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        pg.goto('file://' + os.path.join(HERE, 'deck.html'))
        pg.wait_for_load_state('networkidle')
        pg.evaluate('document.fonts.ready')
        for i, el in enumerate(pg.query_selector_all('[data-artboard]')):
            el.screenshot(path=f'png/{i+1:02d}.png')
        pg.pdf(path='TwoCircles.pdf', width='1920px', height='1080px', print_background=True,
               page_ranges='') if False else None
        b.close()
    build_pptx()
    build_pdf()


def build_pdf():
    from PIL import Image
    files = sorted(os.listdir('png'))
    ims = [Image.open('png/' + f).convert('RGB') for f in files]
    ims[0].save('TwoCircles.pdf', save_all=True, append_images=ims[1:], resolution=144)
    print('TwoCircles.pdf')


def build_pptx():
    from pptx import Presentation
    from pptx.util import Emu
    from PIL import Image
    notes = json.load(open('notes.json'))
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    os.makedirs('jpg', exist_ok=True)
    for i, f in enumerate(sorted(os.listdir('png'))):
        jp = f'jpg/{f[:-4]}.jpg'
        Image.open('png/' + f).convert('RGB').save(jp, quality=88)
        sl = prs.slides.add_slide(blank)
        sl.shapes.add_picture(jp, 0, 0, prs.slide_width, prs.slide_height)
        sl.notes_slide.notes_text_frame.text = notes[i]
    prs.save('TwoCircles.pptx')
    print('TwoCircles.pptx')


if __name__ == '__main__':
    main()
