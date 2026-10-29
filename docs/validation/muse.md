# Validación de Muse Spark para Pendiva

**Corte:** 28 de octubre de 2026, hora de Bogotá. La clave de Meta Model API la configuró el usuario localmente y no se incluye en esta evidencia.

Se realizaron dos solicitudes reales con la misma cotización ficticia y sin enviar la conversación de WhatsApp ni datos de clientes. La primera llegó al proveedor, pero el analizador obtuvo un `JSONDecodeError`; no se guardaron metadatos suficientes para establecer su causa. Después se ajustaron el esfuerzo de razonamiento y el límite de salida. La segunda completó y Pendiva validó estructura e IDs de evidencia:

| Dato | Resultado de la segunda solicitud |
|---|---|
| Proveedor y modelo | Meta Model API, `muse-spark-1.3` |
| Estado | `completed`; una recomendación validada |
| Entrada | Texto y negocio ficticios, IDs temporales |
| Latencia observada | 2,64 segundos |
| Consumo reportado | 322 tokens de entrada y 365 de salida, incluidos 126 de razonamiento; 687 en total |
| Almacenamiento | Se solicitó `store: false` y Meta lo reflejó en la respuesta |

El ajuste fue `reasoning.effort: minimal` y `max_output_tokens: 4096`. La documentación de Meta explica que el límite incluye tanto razonamiento como salida visible; esto hace plausible una salida incompleta con presupuestos pequeños, pero no prueba la causa del primer fallo. La respuesta todavía se valida en el servidor: un esquema válido no garantiza que una recomendación sea correcta.

Para repetir la prueba con la clave ya presente en `.env`:

```powershell
python -m scripts.iniciar_demo --check-model --provider meta
```

Hace una llamada real y puede consumir créditos. El resultado guarda sólo metadatos en `data/model-check-meta.json`; no añade mensajes ficticios a la base ni modifica el proveedor de la demo en ejecución. Las pruebas anteriores permanecen en `data/muse-check.json` si existen. `PENDIVA_AI_PROVIDER=nebius` sigue siendo la configuración seleccionada para el panel principal.

## Mensaje de prueba recibido desde WhatsApp

El 28 de octubre de 2026, con autorización explícita para Meta Model API, se analizó con Muse el único mensaje ficticio recibido del teléfono sandbox autorizado. Se envió el texto, su fecha y un ID temporal; no se envió el número de teléfono, el ID real de WhatsApp ni contexto adicional del negocio.

Meta devolvió una respuesta `completed` en 1,78 segundos, con `store: false`, 305 tokens de entrada y 339 de salida. Pendiva validó una recomendación y su referencia al mensaje, y comprobó que la conversación no cambió durante la solicitud. La recomendación sugiere pedir detalles de los equipos, la ubicación y el horario antes de elaborar la cotización. El resultado sanitizado se guardó localmente en `data/muse-whatsapp-check.json`, excluido de Git.

Esta prueba usó el analizador de Pendiva directamente con el mensaje guardado. No cambió el proveedor del panel ni sobrescribió el análisis de Nebius. Para completar la demo de Muse en el panel falta seleccionar Muse en una instancia de la aplicación y realizar allí una revisión humana con el consentimiento correspondiente. La demo con Nebius se documenta en [live-sandbox.md](live-sandbox.md).

Fuentes oficiales revisadas el 2026-10-28: [inicio rápido de Meta Model API](https://dev.meta.ai/docs/quickstart), [Responses API](https://dev.meta.ai/docs/protocols/responses) y [salida estructurada](https://dev.meta.ai/docs/structured-output).
