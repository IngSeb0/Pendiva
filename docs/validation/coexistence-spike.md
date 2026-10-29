# Spike de WhatsApp Coexistence: plan y evidencia F02

**Resultado al 2026-10-15:** viabilidad plausible; evidencia de producción pendiente. No hubo número real, conexión a Meta/BSP, webhook externo ni VPS. Las pruebas ejecutadas son de contrato simulado únicamente.

## Qué se puede probar con el número sandbox de Meta

La colección oficial de Meta incluye un `Test WhatsApp Business Account`, operaciones de envío de prueba y los pasos de Cloud API. El dashboard de la app de Meta proporciona activos de test y tokens de desarrollo; las llamadas requieren una app/portafolio y datos de acceso del propio entorno. Esta vía sirve para ensayar llamadas Cloud API básicas y estados; para eventos entrantes se necesita además un receptor HTTPS configurado.

Ese número sandbox **no reemplaza** un número colombiano elegible con WhatsApp Business App para verificar Coexistence. No demuestra inicio por QR/código en una cuenta del cliente, historial de la app ni `smb_message_echoes` escritos desde la app. La validación del caso B y el alcance del caso C necesitan un número de prueba con cuenta Business App y elegibilidad de Coexistence confirmada por Meta/proveedor; un número sandbox de Cloud API valida sólo lo que soporte el entorno de prueba.

No se obtuvo acceso a la app/portafolio de Meta ni se envió ningún mensaje. El script `scripts/whatsapp_test_smoke.py` está en modo seco por defecto; con `--send` envía un único template de prueba `hello_world` al destinatario configurado. Requiere variables locales `WHATSAPP_TEST_GRAPH_VERSION`, `WHATSAPP_TEST_PHONE_NUMBER_ID`, `WHATSAPP_TEST_ACCESS_TOKEN` y `WHATSAPP_TEST_RECIPIENT`. No compartir el token en chat, no guardarlo en Git, y elegir sólo un destinatario de prueba propio y autorizado. Usar versión Graph vigente confirmada en el dashboard/docs. Los mensajes entrantes requieren callback HTTPS. No se preparó un callback público ni se desplegó infraestructura en F02.

Fuente: [colección oficial de WhatsApp Cloud API de Meta](https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api), que documenta los activos/tokens, operaciones de test (incluida `hello_world`) y mensajes de prueba.

## Pregunta crítica

¿Podemos dar a una empresa continuidad con WhatsApp Business App y reunir tanto los mensajes entrantes como los que el equipo envía desde la App, con cobertura visible y consentimiento del historial?

Documentación BSP consultada describe `smb_message_echoes` para mensajes nuevos escritos en WhatsApp Business App, `history` para sincronización histórica consentida y `smb_app_state_sync` para contactos. La existencia documentada de eventos no demuestra que el número sea elegible o que nuestro SaaS reciba todos los eventos en operación.

## Contrato simulado

Implementado en `src/whatsapp_provider.py`. API: `connect`, `connection_status`, `verify_webhook`, `normalize_event`, `disconnect`, `get_capabilities`. Es in-memory, no tiene cliente HTTP, conserva estado sólo en el proceso y no usa una carga útil real de Meta. La firma HMAC `sha256=...` es un fixture propio; no es método de autenticación Meta. Las capacidades son ejemplos sintéticos (`simulated=True`), no prueba de un proveedor.

## Matriz de validación A–E

| Caso | Prueba real autorizada requerida | Evidencia esperada | Estado |
|---|---|---|---|
| A. Mensaje entrante cliente → empresa | Enviar mensaje de prueba a número elegible, recoger webhook | evento entrante, timestamp, ID y payload llegan una vez y se correlacionan al tenant | Pendiente, sin número/cuenta conectados |
| B. Mensaje saliente escrito en Business App | Responder desde la App en convivencia | `smb_message_echoes` recibido por phone-number webhook, con ID/timestamp/partes y contenido admitido | Pendiente; bloqueo crítico del piloto hasta demostrarlo |
| C. Historial | Aceptar permiso de sincronización; repetir con rechazo | alcance/rango, chunk order/progress, consentimiento, contenido disponible y error de declinación | Pendiente; no prometer rango o totalidad |
| D. Duplicados y fuera de orden | Reentregar/reordenar fixtures y luego eventos reales si el proveedor lo permite | idempotencia por event/message ID, orden de negocio por timestamp/secuencia, no sobrescritura silenciosa | Simulado parcialmente; integración pendiente |
| E. No elegible, rechazo, caducidad y desconexión | Probar número no elegible/rechazo, expiración de sesión y desconexión | estado entendible, reintento permitido, revocación y corte de ingestión; no datos ficticios | Pendiente |

No ejecutar los casos reales hasta obtener un número de prueba elegible y autorización separada. Evitar mensajes a clientes, cuentas o destinatarios reales.

## Pruebas de contrato incluidas

`python -m unittest discover -s tests -v` cubre ciclo conexión/desconexión, verificación HMAC sintética, normalización provider-neutral, datos requeridos y marca `simulated`. No cubre HTTP, Meta, firma Meta, reintentos, colas, persistencia, sincronización ni cobertura del proveedor.

## Bloqueos para declarar F02 validada por evidencia real

1. Confirmar candidato/contrato y que el proveedor opere para clientes en Colombia y modelo WAAC/PMA.
2. Conseguir número de prueba elegible para Coexistence, acceso administrador y consentimiento para cualquier historia.
3. Acordar una ventana de prueba; validar los casos A–E y guardar fixtures anonimizados, logs sin tokens y timestamps.
4. Probar explícitamente que cada mensaje saliente hecho desde Business App genera evento ingerible. Si falla o falta algún cliente móvil, el MVP no puede prometer analítica completa.
5. Definir retención, exportación y borrado antes de datos reales, con revisión contractual/legal.

F02 permite pasar a diseño de arquitectura con esas limitaciones explícitas; no autoriza construir conexión real en F06 o iniciar un piloto.
