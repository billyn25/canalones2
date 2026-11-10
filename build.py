#!/usr/bin/env python3
"""Build static, crawlable pages using only Python's standard library."""
from pathlib import Path
import json, os, re, shutil, unicodedata, math, hashlib
from html import escape as esc
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
CONFIG=json.loads((ROOT/'config.json').read_text())
BASE=os.environ.get('SITE_URL',CONFIG['site_url']).rstrip('/')
assert urlparse(BASE).scheme=='https' and urlparse(BASE).netloc,'SITE_URL debe ser una URL HTTPS absoluta'
INDEXABLE=os.environ.get('INDEXABLE','true').lower()=='true'
if os.environ.get('CONTEXT')=='production':
 assert INDEXABLE,'Se cancela el build: producción no puede publicarse con INDEXABLE=false.'
 assert BASE==CONFIG['site_url'].rstrip('/'),'Se cancela el build: el dominio de producción no coincide con config.json.'
PHONE=CONFIG['phone']; DISPLAY=CONFIG['phone_display']; BRAND=CONFIG['brand']
PROVINCES={'Bizkaia':('Vizcaya','vizcaya','48'), 'Araba':('Álava','alava','01'), 'Gipuzkoa':('Guipúzcoa','guipuzcoa','20'), 'Burgos':('Burgos','burgos','09'), 'Segovia':('Segovia','segovia','40'), 'Cantabria':('Cantabria','cantabria','39'), 'León':('León','leon','24')}
MUNICIPALITIES=json.loads((ROOT/'data/municipalities.json').read_text())
HUBS=json.loads((ROOT/'data/hubs.json').read_text())
SERVICES=json.loads((ROOT/'data/services.json').read_text())
PHOTOS=json.loads((ROOT/'data/photos.json').read_text())
PHOTO_BY_ID={photo['id']:photo for photo in PHOTOS}
WORK_TOWN_CODES=('24021','20029','48013','39097','09410','09018','48065')
UGAO_WORK_PATH='/trabajos/limpieza-tejado-canalones-ugao-miraballes/'
UGAO_WORK_TITLE='Limpieza de tejado y canalones en Ugao-Miraballes'
UGAO_WORK_PHOTOS=('ugao-restos-hojas','ugao-cubierta-teja','ugao-detalle-cubierta')
def slug(s):
 s=''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
 return re.sub('[^a-z0-9]+','-',s).strip('-')
def short(h):return h['name'].split(' / ')[0]
def d2(a,b):return (a[2]-b[2])**2+((a[3]-b[3])*math.cos(math.radians((a[2]+b[2])/2)))**2
def path(h):return f"/{h['province_slug']}/{h['slug']}/"
def full(p):return BASE+p
ALL={r[1]:r for rows in MUNICIPALITIES.values() for r in rows}
for source,(display,ps,pc) in PROVINCES.items():
 for code,h in HUBS.items():
  if code.startswith(pc):
   h.update(code=code,province=display,province_slug=ps,slug=h.get('slug',slug(short(h))),members=[])
 for row in MUNICIPALITIES[source]:
  h=min((h for code,h in HUBS.items() if code.startswith(pc)),key=lambda h:(d2(row,ALL[h['code']]),h['code']))
  h['members'].append(row)
for h in HUBS.values():h['members'].sort(key=lambda r:slug(r[0]))
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT/'assets',OUT/'assets')
# Content fingerprints prevent repeat visitors from using an older stylesheet or script.
def fingerprint_asset(name):
 source=ROOT/'assets'/name
 version=hashlib.sha256(source.read_bytes()).hexdigest()[:12]
 filename=f'{source.stem}.{version}{source.suffix}'
 shutil.copyfile(source,OUT/'assets'/filename)
 return '/assets/'+filename
STYLE_URL=fingerprint_asset('style.css')
SCRIPT_URL=fingerprint_asset('app.js')
ROUTES=[]
def link(p,label,cls=''):return f'<a href="{p}"'+(f' class="{cls}"' if cls else '')+f'>{esc(label)}</a>'
def crumbs(items):return '<nav class="breadcrumbs" aria-label="Ruta de navegación">'+'<span aria-hidden="true"> / </span>'.join(link(p,n) if i<len(items)-1 else f'<span aria-current="page">{esc(n)}</span>' for i,(n,p) in enumerate(items))+'</nav>'
def icon_markup(markup):
 paths={'↗':'M5 19 19 5M5 5h14v14','→':'M4 12h16m-6-6 6 6-6 6','↓':'M12 4v16m-6-6 6 6 6-6'}
 def decorate(text):
  for glyph,d in paths.items():
   text=text.replace(glyph,f'<svg class="arrow-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{d}"/></svg>')
  return text
 return ''.join(part if part.startswith('<') else decorate(part) for part in re.split(r'(<[^>]*>)',markup))
def header():return f'''<div class="urgency-bar"><span><i aria-hidden="true"></i>Urgencias de tejados y canalones</span><a href="tel:{PHONE}">Llamar ahora ↗</a></div><a class="skip" href="#contenido">Ir al contenido</a><header><a class="brand" href="/" aria-label="Fuentes, inicio">fuentes<span>TEJADOS & CANALONES</span></a><nav aria-label="Menú principal"><a href="/#servicios">Servicios</a><a href="/trabajos/">Trabajos</a><a href="/#zonas">Municipios</a><a href="#presupuesto">Pedir presupuesto ↗</a></nav><a class="call" href="tel:{PHONE}">{DISPLAY}</a></header>'''
def work_gallery(ids=None,compact=False,show_locations=False):
 photos=[PHOTO_BY_ID[key] for key in ids] if ids else PHOTOS
 cards=[]
 for photo in photos:
  fullsrc='/assets/'+photo['file'];thumb='/assets/'+photo['thumbnail']
  cards.append(f'<figure class="work-photo"><a href="{fullsrc}" data-work-photo data-caption="{esc(photo["caption"],quote=True)}" aria-label="Ampliar: {esc(photo["title"],quote=True)}"><img src="{thumb}" width="{photo["width"]}" height="{photo["height"]}" alt="{esc(photo["alt"],quote=True)}" loading="lazy" decoding="async"><span class="photo-zoom" aria-hidden="true">Ampliar ↗</span></a><figcaption><h3>{esc(photo["title"])}</h3><p>{esc(photo["caption"])}</p></figcaption></figure>')
 heading='<h2>El trabajo, visto de cerca.</h2>' if compact else ''
 intro='<p class="work-intro">Fotografías de nuestros trabajos reales en tejados, canalones y aleros.</p>'
 if show_locations:
  links=[]
  for code in WORK_TOWN_CODES:
   row=ALL[code]
   hub=next(h for h in HUBS.values() if row in h['members'])
   links.append(link(town_target(row,hub),municipality_label(row)))
  intro+='<div class="work-intro" id="zonas-trabajos"><h2>Municipios donde hemos trabajado</h2><p>Consulta los servicios disponibles en estas zonas.</p><ul class="home-towns">'+''.join(f'<li>{item}</li>' for item in links)+'</ul></div>'
 more=f'<a class="btn gallery-more" href="/trabajos/">Ver las {len(PHOTOS)} fotografías →</a>' if compact else ''
 return '<section class="work-gallery'+(' compact' if compact else '')+'"><span class="eyebrow">NUESTROS TRABAJOS</span>'+heading+intro+'<div class="work-grid">'+''.join(cards)+'</div>'+more+'</section>'

def ugao_work_feature():
 return f'<section class="related"><span class="eyebrow">TRABAJO REAL · UGAO-MIRABALLES</span><h2>Retirada de hojas del tejado y los canalones</h2><p>La limpieza integral incluyó la retirada y recogida de hojas y restos vegetales. En las fotos se ve la cubierta y el material retirado.</p><div>{link(UGAO_WORK_PATH,"Ver la limpieza en Ugao-Miraballes →")}</div></section>'

def footer():
 return f'''<footer class="site-footer"><div class="footer-top"><div><span class="eyebrow">PARA CUANDO TOCA MIRAR ARRIBA</span><h2>Tejado cuidado.<br>Agua por su sitio.</h2><p>Cuéntanos qué necesitas y dónde está el inmueble.<br>Empezamos por ahí.</p></div><a class="footer-phone" href="tel:{PHONE}">{DISPLAY}<span>Llámanos para consultar disponibilidad ↗</span></a></div><div class="footer-roofs" aria-hidden="true"><svg viewBox="0 0 1200 100" preserveAspectRatio="none"><path d="M0 80H55V58L125 13 195 58V80H255V50L320 8 385 50V80H490V60L555 20 620 60V80H710V48L790 4 870 48V80H935V65L1015 19 1095 65V80H1200"/><path d="M112 75V52H138V75M306 75V45H333V75M542 75V54H568V75M775 75V40H805V75M1001 75V57H1029V75"/></svg></div><div class="footer-grid"><div><a class="brand" href="/">fuentes<span>TEJADOS & CANALONES</span></a><p>Limpieza, mantenimiento<br>y reparación de cubiertas.</p><p>Base del equipo en Bilbao</p><address>Posta Kalea, 21<br>48005 Bilbao, Bizkaia</address><p>Nos desplazamos a las zonas de servicio.</p><a class="footer-wa" href="https://wa.me/34641490536" target="_blank" rel="noopener">Escribir por WhatsApp ↗</a></div><div><h3>En qué te ayudamos</h3>{''.join(link('/servicios/'+s['slug']+'/',s['title']) for s in SERVICES)}<a href="/trabajos/">Fotos de nuestros trabajos</a><a href="/guias/limpieza-o-reparacion/">¿Limpieza o reparación?</a><a href="/guias/presupuesto/">Cómo preparar el presupuesto</a></div><div><h3>Dónde vamos</h3>{''.join(link('/'+ps+'/',display) for display,ps,pc in PROVINCES.values())}</div><div><h3>Antes de empezar</h3><p>Casas, comunidades y naves.</p><p>Presupuesto según el estado,<br>las medidas y el acceso.</p><a href="#presupuesto">Preparar una consulta →</a><a href="/aviso-legal/">Aviso legal</a><a href="/privacidad/">Privacidad y cookies</a></div></div><div class="footer-bottom"><span>© {__import__('datetime').date.today().year} Fuentes · Tejados y Canalones</span><span>Sin rodeos. Con las cosas claras.</span></div></footer><div class="mobile-contact"><a href="tel:{PHONE}">Llamar</a><a href="https://wa.me/34641490536" target="_blank" rel="noopener">WhatsApp ↗</a></div>'''
def contact(town='',service=''):
 opts=''.join(f'<option value="{esc(s["title"],quote=True)}"'+(' selected' if s['title']==service else '')+'>'+s['title']+'</option>' for s in SERVICES)
 return f'''<section id="presupuesto" class="contact"><div><span class="eyebrow">VAMOS AL GRANO</span><h2>Cuéntanos qué pasa.<br>Y vemos cómo ayudarte.</h2><p>Elige limpieza de tejados, de canalones o ambos. Si hay una gotera, cuéntanos cuándo aparece. Una foto desde un lugar seguro ayuda a preparar la consulta.</p><p>Confirmamos desplazamiento y disponibilidad antes de acordar la visita.</p><a class="phone" href="tel:{PHONE}">{DISPLAY} ↗</a></div><form id="quote"><label>¿Dónde está el inmueble?<input name="town" autocomplete="address-level2" value="{esc(town,quote=True)}" placeholder="Municipio o localidad" required maxlength="120"></label><label>¿Qué necesitas?<select name="service">{opts}<option>Limpieza de tejados y canalones</option></select></label><label>Cuéntanos un poco<textarea name="details" placeholder="Casa, comunidad o nave; qué ocurre y desde cuándo…" maxlength="1500"></textarea></label><p class="small">Este formulario prepara el mensaje. Lo revisas y decides si lo envías desde WhatsApp; puedes añadir fotos allí. <a href="/privacidad/">Privacidad</a>.</p><button class="btn" type="submit">Preparar consulta por WhatsApp ↗</button><p id="form-status" role="status"></p><noscript><p>Puedes <a href="https://wa.me/34641490536">escribir directamente por WhatsApp</a> o llamar al {DISPLAY}.</p></noscript></form></section>'''
def faq(items):return '<section class="faq"><span class="eyebrow">LAS DUDAS HABITUALES</span><h2>Antes de empezar.</h2>'+''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in items)+'</section>'
def card(s,i):return f'<a class="service" href="/servicios/{s["slug"]}/"><span class="num">0{i+1} /</span><h3>{s["title"]}</h3><p>{s["description"]}</p><b>Ver el servicio ↗</b></a>'
def page(p,title,description,body,breadcrumbs=None,service=None,area=None,indexable=True,coverage=None):
 body=icon_markup(body)
 idx=INDEXABLE and indexable
 business={'@type':'RoofingContractor','@id':BASE+'/#negocio','name':BRAND,'url':BASE+'/','telephone':PHONE,'address':{'@type':'PostalAddress','streetAddress':'Posta Kalea, 21','postalCode':'48005','addressLocality':'Bilbao','addressRegion':'Bizkaia','addressCountry':'ES'},'areaServed':[{'@type':'AdministrativeArea','name':d} for d,_,_ in PROVINCES.values()]}
 graph=[business,{'@type':'WebSite','@id':BASE+'/#web','name':BRAND,'url':BASE+'/','inLanguage':'es'}, {'@type':'WebPage','@id':full(p)+'#pagina','url':full(p),'name':title,'description':description,'inLanguage':'es','isPartOf':{'@id':BASE+'/#web'}}]
 if breadcrumbs:graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':full(u)} for i,(n,u) in enumerate(breadcrumbs)]})
 if service:graph.append({'@type':'Service','@id':full(p)+'#servicio','name':service,'serviceType':['Limpieza de tejados','Limpieza de canalones','Reparación de goteras','Reparación de tejados','Reparación de canalones y bajantes'] if area else service,'provider':{'@id':BASE+'/#negocio'},'areaServed':coverage or ({'@type':'City','name':area} if area else business['areaServed']),'url':full(p)})
 if service:graph[2]['mainEntity']={'@id':full(p)+'#servicio'}
 schema=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')
 robots='index,follow,max-image-preview:large' if idx else 'noindex,follow'
 text=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="google-adsense-account" content="ca-pub-1569998172644306"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1569998172644306" crossorigin="anonymous"></script><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description,quote=True)}"><meta name="robots" content="{robots}"><link rel="canonical" href="{full(p)}"><meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(description,quote=True)}"><meta property="og:url" content="{full(p)}"><meta property="og:image" content="{BASE}/assets/trabajos/cubierta-comunidad.webp"><meta name="theme-color" content="#253e32"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{STYLE_URL}"><script type="application/ld+json">{schema}</script><script src="{SCRIPT_URL}" defer></script></head><body>{icon_markup(header())}<main id="contenido">{body}</main>{icon_markup(footer())}</body></html>'''
 dest=OUT/p.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
 ROUTES.append({'path':p,'indexable':idx,'title':title})
def municipality_label(row):
 aliases=CONFIG.get('municipality_aliases',{}).get(row[1],[])
 return row[0]+(' ('+', '.join(aliases)+')' if aliases else '')
def town_service_link(target,label):
 return f'<a href="{target}"><span class="municipality-name">{esc(label)}</span></a>'
def town_target(row,h):return path(h) if row[1]==h['code'] else path(h)+'#municipio-'+row[1]
def municipality_service_card(row):
 name,code=row[:2];label=municipality_label(row)
 choices=[('Limpieza de tejados','Limpieza de tejados'),('Limpieza de canalones','Limpieza de canalones'),('Goteras y arreglo de tejado','Reparación de goteras y tejados')]
 actions=''.join(f'<a href="#presupuesto" data-locality="{esc(name,quote=True)}" data-service="{esc(value,quote=True)}" aria-label="{esc(text+" en "+label,quote=True)}">{esc(text)} →</a>' for text,value in choices)
 return f'<li id="municipio-{code}" class="municipality-service"><h3>{esc(label)}</h3><div class="municipality-services">{actions}</div></li>'
def province_zone(source):
 display,ps,pc=PROVINCES[source]; hs=[h for c,h in HUBS.items() if c.startswith(pc)]
 return '<div class="coverage-groups">'+''.join(f'<details class="coverage-group" open><summary>{esc(short(h))} y zona <span>{len(h["members"])} municipios</span></summary><div class="municipality-links">'+''.join(town_service_link(town_target(r,h),municipality_label(r)) for r in h['members'])+f'</div>{link(path(h),"Ver servicios y preparar la consulta en esta zona →","all-zone")}</details>' for h in hs)+'</div>'
# Home: service choices first, whole coverage searchable, no artificial per-village URLs.
HOME_EXTRA_CODES={'48': ['48017', '48054', '48082', '48003', '48090', '48034', '48036', '48084', '48096'], '01': ['01010', '01901', '01028', '01058', '01043', '01018', '01063', '01001', '01004', '01009', '01017', '01042', '01055'], '20': ['20018', '20074', '20067', '20040', '20036', '20902', '20029', '20032', '20056', '20059', '20077', '20081'], '09': ['09124', '09211', '09321', '09394', '09903', '09048', '09289', '09410', '09412', '09427', '09434'], '40': ['40040', '40043', '40112', '40146', '40155', '40906', '40203', '40024', '40057', '40138', '40195', '40208', '40225'], '39': ['39012', '39016', '39008', '39052', '39079', '39085', '39023', '39025', '39042', '39060', '39073', '39074'], '24': ['24134', '24070', '24034', '24038', '24094', '24209']}
zonecards=''
for src,(display,ps,pc) in PROVINCES.items():
 selected=[ALL[c] for c in dict.fromkeys([c for c in HUBS if c.startswith(pc)]+HOME_EXTRA_CODES[pc])]
 assert len(selected)==18 and len({r[1] for r in selected})==18
 townlinks=[]
 for row in selected:
  h=next(h for h in HUBS.values() if any(r[1]==row[1] for r in h['members']))
  label=short(HUBS[row[1]]) if row[1] in HUBS else row[0]
  if row[1]=='09903':label='Villarcayo'
  townlinks.append('<li>'+town_service_link(town_target(row,h),label)+'</li>')
 zonecards+=f'<article class="province-card"><span>{len(MUNICIPALITIES[src])} municipios</span><h3>{link("/"+ps+"/",display+" ↗")}</h3><ul class="home-towns">'+''.join(townlinks)+f'</ul>{link("/"+ps+"/","Ver todos los municipios →","all-zone")}</article>'

body='''<section class="hero"><div class="hero-copy"><span class="eyebrow">LIMPIEZA DE TEJADOS Y CANALONES</span><h1>Que llueva fuera.<br><em>Dentro, tranquilidad.</em></h1><p>Limpiamos tejados y canalones, revisamos bajantes y reparamos goteras. Cuéntanos qué necesitas y preparamos tu presupuesto.</p><a class="btn" href="#presupuesto">Pedir presupuesto ↗</a><a class="textlink" href="#servicios">Ver los servicios ↓</a><div class="hero-note">Casas, comunidades y naves.<br>Una consulta sencilla, sin rodeos.</div></div><figure><img src="/assets/trabajos/cubierta-comunidad.webp" width="900" height="1600" alt="Vista de un tejado de comunidad durante una revisión propia" fetchpriority="high"><figcaption>Fotografía de nuestros trabajos · cubierta de comunidad.</figcaption><span class="stamp">Menos líos.<br>Más cuidado.</span></figure></section><div class="strip">UNA HOJA HOY. UN ATASCO MAÑANA. <span>Mejor echarle un vistazo a tiempo. ↗</span></div><section id="servicios"><div class="section-head"><span class="eyebrow">QUÉ HACEMOS</span><h2>Arriba pasan cosas.<br>Nos ocupamos de ellas.</h2><p>Puedes pedir solo limpieza de tejados, solo limpieza de canalones o ambos servicios. Si hay una filtración, primero hay que revisar su origen.</p></div><div class="services">'''+''.join(card(s,i) for i,s in enumerate(SERVICES))+'''</div></section><section class="split-story"><figure><img src="/assets/trabajos/canalon-alero.webp" width="900" height="1600" alt="Canalón junto al alero fotografiado durante nuestros trabajos" loading="lazy"></figure><div><span class="eyebrow">CADA COSA, POR SU NOMBRE</span><h2>¿Suciedad, atasco<br>o una gotera?</h2><p>Si el canalón rebosa, puede necesitar limpieza. Si pierde por una unión, conviene revisar el tramo. Si aparece una mancha dentro de casa, hay que localizar por dónde entra el agua.</p><p>Nos cuentas lo que ves y valoramos qué revisión hace falta. El presupuesto debe explicar el trabajo que se va a realizar.</p><a class="textlink" href="/guias/limpieza-o-reparacion/">Qué observar antes de contactar →</a></div></section><section class="how"><span class="eyebrow">ASÍ DE SENCILLO</span><h2>Una foto vale<br>más que mil explicaciones.</h2><div class="steps"><article><b>01</b><h3>Nos lo cuentas</h3><p>Municipio, tipo de inmueble y qué ocurre. Envía fotos tomadas desde un lugar seguro.</p></article><article><b>02</b><h3>Revisamos el alcance</h3><p>Confirmamos acceso, medidas y estado. Si hace falta una visita para presupuestar, la acordamos.</p></article><article><b>03</b><h3>Decides con presupuesto</h3><p>Concretamos qué incluye el trabajo y su importe antes de realizarlo.</p></article></div></section><section id="zonas"><div class="section-head"><span class="eyebrow">CERCA DE TU CASA</span><h2>Siete provincias.<br>Busca tu municipio.</h2><p>Municipios principales con página propia y localidades cercanas agrupadas por zona. Puedes consultar cualquiera de los municipios; confirmamos desplazamiento y disponibilidad al contactar.</p></div><label class="search">¿Dónde necesitas el servicio?<input id="town-search" type="search" placeholder="Por ejemplo: Lekeitio, Segovia, Irun…" autocomplete="off" aria-controls="town-results"></label><div id="town-results" class="town-results" aria-live="polite"></div><noscript><p>Consulta el listado completo en cada provincia:</p></noscript><div class="province-cards">'''+zonecards+'''</div></section>'''+faq([('¿Puedo pedir solo limpieza de tejados o solo de canalones?','Sí. Son servicios distintos y puedes solicitar uno, el otro o ambos. El presupuesto debe indicar qué incluye la intervención.'),('¿Cuánto cuesta?','Depende de los metros, el material, la altura, el acceso y el estado. Una fotografía orienta, pero para fijar el importe puede hacer falta una visita.'),('¿Tengo que subir al tejado para hacer fotos?','No. Envía las que puedas tomar desde un lugar seguro. Explica lo que observas y se valorará cómo revisar la cubierta.'),('¿Atendéis goteras urgentes?','Llama para consultar disponibilidad y explica si está entrando agua ahora. El desplazamiento y las condiciones de intervención se confirman al contactar.')])+contact()
body=body.replace('<section class="how">',ugao_work_feature()+work_gallery(['ugao-restos-hojas','canalon-metalico','rastreles-lamina'],compact=True,show_locations=True)+'<section class="how">')
page('/','Limpieza de tejados y canalones | Fuentes','Limpieza de tejados y de canalones, goteras y bajantes. Vizcaya, Álava, Guipúzcoa, Burgos, Segovia, Cantabria y León. Consulta presupuesto.',body)
PROVINCE_NOTES={
 "20": ("Canalones expuestos y uniones deterioradas", "Si el inmueble está cerca del mar, dinos de qué material es el canalón y dónde se ven manchas, corrosión o pérdidas. Una foto de la unión y otra del tramo completo ayudan a valorar si la intervención puede ser localizada.", "reparacion-canalones", "Consultar la reparación de canalones"),
 "24": ("Humedades en la cubierta y evacuación de agua", "Cuando la humedad se ve en el techo, indica en qué habitación aparece y si coincide con lluvia o deshielo. Si desde el suelo ves tejas movidas o agua desbordando por el alero, esos detalles también ayudan a preparar la visita.", "goteras", "Qué contar al pedir una revisión de goteras"),
 "39": ("Canalones en costa y viviendas junto a arbolado", "Si ves hojas acumuladas en el desagüe, indica si el canalón rebosa en un solo punto o a lo largo del borde. Si también ves una unión dañada o corrosión, añádelo para valorar por separado limpieza y reparación.", "limpieza-canalones", "Distinguir un rebose de una pérdida"),
 "40": ("Tejas movidas y filtraciones cerca de remates", "Si la mancha aparece junto a una chimenea, una pared o una ventana de tejado, dinos cuándo empezó y con qué tipo de lluvia se nota. Una foto interior y otra exterior desde un lugar seguro ayudan a orientar la revisión.", "goteras", "Cómo se prepara la revisión de una gotera"),
 "48": ("Canalones de comunidades y patios interiores", "Si la bajante da a un patio, indica por dónde se puede acceder y si el agua rebosa arriba o aparece en una junta. En comunidades ayuda saber quién puede abrir el acceso a la cubierta.", "limpieza-canalones", "Qué se revisa al limpiar un canalón"),
 "01": ("Agua estancada y tramos que pierden pendiente", "Si el canalón conserva agua horas después de llover, señala el tramo y si ves algún soporte vencido. Cuéntanos si la salida está despejada para valorar si hace falta revisar la bajante o corregir la pendiente.", "reparacion-canalones", "Cuándo revisar soportes y bajantes"),
 "09": ("Tejados de vivienda, nave y casa de pueblo", "Indica si necesitas limpiar una parte del tejado o toda la cubierta y si hay elementos frágiles, como claraboyas. Para estimar el acceso y la superficie, envía una foto general del inmueble tomada desde abajo.", "limpieza-tejados", "Qué datos ayudan a valorar la limpieza"),
}
for source,(display,ps,pc) in PROVINCES.items():
 p='/'+ps+'/'
 b=[('Inicio','/'),(display,p)]
 count=len(MUNICIPALITIES[source])
 body=f'<section class="inner">{crumbs(b)}<span class="eyebrow">ZONAS DE SERVICIO</span><h1>Limpieza de tejados<br>y canalones en {display} <span class="heading-area">y sus pueblos.</span></h1><p>Puedes solicitar limpieza de tejados, limpieza de canalones o reparación de tejados, goteras y bajantes. Selecciona tu municipio entre los {count} del listado: te llevará a la zona correspondiente, donde puedes preparar la consulta.</p><p>El equipo sale de Bilbao y se desplaza a tu municipio. Al preparar el presupuesto confirmamos el acceso, la disponibilidad y las condiciones del desplazamiento.</p><a class="btn" href="#municipios">Buscar mi municipio ↓</a></section><section id="municipios" class="directory"><div class="section-head"><span class="eyebrow">TODOS LOS MUNICIPIOS</span><h2>Encuentra tu zona.</h2><p>Abre una zona para ver sus municipios y preparar la consulta. Si tu vivienda está en un núcleo pequeño, indica también su nombre al contactar.</p></div><label class="search">Filtrar municipios en {display}<input type="search" id="province-search" placeholder="Escribe el nombre de tu municipio" aria-controls="directory-list"></label><p id="directory-status" role="status"></p><div id="directory-list">'+province_zone(source)+'</div><p class="data-credit">Nombres y códigos de municipio: datos derivados del INE. Agrupación orientativa por proximidad geográfica; consulta el desplazamiento al contactar.</p></section>'+contact()
 title, advice, service_slug, service_label=PROVINCE_NOTES[pc]
 local_details=f'<section class="inner"><span class="eyebrow">ANTES DE PEDIR PRESUPUESTO</span><h2>{esc(title)}</h2><p>{esc(advice)}</p><a class="textlink" href="/servicios/{service_slug}/">{esc(service_label)} →</a></section>'
 work_towns=[ALL[code][0] for code in WORK_TOWN_CODES if code.startswith(pc)]
 if work_towns:
  town_names=' y '.join([', '.join(work_towns[:-1]),work_towns[-1]]) if len(work_towns)>1 else work_towns[0]
  local_details+=f'<section class="related"><h2>Trabajos realizados en la zona</h2><p>Hemos trabajado en {esc(town_names)}.</p><div><a href="/trabajos/#zonas-trabajos">Ver trabajos y localidades →</a></div></section>'
 if pc=='48':
  local_details+=ugao_work_feature()
 body=body.replace('<section id="municipios"',local_details+'<section id="municipios"',1)
 body=body.replace(contact(),work_gallery(['revision-canalon-red','humedad-techo','mortero-cumbrera'] if source=='León' else ['cubierta-ceramica','canalon-metalico','mortero-cumbrera'],compact=True)+contact())
 page(p,f'Limpieza de tejados y canalones en {display} y sus pueblos',f'Limpieza de tejados y canalones en {display} y sus pueblos. Reparación de goteras y bajantes. Busca tu municipio y pide presupuesto al {DISPLAY}.',body,b,'Limpieza de tejados y canalones en '+display,coverage=[{'@type':'AdministrativeArea','name':display}])
for code,h in HUBS.items():
 p=path(h);n=short(h);b=[('Inicio','/'),(h['province'],'/'+h['province_slug']+'/'),(n,p)]
 neighbors=sorted((other for c,other in HUBS.items() if other['province']==h['province'] and c!=code),key=lambda other:d2(ALL[code],ALL[other['code']]))[:3]
 nearby=''.join(municipality_service_card(r) for r in h['members'])
 close_rows=sorted((r for r in h['members'] if r[1]!=code),key=lambda r:d2(ALL[code],r))[:3]
 close_names=', '.join(municipality_label(r) for r in close_rows)
 zone_intro=(f'<p class="zone-intro">También atendemos consultas de {esc(close_names)} y los demás municipios de esta zona. <a href="#cercanos">Busca el tuyo y elige el servicio →</a></p>' if close_rows else '')
 body=f'<section class="inner">{crumbs(b)}<span class="eyebrow">{esc(h["name"].upper())} Y MUNICIPIOS CERCANOS</span><h1>Limpieza de tejados<br>y canalones en {esc(n)} <span class="heading-area">y municipios cercanos.</span></h1><p class="lead">{esc(h["intro"])}</p>{zone_intro}<a class="btn" href="#presupuesto">Consultar presupuesto en {esc(n)} ↗</a><a class="textlink" href="#cercanos">Ver municipios de esta zona ↓</a></section><section class="local-content"><article><span class="eyebrow">EL TEJADO</span><h2>Limpieza de tejados en {esc(n)}</h2><p>Retirada de suciedad y residuos según el material y el estado de la cubierta. Si también hay canalones que limpiar o piezas deterioradas, se concreta su valoración en el presupuesto.</p><a href="/servicios/limpieza-tejados/" class="textlink">Qué incluye y cómo se valora →</a></article><article><span class="eyebrow">EL DESAGÜE</span><h2>Limpieza de canalones en {esc(n)}</h2><p>Retirada de hojas, barro y acumulaciones; revisión de las salidas hacia las bajantes. Si el agua se pierde por una unión o el tramo está vencido, se diferencia la reparación de la limpieza.</p><a href="/servicios/limpieza-canalones/" class="textlink">Consultar el servicio de canalones →</a></article><article class="roof-repairs"><span class="eyebrow">FILTRACIONES Y PIEZAS DAÑADAS</span><h2>Goteras y reparación de tejados en {esc(n)}</h2><p>Si entra agua o ves tejas rotas, piezas desplazadas o remates deteriorados, puedes consultar su revisión y reparación. Se comprueba el origen de la filtración y el estado de la cubierta para concretar el trabajo, los materiales y el acceso necesarios.</p><a href="/servicios/goteras/" class="textlink">Consultar reparación de goteras y tejados →</a></article></section><section class="local-focus"><div><span class="eyebrow">PARA PREPARAR TU CONSULTA</span><h2>{esc(h["focus"])}.</h2><p>{esc(h["detail"])}</p></div><aside><span class="eyebrow">ESTE DATO NOS AYUDA</span><p>{esc(h["ask"])}</p><p class="small">Haz las fotos desde el suelo o desde un punto seguro. No subas a la cubierta.</p></aside></section><section class="town-coverage" id="cercanos"><span class="eyebrow">COBERTURA DE ESTA ZONA</span><h2>Servicios en {esc(n)} y municipios cercanos.</h2><p>Puedes pedir solo limpieza de tejados, solo limpieza de canalones o consultar goteras y reparación de tejas. Elige el servicio bajo el nombre de tu municipio para preparar el presupuesto con ambos datos. Confirmamos disponibilidad y desplazamiento antes de la visita.</p><ul class="nearby-list municipality-service-list">{nearby}</ul><p>{link("/"+h["province_slug"]+"/","Ver todos los municipios de "+h["province"]+" →","textlink")}</p></section>'+faq([(h['question'],h['answer']),('¿Y si además hay una gotera?','Explica cuándo aparece y dónde está la mancha. Una limpieza puede resolver un rebose por obstrucción, pero una teja o un remate deteriorado necesita otra actuación. Se revisa antes de proponer la reparación.')])+contact(n)+f'<section class="related"><span class="eyebrow">OTRAS ZONAS PRINCIPALES</span><div>'+''.join(link(path(other),short(other)+' ↗') for other in neighbors)+'</div></section>'
 gallery=work_gallery(['revision-canalon-red','humedad-techo','teja-rota-musgo'] if code.startswith('24') else ['teja-vegetacion','canalon-metalico','encuentro-pared'],compact=True)
 if any(row[1] in WORK_TOWN_CODES for row in h['members']):
  gallery+='<section class="related"><h2>Trabajos en esta zona</h2><p>Consulta las fotos del equipo y los municipios donde hemos trabajado.</p><div><a href="/trabajos/#zonas-trabajos">Ver trabajos y localidades →</a></div></section>'
 if ALL['48065'] in h['members']:
  gallery=ugao_work_feature()+gallery
 body=body.replace(contact(n),gallery+contact(n))
 page(p,f'Limpieza de tejados y canalones en {n} y alrededores',f'Limpieza de tejados, canalones y reparación de goteras en {n} y municipios cercanos. Busca tu localidad y pide presupuesto de limpieza o reparación.',body,b,'Limpieza de tejados y canalones en '+n,n,coverage=[{'@type':'City','name':r[0]} for r in h['members']])
for s in SERVICES:
 p='/servicios/'+s['slug']+'/'
 b=[('Inicio','/'),(s['title'],p)]
 body=f'<section class="service-hero"><div>{crumbs(b)}<span class="eyebrow">QUÉ HACEMOS</span><h1>{s["title"]}.</h1><h2>{s["tagline"]}</h2><p>{s["intro"]}</p><a class="btn" href="#presupuesto">Consultar este servicio ↗</a></div><figure><img src="/assets/{s["image"]}" width="{s["width"]}" height="{s["height"]}" alt="{s["alt"]}" fetchpriority="high"><figcaption>{esc(s["photo_caption"])}</figcaption></figure></section><section class="service-detail">'+''.join(f'<article><h2>{title}</h2><p>{txt}</p></article>' for title,txt in s['sections'])+'<aside class="checklist"><h2>Para tu consulta</h2><ul>'+''.join(f'<li>{c}</li>' for c in s['checks'])+'</ul><a href="/guias/presupuesto/" class="textlink">Cómo se prepara el presupuesto →</a></aside></section><section class="related"><h2>Consulta tu zona.</h2><div>'+''.join(link('/'+ps+'/',display+' ↗') for display,ps,pc in PROVINCES.values())+'</div></section>'+faq(s['faq'])+contact(service=s['title'])
 if s['slug']=='limpieza-canalones':
  related='<section class="related"><h2>Cuando hace falta algo más que limpiar</h2><p>Una junta abierta o un tramo descolgado requieren valorar el canalón. Si la humedad aparece dentro de la vivienda, conviene revisar también la cubierta.</p><div><a href="/servicios/reparacion-canalones/">Reparación de canalones y revisión de bajantes →</a><a href="/servicios/goteras/">Revisión de goteras y reparación de tejados →</a></div></section>'
  body=body.replace('<section class="related"><h2>Consulta tu zona.',related+'<section class="related"><h2>Consulta tu zona.',1)
 gallery=work_gallery(s['photo_ids'],compact=True)
 if s['slug'] in ('limpieza-canalones','limpieza-tejados'):
  gallery=ugao_work_feature()+gallery
 body=body.replace(contact(service=s['title']),gallery+contact(service=s['title']))
 page(p,s['title']+' | Fuentes',s['description'],body,b,s['title'])
# A single work gallery; locations of individual photographs are not inferred.
works_path='/trabajos/'
works_crumbs=[('Inicio','/'),('Nuestros trabajos',works_path)]
works_body='<section class="inner works-heading">'+crumbs(works_crumbs)+'<span class="eyebrow">FOTOGRAFÍAS PROPIAS</span><h1>Trabajos reales.<br>El tejado, de cerca.</h1><p>Imágenes tomadas durante nuestros trabajos en cubiertas, canalones y aleros: tejas, encuentros, desagües y detalles del estado de los materiales.</p></section>'+ugao_work_feature()+work_gallery(show_locations=True)+contact()
page(works_path,'Fotos de nuestros trabajos en tejados y canalones | Fuentes','Fotografías propias de trabajos y revisiones en tejados, canalones y aleros. Descubre los detalles de cubiertas, remates y desagües.',works_body,works_crumbs)
ugao_row=ALL['48065']
ugao_hub=next(h for h in HUBS.values() if ugao_row in h['members'])
ugao_crumbs=[('Inicio','/'),('Nuestros trabajos',works_path),(UGAO_WORK_TITLE,UGAO_WORK_PATH)]
ugao_body=f'''<section class="inner guide">
 {crumbs(ugao_crumbs)}
 <span class="eyebrow">TRABAJO REAL · UGAO-MIRABALLES</span>
 <h1>{UGAO_WORK_TITLE}</h1>
 <p>En este trabajo de limpieza integral retiramos hojas y restos vegetales del tejado y de los canalones. Las fotos muestran la cubierta de teja y las bolsas con los restos recogidos.</p>
 <h2>Qué se hizo</h2>
 <ul>
  <li>Retirada de hojas y restos vegetales de la cubierta.</li>
  <li>Limpieza de los canalones y recogida de los residuos.</li>
 </ul>
 <p>Cuando las hojas llegan al canalón pueden dificultar la salida del agua. Si ves acumulación en el tejado o el canalón rebosa al llover, indícanos qué tramo está afectado al pedir presupuesto.</p>
 <a class="btn" href="#presupuesto">Consultar una limpieza similar ↗</a>
</section>'''+work_gallery(UGAO_WORK_PHOTOS)+f'''<section class="related">
 <h2>Servicios relacionados</h2>
 <div>{link('/servicios/limpieza-canalones/','Limpieza de canalones →')}{link('/servicios/limpieza-tejados/','Limpieza de tejados →')}{link(town_target(ugao_row,ugao_hub),'Servicio en Ugao-Miraballes →')}</div>
</section>'''+contact('Ugao-Miraballes','Limpieza de tejados y canalones')
page(UGAO_WORK_PATH,UGAO_WORK_TITLE+' | Trabajo real de Fuentes','Fotos de la limpieza integral de un tejado y sus canalones en Ugao-Miraballes, con retirada y recogida de hojas y restos vegetales.',ugao_body,ugao_crumbs)
# Two practical guides, not a generated blog.
guides=[('limpieza-o-reparacion','¿Limpieza o reparación? Qué observar antes de llamar','Distingue un canalón que rebosa, una unión que pierde y una gotera interior. Qué observar para preparar una consulta de tejados o canalones.', [('El canalón rebosa por arriba','Si ves hojas o residuos, puede haber una obstrucción. Indica si rebosa en un punto o a lo largo de todo el tramo. Si la salida hacia la bajante está bloqueada, retirar solo los restos visibles puede no resolverlo.'),('El agua cae por una unión','Una junta abierta o un material deteriorado pueden necesitar reparación. Envía una foto del detalle y otra del tramo completo; una fuga localizada no permite concluir que haya que sustituir todo el sistema.'),('La humedad aparece dentro','Cuenta si hay goteo o una mancha, con qué lluvia aparece y si está próxima a una pared, chimenea o ventana. El agua puede desplazarse por la cubierta antes de hacerse visible, así que no se presupone el origen por la mancha.'),('El tejado tiene vegetación o suciedad','Explica qué observas y si hay también piezas dañadas. La limpieza debe adaptarse al material y a su estado. No es una impermeabilización ni sustituye la reparación de elementos rotos.'),('Qué no necesitas hacer','No hace falta subir al tejado ni desmontar piezas para pedir una primera valoración. Haz fotos desde un punto seguro y explica el problema. Si se necesita inspección, se acuerdan acceso y condiciones.')]),('presupuesto','Cómo pedir presupuesto de tejados y canalones','Qué datos y fotos ayudan a presupuestar una limpieza de tejado, canalones o reparación de goteras, sin precios inventados.', [('Empieza por el municipio y el inmueble','Indica la localidad, si es casa, comunidad o nave y qué servicio buscas. Si es una comunidad, facilita quién coordina la revisión. Si está fuera del núcleo, puedes enviar una ubicación precisa por WhatsApp.'),('Una foto general y una del problema','La vista general permite entender alturas, accesos y forma de la cubierta. Una imagen de detalle ayuda a mostrar la suciedad, la fuga o la humedad. No subas al tejado para conseguirlas.'),('Las medidas orientan; el acceso también','Si sabes los metros de canalón o la superficie de tejado, indícalos. No son el único factor: altura, espacio alrededor, material, estado y medios de trabajo influyen en el alcance y el importe.'),('Pide que el alcance quede claro','Debe especificarse qué superficies y tramos se incluyen, si se revisan las bajantes y si hay reparaciones o sustituciones. Una limpieza, un desatasco y una reparación no deben darse por equivalentes.'),('La visita puede ser necesaria','Con fotos se puede preparar la consulta, pero para cerrar un importe puede hacer falta revisar el inmueble. Antes se confirma disponibilidad, desplazamiento y acceso. No publicamos un precio universal que ignore estas diferencias.')])]
for s,t,desc,sections in guides:
 p='/guias/'+s+'/'; b=[('Inicio','/'),(t,p)]
 body=f'<section class="inner guide">{crumbs(b)}<span class="eyebrow">PARA DECIDIR CON LAS COSAS CLARAS</span><h1>{t}.</h1><p>{desc}</p>'+''.join(f'<article><h2>{title}</h2><p>{txt}</p></article>' for title,txt in sections)+'</section>'+contact()
 page(p,t+' | Fuentes',desc,body,b)
legal=f'''<section class="inner legal"><h1>Aviso legal</h1><h2>Titular y contacto</h2><p>{esc(CONFIG['owner'])}. Dirección: {esc(CONFIG['address'])}. Teléfono: <a href="tel:{PHONE}">{DISPLAY}</a>.</p><h2>Servicios y presupuestos</h2><p>Esta web presenta servicios de limpieza y mantenimiento de tejados y canalones, revisión de goteras y reparación de bajantes. El alcance, el importe y las condiciones del trabajo se acuerdan en el presupuesto correspondiente. La consulta no reserva una visita ni confirma un plazo de intervención.</p><h2>Uso de las imágenes</h2><p>Las fotografías de trabajos publicadas han sido facilitadas por el titular como imágenes propias. Sus descripciones se refieren a los elementos visibles. La galería reúne imágenes del negocio; la cobertura territorial se indica en las páginas de zonas y municipios.</p><h2>Información y contacto</h2><p>La información general no sustituye la revisión del inmueble. Si necesitas corregir algún dato o realizar una consulta, utiliza el teléfono de contacto. No se publican reseñas, premios ni trabajos locales sin documentación que los respalde.</p></section>'''
page('/aviso-legal/','Aviso legal | Fuentes','Titular de la web, contacto e información sobre servicios e imágenes.',legal+contact(),indexable=False)
privacy=f'''<section class="inner legal"><h1>Privacidad y cookies</h1><h2>Responsable y contacto</h2><p>{esc(CONFIG['owner'])}, {esc(CONFIG['address'])}. Teléfono: <a href="tel:{PHONE}">{DISPLAY}</a>.</p><h2>El formulario prepara un mensaje</h2><p>Lo que escribes en esta web no se envía a una base de datos propia ni se guarda en almacenamiento local. Al continuar, se abre WhatsApp con el texto preparado. Puedes revisarlo y decidir si lo envías; WhatsApp aplica sus propias condiciones y política de privacidad.</p><h2>Gestión de consultas</h2><p>Los datos que envíes al titular se utilizan para responder a tu consulta y preparar el presupuesto solicitado, como medida previa a una posible contratación. Se conservarán mientras se gestione la consulta y, si contratas, durante los plazos que correspondan a la relación y sus obligaciones legales.</p><h2>Tus derechos</h2><p>Puedes solicitar acceso, rectificación, supresión, oposición, limitación o portabilidad contactando con el titular. También puedes reclamar ante la Agencia Española de Protección de Datos.</p><h2>Cookies y recursos externos</h2><p>Esta web incorpora el código de Google AdSense para la gestión de publicidad. Google puede tratar datos técnicos y utilizar cookies según la configuración y las opciones de consentimiento aplicables. La web no incorpora analítica propia, mapas incrustados ni fuentes externas. Los enlaces a WhatsApp se abren al seleccionarlos. El proveedor de alojamiento puede procesar registros técnicos para servir y proteger la web.</p></section>'''
page('/privacidad/','Privacidad y cookies | Fuentes','Cómo funciona la consulta por WhatsApp y qué datos se tratan.',privacy+contact(),indexable=False)
# Real static 404; no fallback that turns missing localities into soft 404s.
notfound=f'<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>Página no encontrada | Fuentes</title><link rel="stylesheet" href="{STYLE_URL}"><main class="inner"><h1>Aquí no hay tejado.</h1><p>No encontramos esta página. Puedes buscar tu municipio desde el inicio o llamarnos.</p><a class="btn" href="/">Volver al inicio</a> <a href="tel:{PHONE}">{DISPLAY}</a></main></html>'
(OUT/'404.html').write_text(notfound)
# Full search data points to real HTML anchors, not thousands of synthetic URLs.
search=[]
for h in HUBS.values():
 for row in h['members']:
  aliases=list(dict.fromkeys(HUBS.get(row[1],{}).get('aliases',[])+CONFIG.get('municipality_aliases',{}).get(row[1],[])))
  search.append({'code':row[1],'name':row[0], 'province':h['province'], 'zone':short(h), 'url':town_target(row,h),'aliases':aliases})
(OUT/'assets/municipios.json').write_text(json.dumps(search,ensure_ascii=False,separators=(',',':')))
indexable=[r for r in ROUTES if r['indexable']]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+full(r['path'])+'</loc></url>' for r in indexable)+'</urlset>')
(OUT/'ads.txt').write_text('google.com, pub-1569998172644306, DIRECT, f08c47fec0942fa0\n')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
(OUT/'_redirects').write_text('/index.html / 301\n')
(OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n/assets/*\n  Cache-Control: public, max-age=86400\n')
(ROOT/'build-report.json').write_text(json.dumps({'site_url':BASE,'pages':len(ROUTES),'sitemap_pages':len(indexable),'principal_municipalities':len(HUBS),'covered_municipalities':len(search),'provinces':{PROVINCES[k][0]:len(v) for k,v in MUNICIPALITIES.items()},'routes':ROUTES},ensure_ascii=False,indent=2))
print(f'{len(ROUTES)} páginas; {len(indexable)} en sitemap; {len(HUBS)} principales; {len(search)} municipios cubiertos.')
