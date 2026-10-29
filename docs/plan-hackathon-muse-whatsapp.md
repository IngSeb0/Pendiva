# Plan de Pendiva: demo real con WhatsApp y Muse

**Actualización técnica:** 2026-10-28. **Estado:** plan de referencia; la priorización está en el [plan de producto](plan-producto-hackathon.md) y la operación actual en la [guía sandbox](validation/live-sandbox.md). La convocatoria y sus reglas fueron revisadas el 2026-10-27; no se pudieron volver a leer el 28. No implica integración terminada ni participación validada. Confirmar evento, aceptación, categoría y condiciones con el equipo.

## Resultado objetivo

Demostrar una conversación de prueba que llega realmente por WhatsApp Cloud API, se guarda, se analiza realmente con Muse Spark mediante Meta Model API y aparece en Pendiva con resumen, señal, próximo paso y referencias verificables a mensajes. Una persona revisa y cambia el estado de la sugerencia. La demo distingue los mensajes reales de prueba de ejemplos sintéticos y muestra fallos sin inventar resultados.

**Prioridad:** una sola empresa de prueba, mensajes de texto, una conversación, revisión humana y un recorrido reproducible. No prometer multiempresa, sincronización histórica ni Coexistence hasta que se prueben. El número de prueba de Meta no demuestra por sí solo que un cliente pueda conectar su WhatsApp Business App existente.

## Reglas oficiales identificadas

Fuente: [Hackathon Terms & Conditions (“Official Rules”) and Event Waiver del organizador](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver), consultada en navegador el 2026-10-27; [página oficial del evento](https://dev.meta.ai/events/global-hackathon).

| Criterio de proyectos | Peso | Respuesta de Pendiva |
|---|---:|---|
| Impacto | 30 % | Demostrar un problema y usuario concretos; señalar que las dos entrevistas reportadas son evidencia preliminar, no métricas de impacto. |
| Uso de IA de Meta | 25 % | Mostrar Muse Spark procesando mensajes reales de prueba, con extracción estructurada, evidencia enlazada y manejo de incertidumbre; medir casos en los que se equivoca. |
| Profundidad y ejecución técnica | 20 % | Webhook verificado, idempotencia, persistencia, validación de salida, estados de error, pruebas y observabilidad sin secretos. |
| Demo | 25 % | Recorrido funcional de extremo a extremo, práctica en vivo y video; confirmar requisitos exactos en el portal. |

Las reglas indican aplicación y aceptación previas, máximo 20.000 participantes aceptados y una sola categoría por proyecto. La categoría indie admite individuales, estudiantes y equipos de hasta cuatro; la de startup tiene condiciones para su representante. La página del evento anuncia cierre de solicitudes el 25 de octubre; el envío de proyectos está previsto para el **4 de noviembre de 2026, 9:00 p. m. ET**, que ese día equivale a **9:00 p. m. en Bogotá**. Verificar cambios directamente en el portal.

Las reglas indican que el participante conserva la propiedad de su entrega, pero concede a los organizadores y entidades indicadas una licencia amplia, mundial, perpetua, irrevocable, gratuita y no exclusiva para usar y explotar la entrega. También indican que los materiales compartidos en el evento no son confidenciales y contemplan derechos sobre grabaciones. Revisar las condiciones completas antes de compartir código, información comercial o una entrega. No inferir que el código previo sea elegible: las reglas revisadas exigen obra original y derechos sobre los componentes, pero no encontramos una cláusula clara sobre cuándo debe haberse escrito; confirmar con la organización y documentar el trabajo anterior.

Los participantes seleccionados reciben, según las reglas, USD 150 en créditos de Meta Model API durante una ventana de desarrollo de diez días, sujetos a sus términos. No se ha comprobado que esta cuenta tenga esos créditos. La aceptación al evento, sus condiciones, los campos de entrega, la duración del video y visibilidad exigida para el repositorio siguen sin verificarse para este equipo.

## Lo que ya tenemos

- App Meta `Pendiva`: número sandbox disponible y un `hello_world` aceptado por Meta tras actualizar el token. Entrega al teléfono pendiente de confirmación. Callback y suscripción comprobados; un texto del teléfono autorizado llegó mediante webhook firmado.
- [Panel local](../src/static/live.html), [servidor](../src/live_app.py) y [pipeline](../src/live_pipeline.py) sin conversaciones precargadas en una base nueva. El [arranque unificado](../scripts/iniciar_demo.py) levanta panel y receptor aislado. Nebius analizó el texto ficticio recibido y generó una recomendación con evidencia válida. Muse respondió a una prueba separada con datos ficticios; falta comprobarlo con una conversación de WhatsApp autorizada. Las pruebas automatizadas simulan proveedores.
- [Smoke test de Cloud API](../scripts/whatsapp_test_smoke.py) ejecutado con aceptación de Meta; spike de Embedded Signup separado y sin prueba de Coexistence.
- Usuario reportó dos entrevistas y una señal de interés. El VPS existe según lo informado por el usuario; no se ha desplegado el prototipo actual.

## Flujo técnico propuesto

```text
Teléfono de prueba autorizado
   → número sandbox WhatsApp de Meta
   → webhook HTTPS verificado y suscrito
   → persistencia + deduplicación por ID de mensaje
   → Muse Spark (Meta Model API) con salida estructurada
   → validación de evidencia y estado de análisis
   → panel Pendiva: conversación → sugerencia → revisión humana
```

Separar mensajes entrantes, salientes y estados de entrega. Usar el cuerpo original para comprobar la firma del webhook según documentación vigente; no procesar solicitudes que fallen la verificación. Responder y procesar eventos de forma idempotente; no volver a llamar al modelo por reintentos duplicados. Evitar inferir pérdida por silencio, confirmar pagos o ejecutar acciones automáticamente. El análisis debe referirse a IDs de mensajes existentes: validar cada referencia en servidor y mostrar el texto fuente original; ello no garantiza que la interpretación sea correcta. Usar resultado estructurado con esquema y tratar texto de mensajes como datos no confiables.

El envío de una plantilla de prueba y la recepción de un mensaje son pruebas diferentes. Un HTTP exitoso de la API no demuestra entrega: verificar el estado y el teléfono. No habilitar envío automático ni conectar el número comercial existente durante esta demo. Obtener consentimiento antes de procesar o mostrar mensajes de terceros y enviar su contenido a Muse; para la demo usar mensajes que el propietario del teléfono de prueba consienta compartir.

## Fases y criterios de salida

### 1. Accesos y primera llamada real

1. Verificar aceptación y reglas de entrega del evento; confirmar categoría y acceso/condiciones de créditos.
2. En Meta Model API, el usuario crea o configura su propia clave de forma segura. Confirmar modelo, límites y coste. No pedir que comparta la clave por chat.
3. El usuario genera el token del entorno de WhatsApp y selecciona/verifica un destinatario propio o consentido. Es distinto de la clave de Muse.
4. Ejecutar una única llamada a Muse con datos sintéticos y el adaptador existente; registrar éxito, modelo, latencia, consumo disponible y resultado, sin secretos. Probar el smoke test de WhatsApp con destinatario autorizado y verificar entrega.

**Salida:** una llamada real a Muse y un mensaje de prueba de WhatsApp comprobados por separado, o error concreto documentado. Sin credenciales, aceptación/condiciones de servicio o autorización requerida, no simular éxito ni conectarse a cuentas.

### 2. Recepción fiable de WhatsApp

Implementar endpoint de verificación GET y recepción POST, verificar firma, limitar tamaño, validar payload, persistir identificadores y tiempo, deduplicar eventos, reconocer sólo tipos admitidos y registrar eventos no soportados de forma segura. Añadir pruebas para firma inválida, mensajes repetidos, eventos de estado, errores y recuperación tras reinicio.

Preparar callback público HTTPS y suscripción de prueba siguiendo los pasos y requisitos vigentes de Meta. **El despliegue/configuración externa requiere autorización específica**; el VPS y Docker son el destino previsto. Comprobar recepción desde el teléfono consentido sin asumir historial anterior.

**Salida:** mensaje de texto real de prueba visible en la base y panel una sola vez, con hora, remitente y estado verificables.

### 3. Muse real y evidencia

Adaptar el cliente existente para analizar la conversación recibida, con control de datos autorizados, entrada acotada y salida con esquema: resumen, señal, incertidumbre, siguiente paso e IDs de evidencia. Enviar sólo lo necesario, solicitar `store: false` donde corresponda y revisar condiciones de Meta para datos y retención; eso por sí solo no constituye una garantía general de privacidad. Validar estructura e IDs antes de guardar. Añadir límites de costo, timeout, errores visibles, reintentos acotados y protección contra instrucciones maliciosas en mensajes.

Preparar un conjunto sintético de evaluación con cotización, objeción, promesa, pago declarado, texto ambiguo y entrada adversarial; medir evidencia válida y resultados revisados manualmente. Añadir prueba real controlada con datos consentidos.

**Salida:** resultado real de Muse para la conversación de prueba, con fuente enlazada y sin confirmar pagos o inventar ventas. Registrar errores y resultados de evaluación, no sólo casos favorables.

### 4. Panel y recorrido de demo

Sustituir datos preparados en el recorrido principal por datos persistidos del sandbox. Mostrar conexión, origen, última recepción, estado de análisis y errores; filtrar casos, abrir detalle y marcar revisado o corregir. Los ejemplos sintéticos deben identificarse. Mantener una forma de reiniciar la demostración sin borrar datos reales.

**Salida:** usuario ve una conversación real de prueba y revisa una recomendación de Muse; la interfaz distingue información verificada, sugerencias y cobertura parcial.

### 5. Seguridad, ensayo y entrega

Para una demo compartida, añadir autenticación, aislamiento mínimo, HTTPS, límites de acceso, secretos fuera de Git, registros sin datos sensibles y estrategia de borrado/retención. En Hostinger usar Docker y revisar TLS, respaldo y despliegue sólo con autorización; no exponer el `http.server` local como servicio público. Probar reconexión, duplicados, caída del modelo y fallo de webhook. Registrar qué está listo para demo y qué falta para producción.

Ensayar el flujo, preparar un video y paquete de entrega según portal oficial, documentar uso verificable de Muse y fuentes, y revisar derechos/licencias antes de enviar. Ninguna cifra de impacto o entrevista se inventará.

**Salida:** demo repetible, métricas de evaluación reales, video y entrega conformes al portal; confirmación del usuario antes de publicar o enviar.

## Secuencia orientativa hasta el 4 de noviembre

| Fecha | Resultado buscado |
|---|---|
| 27–28 oct | Accesos; una llamada real a Muse y smoke test de WhatsApp, si hay credenciales y autorizaciones. |
| 29–30 oct | Webhook, persistencia e idempotencia; autorización y preparación del endpoint HTTPS. |
| 31 oct–1 nov | Conectar mensajes recibidos a Muse; validación estructurada y evaluación sintética/adversarial. |
| 2 nov | Panel conectado, revisión humana, manejo de errores y controles mínimos. |
| 3 nov | Ensayo, grabación, revisión de derechos y requisitos de entrega. |
| 4 nov | Verificación final y entrega por el usuario antes de las 9:00 p. m. Bogotá, sujeto a reglas vigentes. |

Son objetivos, no compromisos; accesos y requisitos pueden cambiar la ruta crítica.

## Fuentes técnicas oficiales

- [Quickstart de Meta Model API](https://dev.meta.ai/docs/quickstart): credencial, endpoint y modelo Muse Spark.
- [Salida estructurada de Meta Model API](https://dev.meta.ai/docs/structured-output): formato estructurado y esquemas soportados.
- [WhatsApp Cloud API de Meta](https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api) y [webhooks](https://www.postman.com/meta/whatsapp-business-platform/folder/lboq68h/webhooks): revisar documentación vigente y permisos antes de implementar o publicar el callback.
