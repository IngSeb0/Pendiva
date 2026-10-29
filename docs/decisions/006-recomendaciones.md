# ADR 006: recomendaciones con evidencia y revisión humana

**Estado:** implementado localmente, pendiente de validación real. Fecha: 2026-10-27.

## Decisión

Cada negocio de la instancia local puede guardar un perfil editable. El modelo recibe ese contexto y hasta los últimos 50 mensajes de una conversación únicamente después de una confirmación explícita para el proveedor seleccionado. Puede devolver hasta ocho recomendaciones, cada una con acción, motivo, prioridad y uno o más IDs de mensajes. El servidor valida formato, límites y referencias, y no ejecuta ni envía acciones. El operador puede completar, descartar o dejar pendiente cada recomendación y guardar una nota.

Se vinculan los análisis a una huella de los mensajes y del perfil. Un cambio durante el análisis rechaza el resultado; un cambio posterior lo marca obsoleto y deshabilita su revisión. La adaptación de resultados antiguos es en memoria y no destruye la base existente.

## Consecuencias y límites

El panel inicia sin datos inventados. Los identificadores de evidencia válidos no prueban que el razonamiento sea correcto: hace falta evaluación humana y pruebas con conversaciones consentidas. No hay agregación empresarial avanzada, medición de ingresos reales ni soporte multiempresa. SQLite guarda datos sin cifrar y el servidor carece de autenticación: se limita a uso local y no es apto para exponerse. Política de retención, control de acceso y TLS son requisitos antes de una demo compartida.

Meta usa salida estructurada y `store: false`; NVIDIA usa un esquema solicitado en el prompt y validación del servidor, sin asumir equivalencia de sus políticas de datos. No existe cambio automático de proveedor. El código y las pruebas de integración simulada no demuestran una llamada real ni conformidad para el concurso. Consultar [Meta Structured Output](https://dev.meta.ai/docs/structured-output) y [NVIDIA Nemotron API](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-super-120b-a12b-infer).

## Actualización: Nebius

El proveedor de inferencia para la cuenta del usuario es Nebius Token Factory. Su adaptador usa consentimiento específico, la variable `NEBIUS_API_KEY` y el modelo Nemotron. Las pruebas son simuladas y la llamada real sigue pendiente; ver [guía de Nebius](../validation/nebius.md).
