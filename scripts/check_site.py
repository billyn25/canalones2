#!/usr/bin/env python3
"""Check deployed HTML, links, fragments, structured data and complete coverage."""
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict,deque
from urllib.parse import urlparse,unquote
import json,xml.etree.ElementTree as ET,re,os
R=Path(__file__).resolve().parents[1];D=R/'dist'
report=json.loads((R/'build-report.json').read_text());base=report['site_url'];pages={};errors=[]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.links=[];self.assets=[];self.images=[];self.ids=set();self.h1=0;self.canonical=[];self.title='';self.description='';self.robot='';self.schema=[];self.scripts=False;self.schemaText='';self.inTitle=False;self.inFooter=False;self.footer='';self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag=='img':self.images.append(a)
  if tag=='script' and a.get('src'):self.assets.append(a['src'])
  if tag=='link' and a.get('rel')=='stylesheet':self.assets.append(a['href'])
  if tag=='h1':self.h1+=1
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
  if tag=='meta' and a.get('name')=='description':self.description=a.get('content','')
  if tag=='meta' and a.get('name')=='robots':self.robot=a.get('content','')
  if tag=='script' and a.get('type')=='application/ld+json':self.scripts=True;self.schemaText=''
  if tag=='title':self.inTitle=True
  if tag=='footer':self.inFooter=True
 def handle_data(self,data):
  if self.scripts:self.schemaText+=data
  if self.inTitle:self.title+=data
  if self.inFooter:self.footer+=data
 def handle_endtag(self,tag):
  if tag=='title':self.inTitle=False
  if tag=='footer':self.inFooter=False
  if tag=='script' and self.scripts:
   self.schema.append(json.loads(self.schemaText));self.scripts=False
expected_provinces={'vizcaya':'Vizcaya','alava':'Álava','guipuzcoa':'Guipúzcoa','burgos':'Burgos','segovia':'Segovia','cantabria':'Cantabria','leon':'León'}
coverage_rows=json.loads((D/'assets/municipios.json').read_text())
for route in report['routes']:
 p=route['path'];text=(D/p.strip('/')/'index.html').read_text();a=Page(text);pages[p]=a
 if a.h1!=1:errors.append(f'{p}: {a.h1} H1')
 for asset in a.assets:
  if asset.startswith('/') and not (D/asset.lstrip('/')).is_file():errors.append(f'{p}: CSS o JavaScript inexistente {asset}')
 for image in a.images:
  src=image.get('src','')
  if src.startswith('/') and not (D/src.lstrip('/')).is_file():errors.append(f'{p}: imagen inexistente {src}')
  if not image.get('alt') or not image.get('width') or not image.get('height'):errors.append(f'{p}: imagen sin descripción o dimensiones')
 if a.canonical!=[base+p]:errors.append(f'{p}: canonical incorrecta')
 if not a.description or not a.title:errors.append(f'{p}: metadatos vacíos')
 if route['indexable'] and 'noindex' in a.robot:errors.append(f'{p}: noindex inesperado')
 if not a.schema:errors.append(f'{p}: sin datos estructurados')
 if 'Roberto' in a.footer or 'González' in a.footer:errors.append(f'{p}: nombre personal en el pie')
 if p not in ['/aviso-legal/','/privacidad/'] and 'Roberto Fuentes González' in text:errors.append(f'{p}: nombre personal fuera de páginas legales')
 if 'chatgpt.site' in text:errors.append(f'{p}: URL de vista previa en SEO')
 for sch in a.schema:
  for item in sch['@graph']:
   if item.get('@type')=='Service':
    if item.get('provider')!={'@id':base+'/#negocio'}:errors.append(f'{p}: proveedor no enlazado')
    coverage=item.get('areaServed',[])
    if isinstance(coverage,dict):coverage=[coverage]
    if p.strip('/') in expected_provinces:
     expected=expected_provinces[p.strip('/')]
     if coverage!=[{'@type':'AdministrativeArea','name':expected}]:errors.append(f'{p}: cobertura provincial incorrecta')
    elif p.split('/')[1] in expected_provinces and len(p.strip('/').split('/'))==2:
     covered_names={row['name'] for row in coverage_rows if urlparse(row['url']).path==p}
     if {place.get('name') for place in coverage}!=covered_names:errors.append(f'{p}: cobertura local no coincide con la lista visible')
   if item.get('@type')=='BreadcrumbList':
    pos=[x['position'] for x in item['itemListElement']]
    if pos!=list(range(1,len(pos)+1)):errors.append(f'{p}: posiciones breadcrumb')
titles=defaultdict(list);descs=defaultdict(list);graph=defaultdict(set)
for p,a in pages.items():
 titles[a.title].append(p);descs[a.description].append(p)
 for href in a.links:
  u=urlparse(href)
  if u.scheme or u.netloc:continue
  target=unquote(u.path) or p
  if target in pages:
   graph[p].add(target)
   if u.fragment and unquote(u.fragment) not in pages[target].ids:errors.append(f'{p}: fragmento roto {href}')
  elif target.startswith('/') and not (D/target.lstrip('/')).is_file():errors.append(f'{p}: enlace roto {href}')
for label,rows in [('título',titles),('descripción',descs)]:
 for k,v in rows.items():
  if len(v)>1:errors.append(f'{label} duplicado: {v}')
seen={'/'};q=deque(['/'])
while q:
 for to in graph[q.popleft()]:
  if to not in seen:seen.add(to);q.append(to)
for p in pages:
 if p not in seen:errors.append('Página huérfana: '+p)
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap=[n.text for n in ET.parse(D/'sitemap.xml').findall('s:url/s:loc',ns)]
expected=[base+r['path'] for r in report['routes'] if r['indexable']]
expected_count=len(json.loads((R/'data/hubs.json').read_text()))+len(expected_provinces)+8
if os.environ.get('CONTEXT')=='production' and len(expected)!=expected_count:errors.append(f'Producción debe tener {expected_count} páginas indexables, no un sitemap vacío')
if set(sitemap)!=set(expected) or len(sitemap)!=len(set(sitemap)):errors.append('Sitemap no coincide con páginas indexables')
allrows=json.loads((D/'assets/municipios.json').read_text())
muni=json.loads((R/'data/municipalities.json').read_text())
if len(allrows)!=sum(len(v) for v in muni.values()) or len(allrows)!=1145:errors.append('Cobertura incompleta')
for row in allrows:
 u=urlparse(row['url'])
 if u.path not in pages or (u.fragment and u.fragment not in pages[u.path].ids):errors.append('Municipio sin destino: '+row['name'])
for key,rows in muni.items():
 for name,code,*_ in rows:
  assigned=[x for x in allrows if x['code']==code]
  if len(assigned)!=1:errors.append('Municipio no encontrado o duplicado: '+code)
# All production pages are directly rendered; no script is needed to read service or coverage.
if any('/* /index.html' in p.read_text() for p in [D/'_redirects']):errors.append('Fallback SPA provoca soft 404')
if not (D/'404.html').exists():errors.append('Falta 404')
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'OK: {len(pages)} páginas, {len(sitemap)} URLs de sitemap, 1145 municipios, enlaces y anclas válidos, sin páginas huérfanas, títulos/descripciones únicos y nombre personal solo en legales.')

