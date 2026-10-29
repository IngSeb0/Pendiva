# ADR 007 — Operación de la demo sandbox

**Fecha:** 2026-10-28. **Alcance elegido por el usuario:** demo de hackathon con sandbox, únicamente Pendiva.

## Decisión

Arrancar el panel local y el receptor aislado mediante `python -m scripts.iniciar_demo`. Ambos leen la misma configuración y base SQLite. El panel escucha en loopback en el puerto 8000; el receptor en 8772 acepta exclusivamente `/webhooks/meta`. `--tunnel` reutiliza el ejecutable local de cloudflared y publica sólo el segundo puerto. Los procesos se detienen con Ctrl+C y un fallo del túnel se informa al operador.

Antes de arrancar se validan proveedor, secretos presentes, puertos distintos y coincidencia entre el emisor del smoke test y el número esperado por el receptor. Esto comprueba configuración, no vigencia de credenciales. `--check-model` realiza una llamada real con una única cotización ficticia; guarda sólo proveedor, modelo, fecha y número de recomendaciones en `data/model-check-<proveedor>.json`. No lee ni precarga conversaciones reales.

`scripts.configurar_webhook` inspecciona la suscripción existente usando el App Secret local sin mostrarlo. `--apply` toma la URL de `data/demo-runtime.json`, valida el desafío público, comprueba que el panel y sus APIs den 404 y que un POST sin firma dé 403. Sólo permite la app Pendiva `889989257436890`, conserva los campos suscritos y verifica el resultado con otra lectura. No da de alta números comerciales ni publica la app. El usuario pidió configurar la demo; el uso del túnel ya había sido autorizado.

SQLite registra fecha y contadores de entregas con firma válida, separándolos del número de textos nuevos. Un reintento incrementa entregas pero no duplica el mensaje. Un evento de estado puede actualizar la recepción sin crear conversación. No se guardan cuerpos de eventos en los registros operativos. El panel informa este alcance y el límite de los últimos 50 mensajes por análisis.

## Evidencia y límites

- Meta aceptó un `hello_world` del sandbox el 28 de octubre; la aceptación no comprueba entrega al teléfono.
- Un texto ficticio enviado desde el teléfono autorizado llegó realmente por el webhook, se guardó una vez y fue analizado con Nebius con autorización explícita. El resultado incluyó una recomendación con evidencia válida y quedó pendiente de decisión humana. Esto no mide calidad general ni acredita uso de Muse.
- Muse Spark se validó por separado con una cotización ficticia y luego, con autorización explícita, con el mensaje ficticio recibido realmente por WhatsApp. Ambas respuestas incluyeron una recomendación con evidencia válida. Se solicitó `store: false`; el panel conservó Nebius. Ver [validación de Muse](../validation/muse.md).
- El perfil comercial de Pendiva está incompleto y su app sigue en desarrollo. El MCP omite los números de prueba; una consulta directa mostró que faltaba la suscripción de Pendiva a la cuenta sandbox. La suscripción se añadió y se confirmó el 28 de octubre; después se recibió el texto real de prueba.
- El analizador sustituye los IDs originales de WhatsApp por alias temporales antes de enviarlos al proveedor y los resuelve de vuelta localmente; el texto y la fecha aún se comparten con el proveedor al autorizar el análisis.
- No se conecta un negocio cliente, no se configura una línea comercial ni se presenta Coexistence como validada. F01 sigue sin evidencia comercial suficiente. Esta excepción de demo no completa las fases productivas F03–F15.
- Cloudflare Quick Tunnel es temporal, cambia de hostname al reiniciar, no garantiza disponibilidad, admite hasta 200 solicitudes simultáneas y no admite SSE. Tras reiniciar `--tunnel`, actualizar y verificar de nuevo el callback. Mantener el equipo y el proceso activos durante la demo.

## Fuentes oficiales revisadas

- [Ejemplo oficial Nebius Nemotron 3 Super](https://github.com/nebius/token-factory-cookbook/blob/main/models/nemotron/nemotron3-super-120B.md): endpoint y nombre del modelo verificados el 2026-10-28.
- [Quick Tunnels de Cloudflare](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/): operación y límites, consultados el 2026-10-28.
- [Colección oficial Meta Cloud API](https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api) y [referencia de suscripciones de apps](https://developers.facebook.com/docs/graph-api/reference/app/subscriptions/). La página de creación de endpoints de Meta devolvió HTTP 429 al consultarla; no se tomó ese error como validación. La configuración se contrastó con lecturas reales de Graph y del MCP de Meta.
