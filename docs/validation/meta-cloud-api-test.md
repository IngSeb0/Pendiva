# Prueba de WhatsApp Cloud API con recursos de test de Meta

**Objetivo:** comprobar un envío básico de plantilla desde un número de test proporcionado por Meta hacia un destinatario de prueba autorizado. Esto valida el acceso básico a Cloud API, no Coexistence.

## Qué ofrece la prueba

La colección oficial de Meta documenta el `Test WhatsApp Business Account`, llamadas de Cloud API y el envío de `hello_world` al `Phone-Number-ID` del emisor. El número de test pertenece al entorno de desarrollo de Meta; no es un número real del negocio ni permite probar por sí solo la convivencia con WhatsApp Business App.

## Pasos en Meta

1. Inicia sesión en [Meta for Developers](https://developers.facebook.com/) con una cuenta que controles y abre la app `Pendiva`.
2. En **Casos de uso → Conectar en WhatsApp → Paso 1. Pruébalo**, usa **Solicitar número de prueba**. Meta debe provisionar el número y mostrar Phone Number ID y token temporal.
3. Usa el número de test y el `Phone Number ID` que aparecen en ese panel. Sigue el asistente para agregar y verificar el número de destinatario de prueba. Usa un teléfono propio o de una persona que haya aceptado recibir el mensaje.
4. Copia el token temporal que genera el panel sólo a una variable de entorno local. No lo pegues en conversaciones, tickets, archivos ni commits.
5. Ejecuta primero el modo seco desde la raíz del proyecto:

   ```powershell
   python scripts/whatsapp_test_smoke.py
   ```

   Debe informar que no envió ninguna solicitud.

6. Configura las variables de entorno en esa sesión local. `WHATSAPP_TEST_GRAPH_VERSION` debe ser una versión vigente aceptada por Meta; la pantalla de prueba de Pendiva mostró `v25.0` el 2026-10-23, pero sigue la que indique el panel. Las otras variables corresponden a los valores mostrados por Meta y al destinatario autorizado.

   ```powershell
   $env:WHATSAPP_TEST_GRAPH_VERSION = "vNN.N"
   $env:WHATSAPP_TEST_PHONE_NUMBER_ID = "ID_DEL_NUMERO_DE_TEST"
   $env:WHATSAPP_TEST_ACCESS_TOKEN = "TOKEN_TEMPORAL"
   $env:WHATSAPP_TEST_RECIPIENT = "57XXXXXXXXXX"
   ```

7. Cuando quieras generar un único mensaje al destinatario configurado, ejecuta explícitamente:

   ```powershell
   python scripts/whatsapp_test_smoke.py --send
   ```

   El script usa el template aprobado `hello_world`, oculta el cuerpo de errores para no filtrar datos y muestra el ID de mensaje si Meta acepta la solicitud. “Aceptado por Meta” no garantiza entrega al dispositivo.

8. Cierra la sesión de terminal o elimina las variables cuando termines. Los tokens temporales caducan; genera otro desde el panel si hace falta.

## Alcance y límites

- El smoke test sólo prueba la aceptación de un envío saliente por Cloud API. Se ejecutó contra Meta el 2026-10-28; la entrega al dispositivo no se confirmó por separado.
- El callback HTTPS, el campo `messages` y la suscripción de la cuenta sandbox de Pendiva se comprobaron el 2026-10-28. Un texto enviado desde el teléfono autorizado llegó al panel. Operación y límites: [guía del sandbox](live-sandbox.md).
- Esto no prueba que una línea con WhatsApp Business App sea elegible para Coexistence, ni mensajes escritos desde la app (`smb_message_echoes`), historial, sincronización de contactos, desconexión o cobertura completa.
- Para esos casos hace falta una cuenta/número de test elegible para Coexistence, acceso al proveedor que se evalúa y autorización específica antes de conectar o enviar mensajes.
- El 2026-10-28 se ejecutó el smoke test desde la configuración local de la app `Pendiva`. Meta aceptó el envío de `hello_world` al destinatario sandbox configurado y devolvió un ID de mensaje. No se guardó el ID para evitar retener datos del destinatario. La aceptación no confirma entrega al teléfono. Un mensaje entrante independiente sí fue recibido, guardado y analizado. Esto no valida Coexistence ni historial. Ver [plan actualizado](../plan-hackathon-muse-whatsapp.md).

## Fuentes oficiales consultadas

- [Colección oficial de WhatsApp Cloud API de Meta](https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api): `Test WhatsApp Business Account`, endpoint de mensajes y ejemplo `hello_world`.
- [Descripción oficial de WhatsApp Business Platform de Meta](https://www.postman.com/meta/whatsapp-business-platform/overview): distingue Cloud API, Embedded Signup y APIs relacionadas.
- Consultar la página **API Setup / Getting Started** de la app y la [documentación actual de Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api/) antes de configurar permisos, versión de Graph o webhooks; estos detalles pueden cambiar.
