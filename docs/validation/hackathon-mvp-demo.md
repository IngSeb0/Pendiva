# Prototipo local para hackathon

**Actualizado:** 2026-10-27  
**Estado:** implementado localmente; validación automatizada y navegador local; no desplegado.

## Qué contiene

- Panel responsivo de actividad comercial.
- Cinco casos de una empresa ficticia, con conversaciones, contexto, evidencia y pasos sugeridos.
- Clasificación por reglas de frases de cotización/precio, objeción de precio, pago por verificar y seguimiento prometido.
- Mensaje de evidencia y una sugerencia revisable junto a cada etiqueta.
- Búsqueda, filtros y estado de revisión manual persistido en SQLite.
- Formulario que acepta un contacto/mensaje sintético y muestra una señal basada en reglas.
- Adaptador opcional a Muse Spark para analizar sólo los casos ficticios empaquetados; sus pruebas usan respuestas simuladas y no se ha hecho una llamada real.
- API local, persistencia SQLite y modo Docker Compose.

La clasificación es determinista, basada en frases explícitas, y declara el método (`reglas_demo`). Una etiqueta sugiere revisión; no confirma pérdida, pago o conversión.

## Cómo ejecutar

Local, Python 3.12 o más reciente, sin dependencias externas:

```powershell
python -m src.mvp_app
```

Visita `http://localhost:8000`. Para detener, `Ctrl+C`.

Docker:

```powershell
docker compose up --build
```

Visita `http://localhost:8000`; detener con `docker compose down`. Los datos locales del volumen se conservan al bajar el servicio. El puerto sólo se publica en `127.0.0.1`.

Pruebas:

```powershell
python -m unittest discover -v
```

## Límites del demo

- No conecta la app Meta, el número de prueba ni WhatsApp Business App.
- No envía mensajes de WhatsApp ni recibe webhooks. El adaptador Meta lee una clave desde el entorno del proceso y no la guarda.
- No utilizar conversaciones reales en el formulario.
- No hay login ni separación entre empresas; no desplegar en VPS ni exponer públicamente.
- Los casos de inicio y todo registro añadido desde la interfaz deben ser datos de demo.

## Análisis opcional con Meta Model API

Con `MODEL_API_KEY` configurada al arrancar Python, el botón del detalle envía únicamente la conversación ficticia seleccionada al modelo `muse-spark-1.3` mediante `POST https://api.meta.ai/v1/responses`. El adaptador solicita `store: false`, limita la respuesta y valida que el índice de evidencia corresponda a un mensaje del caso. La evidencia se recupera del texto original; esto no garantiza que la interpretación del modelo sea correcta. Sin clave no se hace ninguna llamada. Las solicitudes pueden consumir créditos o generar cobros según la cuenta. El resultado no se persiste y exige revisión humana.

La conexión todavía no se ha probado con credenciales reales. Referencias oficiales consultadas el 2026-10-27: [Quickstart de Meta Model API](https://dev.meta.ai/docs/quickstart) y [Responses API](https://dev.meta.ai/docs/protocols/responses). Meta Model API y WhatsApp Cloud API usan configuraciones distintas.

## Estado del sandbox Meta

El 2026-10-23 Meta devolvió un error al solicitar el número de prueba. **Actualización 2026-10-27:** la app `Pendiva` muestra el número y Phone Number ID como completados; el token figuraba sin generar y no había destinatario seleccionado. La UI mostró un endpoint de Graph API `v25.0`, pero no se invocó ni se envió un mensaje de prueba. Ver [plan actualizado](../plan-hackathon-muse-whatsapp.md).

La página de prueba también permite seleccionar un destinatario verificado y una plantilla una vez provisionado el número. Continuar sólo cuando se muestre un número, un destinatario autorizado y el botón habilitado. Nunca guardar el token de acceso en Git, el navegador de demo o el historial de terminal; usar variables secretas fuera del repositorio cuando se integre.

## Decisión técnica

Ver [ADR 003](../decisions/003-hackathon-prototype.md). El backend estándar es deliberadamente temporal y de una instancia; no reemplaza el diseño de la arquitectura SaaS. El modo de demo no equivale a una prueba de Meta.
