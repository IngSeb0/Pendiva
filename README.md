# SaaS de inteligencia comercial para WhatsApp Business

Demo sandbox de inteligencia comercial para WhatsApp Business. El 2026-10-28 se verificó el recorrido completo: un texto ficticio enviado desde el teléfono autorizado llegó por el webhook firmado de Meta, fue guardado una sola vez y Nebius generó una recomendación con evidencia válida que quedó pendiente de revisión. Es una demo local, no un SaaS comercial desplegado.

## Estado actual

- F02 evaluó Embedded Signup, Coexistence y opciones de proveedor; revisa la [matriz](docs/research/whatsapp-provider-matrix.md), el [ADR 001](docs/decisions/001-whatsapp-provider.md) y el [spike de coexistencia](docs/validation/coexistence-spike.md).
- La app Meta `Pendiva` tiene un número de prueba. El 2026-10-28 Meta aceptó un envío `hello_world` y Pendiva recibió un texto real de prueba del teléfono autorizado; la entrega del `hello_world` no se confirmó por separado. Consulta la [guía Cloud API de prueba](docs/validation/meta-cloud-api-test.md) y el [plan real con Muse y WhatsApp](docs/plan-hackathon-muse-whatsapp.md).
- F01 tiene [guía de entrevistas](docs/research/customer-discovery-f01.md) y [ficha CSV](docs/validation/interview-template.csv). El usuario reportó dos entrevistas previas y una señal verbal de interés; faltan detalles documentados y más entrevistas.
- El usuario autorizó crear el repo GitHub `IngSeb0/pendiva`; aún no se creó porque el conector no ofrece creación de repositorios y la sesión del navegador disponible no está autenticada. Consulta el [backlog y roadmap](docs/roadmap.md).
- Se preparó un spike local del botón de [Meta Embedded Signup](docs/validation/embedded-signup-spike.md) para diagnosticar el onboarding de un número propio de WhatsApp Business App; aún faltan los valores de configuración de Meta y no se ha conectado ninguna cuenta.
- Alcance funcional de referencia: [MVP](docs/product/mvp.md).
- Recorrido sandbox: [arranque unificado](scripts/iniciar_demo.py), [servidor local](src/live_app.py), [webhook y análisis](src/live_pipeline.py) y [panel](src/static/live.html). La versión anterior con ejemplos sigue disponible en `python -m src.mvp_app`, pero no alimenta el panel real.
- Investigación de la posible convocatoria y guion de presentación: [Meta Global AI Developer Hackathon](docs/research/meta-hackathon-2026.md). Las reglas oficiales se revisaron y resumieron en el [nuevo plan](docs/plan-hackathon-muse-whatsapp.md); falta confirmar evento y aceptación del usuario.
- Plan de producto, evaluación de las fases y entregas para la hackathon: [plan de producto](docs/plan-producto-hackathon.md).
- El panel permite configurar el negocio, obtener recomendaciones con evidencia y resolverlas individualmente; los cambios de conversación o contexto invalidan el análisis anterior. Las pruebas automatizadas usan simulaciones; Nebius se comprobó además con el texto ficticio recibido realmente desde WhatsApp. Ver [ADR 006](docs/decisions/006-recomendaciones.md) y [operación de la demo](docs/decisions/007-operacion-demo-sandbox.md).

Si hay más de una clave de IA configurada en la sesión, el detalle de cada conversación permite
seleccionar el motor antes de analizarla. La selección exige el consentimiento correspondiente
(por ejemplo, Muse/Meta o Nemotron/Nebius) y el resultado conserva el proveedor y modelo usados;
no hay fallback automático ni se envían datos sin confirmación explícita.

El panel también muestra una bandeja transversal de prioridades: reúne recomendaciones pendientes
de análisis vigentes, las ordena por prioridad y permite abrir directamente la conversación con su
evidencia. Los análisis obsoletos se excluyen hasta que se vuelvan a generar.

La vista del dueño resume los últimos siete días con un denominador explícito: conversaciones y
mensajes recibidos, análisis vigentes, recomendaciones por estado y prioridades pendientes. También
declara que la cobertura es sólo del webhook firmado, no incluye necesariamente mensajes salientes
ni el historial completo y no permite inferir ingresos, conversiones o rentabilidad.
- Hallazgos y decisiones de contexto: [ADR 000](docs/decisions/000-contexto.md).
- Bloqueos y verificaciones pendientes: [bloqueos](docs/validation/bloqueos.md).
- Documento de referencia recibido: `ROADMAP_AGENTE_SAAS_WHATSAPP_HOSTINGER.md` (el original está fuera de este directorio de trabajo; ver ADR 000).

## Principios de trabajo

Colaborar con criterio siguiendo el alcance pedido, preservar el trabajo existente, verificar documentación vigente antes de integrar servicios y usar datos sintéticos en desarrollo. No subir secretos ni datos reales de clientes. Las guías para agentes están en [`AGENTS.md`](AGENTS.md) y [`CLAUDE.md`](CLAUDE.md).

## Arquitectura prevista, aún no aprobada

La arquitectura de producción propuesta aún no se aprobó: Hostinger VPS con Docker Compose, Next.js/TypeScript, FastAPI, PostgreSQL y Redis con worker, proxy TLS y un adaptador para proveedor oficial de WhatsApp. El prototipo de hackathon usa Python estándar y SQLite para evitar configurar infraestructura antes de validar el flujo. Esa decisión temporal no reemplaza la arquitectura futura.

## Ejecutar la demo sandbox

Requiere Python 3.12+; no necesita instalar paquetes.

```powershell
python -m scripts.iniciar_demo --check
python -m scripts.iniciar_demo --tunnel
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
