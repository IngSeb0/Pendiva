/* Presentation preferences stay on this device. Customer content is never translated. */
(() => {
  'use strict';
  const pref = (key, fallback) => { try { return localStorage.getItem(key) || fallback; } catch (_) { return fallback; } };
  const save = (key, value) => { try { localStorage.setItem(key, value); } catch (_) {} };
  let language = pref('pendiva-language', 'es') === 'en' ? 'en' : 'es';
  let theme = pref('pendiva-theme', 'light') === 'dark' ? 'dark' : 'light';
  const tr = (es, en) => language === 'en' ? en : es;
  const dict = {
    'Acceso a Pendiva':'Sign in to Pendiva','Ingresa tus credenciales de empresa.':'Enter your business credentials.', 'Entrar':'Sign in','Correo':'Email','Contraseña':'Password',
    'WhatsApp · entorno de prueba':'WhatsApp · test environment','Qué necesita tu atención.':'What needs your attention.',
    'Conversaciones y recomendaciones para tu negocio, con evidencia para decidir.':'Conversations and recommendations for your business, grounded in evidence.',
    'Tu asistente de negocio':'Your business assistant','Pregunta por tus conversaciones y descubre qué necesita atención.':'Ask about your conversations and discover what needs attention.',
    'Respuestas con evidencia':'Evidence-backed answers','Prueba una pregunta':'Try a question','¿Qué cotizaciones necesitan atención?':'Which quotes need attention?',
    '¿Qué datos faltan para cotizar?':'What details are missing from quotes?','¿Qué debería revisar primero?':'What should I review first?',
    'Las respuestas utilizan una selección de mensajes recibidos. El historial anterior y los mensajes salientes pueden no estar disponibles.':'Answers use a selection of received messages. Earlier history and outgoing messages may not be available.',
    'Tu negocio, en contexto.':'Your business, in context.','Pregunta por pendientes, cotizaciones o información que falta para atender mejor.':'Ask about pending work, quotes, or information needed to serve customers.',
    'Escribe o dicta tu pregunta':'Type or dictate your question','Dictado:':'Dictation:','Reconocimiento del navegador':'Browser recognition','Motor del asistente:':'Assistant provider:',
    'El navegador puede enviar el audio al servicio que reconoce la voz. Pendiva recibe la transcripción y prepara una respuesta.':'Your browser may send audio to its speech-recognition service. Pendiva receives the transcript and prepares an answer.',
    'Para responder, Pendiva enviará tu pregunta, contexto del negocio, hasta 36 fragmentos relevantes y las últimas 3 preguntas al servicio de IA de Meta. Puede consumir créditos. No envía toda la base de datos.':'To answer, Pendiva sends your question, business context, up to 36 relevant saved-message excerpts, and the last 3 questions to Meta AI. This may use credits. It does not send the full database.',
    'Confirmo enviar mi grabación a ElevenLabs para transcribirla.':'I agree to send my recording to ElevenLabs for transcription.',
    '🎙 Dictar':'🎙 Dictate','Preguntar a Pendiva':'Ask Pendiva','▶ Voz ElevenLabs':'▶ ElevenLabs voice',
    'Confirmo enviar la respuesta a ElevenLabs para generar voz. Puede consumir créditos.':'I agree to send the answer to ElevenLabs for speech. This may use credits.',
    'Configura el contexto de tu negocio':'Configure your business','Pendiva guarda estos datos y los usa como contexto en preguntas con IA, sólo después de tu consentimiento.':'Pendiva saves these details and uses them as context for AI questions only after you consent.',
    'Nombre del negocio':'Business name','Sector':'Industry','Servicios o productos':'Services or products','Horarios':'Business hours','Objetivos del negocio':'Business goals','Zonas de cobertura':'Service areas','Tarifas de referencia':'Reference rates','Políticas y condiciones':'Policies and conditions','Guardar contexto':'Save business details',
    'Ventas y gastos del dueño':'Sales and expenses','Importar archivo':'Import file','Conversaciones recibidas':'Conversations received','Recomendaciones pendientes':'Pending recommendations','Recomendaciones completadas':'Completed recommendations',
    'Vista del dueño · últimos 7 días':'Owner overview · last 7 days','Qué necesita atención ahora':'What needs attention now','Cargando resumen…':'Loading overview…','Cargando prioridades…':'Loading priorities…',
    'Actualizar':'Refresh','Mensajes entrantes recibidos desde la conexión. Archivos, audios, historial previo y salientes pueden no estar disponibles.':'Incoming messages received through the connection. Files, audio, previous history and outgoing messages may not be available.',
    'Conversaciones':'Conversations','Detalle y recomendaciones':'Details and recommendations','Selecciona una conversación.':'Select a conversation.','Cargando…':'Loading…',
    'Las recomendaciones son sugerencias para revisión humana. Los datos se guardan en este equipo; este panel no está preparado para acceso público.':'Recommendations require human review. Data is stored on this device; this dashboard is not ready for public access.',
    'No hay recomendaciones pendientes con análisis vigente.':'There are no pending recommendations with a current analysis.',
    'Aún no hay conversaciones.':'No conversations yet.','No hay resultados para esa búsqueda.':'No results for that search.',
    'Configura el webhook y envía un mensaje desde un teléfono autorizado. Los mensajes recibidos aparecerán aquí.':'Configure the webhook and send a message from an authorized phone. Received messages will appear here.',
    'Mensajes recibidos':'Messages received','Análisis vigentes':'Current analyses','Pendientes':'Pending',
    'No se detectaron alertas con estas reglas. Esto no sustituye un análisis contable.':'No alerts were detected by these rules. This is not an accounting analysis.',
    'Aún no hay datos financieros importados.':'No financial data has been imported yet.','Evidencia':'Evidence','Nota o corrección':'Note or correction',
    'Completar':'Complete','Descartar':'Dismiss','Dejar pendiente':'Keep pending','Motor':'Provider','Analizar con':'Analyze with',
    'La llamada puede consumir créditos.':'This request may use credits.','Esta conversación aún no tiene un análisis de IA.':'This conversation has not been analyzed yet.',
    'Sin evidencia disponible; revisa este análisis anterior.':'Evidence unavailable; review this earlier analysis.',
    'No hay recomendaciones con evidencia suficiente.':'There are no recommendations with sufficient evidence.',
    'La conversación o el contexto del negocio cambió. Vuelve a analizar antes de actualizar recomendaciones.':'The conversation or business context changed. Analyze again before updating recommendations.',
    'credenciales configuradas':'credentials configured','configuración pendiente':'configuration needed','Claves de IA:':'AI keys:', 'Estado de servicios:':'Service status:','No comprobado':'Not checked',
    'Esperando la primera recepción con firma válida. Tener credenciales configuradas no comprueba la conexión.':'Waiting for the first signed delivery. Configured credentials do not prove connectivity.',
    'Voz del navegador disponible según tu dispositivo. Para ElevenLabs configura una clave; su plan gratuito es para uso no comercial.':'Browser voice depends on your device. Configure a key for ElevenLabs; its free plan is for non-commercial use.',
    'La voz de ElevenLabs envía el texto a ese proveedor y usa créditos.':'ElevenLabs sends text to the provider and uses credits.',
    'La respuesta se reproduce con la voz del navegador, según el dispositivo.':'The answer plays using the browser voice, depending on your device.',
    'Qué hacer:':'Next step:','alta':'high','media':'medium','baja':'low','Pendiente':'Pending','Completada':'Completed','Descartada':'Dismissed',
    'Faltan datos':'Missing details','Negociación':'Negotiation','Pago por verificar':'Payment to verify','Cita por confirmar':'Appointment to confirm','Cotización enviada':'Quote sent',
    'Falta configurar una clave de IA.':'Configure an AI key.','Confirmo que puedo enviar estos mensajes y el contexto del negocio a':'I agree to send these messages and the business context to',
    'para analizarlos.':'for analysis.','Importa un CSV exportado desde Excel con columnas':'Import a CSV exported from Excel with columns',
    '. Usa tipo':'. Use type','o':'or','; los datos se analizan localmente.':'; the data is analyzed locally.',
    'Las ventas bajaron frente al mes anterior':'Sales decreased compared with the previous month',
    'Confirma primero que puedes enviar estos datos al proveedor indicado.':'First confirm that you can send this data to the selected provider.',
    'Analizando con el proveedor seleccionado…':'Analyzing with the selected provider…',
    'Guardado en este equipo.':'Saved on this device.','Importando…':'Importing…','Archivo importado localmente.':'File imported locally.',
    'Escribe o dicta una pregunta.':'Type or dictate a question.','Confirma primero el envío al proveedor de IA.':'First confirm sending to the AI provider.',
    'Configura primero la clave del proveedor de IA.':'First configure an AI provider key.','Revisando conversaciones y preparando una respuesta…':'Reviewing conversations and preparing an answer…',
    'Respuesta lista para revisar.':'Answer ready to review.','No se pudo abrir la conversación.':'Could not open the conversation.',
    'Confirma primero el envío de tu audio a ElevenLabs.':'First confirm sending your audio to ElevenLabs.',
    'Este navegador no permite grabar audio. Escribe tu pregunta o usa otro navegador.':'This browser cannot record audio. Type your question or use another browser.',
    'Transcribiendo con ElevenLabs…':'Transcribing with ElevenLabs…','Revisa la transcripción y envía tu pregunta.':'Review the transcript and submit your question.',
    '■ Detener dictado':'■ Stop recording','Grabando hasta 15 segundos; pulsa detener cuando termines.':'Recording for up to 15 seconds; press stop when finished.',
    'No se pudo iniciar el micrófono. Revisa sus permisos o escribe tu pregunta.':'Could not start the microphone. Check permissions or type your question.',
    'Este navegador no ofrece dictado. Puedes escribir tu pregunta o usar ElevenLabs si lo configuras.':'This browser does not support dictation. Type your question or configure ElevenLabs.',
    'Escuchando…':'Listening…','No se pudo usar el micrófono o el reconocimiento. Revisa los permisos o escribe tu pregunta.':'Microphone or recognition unavailable. Check permissions or type your question.',
    'No se reconoció voz; intenta de nuevo.':'No speech recognized; try again.','No se pudo iniciar el dictado.':'Could not start dictation.',
    'Primero haz una pregunta para escuchar la respuesta.':'Ask a question first to hear the answer.','Tu navegador no ofrece voz del dispositivo.':'Your browser does not provide device speech.',
    'No se pudo reproducir la voz del dispositivo.':'Could not play device speech.','Primero haz una pregunta.':'Ask a question first.',
    'Confirma primero el envío de la respuesta a ElevenLabs.':'First confirm sending the answer to ElevenLabs.',
    'La respuesta supera el límite de ElevenLabs de esta demo; usa la voz del navegador.':'The answer exceeds this demo’s ElevenLabs limit; use browser speech.',
    'Generando voz…':'Generating speech…','Voz generada con ElevenLabs.':'Speech generated with ElevenLabs.',
    'No se pudo cargar el contexto.':'Could not load business context.','No se pudo cargar el historial del asistente.':'Could not load assistant history.',
    'Configura tu empresa':'Set up your business','Crea la cuenta inicial. Este paso sólo se permite una vez.':'Create the first account. This setup is available only once.',
    'Contraseña (mínimo 12 caracteres)':'Password (at least 12 characters)','Crear cuenta':'Create account',
    'Empresa creada. Inicia sesión para continuar.':'Business created. Sign in to continue.'
  };
  const placeholders = {'Correo':'Email','Buscar nombre, número o mensaje':'Search name, number or message','Por ejemplo: ¿qué información falta para preparar las cotizaciones?':'For example: what information is missing to prepare the quotes?','Añade una nota de revisión':'Add a review note'};
  const originals = new WeakMap();
  function translate() {
    document.documentElement.lang = language;
    document.documentElement.dataset.theme = theme;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode, parent = node.parentElement;
      if (!parent || parent.closest('script,style,.badge,.message,.evidence,.chat-turn,.case,.workflow,.opportunity-panel,.decision-brief,.demo-guide,.header-controls,.studio,.media-studio,.workspace-nav,.workspace-heading,.assistant-launcher,.assistant-close,.assistant-output,.assistant-options summary,.customer-filters,.voice-stage')) continue;
      if (!originals.has(node)) originals.set(node, node.nodeValue);
      const original = originals.get(node), trimmed = original.trim();
      let value = language === 'en' && dict[trimmed] ? original.replace(trimmed, dict[trimmed]) : original;
      if (language === 'en' && parent.matches('#detail > .muted')) value = value.replace(' mensajes recibidos', ' messages received');
      if (language === 'en' && parent.matches('.analysis > h3')) value = value.replace('Análisis de ', 'Analysis by ');
      if (language === 'en' && parent.matches('.analysis > p.fresh')) value = value.replace('Incertidumbre:', 'Uncertainty:').replace('No indicada', 'Not provided');
      if (language === 'en' && parent.closest('#summary, #finance-result, .priority-meta, .counter')) {
        const fragments = [['Pendientes por prioridad:', 'Pending by priority:'], [' alta', ' high'], [' media', ' medium'], [' baja', ' low'], ['No hay datos suficientes para afirmar ingresos, conversiones o rentabilidad.', 'There is not enough data to establish revenue, conversions or profitability.'], ['La cobertura incluye sólo mensajes entrantes del webhook firmado; no implica historial completo ni mensajes salientes.', 'Coverage includes only incoming signed webhook messages; full history and outgoing messages are not guaranteed.'], ['Ventas:', 'Sales:'], ['Gastos:', 'Expenses:'], ['Resultado:', 'Result:'], ['Registros:', 'Records:'], ['Faltan datos', 'Missing details'], ['Negociación', 'Negotiation'], ['Pago por verificar', 'Payment to verify'], ['Cita por confirmar', 'Appointment to confirm'], ['Cotización enviada', 'Quote sent'], ['Prioridad', 'Priority'], ['Pendiente', 'Pending'], ['Completada', 'Completed'], ['Descartada', 'Dismissed']];
        for (const [from, to] of fragments) value = value.replaceAll(from, to);
      }
      if (node.nodeValue !== value) node.nodeValue = value;
    }
    document.querySelectorAll('[placeholder]').forEach(el => {
      if (!el.dataset.originalPlaceholder) el.dataset.originalPlaceholder = el.getAttribute('placeholder');
      const original = el.dataset.originalPlaceholder;
      el.setAttribute('placeholder', language === 'en' && placeholders[original] ? placeholders[original] : original);
    });
    document.querySelectorAll('.lang-choice').forEach(el => { el.value = language; el.setAttribute('aria-label', tr('Idioma', 'Language')); });
    document.getElementById('search').setAttribute('aria-label', tr('Buscar conversaciones', 'Search conversations'));
    document.querySelector('.metrics').setAttribute('aria-label', tr('Resumen de datos recibidos', 'Received data overview'));
    document.querySelectorAll('.theme-choice').forEach(el => { const label = theme === 'dark' ? tr('☀ Claro','☀ Light') : tr('☾ Oscuro','☾ Dark'); if (el.textContent !== label) el.textContent = label; el.setAttribute('aria-label',tr('Cambiar apariencia','Change appearance')); });
    document.querySelectorAll('.prompt').forEach((button, i) => {
      const questions = language === 'en' ? ['Which quotes need attention and what is missing to respond?', 'What information do I need to quote my services?', 'Which conversations should I review first and why?', 'Analyze signals across all available conversations and compare them with imported sales and expenses. Summarize opportunities, risks, and missing data, stating how many conversations and records support each finding.'] : ['¿Qué cotizaciones necesitan atención y qué me falta para responder?', '¿Qué información necesito pedir para cotizar mis servicios?', '¿Qué conversaciones debería revisar primero y por qué?', 'Analiza las señales de todas las conversaciones disponibles y compáralas con las ventas y gastos importados. Resume oportunidades, riesgos y datos faltantes, indicando cuántas conversaciones y registros respaldan cada hallazgo.'];
      button.dataset.question = questions[i];
    });
    const badge = document.querySelector('.badge');
    const badgeText = typeof config !== 'undefined' && config.mode === 'demo' ? tr('Modo demo · incluye datos ficticios','Demo mode · includes fictional data') : tr('WhatsApp · entorno de prueba','WhatsApp · test environment');
    if (badge.textContent !== badgeText) badge.textContent = badgeText;
    const consent = document.getElementById('assistant-consent-label');
    const consentText = tr('Para responder, Pendiva enviará tu pregunta, el contexto del negocio, hasta 36 fragmentos relevantes y las últimas 3 preguntas al servicio de IA de Meta. Puede consumir créditos; no envía toda la base de datos.', 'To answer, Pendiva sends your question, business context, up to 36 relevant message excerpts, and the last 3 questions to Meta AI. This may use credits; it does not send the full database.');
    if (consent.textContent !== consentText) consent.textContent = consentText;
    updateWorkspaceLanguage();
    updateGuide(); updateSector();
  }
  function controls() {
    const wrapper = document.createElement('div'); wrapper.className = 'header-controls';
    wrapper.innerHTML = '<select class="lang-choice"><option value="es">Español</option><option value="en">English</option></select><button class="theme-choice" type="button"></button>';
    wrapper.querySelector('select').onchange = e => { language = e.target.value; save('pendiva-language', language); translate(); renderWorkflow(); renderOpportunities(); renderReplyDrafts(); updateOwnerOptions(); renderList(); renderCustomerBrief(); renderAssistant(); };
    wrapper.querySelector('button').onclick = () => { theme = theme === 'dark' ? 'light' : 'dark'; save('pendiva-theme', theme); translate(); };
    return wrapper;
  }
  document.querySelector('.top').appendChild(controls());
  document.querySelector('#login .auth-topline').appendChild(controls());
  document.querySelector('#bootstrap .auth-topline').appendChild(controls());
  const app = document.getElementById('app');
  const priorities = document.querySelector('.priorities');
  const guide = document.createElement('details'); guide.className = 'demo-guide';
  document.getElementById('activity').after(guide);
  guide.after(document.querySelector('.metrics')); document.querySelector('.metrics').after(priorities);
  priorities.after(document.querySelector('.owner-summary'));
  // Keep each task in its own workspace while retaining the existing data and handlers.
  const nav = document.createElement('nav'); nav.className = 'workspace-nav';
  nav.setAttribute('aria-label', 'Navegación principal');
  const sections = {};
  for (const id of ['home', 'customers', 'improvements', 'finance', 'settings']) {
    const section = document.createElement('section'); section.id = 'page-' + id; section.className = 'workspace-page';
    section.hidden = id !== 'home'; app.appendChild(section); sections[id] = section;
  }
  const navItems = [ ['home','⌂','Inicio','Overview'], ['customers','♙','Clientes','Customers'], ['improvements','✦','Mejoras','Tools'], ['finance','▥','Finanzas','Finances'], ['settings','⚙','Negocio','Business'] ];
  nav.innerHTML = navItems.map(([id, icon]) => `<button type="button" data-page="${id}"><span aria-hidden="true">${icon}</span><span class="nav-label"></span></button>`).join('');
  document.querySelector('.top').after(nav);
  function heading(page, titleEs, titleEn, descEs, descEn) {
    const el = document.createElement('div'); el.className = 'workspace-heading';
    el.dataset.titleEs = titleEs; el.dataset.titleEn = titleEn; el.dataset.descEs = descEs; el.dataset.descEn = descEn;
    el.innerHTML = '<h1></h1><p class="muted"></p>'; sections[page].appendChild(el);
  }
  heading('home','Tu negocio, en perspectiva.','Your business at a glance.','Prioriza lo que necesita atención hoy.','Prioritize what needs your attention today.');
  heading('customers','Tus clientes','Your customers','Consulta conversaciones, archivos y próximos pasos. Los mensajes y análisis conservan su idioma original.','Review conversations, files, and next steps. Messages and previous analyses stay in their original language.');
  heading('improvements','Herramientas para tu negocio','Tools for your business','Crea y ejecuta vistas útiles con tus datos.','Create and run useful views with your data.');
  heading('finance','Finanzas','Finances','Revisa los datos que importaste para tu negocio.','Review the data imported for your business.');
  heading('settings','Tu negocio','Your business','Configura el contexto y revisa el estado de la conexión.','Configure your business context and check your connection status.');
  // The original headline is replaced with page-specific titles.
  app.querySelector(':scope > h1').remove(); app.querySelector(':scope > p.muted').remove();
  sections.home.append(guide, document.querySelector('.metrics'), priorities, document.querySelector('.owner-summary'));
  const followups = document.createElement('section'); followups.className = 'panel followups';
  followups.innerHTML = '<div class="head"></div><p class="followups-note"></p><div class="followups-list" aria-live="polite"></div>';
  priorities.before(followups);
  let followupRows = [];
  function renderFollowups() {
    const signature=language+JSON.stringify(followupRows);
    if(followups.dataset.rendered===signature)return;
    followups.dataset.rendered=signature;
    followups.querySelector('.head').textContent=tr('Seguimientos registrados','Recorded follow-ups');
    followups.querySelector('.followups-note').textContent=tr('Fechas registradas por tu equipo, según la fecha de este dispositivo. Revisa el mensaje de respaldo antes de actuar.','Dates recorded by your team, based on this device’s date. Review the supporting message before acting.');
    const list=followups.querySelector('.followups-list'); list.replaceChildren();
    if(!followupRows.length){list.textContent=tr('No hay seguimientos abiertos. Añade una oportunidad en la ficha de un cliente.','No open follow-ups. Add an opportunity in a customer’s record.');return}
    const labels={overdue:tr('Fecha pasada','Past date'),today:tr('Hoy','Today'),upcoming:tr('Próximamente','Upcoming'),unscheduled:tr('Sin fecha','No date')};
    for(const row of followupRows){const button=document.createElement('button');button.type='button';button.className='followup-row';button.dataset.sender=row.sender;
      const title=document.createElement('strong');title.textContent=row.name+' · '+row.service_key;
      const status=document.createElement('span');status.className='followup-status';status.textContent=labels[row.timing]+(row.due_date?' · '+row.due_date:'');
      const action=document.createElement('span');action.textContent=row.next_action||tr('Sin próximo paso registrado','No next step recorded');button.append(title,status,action);list.appendChild(button)}
  }
  async function loadFollowups(){
    const now=new Date(), today=[now.getFullYear(),String(now.getMonth()+1).padStart(2,'0'),String(now.getDate()).padStart(2,'0')].join('-');
    try{followupRows=await get('/api/followups?today='+today);renderFollowups()}
    catch(_){followups.querySelector('.followups-list').textContent=tr('No se pudieron cargar los seguimientos.','Could not load follow-ups.')}
  }
  followups.addEventListener('click',async event=>{const button=event.target.closest('[data-sender]');if(!button)return;window.pendivaShowPage('customers');selected=button.dataset.sender;try{messages=(await get('/api/conversations/'+selected)).messages;renderList();renderDetail();document.getElementById('detail').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'})}catch(_){document.getElementById('detail').textContent=tr('No se pudo abrir el cliente.','Could not open customer.')}});
  new MutationObserver(()=>{if(!app.hidden)loadFollowups()}).observe(app,{attributes:true,attributeFilter:['hidden']});
  if(!app.hidden)loadFollowups();
  document.getElementById('refresh').addEventListener('click',loadFollowups);
  const refreshBar = document.getElementById('refresh').parentElement;
  sections.customers.append(refreshBar, document.querySelector('.grid'));
  const filters=document.createElement('div'); filters.className='customer-filters';
  document.getElementById('search').after(filters);
  filters.innerHTML='<label data-label="stage"><span></span><select id="filter-stage"></select></label><label data-label="priority"><span></span><select id="filter-priority"></select></label><label data-label="owner"><span></span><select id="filter-owner"></select></label><label data-label="sort"><span></span><select id="filter-sort"></select></label><div class="filter-footer"><span id="customer-count" aria-live="polite"></span><button type="button" class="filter-reset"></button></div>';
  filters.addEventListener('change',renderList); filters.querySelector('.filter-reset').onclick=resetCustomerFilters;
  function localizeFilters() {
    const labelValues={stage:tr('Etapa','Stage'),priority:tr('Prioridad','Priority'),owner:tr('Responsable','Owner'),sort:tr('Orden','Sort')};
    for(const [key,value] of Object.entries(labelValues)){const label=filters.querySelector(`[data-label="${key}"] span`);if(label.textContent!==value)label.textContent=value}
    const definitions={stage:[['',tr('Todas las etapas','All stages')],['new',tr('Consulta nueva','New inquiry')],['missing',tr('Faltan datos','Missing details')],['ready',tr('Lista para cotizar','Ready to quote')],['quoted',tr('Cotización enviada','Quote sent')],['scheduled',tr('Servicio por confirmar','Service to confirm')],['closed',tr('Cerrado','Closed')]],priority:[['',tr('Todas las prioridades','All priorities')],['alta',tr('Alta','High')],['media',tr('Media','Medium')],['baja',tr('Baja','Low')]],sort:[['priority',tr('Pendientes primero','Pending first')],['recent',tr('Más recientes','Most recent')]]};
    for(const [key,options] of Object.entries(definitions)){const select=filters.querySelector('#filter-'+key),value=select.value;const html=options.map(([id,text])=>`<option value="${id}">${text}</option>`).join('');if(select.innerHTML!==html){select.innerHTML=html;if(options.some(([id])=>id===value))select.value=value;}}
    const reset=filters.querySelector('.filter-reset'),label=tr('Limpiar filtros','Clear filters');if(reset.textContent!==label)reset.textContent=label;
  }
  sections.finance.append(document.querySelector('.finance'));
  sections.settings.append(document.getElementById('status'), document.getElementById('activity'), document.getElementById('business-details'));
  const help = app.querySelector(':scope > .help'); if (help) app.appendChild(help);
  window.pendivaShowPage = function(id) {
    if (!sections[id]) return;
    for (const [key, section] of Object.entries(sections)) section.hidden = key !== id;
    nav.querySelectorAll('button').forEach(button => { const active = button.dataset.page === id; button.classList.toggle('active', active); if (active) button.setAttribute('aria-current', 'page'); else button.removeAttribute('aria-current'); });
  };
  nav.addEventListener('click', event => { const button = event.target.closest('[data-page]'); if (button) window.pendivaShowPage(button.dataset.page); });
  priorities.addEventListener('click', event => { if (event.target.closest('[data-sender]')) window.pendivaShowPage('customers'); }, true);
  document.getElementById('assistant-history').addEventListener('click', event => { if (event.target.closest('[data-chat-sender]')) { window.pendivaShowPage('customers'); closeAssistant(); } }, true);
  window.pendivaShowPage('home');
  const assistant = document.querySelector('.assistant');
  assistant.classList.add('assistant-drawer'); assistant.hidden = true;
  assistant.setAttribute('role','dialog'); assistant.setAttribute('aria-modal','false');
  const close = document.createElement('button'); close.className='assistant-close'; close.type='button'; close.textContent='×';
  assistant.querySelector('.assistant-title').appendChild(close);
  const launcher = document.createElement('button'); launcher.type='button'; launcher.className='assistant-launcher'; launcher.setAttribute('aria-controls','assistant-panel'); launcher.setAttribute('aria-expanded','false'); assistant.id='assistant-panel';
  launcher.innerHTML='<span class="launcher-icon" aria-hidden="true">✦</span><span class="launcher-label"></span>';
  app.append(assistant, launcher);
  function closeAssistant() { assistant.hidden=true; stopAssistantVoice(); launcher.setAttribute('aria-expanded','false'); launcher.focus(); }
  close.onclick=closeAssistant;
  launcher.onclick=()=>{ assistant.hidden=false; launcher.setAttribute('aria-expanded','true'); document.getElementById('assistant-question').focus(); };
  assistant.addEventListener('keydown', event=>{if(event.key==='Escape') closeAssistant();});
  const voiceStage=document.createElement('div');voiceStage.className='voice-stage';voiceStage.dataset.state='idle';
  voiceStage.innerHTML='<div class="voice-orb" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></div><div class="voice-copy"><strong></strong><p role="status" aria-live="polite"></p><button type="button" class="voice-mode-toggle"></button><button type="button" class="voice-stop" hidden></button><small class="voice-privacy"></small></div>';
  voiceStage.querySelector('.voice-privacy').textContent=tr('El navegador puede enviar el audio a su servicio de reconocimiento. Pendiva recibe la transcripción y prepara una respuesta con IA.','Your browser may send audio to its speech-recognition service. Pendiva receives the transcript and prepares an AI answer.');
  assistant.querySelector('.assistant-title').after(voiceStage);
  voiceStage.querySelector('.voice-stop').onclick=()=>{voiceSession.stop();if(voiceConversationActive())window.pendivaResumeVoiceConversation?.()};
  window.pendivaRenderVoiceState=(state)=>{voiceStage.dataset.state=state;const labels={idle:[tr('Pendiva está lista','Pendiva is ready'),tr('Inicia y habla; tras 10 segundos de silencio, envío tu pregunta y respondo en voz alta.','Start speaking; after 10 seconds of silence, I send your question and speak back.')],listening:[tr('Te estoy escuchando','Listening to you'),tr('Habla con naturalidad. Al terminar, espero 10 segundos de silencio y envío tu pregunta.','Speak naturally. After you finish, I wait for 10 seconds of silence and send your question.')],waiting:[tr('Ya te escuché','I heard you'),tr('Enviaré tu pregunta tras 10 segundos de silencio. Sigue hablando para añadir más.','I’ll send after 10 seconds of silence. Keep speaking to add more.')],thinking:[tr('Un momento…','One moment…'),tr('Preparando la respuesta','Preparing a response')],speaking:[tr('Pendiva está hablando','Pendiva is speaking'),tr('Puedes interrumpir o terminar la conversación','Interrupt or end the conversation')],review:[tr('Revisa tu pregunta','Review your question'),tr('Confirma la transcripción antes de enviarla','Check the transcript before sending')]};const current=labels[state]||labels.idle;const title=voiceStage.querySelector('strong'),status=voiceStage.querySelector('p'),stop=voiceStage.querySelector('.voice-stop'),mode=voiceStage.querySelector('.voice-mode-toggle');if(title.textContent!==current[0])title.textContent=current[0];if(status.textContent!==current[1])status.textContent=current[1];stop.hidden=state!=='speaking';const stopLabel=tr('Detener voz','Stop voice'),modeLabel=voiceConversationActive()?tr('■ Terminar conversación','■ End voice conversation'):tr('● Iniciar conversación por voz','● Start voice conversation');if(stop.textContent!==stopLabel)stop.textContent=stopLabel;if(mode.textContent!==modeLabel)mode.textContent=modeLabel;mode.setAttribute('aria-pressed',String(voiceConversationActive()))};
  const voiceOptions = document.createElement('details'); voiceOptions.className='assistant-options';
  const voiceSummary=document.createElement('summary'); voiceOptions.appendChild(voiceSummary);
  const form=document.getElementById('assistant-form');
  const dictationLabel=form.querySelector('label[for="dictation-mode"]');
  const dictationHelp=dictationLabel.nextElementSibling;
  form.appendChild(voiceOptions);
  const legacyEleven=document.getElementById('eleven-consent').closest('label');legacyEleven.hidden=true;document.getElementById('speak-eleven').hidden=true;
  const legacyDictateButton=document.getElementById('dictate');
  if(legacyDictateButton)voiceOptions.append(legacyDictateButton);
  voiceOptions.append(dictationLabel,dictationHelp,document.getElementById('transcribe-consent-row'),document.getElementById('speak-eleven'),legacyEleven,document.getElementById('voice-help'),document.getElementById('voice-player'));
  function updateWorkspaceLanguage() {
    const setText = (el, value) => { if (el.textContent !== value) el.textContent = value; };
    nav.setAttribute('aria-label',tr('Navegación principal','Main navigation'));
    navItems.forEach(([id,,es,en]) => setText(nav.querySelector(`[data-page="${id}"] .nav-label`),tr(es,en)));
    document.querySelectorAll('.workspace-heading').forEach(el=>{setText(el.querySelector('h1'),tr(el.dataset.titleEs,el.dataset.titleEn));setText(el.querySelector('p'),tr(el.dataset.descEs,el.dataset.descEn))});
    setText(launcher.querySelector('.launcher-label'),tr('Pregúntale a Pendiva','Ask Pendiva'));
    launcher.setAttribute('aria-label',tr('Abrir asistente de Pendiva','Open Pendiva assistant'));
    close.setAttribute('aria-label',tr('Cerrar asistente','Close assistant'));
    document.querySelectorAll('.prompt[data-label-en]').forEach(button=>{if(!button.dataset.questionEs)button.dataset.questionEs=button.dataset.question;button.textContent=language==='en'?button.dataset.labelEn:button.dataset.labelEs;button.dataset.question=language==='en'?button.dataset.questionEn:button.dataset.questionEs});
    const financeHelp=document.getElementById('finance-import-help');
    if(financeHelp)financeHelp.innerHTML=language==='en'?'Import a CSV with columns <strong>date,type,amount,category</strong>; use <strong>sale</strong> or <strong>expense</strong>. Data is analyzed locally.':'Importa un CSV con columnas <strong>fecha,tipo,monto,categoria</strong>; usa <strong>venta</strong> o <strong>gasto</strong>. Los datos se analizan localmente.';
    setText(voiceSummary,tr('Opciones de voz','Voice options'));
    window.pendivaRenderVoiceState(voicePhase);
    setText(voiceStage.querySelector('.voice-privacy'),tr('El navegador puede enviar el audio a su servicio de reconocimiento. Pendiva recibe la transcripción y prepara una respuesta con IA.','Your browser may send audio to its speech-recognition service. Pendiva receives the transcript and prepares an AI answer.'));
    localizeFilters();
    renderFollowups();
    window.pendivaRenderDecisionBrief?.();
  }
  function updateGuide() {
    if (guide.dataset.lang === language) return;
    guide.dataset.lang = language;
    const open = guide.open;
    guide.innerHTML = language === 'en' ? '<summary>Demo guide · 3 minutes</summary><p>Use the long English fictional conversation. Check the AI consent before asking Pendiva; it sends your question, business context, and a bounded set of saved-message excerpts to Meta.</p><ol><li>Open Ana in Customers. Show the Decision Brief, its saved synthetic-example label, missing details, and source messages.</li><li>Open the editable reply draft without sending it, then use Ask Pendiva. Review its answer and cited evidence.</li><li>Show the coverage note and source count. Stop the voice session.</li><li>Open Sales and expenses and show the monthly chart. The figures are synthetic and the app does not track their currency.</li></ol><p>Demo customers and sales records are fictional. Do not present recommendations as verified payments, bookings, or customer contact.</p>' : '<summary>Guía de la demo · 3 minutos</summary><p>Usa el conjunto ficticio en español. Marca el consentimiento antes de preguntarle a Pendiva; la pregunta, el contexto y una selección limitada de mensajes se envían a Meta.</p><ol><li>Abre a Ana en Clientes. Muestra el resumen de decisión, su etiqueta de ejemplo sintético guardado, los datos faltantes y los mensajes fuente.</li><li>Abre el borrador editable sin enviarlo. Luego usa Preguntar a Pendiva y revisa su respuesta y las fuentes citadas.</li><li>Muestra la cobertura y las fuentes. Detén la conversación por voz.</li><li>Abre Ventas y gastos para mostrar la gráfica mensual. Las cifras son sintéticas y no tienen moneda configurada.</li></ol><p>Los clientes y registros de venta son ficticios. No presentes recomendaciones como pagos, reservas o contactos verificados.</p>';
    guide.open = open;
  }
  const picker = document.createElement('select'); picker.className = 'sector-picker';
  document.getElementById('business-form').prepend(picker);
  function updateSector() {
    if (picker.dataset.lang === language) return;
    picker.dataset.lang = language;
    const previous = picker.value;
    picker.innerHTML = language === 'en' ? '<option value="">Choose an industry (optional)</option><option value="Limpieza">Cleaning</option><option value="Mantenimiento y reparaciones">Maintenance and repair</option><option value="Servicios profesionales">Professional services</option><option value="Belleza y bienestar">Beauty and wellness</option><option value="Personalizado">Custom</option>' : '<option value="">Elegir sector (opcional)</option><option value="Limpieza">Limpieza</option><option value="Mantenimiento y reparaciones">Mantenimiento y reparaciones</option><option value="Servicios profesionales">Servicios profesionales</option><option value="Belleza y bienestar">Belleza y bienestar</option><option value="Personalizado">Personalizado</option>';
    picker.value = previous; picker.setAttribute('aria-label',tr('Elegir sector','Choose industry'));
  }
  picker.onchange = () => { if (picker.value && picker.value !== 'Personalizado') document.getElementById('sector').value = picker.value; document.getElementById('sector').focus(); };
  document.getElementById('assistant-provider').onchange = () => { document.getElementById('assistant-consent').checked = false; translate(); };

  let lastDetail = null;
  async function renderWorkflow() {
    const detail = document.getElementById('detail');
    const sender = typeof selected !== 'undefined' ? selected : null;
    if (!sender || !detail.querySelector('h2')) return;
    const current = detail.querySelector('.workflow');
    const draft = current ? Object.fromEntries(new FormData(current.querySelector('form'))) : null;
    if (current) current.remove();
    const card = document.createElement('section'); card.className = 'workflow';
    card.innerHTML = `<h3>${tr('Ficha de seguimiento','Customer follow-up')}</h3><p class="fresh">${tr('Información registrada por ti; verifica los datos en la conversación.','Information entered by you; verify details in the conversation.')}</p><form class="workflow-form"><div class="workflow-grid"><label>${tr('Etapa','Stage')}<select name="stage"><option value="new">${tr('Consulta nueva','New inquiry')}</option><option value="missing">${tr('Faltan datos','Missing details')}</option><option value="ready">${tr('Lista para cotizar','Ready to quote')}</option><option value="quoted">${tr('Cotización enviada','Quote sent')}</option><option value="scheduled">${tr('Servicio por confirmar','Service to confirm')}</option><option value="closed">${tr('Cerrado','Closed')}</option></select></label><label>${tr('Responsable','Responsible person')}<input name="responsible" maxlength="500"></label><label>${tr('Servicio','Service')}<input name="service" maxlength="500"></label><label>${tr('Ubicación','Location')}<input name="location" maxlength="500"></label><label>${tr('Fecha deseada','Preferred date')}<input name="date" maxlength="500"></label><label>${tr('Fecha de envío de cotización','Quote sent date')}<input name="quote_date" type="date"></label><label class="wide">${tr('Alcance o cantidad','Scope or quantity')}<input name="scope" maxlength="500"></label><label class="wide">${tr('Notas y próximos pasos','Notes and next steps')}<textarea name="notes" maxlength="500"></textarea></label></div><div class="toolbar"><button class="secondary" type="submit">${tr('Guardar ficha','Save card')}</button><span class="fresh workflow-status" role="status"></span></div></form><details class="workflow-history"><summary>${tr('Ver cambios registrados','View recorded changes')}</summary><div class="history-list"></div></details>`;
    (detail.querySelector('#customer-brief') || detail.querySelector('h2')).after(card); lastDetail = detail.querySelector('h2');
    const form = card.querySelector('form'), status = card.querySelector('.workflow-status');
    try { const data = await get('/api/conversations/' + sender + '/workflow'); if (!card.isConnected || selected !== sender) return; const values = draft || data; for (const key of ['stage','service','location','date','scope','notes','quote_date','responsible']) if (values[key]) form.elements[key].value = values[key]; }
    catch (_) { status.textContent = tr('No se pudo cargar la ficha.','Could not load the card.'); }
    const history = card.querySelector('.workflow-history'), historyList = card.querySelector('.history-list');
    async function loadHistory() { try { const rows=await get('/api/conversations/'+sender+'/workflow-history'); if (!historyList.isConnected) return; historyList.replaceChildren(); if(!rows.length){historyList.textContent=tr('No hay cambios registrados.','No recorded changes.');return}const names={stage:tr('Etapa','Stage'),responsible:tr('Responsable','Responsible person'),service:tr('Servicio','Service'),location:tr('Ubicación','Location'),date:tr('Fecha deseada','Preferred date'),quote_date:tr('Fecha de cotización','Quote date'),scope:tr('Alcance','Scope'),notes:tr('Notas','Notes')};for(const row of rows){const p=document.createElement('p');p.className='fresh';p.textContent=(names[row.field]||row.field)+': '+(row.previous||'—')+' → '+(row.value||'—')+' · '+new Date(row.created_at).toLocaleString(language==='en'?'en-US':'es-CO');historyList.appendChild(p)} } catch(_){historyList.textContent=tr('No se pudo cargar el historial.','Could not load the history.')} }
    history.ontoggle=()=>{if(history.open)loadHistory()};
    form.onsubmit = async event => { event.preventDefault(); const data = Object.fromEntries(new FormData(form)); try { const saved=await post('/api/conversations/' + sender + '/workflow', data);const item=conversations.find(c=>c.sender===sender);if(item)item.workflow={stage:saved.stage,responsible:saved.responsible,service:saved.service};updateOwnerOptions();renderList();status.textContent = tr('Ficha guardada.','Card saved.'); if(history.open)await loadHistory(); } catch (_) { status.textContent = tr('No se pudo guardar la ficha.','Could not save the card.'); } };
  }
  let opportunityHeading = null;
  async function renderOpportunities() {
    const detail=document.getElementById('detail'), heading=detail.querySelector('h2'), sender=selected;
    if(!heading || !sender || !csrfToken) return;
    const old=detail.querySelector('.customer-opportunities');if(old)old.remove();
    const panel=document.createElement('section');panel.className='opportunity-panel customer-opportunities';
    panel.innerHTML=`<h3>${tr('Oportunidades de este cliente','Customer opportunities')}</h3><p class="fresh">${tr('Registra cada servicio por separado y selecciona su mensaje de respaldo.','Record each service separately and select its supporting message.')}</p><div class="opportunity-list" aria-live="polite"></div><details><summary>${tr('Añadir oportunidad','Add opportunity')}</summary><form class="opportunity-form"><label>${tr('Servicio','Service')}<input name="service" maxlength="500" required></label><label>${tr('Importe mencionado (no verificado)','Amount mentioned (unverified)')}<input name="value" maxlength="500"></label><label>${tr('Tipo de importe','Amount type')}<select name="amount_type"><option value="unknown">${tr('Sin clasificar','Unclassified')}</option><option value="customer_budget">${tr('Presupuesto del cliente','Customer budget')}</option><option value="business_quote">${tr('Cotización del negocio','Business quote')}</option><option value="payment_claim">${tr('Pago declarado por el cliente','Customer-reported payment')}</option><option value="estimate">${tr('Estimación','Estimate')}</option><option value="other">${tr('Otro','Other')}</option></select></label><label>${tr('Próximo paso (opcional)','Next step (optional)')}<input name="next_action" maxlength="500"></label><label>${tr('Mensaje de respaldo','Supporting message')}<select name="source_message_id" required></select></label><button class="secondary" type="submit">${tr('Guardar oportunidad','Save opportunity')}</button><span class="fresh opportunity-status" role="status"></span></form></details>`;
    (detail.querySelector('#customer-brief')||heading).after(panel);opportunityHeading=heading;
    const select=panel.querySelector('select');const placeholder=document.createElement('option');placeholder.value='';placeholder.textContent=tr('Selecciona un mensaje','Select a message');select.appendChild(placeholder);for(const message of messages){const option=document.createElement('option');option.value=message.id;option.textContent=message.text;select.appendChild(option)}
    const list=panel.querySelector('.opportunity-list'),status=panel.querySelector('.opportunity-status'),createForm=panel.querySelector('.opportunity-form');
    const proposals=document.createElement('details');proposals.className='opportunity-proposals';
    proposals.innerHTML=`<summary>${tr('Buscar oportunidades con Pendiva','Find opportunities with Pendiva')}</summary><p class="fresh">${tr('Envía hasta 30 mensajes de texto a Meta. Puedes incluir hasta 10 observaciones de archivos ya analizados; no se envían los archivos. Puede consumir créditos. Revisa cada propuesta.','Send up to 30 text messages to Meta. You may include up to 10 observations from previously analyzed files; files are not sent. This may use credits. Review each suggestion.')}</p><label class="consent"><input type="checkbox">${tr('Autorizo enviar estos mensajes a Meta para buscar propuestas.','I agree to send these messages to Meta AI for suggestions.')}</label><label class="consent"><input type="checkbox" class="include-media">${tr('Incluir observaciones de archivos analizados','Include observations from analyzed files')}</label><button type="button" class="secondary">${tr('Buscar propuestas','Find suggestions')}</button><div class="proposal-results" aria-live="polite"></div>`;
    panel.insertBefore(proposals,panel.querySelector('details'));
    proposals.querySelector('button').onclick=async()=>{const button=proposals.querySelector('button'),results=proposals.querySelector('.proposal-results');if(!proposals.querySelector('input').checked){results.textContent=tr('Confirma primero el envío a Meta AI.','First confirm sending to Meta.');return}button.disabled=true;results.textContent=tr('Buscando propuestas…','Finding suggestions…');try{const rows=await post('/api/conversations/'+sender+'/opportunity-proposals',{consent_to_send_to_meta:true,include_media:proposals.querySelector('.include-media').checked,language});if(!panel.isConnected||selected!==sender)return;results.replaceChildren();if(!rows.length)results.textContent=tr('No se encontraron servicios suficientemente claros.','No sufficiently clear services were found.');for(const row of rows){const item=document.createElement('article');item.className='opportunity-item';const title=document.createElement('strong');title.textContent=row.service;const evidence=document.createElement('p');evidence.textContent=(row.source_type==='media'?tr('Observación de IA del archivo ','AI observation from file ')+row.source_name+': ':tr('Mensaje de respaldo: ','Supporting message: '))+row.source_text;const action=document.createElement('p');action.textContent=tr('Siguiente paso sugerido: ','Suggested next step: ')+row.next_action;const choose=document.createElement('button');choose.type='button';choose.className='secondary';choose.textContent=tr('Revisar y editar','Review and edit');choose.onclick=()=>{const form=createForm;form.elements.service.value=row.service;form.elements.value.value=row.value;form.elements.amount_type.value=row.amount_type||'unknown';form.elements.next_action.value=row.next_action;if(row.source_type==='media'){for(const old of form.elements.source_message_id.options)if(old.value==='media:'+row.source)old.remove();const option=document.createElement('option');option.value='media:'+row.source;option.dataset.digest=row.source_digest;option.textContent=tr('Observación de IA: ','AI observation: ')+row.source_name;form.elements.source_message_id.appendChild(option);form.elements.source_message_id.value=option.value}else form.elements.source_message_id.value=row.source;form.closest('details').open=true;form.elements.service.focus()};item.append(title,evidence,action,choose);results.appendChild(item)}}catch(_){results.textContent=tr('No se pudieron obtener propuestas. Revisa la configuración y vuelve a intentar.','Could not obtain suggestions. Check configuration and try again.')}finally{button.disabled=false}};
    async function load(){const rows=await get('/api/conversations/'+sender+'/opportunities');if(!panel.isConnected||selected!==sender)return;list.replaceChildren();if(!rows.length){list.textContent=tr('Todavía no hay oportunidades registradas.','No opportunities recorded yet.');return}for(const row of rows){const item=document.createElement('article');item.className='opportunity-item';const title=document.createElement('strong');title.textContent=row.service_key;item.appendChild(title);if(row.value){const p=document.createElement('p');p.className='fresh';p.textContent=tr('Importe no verificado','Unverified amount')+' · '+tr(({customer_budget:'Presupuesto del cliente',business_quote:'Cotización del negocio',payment_claim:'Pago declarado por el cliente',estimate:'Estimación',other:'Otro'})[row.amount_type]||'Sin clasificar',({customer_budget:'Customer budget',business_quote:'Business quote',payment_claim:'Customer-reported payment',estimate:'Estimate',other:'Other'})[row.amount_type]||'Unclassified')+': '+row.value;item.appendChild(p)}for(const value of [row.next_action,row.due_date])if(value){const p=document.createElement('p');p.textContent=value;item.appendChild(p)}if(!row.evidence.length&&!(row.media_evidence||[]).length){const warning=document.createElement('p');warning.className='fresh';warning.textContent=tr('Sin fuente disponible; revisa esta oportunidad.','Source unavailable; review this opportunity.');item.appendChild(warning)}for(const source of row.evidence){const p=document.createElement('p');p.className='fresh';p.textContent=tr('Mensaje de respaldo: ','Supporting message: ')+source.text;item.appendChild(p)}const details=document.createElement('details');details.innerHTML=`<summary>${tr('Editar oportunidad','Edit opportunity')}</summary><form class="opportunity-form"><label>${tr('Servicio','Service')}<input name="service" maxlength="500" required></label><label>${tr('Importe mencionado (no verificado)','Amount mentioned (unverified)')}<input name="value" maxlength="500"></label><label>${tr('Tipo de importe','Amount type')}<select name="amount_type"><option value="unknown">${tr('Sin clasificar','Unclassified')}</option><option value="customer_budget">${tr('Presupuesto del cliente','Customer budget')}</option><option value="business_quote">${tr('Cotización del negocio','Business quote')}</option><option value="payment_claim">${tr('Pago declarado por el cliente','Customer-reported payment')}</option><option value="estimate">${tr('Estimación','Estimate')}</option><option value="other">${tr('Otro','Other')}</option></select></label><label>${tr('Próximo paso','Next step')}<input name="next_action" maxlength="500"></label><label>${tr('Fecha de seguimiento','Follow-up date')}<input name="due_date" type="date"></label><label>${tr('Etapa','Stage')}<select name="stage"><option value="new">${tr('Consulta nueva','New inquiry')}</option><option value="missing">${tr('Faltan datos','Missing details')}</option><option value="ready">${tr('Lista para cotizar','Ready to quote')}</option><option value="quoted">${tr('Cotización enviada','Quote sent')}</option><option value="scheduled">${tr('Servicio por confirmar','Service to confirm')}</option><option value="closed">${tr('Cerrado','Closed')}</option></select></label><button class="secondary">${tr('Guardar cambios','Save changes')}</button><span class="fresh" role="status"></span></form>`;const form=details.querySelector('form');for(const [key,value] of Object.entries({service:row.service_key,value:row.value,amount_type:row.amount_type||'unknown',next_action:row.next_action,due_date:row.due_date,stage:row.stage}))form.elements[key].value=value||'';form.onsubmit=async event=>{event.preventDefault();const button=form.querySelector('button'),message=form.querySelector('[role=status]');button.disabled=true;try{await post('/api/conversations/'+sender+'/opportunities/'+row.id,Object.fromEntries(new FormData(form)));await load();loadFollowups()}catch(e){message.textContent=e.message;button.disabled=false}};for(const source of row.media_evidence||[]){const p=document.createElement('p');p.className='fresh';p.textContent=tr('Observación de IA guardada: ','Saved AI observation: ')+source.media_name+' · '+source.observation;item.appendChild(p);if(source.available){const a=document.createElement('a');a.href='/api/media/'+encodeURIComponent(source.media_id)+'/content';a.target='_blank';a.rel='noopener';a.textContent=tr('Abrir archivo','Open file');item.appendChild(a)}}item.appendChild(details);list.appendChild(item)}}
    try{await load()}catch(_){status.textContent=tr('No se pudieron cargar las oportunidades.','Could not load opportunities.')}
    createForm.onsubmit=async event=>{event.preventDefault();const form=event.currentTarget,button=form.querySelector('button');button.disabled=true;try{const data=Object.fromEntries(new FormData(form)),option=form.elements.source_message_id.selectedOptions[0];if(data.source_message_id.startsWith('media:')){data.source_media_id=data.source_message_id.slice(6);data.source_message_id='';data.source_digest=option.dataset.digest}await post('/api/conversations/'+sender+'/opportunities',data);form.reset();status.textContent=tr('Oportunidad guardada.','Opportunity saved.');await load();loadFollowups()}catch(e){status.textContent=e.message}finally{button.disabled=false}};
  }
  let replyHeading = null;
  async function renderReplyDrafts(){
    const detail=document.getElementById('detail'),heading=detail.querySelector('h2'),sender=selected;
    if(!heading||!sender||!csrfToken)return;
    detail.querySelector('.reply-panel')?.remove();replyHeading=heading;
    const panel=document.createElement('section');panel.className='reply-panel';
    panel.innerHTML=`<h3>${tr('Respuesta al cliente','Customer reply')}</h3><p class="fresh">${tr('Borrador local para revisar. Todavía no se envía por WhatsApp.','Local draft for review. It is not sent to WhatsApp yet.')}</p><label>${tr('Responder al mensaje','Reply to message')}<select class="reply-source"></select></label><textarea maxlength="4096" rows="4" aria-label="${tr('Borrador de respuesta','Reply draft')}"></textarea><div class="toolbar"><button type="button" class="secondary reply-pendiva">${tr('Sugerir respuesta con Pendiva','Suggest reply with Pendiva')}</button><button type="button" class="secondary reply-suggest">${tr('Usar respuesta general','Use general starter')}</button><button type="button" class="secondary reply-save">${tr('Guardar borrador','Save draft')}</button></div><p class="fresh" role="status"></p><div class="reply-list"></div>`;
    (detail.querySelector('#customer-brief')||heading).after(panel);
    const select=panel.querySelector('select');for(const message of messages){const option=document.createElement('option');option.value=message.id;option.textContent=message.text;select.appendChild(option)}
    const result=panel.querySelector('[role=status]'),textarea=panel.querySelector('textarea'),saveButton=panel.querySelector('.reply-save');let activeDraft='';
    async function load(){const rows=await get('/api/conversations/'+sender+'/reply-drafts');if(!panel.isConnected||selected!==sender)return;const list=panel.querySelector('.reply-list');list.replaceChildren();for(const row of rows){const p=document.createElement('p');p.className='opportunity-item';p.textContent=tr('Borrador guardado: ','Saved draft: ')+row.text;const source=document.createElement('small');source.style.display='block';source.textContent=tr('En respuesta a: ','In reply to: ')+(messages.find(m=>m.id===row.source_message_id)?.text||tr('Mensaje no disponible','Message unavailable'));p.appendChild(source);const edit=document.createElement('button');edit.type='button';edit.className='secondary';edit.textContent=tr('Editar borrador','Edit draft');edit.onclick=()=>{activeDraft=row.id;textarea.value=row.text;select.value=row.source_message_id;saveButton.textContent=tr('Actualizar borrador','Update draft');textarea.focus()};p.append(' ',edit);list.appendChild(p)}}
    panel.querySelector('.reply-pendiva').onclick=async()=>{const button=panel.querySelector('.reply-pendiva');button.disabled=true;result.textContent=tr('Pendiva revisa el contexto guardado…','Pendiva is reviewing the saved context…');try{const response=await post('/api/reply-template',{language,sender});textarea.value=response.text;activeDraft='';saveButton.textContent=tr('Guardar borrador','Save draft');result.textContent=tr('Borrador sugerido a partir de los datos guardados. Revísalo antes de guardarlo.','Draft suggested from saved details. Review it before saving.')}catch(_){result.textContent=tr('No se pudo preparar el borrador local.','Could not prepare the local draft.')}finally{button.disabled=false}};
    panel.querySelector('.reply-suggest').onclick=async()=>{try{textarea.value=(await post('/api/reply-template',{language})).text;result.textContent=tr('Respuesta general añadida. Personalízala antes de guardarla.','General starter added. Customize it before saving.')}catch(_){result.textContent=tr('No se pudo cargar la respuesta inicial.','Could not load the starter reply.')}};
    panel.querySelector('.reply-save').onclick=async()=>{try{if(activeDraft)await post('/api/conversations/'+sender+'/reply-drafts/'+activeDraft,{text:textarea.value});else await post('/api/conversations/'+sender+'/reply-drafts',{source_message_id:select.value,text:textarea.value});activeDraft='';saveButton.textContent=tr('Guardar borrador','Save draft');textarea.value='';result.textContent=tr('Borrador guardado en este equipo.','Draft saved on this device.');await load()}catch(_){result.textContent=tr('No se pudo guardar el borrador.','Could not save the draft.')}};
    try{await load()}catch(_){result.textContent=tr('No se pudieron cargar los borradores.','Could not load drafts.')}
  }
  window.pendivaRenderReplyDrafts = renderReplyDrafts;
  let scheduled = false;
  const observer = new MutationObserver(() => { if (scheduled) return; scheduled = true; requestAnimationFrame(() => { scheduled = false; translate(); const heading = document.querySelector('#detail h2'); if (heading && heading !== lastDetail) renderWorkflow(); if(heading&&heading!==opportunityHeading)renderOpportunities(); if(heading&&heading!==replyHeading)renderReplyDrafts(); }); });
  observer.observe(document.body, {childList:true,subtree:true});
  translate();
})();
