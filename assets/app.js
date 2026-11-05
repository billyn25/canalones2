'use strict';
const normalize=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
const form=document.querySelector('#quote');
if(form){
 form.addEventListener('submit',event=>{
  event.preventDefault();if(!form.reportValidity())return;
  const fields=new FormData(form);
  const message=`Hola, quiero consultar un presupuesto.\nMunicipio: ${fields.get('town')}\nServicio: ${fields.get('service')}\n${fields.get('details')||''}`;
  const url='https://wa.me/34641490536?text='+encodeURIComponent(message);
  const status=document.querySelector('#form-status');status.textContent='Consulta preparada. Revisa el mensaje en WhatsApp antes de enviarlo. ';
  const fallback=document.createElement('a');fallback.href=url;fallback.target='_blank';fallback.rel='noopener';fallback.textContent='Abrir WhatsApp ↗';status.append(fallback);
  window.open(url,'_blank','noopener,noreferrer');
 });
 document.querySelectorAll('[data-locality]').forEach(link=>link.addEventListener('click',()=>{
  form.elements.town.value=link.dataset.locality;
  document.querySelector('#form-status').textContent='Municipio seleccionado: '+link.dataset.locality+'.';
 }));
 const fillFromAnchor=()=>{
  if(!/^#municipio-\d{5}$/.test(location.hash))return;
  const item=document.getElementById(location.hash.slice(1));
  const link=item?.querySelector('[data-locality]');
  if(link)form.elements.town.value=link.dataset.locality;
 };
 fillFromAnchor();window.addEventListener('hashchange',fillFromAnchor);
}
const search=document.querySelector('#town-search');
if(search){
 let municipalities=null,request=null,revision=0;
 const results=document.querySelector('#town-results');
 const load=()=>{
  if(municipalities)return Promise.resolve(municipalities);
  if(!request)request=fetch('/assets/municipios.json').then(response=>{if(!response.ok)throw Error('Municipios no disponibles');return response.json()}).then(rows=>{municipalities=rows.map(row=>({...row,searchText:normalize([row.name,row.province,...row.aliases].join(' '))}));return municipalities}).catch(error=>{request=null;throw error});
  return request;
 };
 search.addEventListener('input',async()=>{
  const current=++revision,q=normalize(search.value);results.replaceChildren();
  if(!q)return;
  results.textContent='Buscando municipio…';
  try{
   const rows=await load();if(current!==revision)return;
   const terms=q.split(' ');
   const matches=rows.filter(row=>terms.every(term=>row.searchText.includes(term))).sort((a,b)=>Number(normalize(b.name)===q)-Number(normalize(a.name)===q)||a.name.localeCompare(b.name,'es'));
   results.replaceChildren();
   const status=document.createElement('p');status.textContent=matches.length===0?'No encontramos ese nombre. Consulta el listado de tu provincia o escríbenos la localidad.':`${matches.length} ${matches.length===1?'municipio encontrado':'municipios encontrados'}${matches.length>12?'. Mostramos los 12 primeros; escribe más letras para afinar.':'.'}`;results.append(status);
   for(const row of matches.slice(0,12)){
    const link=document.createElement('a');link.href=row.url;
    const title=document.createElement('strong');title.textContent=row.name+' ↗';
    const detail=document.createElement('span');detail.textContent=`${row.province} · zona de ${row.zone}`;
    link.append(title,detail);results.append(link);
   }
  }catch{
   if(current===revision)results.textContent='No se ha podido cargar el buscador. Los listados completos siguen disponibles en las provincias de abajo.';
  }
 });
}
const provinceSearch=document.querySelector('#province-search');
if(provinceSearch)provinceSearch.addEventListener('input',()=>{
 const q=normalize(provinceSearch.value);let count=0;
 document.querySelectorAll('.coverage-group').forEach(group=>{
  let inGroup=0;
  group.querySelectorAll('.municipality-links a').forEach(link=>{
   const match=!q||normalize(link.textContent).includes(q);
   link.hidden=!match;if(match){inGroup++;count++}
  });
  group.hidden=inGroup===0;if(q&&inGroup)group.open=true;
 });
 document.querySelector('#directory-status').textContent=q?(count?`${count} ${count===1?'municipio encontrado':'municipios encontrados'}.`:'No encontramos ese nombre. Puedes consultar la localidad por teléfono o WhatsApp.'):'';
});
