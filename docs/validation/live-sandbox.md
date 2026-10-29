# Operar la demo sandbox de Pendiva

**Corte: 2026-10-28. Alcance elegido por el usuario: demo de hackathon con sandbox, sólo Pendiva.**

Una base nueva parte vacía. El 2026-10-28 se recibió un texto ficticio desde el teléfono autorizado mediante Meta, se guardó una sola vez y, con autorización explícita del usuario, Nebius generó una recomendación con evidencia validada. La recomendación permanece pendiente. Meta también aceptó un `hello_world`, cuya entrega al teléfono no se confirmó por separado. Esto no valida Coexistence ni constituye una entrega de SaaS comercial.

## Arranque

Requiere Python 3.12+, el archivo privado `.env` y cloudflared para la URL temporal. No requiere paquetes Python externos. No sobrescribas un `.env` que ya tiene tus claves; `.env.example` describe los nombres disponibles.

```powershell
python -m scripts.iniciar_demo --check
python -m scripts.iniciar_demo --tunnel
```

Para una presentación reproducible con datos sintéticos realistas, inicia el modo demo:

```powershell
python -m scripts.iniciar_demo --demo
```

Carga cinco clientes ficticios con conversaciones de cotización, objeción de precio, pago por
verificar, cita pendiente e información incompleta. También carga recomendaciones con IDs de
evidencia, ventas y gastos de dos meses. El comando imprime las credenciales temporales de
`demo@pendiva.local`. Para combinarlo con WhatsApp, usa `--demo --tunnel`: el número configurado
queda asociado al tenant demo y los eventos firmados entrantes se convierten en mensajes y
contactos dentro de ese mismo tenant. Los datos no representan clientes reales.

El primer comando valida la configuración sin solicitudes externas. El segundo inicia dos servicios que comparten `data/live.sqlite3`:

| Servicio | Dirección | Acceso |
|---|---|---|
| Panel | http://127.0.0.1:8000 | Sólo este equipo |
| Receptor | http://127.0.0.1:8772/webhooks/meta | Sólo esta ruta se publica mediante Cloudflare |

El comando imprime la URL temporal y guarda el estado en `data/demo-runtime.json`, excluido de Git. Mantén esa terminal y el equipo activos. Ctrl+C detiene ambos servidores y el túnel. Sin `--tunnel`, ambos servicios quedan sólo en local. Las variables `PENDIVA_PORT`, `PENDIVA_WEBHOOK_PORT` y `PENDIVA_LIVE_DB` permiten cambiar puertos o base; los puertos deben ser distintos. El launcher conserva los datos existentes.

Desde otra terminal, actualiza el callback de la app Pendiva después de cada reinicio del túnel:

```powershell
python -m scripts.configurar_webhook
python -m scripts.configurar_webhook --apply
```

El primer comando es de lectura. El segundo comprueba el desafío público, que las rutas del panel devuelvan 404 y que un POST sin firma devuelva 403 antes de cambiar la URL. Conserva los eventos ya suscritos y lee de nuevo Graph para confirmar. Sólo admite la app Pendiva `889989257436890`; no crea cuentas ni da de alta números comerciales. No muestra el App Secret ni el token de verificación. No uses esta herramienta para alterar otro negocio.

Para consultar la suscripción de la cuenta sandbox ya identificada y, sólo si hace falta, suscribirla a la app Pendiva:

```powershell
python -m scripts.verificar_sandbox
python -m scripts.verificar_sandbox --subscribe
```

La primera llamada es de lectura. La segunda valida el token y comprueba que el número configurado pertenece a la cuenta sandbox de Pendiva antes de suscribir; si ya está suscrita, no modifica nada. No admite otra app ni otra cuenta. El 28 de octubre se detectó que faltaba la suscripción; se añadió y la lectura posterior la confirmó.

La URL cambia en cada Quick Tunnel. El uso de Cloudflare para esta prueba ya fue autorizado por el usuario; el tráfico del webhook pasa por ese proveedor. El túnel no tiene garantía de disponibilidad y admite hasta 200 solicitudes simultáneas. La [documentación oficial](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) lo destina a pruebas y desarrollo.

## Variables

| Variable | Uso |
|---|---|
| `WHATSAPP_PHONE_NUMBER_ID` | Identificador del emisor sandbox esperado por el webhook; debe coincidir con `WHATSAPP_TEST_PHONE_NUMBER_ID`. |
| `WHATSAPP_APP_SECRET` | Secreto de la app Pendiva para verificar firmas y gestionar su callback. |
| `WHATSAPP_VERIFY_TOKEN` | Secreto de verificación compartido con la configuración de webhook de Meta. |
| `WHATSAPP_APP_ID` | App Pendiva; el configurador está restringido a `889989257436890`. |
| `PENDIVA_AI_PROVIDER` | `nebius`, `meta` o `nvidia`; sin cambio automático de proveedor. |
| `NEBIUS_API_KEY` | Requerida para el proveedor actual `nebius`. |
| `MODEL_API_KEY` | Sólo para `meta` / Muse. Distinta del token de WhatsApp. |
| `NVIDIA_API_KEY` | Sólo para el proveedor alternativo `nvidia`. |

El token de WhatsApp `WHATSAPP_TEST_ACCESS_TOKEN` se usa para el script saliente y para consultar o configurar la suscripción sandbox; el destinatario `WHATSAPP_TEST_RECIPIENT` sólo se usa en el envío. Ninguno hace falta para recibir mensajes ni analizar con Nebius. El servidor lee `.env` al arrancar; las variables de la sesión prevalecen. Reinicia después de cambiar credenciales del servidor. `.env` y `data/` están excluidos de Git y de la imagen Docker.

## Comprobar IA sin datos de clientes

```powershell
python -m scripts.iniciar_demo --check-model
python -m scripts.iniciar_demo --check-model --provider meta
```

Cada comando hace **una llamada real** con una cotización completamente ficticia y puede consumir créditos. El primero usa el proveedor configurado y el segundo prueba Muse sin cambiar la demo. Se validan estructura e IDs de evidencia mediante el analizador del panel. Se guardan sólo metadatos en `data/model-check-<proveedor>.json`; no se insertan ejemplos en la base. Nebius y Muse se verificaron por separado el 2026-10-28. Posteriormente, con autorización explícita, Muse también analizó el mensaje de prueba recibido por WhatsApp, en una comprobación separada del panel Nebius. Esto no mide calidad general. Ver [validación de Muse](muse.md).

Antes de enviar mensajes al proveedor, Pendiva sustituye los IDs originales de WhatsApp por alias temporales y resuelve la evidencia de vuelta en el equipo local. El texto, las fechas y el contexto del negocio sí se envían al proveedor cuando se confirma el análisis; los alias no anonimizan el contenido escrito.

Los scripts anteriores `iniciar_nebius_privado`, `iniciar_nemotron_privado` e `iniciar_muse_privado` se conservan para introducir claves mediante prompt oculto; no arrancan por sí solos el receptor aislado ni el túnel.

## Ensayo real desde el teléfono

1. Abre el panel local y completa el contexto del negocio de demostración. Usa datos ficticios si se va a grabar o compartir la pantalla.
2. Desde el teléfono que figura como destinatario autorizado en la página de pruebas de la app Pendiva, escribe al número sandbox **+1 555-150-1569**: «Hola, necesito una cotización de mantenimiento para dos equipos la próxima semana».
3. Pulsa **Actualizar**. Debe aparecer una conversación con ese texto una sola vez. El indicador informa fecha de la última recepción con firma válida y número de textos guardados. Tener claves configuradas no significa que haya llegado un mensaje; un evento de estado tampoco crea una conversación.
4. Selecciona la conversación y confirma que puedes enviar sus mensajes y el contexto al proveedor que indica el panel. Pulsa **Analizar** y revisa resumen, recomendaciones, incertidumbre y mensajes de evidencia.
5. Marca una recomendación como completada o descartada, añade una nota y actualiza: debe conservarse. Un mensaje nuevo o un cambio de contexto vuelve obsoleto el análisis anterior.

Sólo se muestran y analizan los últimos 50 mensajes de cada conversación. No se importa historial previo. Las recomendaciones requieren revisión humana y no confirman ingresos ni pagos. La validación de IDs evita referencias inexistentes, pero no garantiza que la interpretación sea correcta.

## Si el mensaje no aparece

- Comprueba que el proceso de la demo y el túnel sigan activos. Repite la lectura de `scripts.configurar_webhook` y compara el callback con `data/demo-runtime.json`.
- Si cambió la URL del túnel, vuelve a aplicar el callback. El script comprueba aislamiento y firma antes de cambiar Meta.
- Comprueba que el teléfono sea un destinatario autorizado del sandbox en la página de pruebas de la app Meta. Esa lista se gestiona allí; el MCP de Meta omite los números públicos de prueba y no permite administrarla.
- Comprueba el evento `messages` y ejecuta `python -m scripts.verificar_sandbox` para consultar la suscripción de la cuenta de prueba. El MCP sólo muestra las cuentas comerciales: una lista vacía allí no prueba que la cuenta sandbox esté sin suscripción.
- El perfil comercial de Pendiva sigue incompleto y la app está en desarrollo. Esto limita el paso a un número comercial; no se debe interpretar como ausencia del sandbox. El perfil se completa en https://business.facebook.com/settings/info/?business_id=1009950238795771 con datos verdaderos del titular, nunca inventados.
- No imprimas cuerpos de errores ni claves para diagnosticar. Los scripts emiten estados sanitizados. Las firmas inválidas se rechazan antes de persistir datos.

## Evidencia y pendientes

| Comprobación | Resultado del 2026-10-28 |
|---|---|
| `hello_world` con autorización explícita | Meta aceptó un envío; entrega al teléfono no comprobada |
| Callback de la app Pendiva | Actualizado al túnel de esta sesión y confirmado por lectura de Graph |
| Desafío HTTPS / aislamiento / firma ausente | 200 con desafío correcto / 404 para panel y APIs / 403 para POST sin firma |
| Suscripción de la cuenta de prueba | Pendiva se añadió a la cuenta sandbox y una lectura posterior lo confirmó |
| Nebius con cotización ficticia | Respuesta real validada; una recomendación en la última prueba |
| Pruebas automatizadas | 74 de 74 correctas; proveedores simulados |
| Ensayo HTTP de dos servidores | Desafío, aislamiento, firma, duplicados, consentimiento y revisión persistida correctos en base temporal; modelo simulado |
| Panel | Interfaz abierta; conversación, recomendación y evidencia visibles mediante el navegador integrado |
| Recepción desde teléfono | Un texto de prueba recibido con firma válida y guardado una sola vez; una recomendación de Nebius persistida, pendiente de decisión humana |
| Muse | Prueba ficticia y análisis independiente del mensaje real sandbox completados y validados; mostrarlo y revisarlo en el panel Muse sigue pendiente |
| Coexistence y SaaS comercial | Fuera de esta demo; no validados |

La muestra enviada anteriormente desde el panel de Meta informó éxito; esa muestra no demuestra recepción desde un teléfono. Un intento saliente previo había devuelto HTTP 401 y fue superado por el envío aceptado tras actualizar el token. El MCP oficial quedó autenticado y permite inspeccionar Pendiva, pero sus resultados de onboarding comercial no sustituyen el ensayo sandbox.

La inspección real del token confirmó que pertenece a la app Pendiva y era válido al revisarlo. Su caducidad indicada es el 28 de octubre de 2026 a las 9:00 p. m. Bogotá. El token también permite consultar o configurar la suscripción sandbox; el receptor firmado y Nebius usan credenciales distintas. Un token temporal apareció en la salida de una herramienta al leer Meta; el usuario informó que lo renovó. No se confirmó si el anterior fue revocado. No se guardó el token en Git ni en esta documentación.

El agente puede operar el emisor sandbox mediante Cloud API, pero no tiene acceso al WhatsApp personal del teléfono autorizado. La recepción real se comprobó mediante un envío manual de ese teléfono; no se insertó un evento ficticio en la base principal.

Pruebas automatizadas: `python -m unittest discover`. Los proveedores se simulan en esa suite; el comando `--check-model` es una validación real separada. Arquitectura y límites: [ADR 007](../decisions/007-operacion-demo-sandbox.md). Esta entrega no declara completadas las fases comerciales ni productivas del roadmap.
