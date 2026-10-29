# Investigación y decisiones de alcance

## Decisiones resueltas

### Interfaz principal

**Decisión:** construir el asistente conversacional sobre recuperación estructurada y métricas
deterministas, no sobre una conversación libre que consulte directamente toda la base.

**Razón:** permite respuestas rápidas y fáciles para el dueño, reduce alucinaciones y conserva
trazabilidad. El modelo recibirá sólo el contexto seleccionado por el sistema.

**Alternativas consideradas:** chat libre sobre SQLite (rechazado por riesgo de datos mezclados y
respuestas no reproducibles); sólo dashboards (rechazado porque exige aprender CRM).

### Importación financiera

**Decisión:** mantener CSV exportado desde Excel como primera versión y dejar `.xlsx` nativo como
decisión posterior.

**Razón:** el prototipo no tiene dependencias externas, CSV evita macros y mantiene pruebas
reproducibles. La UI puede explicar el formato requerido.

**Alternativas consideradas:** `openpyxl` (requiere dependencia y validación de archivos); lectura
de hojas arbitrarias (riesgo de ambigüedad de columnas y fórmulas).

### Calidad de IA

**Decisión:** separar extracción, validación, analítica y explicación.

**Razón:** una respuesta lingüísticamente convincente no prueba que una fecha, precio, cita o
recomendación sea correcta. Las reglas permiten auditar y comparar proveedores.

### Multiempresa

**Decisión:** diseñar tenant_id en las entidades antes de agregar más funcionalidades de CRM.

**Razón:** introducirlo tarde obliga a migrar todas las consultas y aumenta el riesgo de fuga de
datos. La autenticación de contraseña única actual sólo es apropiada para demo privada.

## Incertidumbres que requieren decisión del producto

- Segmento inicial y campos obligatorios por servicio.
- Moneda y zona horaria por tenant.
- Retención y borrado de conversaciones y archivos financieros.
- Si una importación financiera representa un reemplazo completo o un periodo incremental.
- Qué roles necesita el primer equipo de asesores.
- Qué proveedores IA pueden recibir datos y bajo qué consentimiento.
- Política para mostrar métricas cuando faltan mensajes salientes o historial.

## Evidencia existente y límites

- El repositorio ya tiene webhook firmado, recomendaciones con evidencia, asistente con recuperación
  limitada, autenticación local opcional e importación CSV.
- La integración real comprobada es un sandbox de Meta y un análisis con Nebius sobre texto ficticio.
- No existe evidencia de Coexistence, historial completo, multiempresa real ni calidad general del
  modelo.
- Las entrevistas reportadas son una señal inicial, no validación suficiente de segmento o precio.

