# ADR 004 — Ingesta real de prueba y análisis de Muse

**Estado:** implementado para pruebas locales, no validado contra Meta. **Fecha:** 2026-10-27.

## Decisión

Mantener la demo anterior intacta y añadir un servidor local distinto que inicia sin conversaciones ni resultados inventados. Recibir mensajes de texto por Cloud API, autenticar las entregas mediante firma HMAC sobre bytes originales, restringir el número mediante Phone Number ID y deduplicar por ID. Guardar mensajes y sugerencias de una sola instancia en SQLite. La persona selecciona una conversación y confirma su envío a Muse Spark; la salida estructurada incluye IDs de evidencia, que se validan contra el lote enviado. Si llegan mensajes durante la llamada, se rechaza guardar la respuesta obsoleta. No se envían mensajes de WhatsApp ni se ejecutan acciones automáticamente.

## Motivos y límites

El alcance permite validar el recorrido real sin simular un SaaS terminado. El servicio funciona sólo como desarrollo o prueba local: carece de autenticación, aislamiento por empresa, cifrado de base de datos, trabajos en cola, respaldo y observabilidad de producción. SQLite almacena conversaciones en texto claro. El webhook no se ha publicado y la firma, payload y análisis no se han probado con Meta real; las pruebas usan fixtures y respuestas simuladas. El indicador de configuración sólo refleja presencia de variables, no conectividad o credenciales válidas.

Una conexión pública para la hackathon requiere autorización específica, HTTPS, exponer exclusivamente el callback, y antes diseñar autenticación, privacidad, aislamiento, protección de red y operación de datos. El número de prueba no verifica Coexistence ni historial. El procesamiento con Muse requiere consentimiento de quienes aporten mensajes y puede generar costos. Se solicita `store: false`; verificar condiciones y retención del proveedor.

## Referencias revisadas

- [Ejemplo de Meta para firma de webhooks](https://github.com/fbsamples/whatsapp-api-examples/tree/main/signature-validation-with-webhooks-payloads) y [webhooks de WhatsApp](https://www.postman.com/meta/whatsapp-business-platform/folder/lboq68h/webhooks).
- [Responses API de Meta Model API](https://dev.meta.ai/docs/protocols/responses) y [salida estructurada](https://dev.meta.ai/docs/structured-output).
