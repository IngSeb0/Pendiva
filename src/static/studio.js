/* A constrained, reviewable customization flow and explicitly approved media analysis. */
(() => {
  'use strict';
  const lang = () => document.documentElement.lang === 'en' ? 'en' : 'es';
  const t = (es,en) => lang() === 'en' ? en : es;
  let messagesForBuilder = [], proposed = null, importContent = '', detailHeading = null, lastLanguage = '';
  const studio = document.createElement('section'); studio.className = 'panel studio';
  document.querySelector('#page-improvements').appendChild(studio);
  function renderStudio() {
    const draft = studio.querySelector('#builder-input')?.value || '';
    studio.innerHTML = `<div class="head">✦ ${t('Crea una herramienta para tu negocio','Create a tool for your business')}</div><div class="studio-body">
      <p class="fresh">${t('Cuéntale a Pendiva lo que necesitas. Te hará preguntas y propondrá una vista para revisar.','Tell Pendiva what you need. It will ask questions and propose a view for review.')}</p>
      <p class="fresh">${t('Puedes crear listas de seguimiento, datos faltantes o servicios por confirmar. No envía mensajes ni ejecuta código.','You can create follow-up, missing details or service confirmation lists. No messages or code will be executed.')}</p>
      <div class="preset-grid" aria-label="${t('Ideas listas para revisar','Ready-to-review ideas')}">
        <button type="button" class="preset" data-preset="follow_up"><strong>${t('Cotizaciones sin seguimiento','Quotes needing follow-up')}</strong><span>${t('Requiere etapa y fecha de envío.','Requires the stage and quote date.')}</span></button>
        <button type="button" class="preset" data-preset="missing_info"><strong>${t('Datos por completar','Missing customer details')}</strong><span>${t('Revisa servicio y ubicación de cada ficha.','Checks service and location in customer cards.')}</span></button>
        <button type="button" class="preset" data-preset="appointments"><strong>${t('Servicios por confirmar','Services to confirm')}</strong><span>${t('Requiere marcar la etapa en la ficha.','Requires marking the stage in the customer card.')}</span></button>
      </div>
      <div id="builder-chat" class="builder-chat" aria-live="polite"></div>
      <form id="builder-form"><label for="builder-input">${t('¿Qué quieres crear?','What would you like to create?')}</label><textarea id="builder-input" maxlength="1000" placeholder="${t('Ejemplo: quiero seguir cotizaciones después de dos días','Example: follow up on quotes after two days')}"></textarea>
      <label class="consent"><input id="builder-consent" type="checkbox">${t('Acepto enviar esta conversación de configuración a Meta. Puede consumir créditos.','I agree to send this configuration conversation to Meta. This may use credits.')}</label>
      <div class="toolbar"><button class="action" type="submit">${t('Preguntar a Pendiva','Ask Pendiva')}</button><button type="button" id="builder-reset" class="secondary">${t('Empezar de nuevo','Start over')}</button></div></form>
      <p class="error" id="builder-error" role="status"></p><div id="builder-preview"></div>
      <details class="data-import"><summary>${t('Cargar fechas de cotización desde CSV','Import quote dates from CSV')}</summary><p class="fresh">${t('Columnas exactas: sender,quote_date. Usa el número de una conversación existente y fechas AAAA-MM-DD. La etapa se confirma en la ficha.','Exact columns: sender,quote_date. Use an existing conversation number and YYYY-MM-DD dates. Confirm the stage in the customer card.')}</p><input id="quote-file" type="file" accept=".csv,text/csv"><button type="button" class="secondary" id="quote-preview">${t('Revisar archivo','Review file')}</button><div id="quote-result" role="status"></div></details>
      <div class="studio-views"><h3>${t('Herramientas activas','Active tools')}</h3><div id="views-list"></div></div></div>`;
    const input = studio.querySelector('#builder-input'); input.value = draft;
    studio.querySelectorAll('[data-preset]').forEach(button=>button.onclick=()=>{const template=button.dataset.preset;const names={follow_up:t('Seguimiento después de 2 días','Follow up after 2 days'),missing_info:t('Datos por completar','Missing customer details'),appointments:t('Servicios por confirmar','Services to confirm')};proposed={name:names[template],template,days:2};paintProposal();studio.querySelector('#builder-preview').scrollIntoView({block:'nearest'});});
    paintConversation(); paintProposal(); loadViews();
    studio.querySelector('#builder-form').onsubmit = async event => {
      event.preventDefault(); const error = studio.querySelector('#builder-error'), question = input.value.trim();
      if (!question) { error.textContent = t('Escribe qué necesitas.','Describe what you need.'); return; }
      if (!studio.querySelector('#builder-consent').checked) { error.textContent = t('Confirma el envío a Meta.','Confirm sending to Meta.'); return; }
      const button = event.submitter; button.disabled = true; error.textContent = t('Pendiva está preparando una propuesta…','Pendiva is preparing a proposal…');
      const requestMessages = [...messagesForBuilder, {role:'user', text:question}];
      try {
        const result = await post('/api/custom-views/propose',{messages:requestMessages,language:lang(),consent_to_send_to_meta:true});
        messagesForBuilder = [...requestMessages,{role:'assistant',text:result.message}]; input.value = ''; proposed = result.status === 'ready' ? result.config : null;
        paintConversation(); await paintProposal(); error.textContent = '';
      } catch (e) { error.textContent = e.message || t('No se pudo crear la propuesta.','Could not create a proposal.'); }
      finally { button.disabled = false; }
    };
    studio.querySelector('#builder-reset').onclick = () => { messagesForBuilder = []; proposed = null; input.value = ''; paintConversation(); paintProposal(); };
    studio.querySelector('#quote-preview').onclick = async () => {
      const file = studio.querySelector('#quote-file').files[0], target = studio.querySelector('#quote-result');
      if (!file) { target.textContent=t('Selecciona un CSV.','Select a CSV file.'); return; }
      if (file.size > 200000) { target.textContent=t('El archivo supera el límite de 200 KB.','The file exceeds 200 KB.'); return; }
      importContent = await file.text();
      try { const result = await post('/api/custom-views/import',{content:importContent,commit:false});
        target.textContent = t('Filas válidas: ','Valid rows: ') + result.rows.length + '. ' + t('Revisa el archivo antes de importar.','Review the file before importing.');
        const button = document.createElement('button'); button.type='button'; button.className='secondary'; button.textContent=t('Confirmar importación','Confirm import'); target.append(' ',button);
        button.onclick = async () => { button.disabled=true; try { const saved=await post('/api/custom-views/import',{content:importContent,commit:true}); target.textContent=t('Fechas cargadas: ','Dates imported: ')+saved.rows.length+'. '+t('Confirma la etapa en cada ficha.','Confirm each stage in the customer card.'); await paintProposal(); await loadViews(); } catch(e) { target.textContent=e.message; } };
      } catch(e) { target.textContent=e.message; }
    };
  }
  function paintConversation() {
    const box=studio.querySelector('#builder-chat'); box.replaceChildren();
    for (const item of messagesForBuilder) { const p=document.createElement('p'); p.className=item.role==='user'?'builder-user':'builder-answer'; p.textContent=(item.role==='user'?t('Tú: ','You: '):'Pendiva: ')+item.text; box.appendChild(p); }
  }
  function viewDescription(config) {
    if (config.template==='follow_up') return t('Cotizaciones marcadas como enviadas hace al menos ','Quotes marked as sent at least ')+config.days+t(' días. Usa la fecha registrada por el usuario.',' days ago. Uses the user-entered date.');
    if (config.template==='missing_info') return t('Conversaciones sin servicio o ubicación en la ficha.','Conversations missing a service or location in the customer card.');
    return t('Fichas marcadas como servicio por confirmar.','Cards marked as service to confirm.');
  }
  function renderRows(target, result) {
    target.replaceChildren(); const summary=document.createElement('p'); summary.className='fresh';
    summary.textContent=t('Conversaciones revisadas: ','Conversations checked: ')+result.conversations_checked+'. '+t('Fuente: ficha registrada por el usuario.','Source: user-entered customer card.'); target.appendChild(summary);
    if (!result.rows.length) { const empty=document.createElement('p'); empty.textContent=t('No hay resultados con estos datos.','No results with the current data.'); target.appendChild(empty); }
    for (const row of result.rows) { const line=document.createElement('div'); line.className='view-row'; const description=document.createElement('span'); const fieldNames={service:t('servicio','service'),location:t('ubicación','location')}; description.textContent=[row.name||row.sender,row.service||t('Servicio sin registrar','Service not recorded'),row.responsible?t('Responsable: ','Responsible: ')+row.responsible:'',row.quote_date||'',row.days_elapsed!==undefined?row.days_elapsed+t(' días',' days'):'',row.missing_fields? t('Falta: ','Missing: ')+row.missing_fields.map(field=>fieldNames[field]||field).join(', '):''].filter(Boolean).join(' · ');line.appendChild(description);const open=document.createElement('button');open.type='button';open.className='secondary';open.textContent=t('Abrir cliente','Open customer');open.onclick=()=>{window.pendivaShowPage('customers');resetCustomerFilters();const match=Array.from(document.querySelectorAll('#list [data-sender]')).find(button=>button.dataset.sender===row.sender);if(match)match.click()};line.appendChild(open);target.appendChild(line); }
    if (result.missing.length) { const missing=document.createElement('p'); missing.className='alert'; missing.textContent=t('Falta la fecha de cotización en ','Quote date is missing for ')+result.missing.map(x=>x.name||x.sender).join(', ')+'. '+t('Completa la ficha o importa un CSV antes de calcular el seguimiento.','Complete the card or import a CSV before calculating follow-up.'); target.appendChild(missing); }
  }
  async function paintProposal() {
    const target=studio.querySelector('#builder-preview'); if (!target) return; target.replaceChildren(); if (!proposed) return;
    const title=document.createElement('h3'); title.textContent=t('Vista previa: ','Preview: ')+proposed.name; target.appendChild(title);
    const desc=document.createElement('p'); desc.textContent=viewDescription(proposed); target.appendChild(desc);
    const need=document.createElement('p');need.className='fresh';need.textContent=proposed.template==='follow_up'?t('Necesita fichas marcadas como cotización enviada y una fecha de envío.','Requires cards marked as quote sent and a send date.'):proposed.template==='missing_info'?t('Usa el servicio y la ubicación registrados en la ficha.','Uses service and location recorded in the customer card.'):t('Usa fichas marcadas como servicio por confirmar.','Uses cards marked as service to confirm.');target.appendChild(need);
    const data=document.createElement('div'); target.appendChild(data);
    try { const result=await post('/api/custom-views/preview',{config:proposed}); if (!target.isConnected) return; renderRows(data,result); }
    catch(e) { data.textContent=e.message; return; }
    const button=document.createElement('button'); button.type='button'; button.className='action'; button.textContent=t('Activar esta herramienta','Activate this tool'); target.appendChild(button);
    button.onclick=async()=>{button.disabled=true;try{await post('/api/custom-views/activate',{config:proposed});proposed=null;target.textContent=t('Herramienta activada.','Tool activated.');await loadViews()}catch(e){data.textContent=e.message;button.disabled=false}};
  }
  async function loadViews() {
    const list=studio.querySelector('#views-list'); if (!list) return;
    try {
      const views=await get('/api/custom-views'); if (!list.isConnected) return; list.replaceChildren();
      if(!views.length){list.textContent=t('Todavía no hay herramientas activas.','No active tools yet.');return}
      for(const view of views){
        const card=document.createElement('article'); card.className='custom-view'; const heading=document.createElement('h4'); heading.textContent=view.id==='dddddddddddddddddddddddddddddddd' ? t('Datos por completar · ejemplo','Missing details · example') : view.config.name; card.appendChild(heading);
        const desc=document.createElement('p'); desc.className='fresh'; desc.textContent=viewDescription(view.config); card.appendChild(desc);
        const run=document.createElement('button'); run.type='button'; run.className='action'; run.textContent=t('Ejecutar herramienta','Run tool');card.appendChild(run);
        const disable=document.createElement('button'); disable.type='button'; disable.className='secondary'; disable.textContent=t('Desactivar','Deactivate'); card.append(' ',disable);
        const content=document.createElement('div'); content.setAttribute('role','status'); card.appendChild(content);
        run.onclick=async()=>{run.disabled=true;try{renderRows(content,await get('/api/custom-views/'+view.id))}catch(e){content.textContent=e.message}finally{run.disabled=false}};
        disable.onclick=async()=>{disable.disabled=true;try{await post('/api/custom-views/deactivate',{id:view.id});await loadViews()}catch(e){content.textContent=e.message;disable.disabled=false}}; list.appendChild(card);
      }
    }catch(e){list.textContent=e.message}
  }
  async function mediaPanel() {
    const detail=document.querySelector('#detail'), heading=detail.querySelector('h2');
    if(!heading || !selected || detail.querySelector('.media-studio')) return;
    detailHeading=heading; const sender=selected, box=document.createElement('section'); box.className='media-studio';
    box.innerHTML=`<h3>${t('Archivos de esta conversación','Conversation files')}</h3><p class="fresh">${t('Añade PNG, JPG, MP4, audio OGG o WAV PCM mono de 16 bits a 16/24 kHz; máximo 4 MB. Audio OGG: se analizan como máximo los primeros 60 segundos.','Add PNG, JPG, MP4, OGG audio or mono 16-bit PCM WAV at 16/24 kHz; up to 4 MB. OGG audio: at most the first 60 seconds are analyzed.')}</p><p class="fresh">${t('Guardar conserva el archivo en este equipo. Analizar lo envía a Meta solo con tu confirmación.','Saving stores the file on this device. Analysis sends it to Meta only with your confirmation.')}</p><label>${t('Elegir archivo','Choose file')} <input class="media-file" type="file" accept="image/png,image/jpeg,video/mp4,audio/wav,audio/ogg"></label><button type="button" class="secondary media-upload">${t('Guardar archivo','Save file')}</button><p class="error media-error" role="status"></p><div class="whatsapp-media"></div><div class="media-list"></div>`;
    (detail.querySelector('#customer-brief') || heading).after(box); const error=box.querySelector('.media-error');
    async function refreshMedia(){
      const list=box.querySelector('.media-list'); const assets=await get('/api/conversations/'+sender+'/media'); const pending=await get('/api/conversations/'+sender+'/whatsapp-media'); if(!box.isConnected)return; list.replaceChildren();
      const waiting=box.querySelector('.whatsapp-media');waiting.replaceChildren();
      for(const item of pending){const row=document.createElement('p');row.className='alert';row.append(document.createTextNode(t('WhatsApp recibió un archivo: ','WhatsApp received a file: ')+item.kind+' · '+new Date(item.timestamp*1000).toLocaleString(lang()==='en'?'en-US':'es-CO')+' '));const button=document.createElement('button');button.type='button';button.className='secondary';button.textContent=t('Descargar de WhatsApp','Download from WhatsApp');row.appendChild(button);button.onclick=async()=>{button.disabled=true;error.textContent=t('Descargando desde WhatsApp…','Downloading from WhatsApp…');try{await post('/api/media/fetch',{sender,message_id:item.message_id,consent_to_download:true});error.textContent='';await refreshMedia()}catch(e){error.textContent=e.message;button.disabled=false}};waiting.appendChild(row)}
      if(!assets.length){list.textContent=t('No hay archivos añadidos.','No files added.');return}
      for(const asset of assets){const item=document.createElement('article');item.className='media-item';
        const link=document.createElement('a');link.href='/api/media/'+asset.id+'/content';link.target='_blank';link.rel='noopener';link.textContent=asset.name;item.appendChild(link);
        const type=document.createElement('span');type.className='fresh';type.textContent=' · '+asset.mime;item.appendChild(type);
        const visual=document.createElement(asset.mime.startsWith('image/')?'img':asset.mime.startsWith('video/')?'video':'audio');visual.src=link.href;visual.className='media-preview';if(visual.tagName==='IMG'){visual.alt=t('Imagen adjunta: ','Attached image: ')+asset.name;visual.loading='lazy'}else{visual.controls=true;visual.preload='none'}item.appendChild(visual);
        if(asset.result){const result=document.createElement('p');result.className='media-result';result.textContent=t('Observación o transcripción de IA (revisar): ','AI observation or transcript (review): ')+asset.result;item.appendChild(result)}
        const consent=document.createElement('label');consent.className='consent';const check=document.createElement('input');check.type='checkbox';consent.append(check,document.createTextNode(t('Acepto enviar este archivo a Meta para analizarlo. Puede consumir créditos.','I agree to send this file to Meta for analysis. This may use credits.')));item.appendChild(consent);
        const button=document.createElement('button');button.type='button';button.className='secondary';button.textContent=t('Analizar con Pendiva','Analyze with Pendiva');item.appendChild(button);
        button.onclick=async()=>{if(!check.checked){error.textContent=t('Confirma el envío a Meta.','Confirm sending to Meta.');return}button.disabled=true;error.textContent=t('Analizando archivo…','Analyzing file…');try{await post('/api/media/analyze',{id:asset.id,language:lang(),consent_to_send_to_meta:true});error.textContent='';await refreshMedia()}catch(e){error.textContent=e.message;button.disabled=false}};
        const remove=document.createElement('button');remove.type='button';remove.className='secondary';remove.textContent=t('Eliminar archivo local','Delete local file');remove.onclick=async()=>{if(!window.confirm(t('¿Eliminar el archivo y su análisis? Las respuestas anteriores del asistente no se borrarán.','Delete the file and its analysis? Previous assistant answers will remain.')))return;remove.disabled=true;try{await post('/api/media/delete',{id:asset.id});await refreshMedia()}catch(e){error.textContent=e.message;remove.disabled=false}};item.append(' ',remove);
        list.appendChild(item);
      }
    }
    box.querySelector('.media-upload').onclick=async()=>{
      const file=box.querySelector('.media-file').files[0];if(!file){error.textContent=t('Selecciona un archivo.','Select a file.');return}if(file.size>4*1024*1024){error.textContent=t('El archivo supera 4 MB.','The file exceeds 4 MB.');return}
      const mime=file.type==='audio/x-wav'?'audio/wav':file.type;
      try{const data=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(String(reader.result).split(',')[1]);reader.onerror=reject;reader.readAsDataURL(file)});await post('/api/media/upload',{sender,name:file.name,mime,content:data});error.textContent=t('Archivo guardado.','File saved.');await refreshMedia()}catch(e){error.textContent=e.message||t('No se pudo guardar.','Could not save.')}
    };
    try{await refreshMedia()}catch(e){error.textContent=e.message}
  }
  const observer=new MutationObserver(()=>{const heading=document.querySelector('#detail h2');if(heading&&heading!==detailHeading)mediaPanel();if(lang()!==lastLanguage){lastLanguage=lang();renderStudio();const old=document.querySelector('.media-studio');if(old)old.remove();detailHeading=null;mediaPanel()}});
  observer.observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['lang']});
  lastLanguage=lang();renderStudio();mediaPanel();
})();
