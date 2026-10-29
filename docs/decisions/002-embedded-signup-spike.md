# ADR 002 — Spike local de Embedded Signup

- **Estado:** aceptado para diagnóstico local; no autoriza despliegue ni almacenamiento de credenciales.
- **Fecha:** 2026-10-23.
- **Motivo:** el usuario pidió probar un botón similar a la conexión de WhatsApp Business que ha visto en Make, usando una línea propia.

## Decisión

Preparar un harness mínimo separado del producto. Abre el flujo `FB.login` configurado por Meta, recibe el código en el servidor, intercambia el código y consulta la lista de teléfonos de la WABA. El token sólo vive durante la petición y se descarta. El servidor escucha en `127.0.0.1` y no contiene persistencia ni envío de mensajes.

## Razones y límites

- Embedded Signup permite una experiencia guiada de autorización, pero no elimina la configuración de app/configuración/permiso ni la revisión que Meta exige para ofrecerlo a negocios.
- La app debe tener habilitada la ruta de onboarding de un número de WhatsApp Business App para probar Coexistence. Si esa ruta no aparece para la app/cuenta/número, el flujo no se considera viable todavía.
- No se incorporó credencial ni proveedor real; no se puede completar la prueba end-to-end hasta disponer de Meta App ID, config ID, App Secret, versión Graph soportada y origen autorizado.
- No se eligió un proveedor, no se desplegó, no se modificó el VPS ni se guardaron datos de la línea.

## Consecuencias

El spike permite separar el problema del botón/UI de la habilitación comercial y técnica que controla Meta. Antes de integrarlo en el SaaS, las fases de arquitectura/identidad deben diseñar almacenamiento cifrado por empresa, controles de acceso, desconexión, consentimiento y webhooks. La validación con un número propio no autoriza a conectar números de clientes.

## Referencias

- [Colección oficial de Meta Embedded Signup](https://www.postman.com/meta/whatsapp-business-platform/documentation/du6gzjv/embedded-signup)
- [Documentación de Meta Embedded Signup](https://developers.facebook.com/docs/whatsapp/embedded-signup/)
