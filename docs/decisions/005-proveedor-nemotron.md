# ADR 005 — Alternativa Nemotron mediante NVIDIA

**Fecha:** 2026-10-27. **Estado:** implementada y probada con respuestas simuladas; sin validación real con NVIDIA.

El usuario quiere avanzar con una API distinta mientras no dispone de Muse. Pendiva acepta `PENDIVA_AI_PROVIDER=nvidia` con `NVIDIA_API_KEY` y envía solicitudes al endpoint hospedado por NVIDIA con el modelo `nvidia/nemotron-3-super-120b-a12b`. El valor por defecto sigue siendo `meta`; no existe conmutación automática entre proveedores. La clave nunca aparece en la interfaz, ni se almacena en Git.

El panel debe identificar el proveedor elegido y exigir consentimiento para ese destinatario; un consentimiento para Meta no autoriza enviar conversaciones a NVIDIA. La prueba inicial envía una frase neutral, no conversaciones. NVIDIA puede cobrar o consumir créditos según la cuenta. Consultar su política de datos y obtener autorización antes de enviar conversaciones reales.

La ruta de Meta solicita JSON Schema en Responses API y `store: false`; la de NVIDIA pide JSON en el prompt y valida los campos y referencias en el servidor. No se presume que el modelo cumpla el esquema: cualquier JSON inválido, campo inesperado o referencia inventada provoca error. La validación estructural no demuestra que una conclusión sea correcta. No se ha probado todavía una respuesta real de NVIDIA ni la calidad comercial del modelo.

Probar con NVIDIA no equivale a demostrar uso de Muse. La [convocatoria de Meta](https://dev.meta.ai/events/global-hackathon) promueve el uso de sus modelos y las reglas oficiales ponderan el uso de sus herramientas de IA; verificar requisitos aplicables para la entrega. Para una demostración con Meta hace falta acceso y una prueba real por separado.

Fuentes consultadas: [catálogo NVIDIA Nemotron](https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b?nim=hosted&section=deploy), [referencia de la API NVIDIA](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-super-120b-a12b-infer) y [documentación Meta Model API](https://dev.meta.ai/docs/quickstart).
