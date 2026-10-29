# Plan de implementación: Inteligencia comercial conversacional para servicios

**Fecha:** 2026-10-28  
**Estado:** propuesta de implementación por fases  
**Base:** [MVP](../product/mvp.md), [roadmap](../roadmap.md), [plan de producto para hackathon](../plan-producto-hackathon.md)

## Resumen

Evolucionar Pendiva desde un panel de conversaciones y recomendaciones hacia una capa de
inteligencia comercial que:

1. Organice contactos, conversaciones, oportunidades, cotizaciones, citas, pagos y actividades
   como entidades relacionadas, sin perder el mensaje original como evidencia.
2. Se adapte a distintos negocios de servicios mediante configuración de sector, servicios y
   campos de cotización, sin asumir un CRM complejo.
3. Detecte con reglas reproducibles dónde se pierden oportunidades: respuesta tardía, cotización
   ausente, seguimiento vencido, cita no confirmada, pago por verificar o margen deteriorado.
4. Cruce los hallazgos de WhatsApp con ventas y gastos importados.
5. Ofrezca un asistente conversacional de lenguaje natural que explique el estado del negocio,
   responda preguntas y proponga acciones en pocos segundos, siempre con evidencia, cobertura y
   límites explícitos.
6. Proteja los datos con usuarios, empresas, roles, sesiones y aislamiento por tenant antes de
   compartir la aplicación.

La IA no será la fuente única de verdad. La extracción asistida por modelo será validada por
reglas, métricas deterministas y corrección humana. El sistema nunca marcará una venta perdida por
silencio, nunca confirmará un pago sin evidencia y no inferirá ingresos o rentabilidad fuera de
los datos importados.

## Requisitos

- **REQ-001:** El sistema debe modelar contactos separados de conversaciones y permitir que un
  contacto tenga varias oportunidades.
- **REQ-002:** El sistema debe modelar oportunidades de servicios con etapa, servicio, valor,
  próxima acción, responsable, estado y evidencia.
- **REQ-003:** El sistema debe extraer y mostrar datos de cotización, agenda, precio, pagos,
  compromisos y datos faltantes con estado `confirmado`, `inferido` o `pendiente`.
- **REQ-004:** El sistema debe conservar el mensaje fuente y permitir corregir cualquier dato
  extraído sin borrar la evidencia original.
- **REQ-005:** El sistema debe soportar etapas configurables para varios negocios de servicios y
  campos específicos por servicio.
- **REQ-006:** El sistema debe detectar fugas del embudo comercial y medir tiempos de respuesta,
  cotización, seguimiento, confirmación y pago con periodo y denominador explícitos.
- **REQ-007:** El sistema debe importar datos de ventas y gastos desde CSV exportado desde Excel,
  validarlos y asociarlos opcionalmente a servicio, categoría y periodo.
- **REQ-008:** El sistema debe producir recomendaciones explicables que combinen evidencia de
  WhatsApp y evidencia financiera, sin afirmar causalidad no demostrada.
- **REQ-009:** El dueño debe poder hablar con un asistente en lenguaje natural para pedir resumen,
  contexto, prioridades, fallas del embudo y acciones concretas sin conocer conceptos de CRM.
- **REQ-010:** Cada respuesta del asistente debe mostrar fuentes, periodo, cobertura, datos faltantes
  y acciones sugeridas; el modelo no puede ejecutar envíos ni cambios automáticamente.
- **REQ-011:** El asistente debe entender consultas sobre contactos, oportunidades, cotizaciones,
  citas, ventas, gastos, márgenes y pendientes, con recuperación de la conversación relevante.
- **REQ-012:** El sistema debe ofrecer autenticación, sesiones seguras, empresas, roles y
  aislamiento de datos antes de uso multiempresa.
- **REQ-013:** El sistema debe registrar correcciones humanas, análisis, proveedor, modelo,
  latencia, versión de instrucciones y resultado validado para medir calidad.
- **REQ-014:** El sistema debe funcionar con WhatsApp como canal operativo y declarar límites de
  historial, mensajes salientes, multimedia y cobertura del proveedor.

## Contexto técnico actual

**Lenguaje/runtime:** Python 3.12+, biblioteca estándar, servidor `http.server`.  
**Persistencia actual:** SQLite local en [live_pipeline.py](../../src/live_pipeline.py).  
**Interfaz actual:** HTML/CSS/JavaScript sin framework en [live.html](../../src/static/live.html).  
**Proveedores IA:** Muse/Meta, NVIDIA y Nebius mediante contratos estructurados.  
**Integración:** webhook firmado de Meta, deduplicación y almacenamiento de mensajes entrantes.  
**Finanzas existentes:** CSV con ventas/gastos y alertas deterministas en [finance.py](../../src/finance.py).  
**Asistente existente:** recuperación acotada de mensajes y preguntas con evidencia en
[business_assistant.py](../../src/business_assistant.py).  
**Restricción:** el sistema actual es un prototipo local de una sola instancia; SQLite, contraseña
única y `http.server` no deben presentarse como SaaS productivo.

## Principios de diseño

1. **Evidencia antes que interpretación:** cada dato y recomendación debe apuntar a mensajes,
   registros financieros o correcciones humanas.
2. **CRM invisible:** el dueño habla en lenguaje cotidiano; las entidades estructuradas se crean
   detrás de la interfaz y pueden corregirse desde el detalle.
3. **Hechos, inferencias y pendientes separados:** la interfaz debe etiquetar su origen.
4. **No convertir ausencia en conclusión:** silencio no significa pérdida; pago declarado significa
   pago por verificar.
5. **IA híbrida:** el modelo extrae y explica; reglas y consultas calculan y validan.
6. **Tenant-aware desde el modelo:** ninguna consulta debe depender sólo de ocultar datos en UI.
7. **Cobertura honesta:** toda métrica indica periodo, denominador, fuente y límites.
8. **No automatizar acciones externas:** la IA recomienda; una persona confirma cambios o envíos.

## Plan por fases

### Fase 0 — Contrato de dominio y configuración sectorial

**Requisitos:** REQ-001, REQ-002, REQ-003, REQ-005, REQ-014  
**Objetivo:** definir el lenguaje común antes de extraer datos.

1. Crear tablas y contratos para `tenants`, `users`, `contacts`, `conversations`,
   `opportunities`, `quotes`, `appointments`, `payments`, `activities`, `services`,
   `business_profiles` y `evidence_links`.
2. Definir estados y transiciones: consulta, información pendiente, por cotizar, cotización
   enviada, negociación, cita por confirmar, cita agendada, servicio realizado, pago por
   verificar, ganada, perdida confirmada y sin clasificar.
3. Crear configuración sectorial editable: moneda, zona horaria, etapas, servicios, campos
   requeridos y reglas de seguimiento.
4. Mantener compatibilidad con los datos actuales y migrar sin borrar `live_messages`.

**Salida:** modelo versionado y fixtures de al menos dos tipos de servicio.

### Fase 1 — Identidad, tenants y seguridad de acceso

**Requisitos:** REQ-012, REQ-014  
**Objetivo:** pasar de contraseña única a acceso controlado.

1. Crear usuarios, empresas, roles `owner`, `manager`, `advisor` y `viewer`.
2. Reemplazar la contraseña global por credenciales de usuario, sesiones revocables y expiración.
3. Asociar cada mensaje, contacto, oportunidad, finanza y análisis a un tenant.
4. Añadir autorización por operación, protección CSRF para mutaciones, límite de intentos y
   auditoría de accesos/correcciones.
5. Mantener el webhook fuera de la sesión del navegador, pero resolver tenant por configuración
   de conexión verificada.

**Salida:** pruebas de aislamiento que demuestren que un tenant no puede leer ni modificar otro.

### Fase 2 — Contactos y oportunidades desde WhatsApp

**Requisitos:** REQ-001, REQ-002, REQ-003, REQ-004, REQ-014  
**Objetivo:** convertir mensajes en memoria comercial estructurada.

1. Crear un normalizador de contacto por teléfono y herramientas para fusionar duplicados.
2. Crear una oportunidad por solicitud comercial, sin asumir que una conversación equivale a una
   sola venta.
3. Implementar extracción estructurada de servicio, ubicación, fecha, precio, intención, etapa,
   compromiso y campos faltantes.
4. Validar fechas, monedas, precios y estados con reglas; guardar confianza como evidencia del
   origen, no como una cifra inventada.
5. Mostrar cada atributo junto con sus mensajes fuente y permitir aceptar, editar o rechazar.

**Salida:** una conversación con varias solicitudes puede generar varias oportunidades y ninguna
conclusión queda sin evidencia.

### Fase 3 — Cotizaciones, agenda y operación del servicio

**Requisitos:** REQ-002, REQ-003, REQ-004, REQ-005, REQ-008  
**Objetivo:** cubrir el ciclo operativo de negocios de servicios.

1. Modelar cotización con precio, moneda, vigencia, fecha de envío, estado y evidencia.
2. Modelar cita con fecha propuesta, fecha confirmada, duración, dirección, responsable y estado.
3. Detectar citas sin confirmación, datos de visita faltantes, conflictos y cotizaciones sin
   seguimiento.
4. Crear agenda interna móvil antes de integrar calendarios externos.
5. Registrar pago declarado como `por_verificar` y permitir confirmación manual.

**Salida:** el dueño puede ver qué servicio se pidió, qué falta para cotizar, qué está agendado y
qué requiere confirmación.

### Fase 4 — Embudo y analítica de fallas

**Requisitos:** REQ-006, REQ-008, REQ-014  
**Objetivo:** explicar dónde se está perdiendo valor comercial.

1. Construir consultas deterministas del embudo: consultas, datos completos, cotizaciones,
   seguimientos, citas, servicios y pagos.
2. Calcular tiempos de respuesta y envejecimiento con mensajes disponibles.
3. Detectar fugas: solicitud sin respuesta, cotización no enviada, cotización envejecida, cita
   no confirmada, servicio sin pago verificado y oportunidades sin próxima acción.
4. Mostrar denominador, periodo, cobertura y ejemplos concretos por cada hallazgo.
5. Generar recomendaciones con formato `hallazgo`, `por qué importa`, `acción`, `evidencia`,
   `dato faltante` y `limitación`.

**Salida:** una recomendación puede explicar qué etapa falla sin declarar causalidad no demostrada.

### Fase 5 — Finanzas cruzadas con ventas y gastos

**Requisitos:** REQ-007, REQ-008, REQ-014  
**Objetivo:** conectar desempeño comercial y resultado financiero.

1. Mejorar el importador para soportar categorías, servicio, moneda y periodo con validación.
2. Permitir reemplazar una importación identificada sin duplicar registros.
3. Calcular ventas, gastos, resultado, gasto/venta, tendencia mensual y datos sin categoría.
4. Cruzar servicio/categoría financiera con oportunidades, cotizaciones y volumen de consultas
   cuando exista una clave explícita.
5. Señalar discrepancias entre ventas reportadas y oportunidades sin convertirlas en conversión
   implícita.

**Salida:** el dueño ve qué está pasando en conversaciones y finanzas, con fuentes separadas y
recomendaciones de revisión.

### Fase 6 — Asistente conversacional “habla con Pendiva”

**Requisitos:** REQ-009, REQ-010, REQ-011, REQ-008, REQ-014  
**Objetivo:** permitir que el dueño obtenga contexto y decisiones sin aprender CRM.

1. Crear una capa de intención para clasificar preguntas: resumen, prioridades, cliente,
   cotización, agenda, embudo, finanzas, comparación de periodos y recomendación.
2. Recuperar entidades estructuradas, métricas deterministas y evidencia relevante antes de
   llamar al modelo.
3. Implementar respuestas cortas por defecto, con opción “ver detalle” y lenguaje no técnico.
4. Responder preguntas como:
   - “¿Qué está fallando en mi negocio?”
   - “¿A quién debo atender hoy?”
   - “¿Qué cotizaciones no he seguido?”
   - “¿Qué servicio vende más y cuál deja menos resultado?”
   - “¿Qué información me falta para cotizar?”
   - “Dame el resumen de esta semana.”
5. Mostrar cada respuesta con periodo, fuentes, cobertura, datos faltantes y acciones; permitir
   abrir la conversación, oportunidad o registro financiero citado.
6. Permitir voz como interfaz posterior: transcripción revisable, consentimiento y misma respuesta
   estructurada que el canal escrito.
7. Impedir que el asistente envíe mensajes, cambie estados o confirme pagos sin acción humana.

**Salida:** el dueño puede preguntar en lenguaje cotidiano y recibir una respuesta accionable en
formato breve, sustentada en datos reproducibles.

### Fase 7 — Calidad de análisis y aprendizaje por corrección

**Requisitos:** REQ-003, REQ-004, REQ-008, REQ-010, REQ-013  
**Objetivo:** medir y mejorar la calidad, no sólo la validez del JSON.

1. Crear fixtures anotados por sector y casos difíciles: precio, pago declarado, ambigüedad,
   prompt injection, múltiples servicios, fechas y mensajes multimedia.
2. Medir extracción de entidades, evidencia correcta, etapa, recomendación útil, falsos positivos
   y falsos negativos.
3. Registrar proveedor, modelo, instrucciones, latencia, errores y correcciones humanas.
4. Comparar recomendaciones aceptadas, editadas y descartadas por tipo.
5. Versionar prompts y reglas con migraciones de esquema compatibles.

**Salida:** un reporte de calidad por sector y proveedor, separado de las pruebas de conectividad.

### Fase 8 — Migración de prototipo a SaaS desplegable

**Requisitos:** REQ-012, REQ-013, REQ-014  
**Objetivo:** preparar el producto para uso controlado sin fingir que el prototipo ya es producción.

1. Separar dominios de ingesta, dominio comercial, analítica, asistente y autenticación.
2. Evaluar PostgreSQL para datos multiempresa y worker para análisis asíncrono.
3. Añadir backups, retención, borrado por tenant, observabilidad sin contenido privado y healthchecks.
4. Configurar HTTPS, secretos externos, límites de carga y política de despliegue.
5. Ejecutar revisión de seguridad y pruebas de recuperación antes de conectar cuentas reales.

**Salida:** decisión documentada de despliegue, checklist de seguridad y límites explícitos.

## Tareas ejecutables

### Setup y fundaciones

- [ ] T001 [Plan:0.1] Definir migraciones SQLite compatibles para tenants, usuarios, contactos, oportunidades, cotizaciones, citas, pagos, actividades y evidencias en `src/live_pipeline.py`.
- [ ] T002 [P] [Plan:0.2] Crear configuración sectorial y fixtures de dos negocios de servicios en `src/service_profiles.py`.
- [ ] T003 [P] [Plan:0.3] Añadir validadores de estados, moneda, fecha, precio y origen de evidencia en `src/domain_validation.py`.
- [ ] T004 [Plan:1.1,1.2] Implementar usuarios, roles, sesiones revocables y autorización por tenant en `src/auth.py` y `src/live_app.py`.
- [ ] T005 [Plan:1.3,1.4] Añadir tenant_id, auditoría de mutaciones y protección CSRF a las operaciones de `src/live_pipeline.py` y `src/live_app.py`.

### US1 — Memoria comercial estructurada

- [ ] T006 [US1] [Plan:2.1] Normalizar contactos por teléfono y fusionar duplicados en `src/customer_memory.py`.
- [ ] T007 [US1] [Plan:2.2,2.3] Crear oportunidades y extracción estructurada con evidencia en `src/opportunity_pipeline.py`.
- [ ] T008 [P] [US1] [Plan:2.4] Validar atributos extraídos y estados confirmado/inferido/pendiente en `src/domain_validation.py`.
- [ ] T009 [US1] [Plan:2.5] Exponer edición, aceptación y rechazo de atributos con auditoría en `src/live_app.py` y `src/static/live.html`.

### US2 — Cotización y agenda

- [ ] T010 [US2] [Plan:3.1,3.2] Implementar cotizaciones, citas y pagos por verificar en `src/service_operations.py`.
- [ ] T011 [US2] [Plan:3.3,3.4] Crear agenda interna, conflictos y pendientes operativos en `src/live_pipeline.py` y `src/static/live.html`.
- [ ] T012 [US2] [Plan:3.5] Añadir corrección humana y transición segura de pagos declarados a verificados en `src/live_app.py`.

### US3 — Analítica comercial

- [ ] T013 [US3] [Plan:4.1,4.2] Implementar métricas deterministas de embudo, tiempos y envejecimiento en `src/commercial_analytics.py`.
- [ ] T014 [US3] [Plan:4.3,4.4] Implementar detector de fugas con denominadores, periodos y cobertura en `src/commercial_analytics.py`.
- [ ] T015 [US3] [Plan:4.5] Renderizar hallazgos y recomendaciones explicables en `src/static/live.html`.

### US4 — Finanzas cruzadas

- [ ] T016 [US4] [Plan:5.1,5.2] Extender importación financiera con identificador de archivo, servicio, moneda y reemplazo idempotente en `src/finance.py`.
- [ ] T017 [US4] [Plan:5.3,5.4] Calcular métricas por servicio/categoría y cruzarlas sólo cuando exista clave explícita en `src/finance.py` y `src/commercial_analytics.py`.
- [ ] T018 [US4] [Plan:5.5] Mostrar discrepancias, fuentes y limitaciones financieras en `src/static/live.html`.

### US5 — Asistente conversacional

- [ ] T019 [US5] [Plan:6.1,6.2] Clasificar intención y construir contexto determinista desde entidades, métricas y evidencias en `src/business_assistant.py`.
- [ ] T020 [US5] [Plan:6.3,6.4] Implementar respuestas breves para resumen, prioridades, embudo, finanzas y cotizaciones en `src/business_assistant.py`.
- [ ] T021 [US5] [Plan:6.5] Mostrar fuentes, periodo, cobertura, datos faltantes y enlaces de navegación en `src/static/live.html`.
- [ ] T022 [US5] [Plan:6.6,6.7] Mantener voz revisable y bloquear acciones externas automáticas en `src/voice.py` y `src/live_app.py`.

### US6 — Calidad y confianza

- [ ] T023 [US6] [Plan:7.1,7.2] Crear dataset sintético anotado y evaluadores de entidades, evidencia y recomendaciones en `tests/fixtures/analysis_cases.json` y `tests/test_analysis_quality.py`.
- [ ] T024 [US6] [Plan:7.3,7.4] Registrar trazabilidad de análisis y correcciones humanas en `src/analysis_trace.py`.
- [ ] T025 [US6] [Plan:7.5] Versionar prompts, reglas y resultados sin guardar secretos en `src/analysis_trace.py`.

### Pulido y transición

- [ ] T026 [Plan:8.1] Separar módulos de ingesta, dominio comercial, analítica, asistente y autenticación sin cambiar los contratos actuales.
- [ ] T027 [P] [Plan:8.2,8.3] Documentar decisión SQLite/PostgreSQL, backups, retención, borrado y observabilidad en `docs/decisions/008-saas-runtime.md`.
- [ ] T028 [P] [Plan:8.4,8.5] Ejecutar revisión de seguridad, aislamiento, recuperación y configuración de despliegue en `tests/` y `docs/validation/`.

## Estructura objetivo

```text
src/
  live_app.py                 # HTTP y autorización
  live_pipeline.py            # compatibilidad de ingesta y persistencia temporal
  auth.py                     # usuarios, sesiones, roles, tenant
  customer_memory.py          # contactos y oportunidades
  opportunity_pipeline.py     # extracción estructurada y evidencia
  service_operations.py       # cotizaciones, agenda, pagos
  commercial_analytics.py     # embudo, tiempos y fugas
  finance.py                  # importación y métricas financieras
  business_assistant.py       # interfaz conversacional fundamentada
  analysis_trace.py           # trazabilidad y calidad
  service_profiles.py         # configuración por sector
  domain_validation.py        # invariantes y estados
  static/live.html            # panel y asistente
tests/
  fixtures/analysis_cases.json
  test_domain_model.py
  test_commercial_analytics.py
  test_finance.py
  test_assistant.py
  test_tenant_isolation.py
docs/
  plan-inteligencia-comercial/
```

## Estrategia de validación

- **Tipo de aplicación:** servidor HTTP local + webhook + interfaz HTML + proveedor IA opcional.
- **Viaje 1:** un mensaje genera contacto, oportunidad y datos faltantes con evidencia.
- **Viaje 2:** una cotización, cita y pago declarado atraviesan revisión humana sin marcar pago
  confirmado automáticamente.
- **Viaje 3:** una consulta sin seguimiento aparece en el embudo con denominador y periodo.
- **Viaje 4:** ventas/gastos importados producen una alerta financiera explicable.
- **Viaje 5:** el dueño pregunta “¿qué está fallando?” y recibe resumen corto con enlaces y
  limitaciones.
- **Viaje 6:** dos tenants no pueden leer, modificar ni usar evidencia del otro.
- **Pruebas sintéticas:** deterministas, anonimizadas y separadas de llamadas reales.
- **Pruebas reales:** sólo con credenciales autorizadas y texto ficticio; registrar proveedor,
  latencia y resultado sin guardar claves.
- **Criterio de aceptación:** ninguna recomendación sin fuente; ninguna métrica sin periodo y
  denominador; ningún tenant cruzado; ninguna acción externa ejecutada por la IA.

## Decisiones pendientes

1. Confirmar si el primer despliegue multiempresa usará PostgreSQL o SQLite endurecido para una
   sola instancia.
2. Confirmar el sector inicial y los campos obligatorios con entrevistas reales.
3. Definir si los archivos financieros se importarán sólo como CSV o también como `.xlsx` nativo.
4. Elegir proveedor principal de IA después de comparar calidad, latencia, costo y retención.
5. Confirmar política legal de datos y retención antes de conectar clientes reales.

## Requirement Mapping

| REQ ID | Descripción | Plan items | Implementación prevista |
|---|---|---|---|
| REQ-001 | Contactos separados de conversaciones | 0.1, 2.1 | `customer_memory.py`, migraciones |
| REQ-002 | Oportunidades estructuradas | 0.1, 2.2 | `opportunity_pipeline.py` |
| REQ-003 | Cotizaciones, agenda, pagos y datos faltantes | 2.3, 3.1 | `service_operations.py`, validadores |
| REQ-004 | Evidencia y corrección humana | 2.4, 2.5, 7.4 | `evidence_links`, auditoría |
| REQ-005 | Configuración para varios sectores | 0.2, 3.3 | `service_profiles.py` |
| REQ-006 | Analítica de embudo y tiempos | 4.1–4.4 | `commercial_analytics.py` |
| REQ-007 | Ventas y gastos desde Excel/CSV | 5.1–5.3 | `finance.py` |
| REQ-008 | Recomendaciones cruzadas explicables | 4.5, 5.4, 6.2 | analítica + asistente |
| REQ-009 | Asistente en lenguaje natural | 6.1–6.4 | `business_assistant.py` |
| REQ-010 | Fuentes, límites y no automatización | 6.5–6.7 | UI, API y validadores |
| REQ-011 | Preguntas sobre CRM invisible y finanzas | 6.1–6.4 | recuperación estructurada |
| REQ-012 | Autenticación y multiempresa | 1.1–1.5 | `auth.py`, tenant guards |
| REQ-013 | Calidad y trazabilidad | 7.1–7.5 | fixtures, trace y métricas |
| REQ-014 | WhatsApp y cobertura honesta | 0.4, 2.4, 8.4 | webhook, cobertura y documentación |

