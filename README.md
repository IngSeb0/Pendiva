# SaaS de inteligencia comercial para WhatsApp Business

Demo sandbox de inteligencia comercial para WhatsApp Business. El recorrido previo de recepción real y análisis con proveedores quedó documentado con fecha y alcance en `docs/validation/`. El panel actual usa exclusivamente Muse (Meta Model API); la integración de WhatsApp sigue en modo sandbox y no es un SaaS desplegado.

## Estado actual

- F02 evaluó Embedded Signup, Coexistence y opciones de proveedor; revisa la [matriz](docs/research/whatsapp-provider-matrix.md), el [ADR 001](docs/decisions/001-whatsapp-provider.md) y el [spike de coexistencia](docs/validation/coexistence-spike.md).
- La app Meta `Pendiva` tiene un número de prueba. El 2026-10-28 Meta aceptó un envío `hello_world` y Pendiva recibió un texto real de prueba del teléfono autorizado; la entrega del `hello_world` no se confirmó por separado. Consulta la [guía Cloud API de prueba](docs/validation/meta-cloud-api-test.md) y el [plan real con Muse y WhatsApp](docs/plan-hackathon-muse-whatsapp.md).
- F01 tiene [guía de entrevistas](docs/research/customer-discovery-f01.md) y [ficha CSV](docs/validation/interview-template.csv). El usuario reportó dos entrevistas previas y una señal verbal de interés; faltan detalles documentados y más entrevistas.
- El código fuente está publicado en la rama `e` de `IngSeb0/Pendiva`; el despliegue productivo sigue pendiente y no se debe confundir con el sandbox local.
- Se preparó un spike local del botón de [Meta Embedded Signup](docs/validation/embedded-signup-spike.md) para diagnosticar el onboarding de un número propio de WhatsApp Business App; aún faltan los valores de configuración de Meta y no se ha conectado ninguna cuenta.
- Alcance funcional de referencia: [MVP](docs/product/mvp.md).
- Recorrido sandbox: [arranque unificado](scripts/iniciar_demo.py), [servidor local](src/live_app.py), [webhook y análisis](src/live_pipeline.py) y [panel](src/static/live.html). La versión anterior con ejemplos sigue disponible en `python -m src.mvp_app`, pero no alimenta el panel real.
- Investigación de la posible convocatoria y guion de presentación: [Meta Global AI Developer Hackathon](docs/research/meta-hackathon-2026.md). Las reglas oficiales se revisaron y resumieron en el [nuevo plan](docs/plan-hackathon-muse-whatsapp.md); falta confirmar evento y aceptación del usuario.
- Plan de producto, evaluación de las fases y entregas para la hackathon: [plan de producto](docs/plan-producto-hackathon.md).
- Plan de evolución hacia inteligencia comercial estructurada, analítica cruzada y asistente conversacional: [plan de implementación](docs/plan-inteligencia-comercial/plan.md).
- El panel permite configurar el negocio, obtener recomendaciones con evidencia y resolverlas individualmente; los cambios de conversación o contexto invalidan el análisis anterior. El uso actual es Muse; el análisis histórico con Nebius está registrado sólo como evidencia pasada, no como opción de producto.

El detalle de cada conversación usa Muse (Meta Model API) y requiere consentimiento antes de enviar
mensajes y contexto. Nebius y otros proveedores no se ofrecen ni se llaman desde la aplicación;
variables antiguas en `.env` se ignoran. El asistente del dueño responde en el idioma seleccionado,
recupera hasta 36 fuentes relevantes tras buscar localmente todas las conversaciones del tenant y
declara la cobertura parcial. La vista financiera muestra ventas y gastos mensuales desde CSV local.
Consulta [las mejoras y sus límites](docs/validation/mejoras-demo.md).
Para grabar la demo en inglés, usa el [Recording Pack](docs/validation/demo-recording-pack-en.md),
que incluye pitch, storyboard de tres minutos, prompts, CSV de ventas y preparación de datos
sintéticos en inglés.

El panel también muestra una bandeja transversal de prioridades: reúne recomendaciones pendientes
de análisis vigentes, las ordena por prioridad y permite abrir directamente la conversación con su
evidencia. Los análisis obsoletos se excluyen hasta que se vuelvan a generar.

Inicio también muestra los seguimientos abiertos de las oportunidades que el equipo registró en
cada ficha de cliente. Las fechas se comparan con la fecha local del dispositivo y se distinguen
fechas pasadas, hoy, próximas y sin fecha. Son datos ingresados manualmente, no compromisos
detectados automáticamente ni evidencia de que se contactó al cliente. Cada fila abre la ficha
para revisar su mensaje de respaldo y actualizar la oportunidad.

En cada ficha, **Buscar oportunidades con Muse** envía hasta 30 mensajes de texto al proveedor
únicamente después de confirmar el consentimiento de esa búsqueda. Devuelve propuestas temporales
con mensaje de respaldo; la persona debe revisarlas, editarlas y guardar cada oportunidad. Un importe
que no aparezca literalmente en el mensaje citado se descarta. Opcionalmente se incluyen hasta diez
observaciones de archivos ya analizados; se envía su texto, no el archivo original. Las observaciones
son salidas de IA y requieren comprobar el archivo. El importe procedente de una observación se deja
vacío. Al guardar, se conserva la observación revisada con su archivo; si cambia antes de guardar,
hay que generar otra propuesta. Al borrar el archivo se borra también esa copia de evidencia, aunque
la oportunidad permanece y debe revisarse. Una propuesta no se guarda por sí sola.

La ficha del cliente permite pedir a Muse un borrador basado en la conversación (con consentimiento
explícito), ver sus mensajes fuente y guardarlo o editarlo localmente; también incluye una plantilla
bilingüe. Los borradores no se envían a WhatsApp ni activan un bot. La conexión de
salida, estados de entrega, ventanas de mensajería, automatización y validación del sandbox siguen
pendientes antes de responder a clientes reales.

La vista del dueño resume los últimos siete días con un denominador explícito: conversaciones y
mensajes recibidos, análisis vigentes, recomendaciones por estado y prioridades pendientes. También
declara que la cobertura es sólo del webhook firmado, no incluye necesariamente mensajes salientes
ni el historial completo y no permite inferir ingresos, conversiones o rentabilidad.

El dueño puede proteger el panel configurando `PENDIVA_AUTH_PASSWORD` en `.env`; la contraseña no
se guarda en la base ni se envía al navegador y las sesiones usan una cookie `HttpOnly` de duración
limitada. Para análisis financiero puede importar un CSV exportado desde Excel con columnas
`fecha,tipo,monto,categoria`, donde la fecha usa `YYYY-MM-DD` y `tipo` es `venta` o `gasto`.
Pendiva calcula resultado, proporción de gastos y tendencia mensual, y sólo formula alertas
explicables; no reemplaza contabilidad, conexión bancaria ni análisis causal.
La fundación SaaS local ya incluye tenants, usuarios, membresías, roles (`owner`, `manager`,
`advisor`, `viewer`), sesiones persistentes revocables, auditoría, perfiles sectoriales y tablas
de contactos, oportunidades, cotizaciones, citas, pagos, actividades y evidencias. El modo
`PENDIVA_AUTH_PASSWORD` se conserva sólo para compatibilidad con la demo; el camino SaaS usa
`/api/auth/bootstrap` una sola vez y después `/api/auth/login` con correo y contraseña.
- Hallazgos y decisiones de contexto: [ADR 000](docs/decisions/000-contexto.md).
- Bloqueos y verificaciones pendientes: [bloqueos](docs/validation/bloqueos.md).
- Documento de referencia recibido: `ROADMAP_AGENTE_SAAS_WHATSAPP_HOSTINGER.md` (el original está fuera de este directorio de trabajo; ver ADR 000).

## Principios de trabajo

Colaborar con criterio siguiendo el alcance pedido, preservar el trabajo existente, verificar documentación vigente antes de integrar servicios y usar datos sintéticos en desarrollo. No subir secretos ni datos reales de clientes. Las guías para agentes están en [`AGENTS.md`](AGENTS.md) y [`CLAUDE.md`](CLAUDE.md).

## Arquitectura prevista, aún no aprobada

La arquitectura de producción propuesta aún no se aprobó: Hostinger VPS con Docker Compose, Next.js/TypeScript, FastAPI, PostgreSQL y Redis con worker, proxy TLS y un adaptador para proveedor oficial de WhatsApp. El prototipo de hackathon usa Python estándar y SQLite para evitar configurar infraestructura antes de validar el flujo. Esa decisión temporal no reemplaza la arquitectura futura.

## Ejecutar la demo sandbox

Requiere Python 3.12+; no necesita instalar paquetes.

### Inicializar una empresa local

Con el servidor iniciado, crea la primera empresa una sola vez:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/auth/bootstrap `
  -H "Content-Type: application/json" `
  -d '{"name":"Pendiva Demo","email":"demo@example.com","password":"change-this-demo-password","sector":"cleaning"}'
```

Después inicia sesión desde el panel con ese correo y contraseña. La base local se prepara para
una migración posterior a PostgreSQL, pero SQLite no debe exponerse directamente a Internet ni
usarse aún como despliegue multiusuario.

### Demo reproducible con WhatsApp

Para presentar el producto sin depender de que llegue primero un mensaje externo, usa:

```powershell
python -m scripts.iniciar_demo --demo
```

El comando usa `data/demo.sqlite3`, una base separada de `PENDIVA_LIVE_DB`, y carga nueve clientes
ficticios, conversaciones, recomendaciones con evidencia y finanzas sintéticas. El usuario y la
contraseña de demostración se muestran en la terminal. La demo puede abrirse sin claves: ninguna
llamada de IA ni de voz ocurre automáticamente. Al agregar `--tunnel`, sí se exige la configuración
del sandbox y se asocia el número de prueba con el tenant demo. Puedes elegir otra base aislada con
`--demo-db ruta.sqlite3`; no uses como destino la base que contiene datos que quieras mantener separados.

Si además usas `--tunnel`, los mensajes reales que lleguen por el webhook firmado se guardan en
el mismo tenant demo y el contacto se crea o actualiza por teléfono. Esto no mezcla mensajes de
otro número: el webhook sólo acepta el `WHATSAPP_PHONE_NUMBER_ID` configurado y la conexión
verificada del tenant.

Los datos demo son acumulativos e idempotentes: ejecutar `--demo` dos veces no duplica clientes,
mensajes ni finanzas. No incluye un comando de borrado automático. Las conversaciones ficticias
incluyen ejemplos de intervenciones del asesor; los datos reales disponibles dependen del webhook.

### Personalizar y presentar

La barra principal organiza la demo en **Inicio**, **Clientes**, **Mejoras**, **Finanzas** y
**Negocio**. El asistente se abre desde la burbuja disponible en cualquier sección; permite dictar,
escribir y leer la respuesta en voz alta con la voz del navegador, sin generar un archivo de audio.
Una animación indica cuándo escucha, procesa y habla; refleja el estado, no una forma de onda real.
En «Opciones de voz» se puede elegir ElevenLabs para transcribir el dictado con consentimiento;
esto puede consumir créditos. La disponibilidad del micrófono, dictado y voz depende del navegador,
del dispositivo y de sus permisos; la transcripción debe revisarse antes de enviar la pregunta.

En **Mejoras** hay una herramienta ficticia de ejemplo para ejecutar y abrir los clientes con
información pendiente. Muse también puede proponer herramientas basadas en las tres vistas
compatibles, que se revisan antes de activarlas; no genera código ni contacta clientes. Las
herramientas utilizan los datos de la ficha registrados por el usuario, por lo que un dato mencionado
en una conversación puede seguir figurando como pendiente hasta que se registre en la ficha.
Las etiquetas de la interfaz cambian de idioma; mensajes, archivos y análisis ya guardados conservan
su idioma original.

En el encabezado puedes elegir español o inglés y modo claro u oscuro; las preferencias se guardan
en ese navegador. La lista de clientes permite combinar filtros de etapa, prioridad y responsable;
la prioridad usa recomendaciones pendientes y vigentes, y las fichas se actualizan al guardar.
El idioma elegido se solicita también para las nuevas respuestas y análisis de IA,
y configura el dictado. Los mensajes originales y los análisis anteriores no se traducen
automáticamente. En **Configura el contexto de tu negocio**, elige un sector sugerido o escribe uno
propio y describe los servicios, horarios y objetivos. Abrir una conversación permite guardar una
ficha manual con etapa, responsable, servicio, ubicación, fecha, alcance y notas. Puedes registrar
varias oportunidades por cliente, con servicio, valor y próximo paso declarados manualmente y un
mensaje de respaldo seleccionado. Puedes editar los campos, etapa y fecha de seguimiento; el
asistente también puede recuperar estos registros como datos declarados por el usuario. Esta primera
versión requiere sesión de empresa. También puedes registrar zonas, tarifas
de referencia y condiciones en el contexto; el asistente recibe esos datos
si autorizas el envío. Los cambios de la ficha se registran en su historial local. El responsable es
un nombre escrito a mano; no crea una cuenta ni envía notificaciones. Estos datos son del usuario,
no hechos verificados automáticamente ni reservas o mensajes enviados. La guía desplegable propone
un recorrido de tres minutos; el [guion de presentación](docs/validation/demo-tres-minutos.md)
incluye alternativas si falla la voz o el proveedor. El indicador de credenciales no verifica por sí mismo conectividad.

El panel y la ficha son para una demo local de una empresa. El aislamiento completo de todas las
rutas multiempresa y el despliegue seguro siguen pendientes. Para voz ElevenLabs se necesita una
clave válida, consentimiento y créditos; tener una clave configurada no prueba el servicio. El plan
gratuito es no comercial y requiere atribución según la [documentación de ElevenLabs](https://elevenlabs.io/docs/overview/administration/billing).
El dictado envía `es` o `en` como código de idioma a la [API de transcripción](https://elevenlabs.io/docs/api-reference/speech-to-text/convert); la voz utiliza el [modelo multilingüe de síntesis](https://elevenlabs.io/docs/overview/capabilities/text-to-speech).

### Archivos y herramientas personalizadas

Abre la conversación ficticia de Ana: incluye una imagen, un audio en inglés y un video estático
de ejemplo. Se guardan localmente y no se analizan al arrancar. Para obtener una observación o
transcripción real, confirma el envío de cada archivo a Meta y pulsa **Analizar con Muse**. El
asistente puede usar los resultados junto con los mensajes y muestra sus fuentes; el archivo es
una fuente indirecta y las observaciones deben revisarse. El selector del asistente permite elegir
Muse u otro proveedor configurado antes de confirmar el envío del contexto.

El panel admite PNG, JPG, MP4, WAV y OGG de hasta 4 MB. El WAV para Muse debe ser PCM mono de
16 bits a 16 o 24 kHz. Un OGG se convierte localmente con FFmpeg y se transcriben como máximo los
primeros 60 segundos. FFmpeg se busca en el PATH, en `PENDIVA_FFMPEG_PATH`, o en la carpeta
opcional `data/demo-tools` del entorno local. Los archivos de WhatsApp que el webhook registra se
pueden descargar desde la conversación mediante una acción explícita y `WHATSAPP_TEST_ACCESS_TOKEN`;
descargar no los analiza automáticamente. El sandbox real con multimedia sigue sin verificarse.

En **Crea una herramienta para tu negocio**, escribe una solicitud, responde a Muse y revisa la
vista previa antes de activarla. El prototipo admite listas de cotizaciones pendientes, fichas con
datos faltantes y servicios por confirmar. Las reglas se ejecutan con datos de fichas ingresados
por el usuario; no ejecutan código ni envían mensajes. Para seguimiento, registra la etapa
«Cotización enviada» y la fecha de envío en la ficha. También puedes previsualizar y cargar un CSV
con encabezado `sender,quote_date`, números de conversaciones existentes y fechas `AAAA-MM-DD`;
importar fechas no cambia la etapa. No se inventan fechas ausentes. Puedes desactivar una vista.

Las pruebas reales y simuladas, límites y referencias técnicas están en la [guía de validación](docs/validation/estudio-multimodal.md).

```powershell
python -m scripts.iniciar_demo --check
python -m scripts.iniciar_demo --tunnel
python -m scripts.iniciar_demo --demo
```

Abre `http://127.0.0.1:8000`. El comando levanta el panel y un receptor separado en el puerto 8772. `--tunnel` requiere cloudflared y publica exclusivamente el receptor. La URL temporal cambia al reiniciar; para actualizar el callback de la app Pendiva existente, ejecuta `python -m scripts.configurar_webhook --apply` desde otra terminal. El script comprueba el desafío, las rutas privadas y el rechazo de eventos sin firma antes del cambio. Consulta la [guía de operación](docs/validation/live-sandbox.md).

Los mensajes y análisis se guardan en `data/live.sqlite3`, excluido de Git. Sin túnel, `python -m scripts.iniciar_demo` arranca ambos puertos sólo en local. `python -m src.live_app` conserva la opción de arrancar únicamente el panel. Compose sigue disponible para el panel, pero no configura por sí solo el túnel ni el webhook de Meta.

Para recibir mensajes hacen falta `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_VERIFY_TOKEN`, `WHATSAPP_APP_SECRET` y un webhook HTTPS suscrito a la cuenta de prueba. Para analizarlos se necesita además la clave del proveedor elegido: `NEBIUS_API_KEY` en la configuración actual o `MODEL_API_KEY` para Muse. El token de acceso de WhatsApp es distinto y se usa para envíos y gestión de la suscripción sandbox. La [guía del recorrido real](docs/validation/live-sandbox.md) explica el orden, las autorizaciones y los límites.

Para probar Nemotron mediante Nebius Token Factory, consulta la [guía de Nebius](docs/validation/nebius.md). Usa `PENDIVA_AI_PROVIDER=nebius` y `NEBIUS_API_KEY`. `python -m scripts.iniciar_demo --check-model` hace una llamada real con texto ficticio y puede consumir créditos. Muse se validó por separado con texto ficticio mediante `python -m scripts.iniciar_demo --check-model --provider meta`; consulta la [evidencia](docs/validation/muse.md). La demo principal sigue usando Nebius.

Al seleccionar una conversación y confirmar el envío al proveedor indicado, el panel solicita un análisis al modelo configurado. Cada llamada puede consumir créditos o generar costos. En la ruta de Meta se solicita `store: false`; esta opción no se aplica automáticamente a NVIDIA: revisa sus condiciones de datos. El sistema comprueba que los IDs de evidencia correspondan a mensajes de la conversación, pero no puede garantizar que la interpretación del modelo sea correcta. No pegues claves en el chat o en Git.

Pruebas automatizadas:

```powershell
python -m unittest discover -v
```
