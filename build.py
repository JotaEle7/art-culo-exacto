import json, os, random, html, shutil, sys, datetime

BASE = os.environ.get("BASE", "https://EJEMPLO.pages.dev").rstrip("/")
GSC = os.environ.get("GSC", "")  # código de verificación de Search Console (meta tag)
OUT = "site"
BRAND = "Artículo Exacto"
TODAY = datetime.date.today().isoformat()

LAWS = {
    "CE": ("Constitución Española", "BOE-A-1978-31229", "CE"),
    "L39": ("Ley 39/2015, del Procedimiento Administrativo Común", "BOE-A-2015-10565", "Ley 39/2015"),
    "L40": ("Ley 40/2015, de Régimen Jurídico del Sector Público", "BOE-A-2015-10566", "Ley 40/2015"),
}
TOPICS = [
    ("titulo-preliminar", "Título Preliminar de la Constitución", "artículos 1 a 9: valores superiores, soberanía, lenguas, bandera, partidos y Fuerzas Armadas"),
    ("derechos-fundamentales", "Derechos fundamentales (arts. 10 a 29 CE)", "igualdad, vida, libertad, detención de 72 horas, habeas corpus, reunión, asociación y tutela judicial"),
    ("derechos-deberes-principios", "Deberes y principios rectores (arts. 30 a 55 CE)", "sistema tributario, propiedad, principios de política social y económica, amparo y Defensor del Pueblo"),
    ("corona", "La Corona (Título II CE)", "funciones del Rey, sucesión, Regencia, refrendo y Casa del Rey"),
    ("cortes-generales", "Las Cortes Generales (Título III CE)", "Congreso y Senado, Diputados y Senadores, leyes orgánicas, decretos-leyes e iniciativa legislativa"),
    ("gobierno", "Gobierno y relaciones con las Cortes (Títulos IV y V CE)", "investidura, moción de censura, cuestión de confianza, estados de alarma, excepción y sitio"),
    ("poder-judicial", "Poder Judicial y Hacienda (Títulos VI y VII CE)", "jueces, CGPJ, Tribunal Supremo, Ministerio Fiscal, Jurado, Presupuestos y Tribunal de Cuentas"),
    ("organizacion-territorial", "Organización territorial del Estado (Título VIII CE)", "municipios, provincias, Comunidades Autónomas, Estatutos, competencias y artículo 155"),
    ("tribunal-constitucional", "Tribunal Constitucional y reforma (Títulos IX y X CE)", "composición, recursos de inconstitucionalidad y amparo, y procedimientos de reforma"),
    ("interesados-ley-39", "Interesados y derechos (Ley 39/2015)", "capacidad de obrar, interesado, representación, relación electrónica, lengua y registros"),
    ("plazos-y-silencio", "Plazos y silencio administrativo (Ley 39/2015)", "obligación de resolver, plazo de 3 y 6 meses, silencio, cómputo de plazos, ampliación y urgencia"),
    ("actos-administrativos", "Actos administrativos y notificaciones (Ley 39/2015)", "motivación, forma, eficacia, notificación en papel y electrónica, publicación"),
    ("nulidad-y-anulabilidad", "Nulidad y anulabilidad (arts. 47 a 52 Ley 39/2015)", "causas de nulidad de pleno derecho, anulabilidad, conversión, conservación y convalidación"),
    ("procedimiento-administrativo", "Fases del procedimiento (Ley 39/2015)", "iniciación, subsanación, prueba, informes, audiencia, información pública y terminación"),
    ("recursos-administrativos", "Revisión de oficio y recursos (Ley 39/2015)", "lesividad, recurso de alzada, reposición y extraordinario de revisión con sus plazos"),
    ("competencia-ley-40", "Principios y competencia (Ley 40/2015)", "principios de actuación, órganos, delegación, avocación, encomienda, delegación de firma y suplencia"),
    ("organos-colegiados-abstencion", "Órganos colegiados, abstención y recusación (Ley 40/2015)", "Secretario, actas, sesiones a distancia, motivos de abstención y plazos de la recusación"),
    ("potestad-sancionadora", "Potestad sancionadora (Ley 40/2015)", "legalidad, irretroactividad, tipicidad, culpabilidad, proporcionalidad, prescripción y non bis in idem"),
    ("responsabilidad-patrimonial", "Responsabilidad patrimonial (Ley 40/2015)", "requisitos del daño, fuerza mayor, responsabilidad solidaria, acción de regreso y plazo de un año"),
]
SIM = ("simulacro-examen", "Simulacro de examen: 30 preguntas mezcladas", "30 preguntas de todo el bloque I, como en el examen real")

qs = json.load(open("questions.json", encoding="utf-8"))
for i, q in enumerate(qs):
    q["id"] = i + 1
    rnd = random.Random(1000 + i)
    order = [0, 1, 2, 3]; rnd.shuffle(order)
    q["o"] = [q["opts"][k] for k in order]
    q["c"] = order.index(0)

def boe_url(q):
    return f"https://www.boe.es/buscar/act.php?id={LAWS[q['law']][1]}#a{q['art'].replace(' ', '')}"

def art_label(q):
    return f"Art. {q['art']} {LAWS[q['law']][2]}"

CSS = """
:root{--bg:#f7f8fa;--card:#fff;--ink:#14202e;--muted:#5b6876;--line:#dfe4ea;--brand:#1d4e89;--brand-soft:#e6eef8;--ok:#1f7a45;--ok-soft:#e4f4ea;--bad:#b3261e;--bad-soft:#fbe9e7;--font:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
@media (prefers-color-scheme:dark){:root{--bg:#0f151c;--card:#17202a;--ink:#e6ebf0;--muted:#9aa7b4;--line:#2a3542;--brand:#7fb0ea;--brand-soft:#1b2a3b;--ok:#6cc48f;--ok-soft:#163323;--bad:#f08b80;--bad-soft:#3a1b18;color-scheme:dark}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 var(--font)}
a{color:var(--brand)}
.wrap{max-width:760px;margin:0 auto;padding:0 16px}
header.top{background:var(--card);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-block:12px}
.logo{font-weight:700;text-decoration:none;color:var(--ink);letter-spacing:-.01em}
.logo span{color:var(--brand)}
nav a{font-size:.9rem;margin-left:14px;text-decoration:none}
main{padding-block:24px 48px}
h1{font-size:1.6rem;line-height:1.2;margin:0 0 10px;text-wrap:balance}
h2{font-size:1.2rem;margin:28px 0 10px}
.lead{color:var(--muted);margin:0 0 18px}
.crumbs{font-size:.85rem;color:var(--muted);margin-bottom:10px}
.q{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:0 0 14px}
.q h3{font-size:1rem;margin:0 0 12px;font-weight:600}
.q .n{color:var(--muted);font-weight:500;margin-right:4px}
.opts{display:grid;gap:8px;margin:0;padding:0;list-style:none}
.opt{width:100%;text-align:left;font:inherit;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px 12px;cursor:pointer}
.opt:hover{border-color:var(--brand)}
.opt:focus-visible{outline:2px solid var(--brand);outline-offset:2px}
.opt.ok{background:var(--ok-soft);border-color:var(--ok)}
.opt.bad{background:var(--bad-soft);border-color:var(--bad)}
.opt .l{font-weight:600;margin-right:6px}
.exp{margin-top:12px;font-size:.92rem;border-left:3px solid var(--brand);padding:6px 0 6px 12px;background:transparent}
.exp q{font-style:italic}
.exp .src{display:block;margin-top:4px;color:var(--muted)}
.btn{display:inline-block;background:var(--brand);color:#fff;border:0;border-radius:8px;padding:11px 16px;font:inherit;font-weight:600;text-decoration:none;cursor:pointer}
@media (prefers-color-scheme:dark){.btn{color:#0f151c}}
.btn.alt{background:transparent;color:var(--brand);border:1px solid var(--brand)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin:0;padding:0;list-style:none}
.grid a{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;text-decoration:none;color:var(--ink);height:100%}
.grid a strong{display:block;margin-bottom:4px}
.grid a small{color:var(--muted)}
.box{background:var(--brand-soft);border-radius:10px;padding:16px;margin:18px 0}
.score{font-size:1.1rem;font-weight:700}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:.85rem}
footer .wrap{padding-block:18px}
.tag{display:inline-block;font-size:.75rem;border:1px solid var(--line);border-radius:99px;padding:1px 8px;color:var(--muted)}
table{border-collapse:collapse;width:100%;font-size:.92rem}td,th{border-bottom:1px solid var(--line);padding:8px;text-align:left}
"""

QUIZ_JS = """
document.querySelectorAll('.q').forEach(function(card){
  var c=+card.dataset.c, done=false;
  card.querySelectorAll('.opt').forEach(function(b,i){
    b.addEventListener('click',function(){
      if(done)return;done=true;
      card.querySelectorAll('.opt')[c].classList.add('ok');
      if(i!==c)b.classList.add('bad');
      card.querySelector('.exp').hidden=false;
      var s=document.getElementById('score');
      if(s){var r=+s.dataset.r+(i===c?1:0),t=+s.dataset.t+1;s.dataset.r=r;s.dataset.t=t;s.textContent=r+' aciertos de '+t;}
    });
  });
});
"""

def page(title, desc, body, path, extra_head="", scripts=""):
    canon = BASE + path
    gsc = f'<meta name="google-site-verification" content="{html.escape(GSC)}">' if GSC else ""
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta name="theme-color" content="#1d4e89">
<link rel="manifest" href="/manifest.webmanifest">
{gsc}
<style>{CSS}</style>
{extra_head}
</head>
<body>
<header class="top"><div class="wrap"><a class="logo" href="/">Artículo <span>Exacto</span></a><nav><a href="/#temas">Temas</a><a href="/app/">Practicar</a></nav></div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">
<p>{BRAND}: test de oposiciones con cada respuesta citada del texto consolidado del BOE. Web no oficial, sin relación con el INAP ni con ningún organismo público.</p>
<p><a href="/aviso-legal/">Aviso legal</a> · <a href="/privacidad/">Privacidad</a></p>
</div></footer>
{scripts}
</body></html>"""

def q_html(q, n):
    letters = "abcd"
    opts = "".join(f'<li><button class="opt" type="button"><span class="l">{letters[k]})</span>{html.escape(o)}</button></li>' for k, o in enumerate(q["o"]))
    return f"""<article class="q" data-c="{q['c']}" id="p{q['id']}">
<h3><span class="n">{n}.</span>{html.escape(q['q'])}</h3>
<ul class="opts">{opts}</ul>
<div class="exp" hidden><strong>Correcta: {letters[q['c']]}) {html.escape(q['o'][q['c']])}</strong>
<span class="src">{art_label(q)}: <q>{html.escape(q['cita'])}</q> · <a href="{boe_url(q)}" rel="nofollow noopener" target="_blank">ver en el BOE</a></span></div>
</article>"""

def faq_ld(items):
    ents = [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": f"{q['o'][q['c']]}. {art_label(q)}: «{q['cita']}»."}} for q in items]
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ents}, ensure_ascii=False) + "</script>"

def write(path, content):
    full = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith((".xml", ".txt", ".json", ".webmanifest", ".html", ".svg")) else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

shutil.rmtree(OUT, ignore_errors=True)
urls = ["/"]

# Páginas de tema
by_topic = {}
for q in qs: by_topic.setdefault(q["topic"], []).append(q)
all_topics = TOPICS + [SIM]
for i, (slug, name, about) in enumerate(all_topics):
    if slug == SIM[0]:
        items = random.Random(7).sample(qs, 30)
    else:
        items = sorted(by_topic[slug], key=lambda x: (x["law"], int(x["art"].split()[0])))
    title = f"Test {name} | Auxiliar Administrativo del Estado"
    desc = f"Test gratis de {len(items)} preguntas sobre {about}. Cada respuesta cita el artículo exacto del BOE."
    path = f"/test/{slug}/"
    arts = sorted({(q['law'], q['art']) for q in items}, key=lambda x: (x[0], int(x[1].split()[0])))
    laws_used = sorted({LAWS[l][0] for l, _ in arts})
    prev_ = all_topics[i - 1] if i > 0 else None
    next_ = all_topics[i + 1] if i + 1 < len(all_topics) else None
    nav = '<p style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap">'
    nav += f'<a href="/test/{prev_[0]}/">← {html.escape(prev_[1])}</a>' if prev_ else '<span></span>'
    nav += f'<a href="/test/{next_[0]}/">{html.escape(next_[1])} →</a>' if next_ else ''
    nav += '</p>'
    body = f"""<p class="crumbs"><a href="/">Inicio</a> › Auxiliar Administrativo del Estado › Test</p>
<h1>Test: {html.escape(name)}</h1>
<p class="lead">{len(items)} preguntas tipo examen sobre {html.escape(about)}. Pulsa una opción para ver la respuesta y el texto literal del artículo. Fuente: {html.escape(', '.join(laws_used))}, texto consolidado del BOE.</p>
<p><span id="score" class="score" data-r="0" data-t="0">0 aciertos de 0</span></p>
{''.join(q_html(q, n + 1) for n, q in enumerate(items))}
<div class="box"><strong>¿Quieres más?</strong> Practica con test aleatorios de las 300 preguntas y repasa tus fallos. Gratis 20 preguntas al día.<br><br><a class="btn" href="/app/">Hacer un test aleatorio</a></div>
{nav}"""
    write(path, page(title, desc, body, path, faq_ld(items), f"<script>{QUIZ_JS}</script>"))
    urls.append(path)

# Portada
cards = "".join(f'<li><a href="/test/{s}/"><strong>{html.escape(n)}</strong><small>{html.escape(a)}</small></a></li>' for s, n, a in all_topics)
home = f"""<h1>Test Auxiliar Administrativo del Estado gratis, con el artículo exacto</h1>
<p class="lead">{len(qs)} preguntas tipo examen del bloque I: Constitución Española, Ley 39/2015 y Ley 40/2015. Cada respuesta enlaza al artículo del BOE y muestra su texto literal, así sabes por qué es correcta.</p>
<p style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="/app/">Empezar un test</a><a class="btn alt" href="/test/simulacro-examen/">Simulacro de 30 preguntas</a></p>
<h2 id="temas">Test por tema</h2>
<ul class="grid">{cards}</ul>
<h2>Cómo funciona</h2>
<table>
<tr><th>Plan</th><th>Qué incluye</th><th>Precio</th></tr>
<tr><td>Gratis</td><td>Los {len(all_topics)} test por tema y 20 preguntas aleatorias al día</td><td>0 €</td></tr>
<tr><td>Completo</td><td>Test ilimitados, repaso de fallos y simulacros nuevos cada semana</td><td>4,99 €/mes (próximamente)</td></tr>
</table>
<p class="lead" style="margin-top:14px">Textos legales: versión consolidada publicada por el BOE (Constitución actualizada a 20/05/2026; Ley 39/2015 a 06/11/2024; Ley 40/2015 a 02/08/2024). Cada pregunta se ha comprobado contra el texto legal.</p>"""
write("/", page("Test Auxiliar Administrativo del Estado gratis | Artículo Exacto", f"{len(qs)} preguntas tipo examen de Constitución, Ley 39/2015 y Ley 40/2015 con el artículo exacto del BOE en cada respuesta. Gratis.", home, "/"))

# App de práctica (freemium)
app_body = """<h1>Test aleatorio</h1>
<p class="lead">Elige el bloque y el número de preguntas. Plan gratis: 20 preguntas al día. Tus resultados se guardan solo en este dispositivo.</p>
<div id="setup" class="q">
<label for="blk"><strong>Bloque</strong></label><br>
<select id="blk" style="font:inherit;padding:8px;margin:6px 0 12px;width:100%"><option value="all">Todo el bloque I</option><option value="CE">Constitución Española</option><option value="L39">Ley 39/2015</option><option value="L40">Ley 40/2015</option><option value="fallos">Solo mis fallos</option></select><br>
<label for="num"><strong>Preguntas</strong></label><br>
<select id="num" style="font:inherit;padding:8px;margin:6px 0 12px;width:100%"><option>10</option><option selected>20</option></select><br>
<button class="btn" id="go" type="button">Empezar</button>
<p id="quota" class="lead" style="margin:12px 0 0"></p>
</div>
<div id="run" hidden></div>
<div id="paywall" class="box" hidden><strong>Has hecho tus 20 preguntas gratis de hoy.</strong><br>Mañana tienes 20 más. Con el plan completo (4,99 €/mes, próximamente) los test son ilimitados. Mientras tanto, los test por tema siguen abiertos: <a href="/#temas">ver temas</a>.</div>"""
app_js = r"""
var Q=[],L='abcd',LIM=20;
function st(k,d){try{return JSON.parse(localStorage.getItem(k))||d}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function today(){return new Date().toISOString().slice(0,10)}
function used(){var u=st('uso',{});return u.d===today()?u.n:0}
function addUse(){var u={d:today(),n:used()+1};sv('uso',u)}
function quota(){document.getElementById('quota').textContent='Te quedan '+Math.max(0,LIM-used())+' preguntas gratis hoy.'}
function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
fetch('/preguntas.json').then(function(r){return r.json()}).then(function(d){Q=d;quota()});
document.getElementById('go').onclick=function(){
  var left=LIM-used(); if(left<=0){document.getElementById('paywall').hidden=false;return}
  var b=document.getElementById('blk').value, n=Math.min(+document.getElementById('num').value,left);
  var f=st('fallos',[]), pool=Q.filter(function(q){return b==='all'||(b==='fallos'?f.indexOf(q.id)>-1:q.law===b)});
  if(!pool.length){document.getElementById('quota').textContent='Aún no tienes fallos guardados.';return}
  var set=shuffle(pool.slice()).slice(0,n), run=document.getElementById('run'), ok=0, done=0;
  document.getElementById('setup').hidden=true; run.hidden=false; run.innerHTML='<p class="score" id="sc">0 de '+set.length+'</p>';
  set.forEach(function(q,idx){
    var ord=shuffle([0,1,2,3]), card=document.createElement('article'); card.className='q';
    var h='<h3><span class="n">'+(idx+1)+'.</span></h3><ul class="opts"></ul><div class="exp" hidden></div>';
    card.innerHTML=h; card.querySelector('h3').appendChild(document.createTextNode(q.q));
    var ul=card.querySelector('ul');
    ord.forEach(function(k,i){var li=document.createElement('li'),bt=document.createElement('button');bt.type='button';bt.className='opt';bt.innerHTML='<span class="l">'+L[i]+')</span>';bt.appendChild(document.createTextNode(q.o[k]));li.appendChild(bt);ul.appendChild(li);
      bt.onclick=function(){ if(card.dataset.d)return; card.dataset.d=1; addUse(); done++;
        var good=ord.indexOf(q.c); ul.children[good].firstChild.classList.add('ok');
        var fl=st('fallos',[]);
        if(k===q.c){ok++; fl=fl.filter(function(x){return x!==q.id})} else {bt.classList.add('bad'); if(fl.indexOf(q.id)<0)fl.push(q.id)}
        sv('fallos',fl);
        var e=card.querySelector('.exp'); e.hidden=false; e.innerHTML='<strong></strong><span class="src"></span>';
        e.firstChild.textContent='Correcta: '+L[good]+') '+q.o[q.c];
        e.lastChild.textContent=q.a+': «'+q.t+'» ';
        var a=document.createElement('a');a.href=q.u;a.target='_blank';a.rel='noopener nofollow';a.textContent='ver en el BOE';e.lastChild.appendChild(a);
        document.getElementById('sc').textContent=ok+' aciertos de '+done+' (de '+set.length+')';
        if(done===set.length){var p=document.createElement('p');p.innerHTML='<button class="btn" type="button" onclick="location.reload()">Otro test</button>';run.appendChild(p)}
      }});
    run.appendChild(card);
  });
};
"""
write("/app/", page("Test aleatorio | Artículo Exacto", "Test aleatorio de oposiciones con repaso de fallos.", app_body, "/app/", '<meta name="robots" content="noindex">', f"<script>{app_js}</script>"))
urls_noindex = ["/app/"]

slim = [{"id": q["id"], "law": q["law"], "q": q["q"], "o": q["o"], "c": q["c"], "a": art_label(q), "t": q["cita"], "u": boe_url(q)} for q in qs]
write("/preguntas.json", json.dumps(slim, ensure_ascii=False, separators=(",", ":")))

legal = """<h1>Aviso legal</h1>
<p>Web en fase de pruebas, gratuita y sin actividad económica. Los datos del titular se publicarán aquí antes de activar cualquier plan de pago.</p>
<p>Esta web ofrece test de práctica para oposiciones. No es una web oficial ni está vinculada al INAP ni a ningún organismo público. Los textos legales citados proceden de la legislación consolidada publicada por la Agencia Estatal Boletín Oficial del Estado, que es la única versión con valor jurídico.</p>
<p>Las preguntas se revisan contra el texto legal, pero pueden contener errores. Comprueba siempre el artículo en el BOE.</p>"""
write("/aviso-legal/", page("Aviso legal | Artículo Exacto", "Aviso legal.", legal, "/aviso-legal/"))
priv = """<h1>Privacidad</h1>
<p>Esta web no usa cookies de publicidad ni de analítica de terceros. El progreso de tus test (preguntas usadas hoy y fallos) se guarda solo en tu navegador, con almacenamiento local, y no se envía a ningún servidor.</p>
<p>Si nos escribes por correo, usaremos tu dirección solo para responderte.</p>"""
write("/privacidad/", page("Privacidad | Artículo Exacto", "Política de privacidad.", priv, "/privacidad/"))
urls += ["/aviso-legal/", "/privacidad/"]

write("/404.html", page("Página no encontrada | Artículo Exacto", "Página no encontrada.", '<h1>Esta página no existe</h1><p><a href="/">Volver al inicio</a></p>', "/404.html"))
write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /app/\nSitemap: {BASE}/sitemap.xml\n")
write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
write("/manifest.webmanifest", json.dumps({"name": "Artículo Exacto · Test oposiciones", "short_name": "Artículo Exacto", "start_url": "/app/", "display": "standalone", "background_color": "#f7f8fa", "theme_color": "#1d4e89", "lang": "es", "icons": [{"src": "/icon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False))
write("/icon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1d4e89"/><text x="32" y="43" font-family="Georgia,serif" font-size="34" font-weight="700" fill="#fff" text-anchor="middle">§</text></svg>')
llms = "# Artículo Exacto\n\n> Test gratuitos de oposiciones a Auxiliar Administrativo del Estado (bloque I). Cada pregunta cita el texto literal del artículo de la Constitución Española, la Ley 39/2015 o la Ley 40/2015, con enlace al BOE consolidado.\n\n## Test por tema\n\n" + "".join(f"- [{n}]({BASE}/test/{s}/): {a}\n" for s, n, a in all_topics) + f"\n## Datos\n\n- [Todas las preguntas en JSON]({BASE}/preguntas.json): pregunta, opciones, respuesta correcta, artículo y cita literal.\n"
write("/llms.txt", llms)
print("páginas:", len(urls), "preguntas:", len(qs), "base:", BASE)
