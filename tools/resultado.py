"""Card de RESULTADO (estilo Xerifão) -> mp4 6s.
uso: python3 resultado.py dados.json saida.mp4
dados.json: {"data":"2026-11-20","extracao":"PTM","hora":"11h20","premios":["0746","9974","4209","7883","6369","9181","440"]}
grupo e bicho são calculados pela dezena (não confia no site)."""
import sys, json, os, subprocess, datetime as dt
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); F = H + '/fonts/'
BI = [('Avestruz','🦤'),('Águia','🦅'),('Burro','🫏'),('Borboleta','🦋'),('Cachorro','🐶'),('Cabra','🐐'),('Carneiro','🐏'),('Camelo','🐫'),('Cobra','🐍'),('Coelho','🐰'),('Cavalo','🐴'),('Elefante','🐘'),('Galo','🐓'),('Gato','🐱'),('Jacaré','🐊'),('Leão','🦁'),('Macaco','🐵'),('Porco','🐷'),('Pavão','🦚'),('Peru','🦃'),('Touro','🐂'),('Tigre','🐯'),('Urso','🐻'),('Veado','🦌'),('Vaca','🐮')]
DIAS = ['Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo']
def grupo(m):
    dz = int(m[-2:]); return 25 if dz == 0 else (dz + 3) // 4
CSS = f"""@font-face{{font-family:Roboto;font-weight:900;src:url(file://{F}roboto-latin-900-normal.woff2)}}
@font-face{{font-family:Roboto;font-weight:700;src:url(file://{F}roboto-latin-700-normal.woff2)}}
@font-face{{font-family:Anton;src:url(file://{F}anton-latin-400-normal.woff2)}}
body{{margin:0}} *{{box-sizing:border-box}}
.pg{{width:1080px;height:1920px;background:#fff;font-family:Roboto,'Noto Color Emoji';color:#111;display:flex;flex-direction:column;align-items:center;padding:150px 60px 0}}
.hd{{display:flex;align-items:center;gap:22px}} .hd img{{width:110px;height:110px;border-radius:50%;border:5px solid #FFC400;object-fit:cover}} .hd span{{font-weight:900;font-size:54px}}
.date{{margin-top:26px;border:6px solid #FFC400;border-radius:60px;padding:4px 40px;font-weight:900;font-size:54px}}
.tt{{margin-top:18px;background:#16a34a;color:#fff;border:6px solid #111;border-radius:22px;padding:0 46px;font-family:Anton;font-size:110px;font-style:italic;line-height:1.15;box-shadow:0 10px 0 #111}}
.ex{{font-weight:900;font-size:74px;margin-top:22px}}
.rows{{width:100%;display:flex;flex-direction:column;gap:14px;margin-top:30px}}
.row{{display:flex;align-items:center;border:4px solid #e2e2e2;border-radius:28px;padding:8px 24px;box-shadow:0 6px 14px rgba(0,0,0,.08);height:124px}}
.row.p1{{border-color:#FFC400;background:#FFF8DB}}
.pr{{font-weight:900;font-size:46px;width:90px}} .em{{font-family:'Noto Color Emoji';font-size:78px;width:110px;text-align:center}}
.nm{{flex:1;font-weight:900;font-size:50px;padding-left:8px}} .gp{{text-align:center;border-right:4px solid #111;padding:0 26px;line-height:1}} .gp small{{display:block;font-weight:700;font-size:26px}} .gp b{{font-weight:900;font-size:64px}}
.mi{{padding-left:26px;font-weight:900;font-size:72px;width:230px;text-align:right}}
.cta{{margin-top:28px;background:#111;color:#FFC400;border-radius:24px;padding:12px 40px;font-weight:900;font-size:44px}}"""
def html(d):
    data = dt.date.fromisoformat(d['data']); ps = d['premios']; rows = ''
    for i, m in enumerate(ps[:7]):
        if i < 5:
            g = grupo(m); n, e = BI[g-1]
            rows += f'<div class="row{" p1" if i==0 else ""}"><div class="pr">{i+1}º</div><div class="em">{e}</div><div class="nm">{n}</div><div class="gp"><small>Grupo</small><b>{g:02d}</b></div><div class="mi">{m}</div></div>'
        else:
            rows += f'<div class="row"><div class="pr">{i+1}º</div><div class="em"></div><div class="nm" style="color:#666;font-size:40px">{"soma" if i==5 else "multiplicação"}</div><div class="mi">{m}</div></div>'
    return f'''<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class="pg">
<div class="hd"><img src="file://{H}/avatar.jpg"><span>professordamilhar</span></div>
<div class="date">📅 {data:%d/%m/%Y} · {DIAS[data.weekday()]}</div>
<div class="tt">RESULTADO</div><div class="ex">{d["extracao"]} · {d["hora"]}</div>
<div class="rows">{rows}</div><div class="cta">Acertou? Comenta 🍀 aqui</div></div></body></html>'''
def legenda(d):
    data = dt.date.fromisoformat(d['data']); m = d['premios'][0]; g = grupo(m); n, e = BI[g-1]
    return (f"RESULTADO {d['extracao']} {d['hora']} · {data:%d/%m} ✅\n\nDeu {n} {e} na cabeça (grupo {g:02d}) · milhar {m}\n\n"
            "Quem acertou comenta 🍀 aqui!\nPalpite da próxima extração no GRUPO, comenta GRUPO que eu te mando o link 👇\n\n"
            "+18 | Conteúdo informativo. Jogue com responsabilidade.\n#resultado #jogodobicho #" + d['extracao'].lower() + " #riodejaneiro #professordamilhar")
if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); out = sys.argv[2]
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width':1080,'height':1920})
        open('/tmp/res.html','w').write(html(d)); pg.goto('file:///tmp/res.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        pg.screenshot(path='/tmp/res.png'); br.close()
    subprocess.run(['ffmpeg','-y','-v','error','-framerate','30','-i','/tmp/res.png','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-vf','format=yuv420p,loop=-1:1,trim=duration=6','-t','6','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-r','30','-c:a','aac','-shortest','-movflags','+faststart',out], check=True)
    open(out.replace('.mp4','.txt'),'w').write(legenda(d)); print(out); print(legenda(d))
