# Spike local de WhatsApp Embedded Signup

**Objetivo:** comprobar si Meta presenta a una persona el inicio de sesión y el onboarding de WhatsApp Business desde un botón propio, y leer los IDs/números que el negocio comparte al terminar.

## Qué implementa

- Carga el Facebook JavaScript SDK e inicia `FB.login` usando el App ID y el `config_id` configurado en Meta.
- Recibe el código OAuth en el navegador y lo envía al servidor local. El servidor intercambia el código con Meta y consulta los números de la WABA compartida.
- Muestra los IDs/nombres/números devueltos. El token se mantiene en memoria durante esa petición y se descarta; no se guarda en disco ni en Git.
- El servidor se enlaza sólo a `127.0.0.1`; no hay almacenamiento, webhook público ni envío de mensajes.

El código está en [`spikes/meta_embedded_signup/`](../../spikes/meta_embedded_signup/). Es una prueba diagnóstica temporal, no una conexión reutilizable del producto. No supone que el número sea elegible para Coexistence.

## Configuración requerida en Meta

Meta describe Embedded Signup como onboarding para Solution Partners, Tech Providers y Tech Partners. Su colección oficial indica configurar el SDK de Facebook Login, completar la revisión y Advanced Access para uso con negocios fuera del entorno de prueba, integrar las operaciones requeridas y servir los endpoints con HTTPS. El panel de Meta genera el `config_id`; no se inventa en el código.

En Meta for Developers, desde una app de tipo negocio controlada por ti:

1. Añade WhatsApp Business Platform y Facebook Login for Business.
2. Crea una configuración de Embedded Signup para WhatsApp y activa el flujo que permite incorporar un número que ya usa WhatsApp Business App (Coexistence). La disponibilidad de esa opción depende de que Meta habilite el producto/configuración para la app.
3. Añade el dominio permitido para el SDK, la URL de retorno válida y permisos requeridos por la configuración. Para ofrecerlo a otros negocios, completa App Review y Advanced Access según el panel/documentación de Meta.
4. Anota el App ID, `config_id`, App Secret y versión Graph vigente. El App Secret se configura únicamente como variable local del servidor. Si el asistente oficial presenta un objeto `extras` para el flujo habilitado, se puede pasar como JSON por la variable local `META_EMBEDDED_SIGNUP_EXTRAS`; usa la estructura actual que proporciona Meta, sin copiar secretos.

Un flujo estándar de Embedded Signup puede mostrar una selección/registro de activo nuevo y no ofrecer el número de Business App existente. Si Meta no ofrece la ruta de Coexistence, cancela el flujo; no elijas opciones que indiquen reemplazo, migración o desconexión de la app.

## Ejecutar localmente en Windows PowerShell

Abre PowerShell en la raíz del repositorio. Define estos valores sólo en la sesión actual; no guardes el App Secret en archivos, chat ni Git:

```powershell
$env:META_APP_ID = "ID_DE_APP"
$env:META_EMBEDDED_SIGNUP_CONFIG_ID = "CONFIG_ID"
$env:META_APP_SECRET = "SECRETO_DE_APP"
$env:META_GRAPH_VERSION = "vNN.N"
# Opcional: copia sólo extras no secretos de la configuración oficial vigente.
# $env:META_EMBEDDED_SIGNUP_EXTRAS = '{"featureType":"..."}'
python spikes/meta_embedded_signup/server.py
```

Abre `http://127.0.0.1:8765`. Pulsa **Continuar con Meta** y selecciona sólo tu propio negocio/número para la prueba. El estado termina con los IDs y números que Meta compartió, o un error genérico sin imprimir respuestas que puedan contener datos sensibles. Presiona `Ctrl+C` para cerrar el servidor.

Este servidor es local y HTTP para la primera comprobación. Meta exige HTTPS para un flujo de Embedded Signup integrado en una web pública; si el SDK o la configuración rechazan localhost, hace falta un dominio HTTPS de desarrollo permitido en la app. Este spike no crea un túnel, no despliega en Hostinger y no modifica DNS.

## Criterio de prueba

1. El botón abre la ventana de inicio de sesión de Meta con la configuración de la app.
2. Meta permite elegir y compartir una cuenta/número existente de WhatsApp Business App.
3. El callback devuelve autorización y el backend obtiene el ID de WABA y los números compartidos.
4. El número sigue accesible desde WhatsApp Business App después del flujo.

Si el paso 2 no aparece, es un bloqueo de disponibilidad/configuración/elegibilidad de Meta o del proveedor; el botón por sí solo no lo resuelve. Si 1–3 funcionan pero el 4 no, detén la prueba y no reintentes sobre esa línea hasta entender la indicación de Meta.

## Límites y seguridad

- El spike no almacena el token, WABA, número ni una relación persistente de la cuenta. Reiniciar el proceso no conserva conexión alguna.
- El App Secret y token nunca se devuelven al navegador ni se registran. El intercambio real no se ha probado todavía porque no hay App ID/config ID/secret configurados.
- Completar Embedded Signup puede dejar concedido a la app de Meta acceso a los activos aunque este spike descarte el token. El descarte no revoca permisos ni desconecta el número; al terminar, retira el acceso desde la configuración de integraciones empresariales de Meta si no deseas conservarlo.
- No se envían mensajes ni se crean webhooks. Después de validar el onboarding, el producto necesita diseño de persistencia cifrada, tenant/usuario autenticado, desconexión y manejo de webhooks antes de conservar credenciales o datos.
- Una prueba correcta de Embedded Signup no demuestra historial completo, eventos `smb_message_echoes`, compatibilidad de dispositivos, ni elegibilidad general de clientes.
- No pruebes con una línea con conversaciones críticas o sin respaldo. Sigue las pantallas y advertencias de Meta; cancela si propone una migración que no entiendes.

## Fuentes oficiales vigentes consultadas

- [Meta: Embedded Signup, colección oficial](https://www.postman.com/meta/whatsapp-business-platform/documentation/du6gzjv/embedded-signup): propósito, SDK, permisos, revisión/acceso avanzado, endpoints requeridos y HTTPS.
- [Meta: colección oficial de WhatsApp Business Platform](https://www.postman.com/meta/whatsapp-business-platform/overview): Cloud API, Business Management API y Embedded Signup.
- [Meta for Developers: Embedded Signup](https://developers.facebook.com/docs/whatsapp/embedded-signup/): verificar requisitos y el código/configuración que muestra actualmente el dashboard antes de usar una app real.
