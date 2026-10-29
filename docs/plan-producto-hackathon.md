# Pendiva — plan de producto y entrega para la hackathon

**Actualizado:** 28 de octubre de 2026, hora de Bogotá. **Alcance elegido:** demo de hackathon con sandbox, sólo Pendiva. La operación y evidencia actual están en la [guía sandbox](validation/live-sandbox.md). La convocatoria se identifica provisionalmente como Meta Global AI Developer Hackathon; falta confirmar aceptación del equipo y categoría. Las reglas citadas conservan la revisión del 27 de octubre.

## 1. Producto que queremos construir

Pendiva es un **asistente comercial para el dueño y su equipo de ventas**. A partir de conversaciones autorizadas, ayuda a decidir qué hacer ahora, explica por qué y facilita que una persona marque, corrija o descarte la recomendación. El producto debe funcionar con distintos tipos de negocio mediante contexto configurable, sin prometer que todos los sectores o fuentes estén cubiertos desde el primer día.

La experiencia debe responder a tres preguntas en lenguaje cotidiano:

1. **¿A quién debo atender?** Solicitudes, cotizaciones y compromisos que necesitan revisión, con mensaje fuente y contexto.
2. **¿Qué debería hacer?** Varias recomendaciones independientes por conversación cuando exista evidencia; cada una con acción concreta, prioridad explicable y opción de revisar, completar o descartar.
3. **¿Qué está pasando en mi negocio?** Resúmenes y patrones basados en datos disponibles, con periodo, cobertura y fuentes. Si falta evidencia, se explica qué dato hace falta.

El asistente no presupone que el negocio tenga que adoptar un CRM completo. El vendedor trabaja desde una bandeja de prioridades y el dueño ve explicaciones y preguntas útiles; se evita obligarlos a llenar campos para que el producto muestre valor. La configuración de negocio, productos, servicios y reglas debe poder ajustarse sin editar código.

## 2. Evaluación realista de las fases existentes

| Fases del roadmap | Valor actual | Mejora para la hackathon |
|---|---|---|
| F00 auditoría y backlog | Bien como base y registro del trabajo. | Mantener inventario y decisiones; actualizar estados a partir de evidencia real. |
| F01 entrevistas y F02 viabilidad | Bien por atacar riesgo comercial y de plataforma. F01 sólo tiene dos entrevistas reportadas y una señal de interés; F02 tiene número sandbox, pero no una integración real validada. | Ejecutar descubrimiento y pruebas técnicas en paralelo; no presentar el interés como prueba de demanda ni el sandbox como Coexistence. |
| F03 arquitectura y F04 entorno | Necesarios para la seguridad y reproducción. El diseño objetivo no está cerrado y el servidor actual es local. | Elegir una arquitectura mínima, documentarla y asegurar sólo lo necesario para una demo compartida; preparar Hostinger VPS y Docker sin desplegar sin autorización. |
| F05 identidad, F06 onboarding | Indispensables para un SaaS, pero el alta completa de cualquier cliente y permisos de Meta no son supuestos verificables hoy. | Para la hackathon: acceso controlado a una empresa de prueba. Conexión sencilla de otros negocios y Coexistence quedan sujetos a revisión y elegibilidad. |
| F07 ingesta, F08 señales, F09 panel | Son el núcleo del valor y deben avanzar juntos para tener un recorrido visible. | Entregar verticalmente: un mensaje real → varias recomendaciones de Muse → evidencia → decisión humana. |
| F10 resúmenes y consultas | Diferencia a Pendiva de una lista de contactos. | Un resumen útil para el dueño, limitado a hechos y métricas con cobertura demostrada; no inventar ingresos, gastos ni causas. |
| F11 seguridad y F12 despliegue | Correctos como barrera antes de compartir datos o acceso. | Convertirlos en controles desde el principio y una revisión final medible, sin exponer el servidor local actual. |
| F13 piloto, F14 comercialización, F15 expansión | Importantes para después del concurso; dependen de usuarios, conexión y operación reales. | Preparar el camino, sin presentar una demo de sandbox como piloto comercial terminado. |

**Juicio:** el roadmap original es sólido para construir un SaaS de forma ordenada, pero para una hackathon conviene reorganizarlo alrededor de una demostración real y evaluable. No se borran fases ni se declaran completadas por hacer un prototipo.

## 3. Punto de partida y potencial

**Existe:** app Meta con número de prueba generado; panel local sin conversaciones precargadas; código para verificar webhooks, deduplicar mensajes y llamar a Muse con salida estructurada; pruebas automáticas con proveedores simulados; VPS comunicado por el usuario. El usuario informa que ya tiene acceso a Meta Model API. La clave debe introducirla él en una sesión privada.

**Implementado localmente:** perfil editable de negocio, varias recomendaciones independientes por conversación con referencias a mensajes, revisión y notas por recomendación, detección de análisis obsoletos ante cambios, bandeja transversal de prioridades y una vista del dueño con periodo, cobertura y límites explícitos. El panel arranca vacío; las pruebas automatizadas usan servicios simulados.

**Comprobado el 28 de octubre:** Meta aceptó un `hello_world`; una cotización ficticia enviada desde el teléfono autorizado llegó por el callback de Pendiva y Nebius devolvió una recomendación con evidencia válida. El arranque y el ensayo HTTP local usan dos puertos y mantienen el panel fuera del túnel.

**Pendiente:** confirmar entrega del `hello_world` al teléfono, conectar la conversación de WhatsApp a Muse con consentimiento específico, evaluar calidad comercial de las recomendaciones, autenticación para compartir el panel, despliegue estable, multiempresa y Coexistence. Muse respondió correctamente a una prueba real con texto ficticio; H2 y H3 no están cerrados.

**Alternativa temporal:** el proveedor del panel es Nebius Token Factory con Nemotron. Las pruebas reales con texto ficticio funcionaron; Muse también se probó por separado con datos ficticios. Esa evidencia no acredita calidad general. Los adaptadores de NVIDIA directo y Meta siguen disponibles de forma explícita. Ver [ADR 005](decisions/005-proveedor-nemotron.md), [ADR 007](decisions/007-operacion-demo-sandbox.md) y [validación de Muse](validation/muse.md).

**Potencial:** se puede aspirar a una demo competitiva si, antes de la fecha límite, se demuestra un flujo real de principio a fin, se construye una experiencia convincente y se miden aciertos y fallos. Hoy no hay evidencia suficiente para prometer primer lugar, preparación de producción o compatibilidad con cualquier negocio. La ruta crítica es acceso y credenciales → Muse real → webhook real → recomendaciones con evidencia → demo segura y reproducible.

## 4. Convocatoria y criterios

La [página oficial de Meta](https://dev.meta.ai/events/global-hackathon) indica entrega el **4 de noviembre de 2026 a las 9:00 p. m. ET**, equivalente ese día a **9:00 p. m. en Bogotá**; comprobar cambios en el portal. El evento requiere haber sido seleccionado y tiene categorías indie y startup.

Las [reglas oficiales del organizador](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver) ponderan **impacto 30 %**, **uso de IA de Meta 25 %**, **demo 25 %** y **profundidad técnica 20 %**. El equipo debe confirmar admisión, categoría, requisitos exactos de video y entrega y tratamiento del código previo. Las reglas prevén una licencia amplia y perpetua sobre lo entregado y los materiales del evento; revisarla antes de compartir el proyecto. No presentar cifras ficticias o usar datos de clientes sin autorización.

## 5. Etapas propuestas hasta la entrega

Cada etapa contiene su criterio de salida. Las fechas son una guía para un equipo pequeño; no garantizan aprobación de Meta ni un resultado de concurso.

### H0 — Preparación y prueba real de Muse · 27–28 de octubre

**Objetivo:** demostrar que el modelo está disponible y registrar las condiciones reales de uso.

- Introducir la clave en una sesión local oculta, comprobar acceso y créditos con el proveedor, y ejecutar una primera solicitud controlada con texto autorizado. Distinguir `MODEL_API_KEY` del token de WhatsApp.
- Confirmar participación, track y campos de entrega. Conservar la pantalla y los errores sin guardar secretos.
- Verificar la documentación vigente de Muse Spark, límites, formato de salida estructurada, costos y retención; establecer tope de uso.
- Elegir un escenario de servicios para la presentación y documentar que es una hipótesis inicial, con configuración reutilizable para otros negocios.

**Salida:** una respuesta real del modelo registrada con versión, latencia y resultado sin secretos; acceso al evento confirmado o bloqueo documentado. H0 reutiliza F00–F02.

### H1 — WhatsApp de prueba conectado · 28–30 de octubre

**Objetivo:** recibir mensajes reales del número de prueba, sin depender de datos precargados.

- Seleccionar un destinatario propio o autorizado y comprobar envío y entrega de una prueba; diferenciar envío, recepción y estados.
- Preparar webhook HTTPS, registrar verificación y suscripción, verificar firma y número, guardar mensajes y deduplicar reintentos. Probar texto, duplicados, eventos no soportados y reinicios.
- El código del webhook existe, pero sólo está probado con fixtures. Preparar despliegue seguro y pedir autorización específica antes de modificar el VPS o conectar cuentas reales.

**Salida:** un mensaje real de prueba entra una vez, aparece en el panel y conserva fecha y fuente. Coexistence, envío desde la Business App y el historial siguen sin validarse. Mapea F02/F06/F07.

### H2 — Muse como motor de recomendaciones · 30 de octubre–1 de noviembre

**Objetivo:** transformar conversaciones reales en propuestas concretas y verificables.

- Cambiar el esquema de una acción única a una **lista de recomendaciones**, cada una con tipo, descripción, acción propuesta, prioridad explicada, incertidumbre, estado e IDs de mensajes que la respaldan. El servidor valida estructura y referencias; una referencia válida no garantiza que la conclusión sea correcta.
- Permitir que las señales coexistan: por ejemplo, una solicitud de cotización y una preferencia de horario pueden dar lugar a acciones diferentes. Sólo generar recomendaciones sustentadas por información disponible; ante ambigüedad, solicitar revisión o no proponer una acción.
- Usar la API real de Muse con configuración de negocio, instrucciones separadas del contenido no confiable, contexto limitado, tiempos de espera, control de costos y errores visibles. No enviar mensajes ni ejecutar recomendaciones automáticamente.
- Evaluar con conversaciones autorizadas y un conjunto de pruebas sintéticas aisladas: varias acciones, evidencia incorrecta, solicitudes ambiguas, pagos declarados, intentos de instrucción maliciosa, entradas largas y mensajes nuevos durante el análisis.

**Salida:** al menos una conversación real de prueba produce varias recomendaciones cuando su contenido las justifica; se puede abrir cada evidencia y se registran aciertos, fallos y latencia. No confundir pruebas simuladas con validación real. Mapea F07/F08/F10.

### H3 — Experiencia para ventas y dueño · 1–2 de noviembre

**Objetivo:** mostrar valor en menos de un minuto sin exigir tareas propias de un CRM completo.

- **Vista de ventas:** «Qué atender ahora», por prioridad, filtros, nombre o teléfono, contexto breve, evidencia, decisión humana y estado. Seleccionar, completar, descartar o corregir sin enviar mensajes automáticamente.
- **Vista del dueño:** resumen por periodo de oportunidades atendidas y recomendaciones pendientes; incluir sólo indicadores reproducibles a partir de los datos recibidos. Explicar desde cuándo hay datos y qué tipos de mensajes están cubiertos.
- Incorporar un contexto editable de negocio: nombre, sector, servicios, horario y objetivos. Presentar como configuración, sin afirmar compatibilidad universal. Accesibilidad básica y vista móvil.
- Preguntas que necesitan datos ausentes —ingresos reales, rentabilidad o impacto de campañas— deben mostrar «sin datos suficientes» y la fuente requerida.

**Salida:** un vendedor puede revisar y resolver una recomendación; el dueño entiende qué se sabe y qué falta. Verificación en escritorio y móvil. Mapea F05/F08/F09/F10.

### H4 — Datos, seguridad y confiabilidad · 2–3 de noviembre

**Objetivo:** que la demostración compartida proteja los datos y aguante errores habituales.

- Acceso autenticado a la demo, controles de autorización, datos separados por negocio si se muestra más de uno, TLS, secretos fuera del repositorio, registros sin contenido privado, política de retención/borrado y respaldo recuperable.
- El servidor actual `http.server` y SQLite en texto claro son locales, no son una base de producción. Elegir backend y almacenamiento apropiados para una sola instancia; evaluar PostgreSQL y un worker si la complejidad realmente lo exige. Docker en Hostinger es la arquitectura prevista.
- Probar webhook repetido, firma inválida, caída de Muse, límites de cuota, reinicio, actualización de mensaje y ausencia de datos. La interfaz debe mostrar errores recuperables y no marcar un mensaje como pago confirmado o venta perdida sin evidencia.
- Configurar un ambiente de prueba accesible sólo tras autorización explícita para los cambios externos; no abrir el panel actual sin protección.

**Salida:** acceso controlado, datos y fallos manejados, checklist y evidencias de verificación. Mapea F03–F05/F11/F12.

### H5 — Ensayo y entrega · 3–4 de noviembre

**Objetivo:** que jueces puedan entender y comprobar el valor sin depender de una secuencia frágil.

- Guion: dueño recibe mensajes de prueba → Pendiva muestra varias acciones sustentadas → vendedor revisa una → el dueño ve un resumen derivado de datos disponibles. Enseñar una llamada real a Muse y diferenciar sandbox, datos autorizados y límites.
- Preparar video y documentación de acuerdo con el portal oficial; registrar arquitectura, cómo se usa Meta AI, evaluación y sus límites. Ensayar recuperación si la API, webhook o internet falla: mostrar una captura de una ejecución real identificada como grabación previa, nunca como ejecución en vivo.
- Revisar licencia de participación, derechos, consentimiento y campos exigidos. Preparar la entrega y dejarla para aprobación final antes de publicar o enviar.

**Salida:** demo real repetida al menos dos veces, evidencia de evaluación, documentación y video listos; enviar con antelación a la fecha límite. Mapea F11–F12 y preparación de F13.

## 6. Backlog priorizado y criterios de calidad

| ID | Prioridad | Entrega | Criterio verificable |
|---|---|---|---|
| P0-01 | Imprescindible | Primera llamada real a Muse | Modelo responde con credencial del usuario; registrar resultado y uso sin exponer clave. |
| P0-02 | Imprescindible | WhatsApp sandbox real | Envío/entrega y webhook de recepción probados con un teléfono autorizado; duplicados no crean mensajes nuevos. |
| P0-03 | Imprescindible | Varias recomendaciones con evidencia | La salida es una lista; cada referencia coincide con un mensaje existente y los casos sin evidencia quedan inciertos o sin recomendación. |
| P0-04 | Imprescindible | Decisión humana | El vendedor puede revisar, completar, descartar y corregir; no hay envío automático. |
| P0-05 | Imprescindible | Demo segura y reproducible | Acceso restringido, HTTPS, secretos protegidos y dos recorridos reales completados; autorización para infraestructura. |
| P1-01 | Alto | Configuración para distintos negocios | Nombre, sector, servicios y horario editables; probar al menos dos configuraciones y no inventar capacidades de sectores no probados. |
| P1-02 | Alto | Resumen del dueño | Periodo, denominador y cobertura visibles; números calculados desde datos almacenados, nunca ingresos inferidos. |
| P1-03 | Alto | Calidad de Muse | Registro de casos evaluados, cobertura, evidencia válida, errores y revisión humana; metas acordadas antes de medir. |
| P1-04 | Alto | Preparación de entrega | Video, explicación técnica y materiales ajustados a reglas y portal, con identidad y derechos confirmados. |

**Puerta de decisión el 2 de noviembre:** si H0–H2 no han logrado una llamada real y un mensaje real recibido, concentrar el tiempo en resolver ese flujo y entregar una demo honesta de lo que sí funciona. Si la seguridad para acceso compartido no está lista, usar una demostración controlada local y no publicar el panel sin protección. La admisibilidad de esa alternativa debe confirmarse en el portal.

## 7. Expansión después de la hackathon

| Posible módulo | Valor para el usuario | Datos y dependencias antes de recomendar o automatizar |
|---|---|---|
| Campañas | Preparar, revisar y evaluar acciones comerciales. | Consentimiento, políticas y plantillas del proveedor, envío autorizado, costos y datos reales de rendimiento. |
| Gastos | Registrar y comprender costos del negocio. | Captura o integración verificable, categorías configurables, moneda, fechas y permisos. |
| Ingresos reales | Ver ingresos y tendencias sustentadas. | Fuente de pagos/ventas verificada o registro manual confirmado; no inferir ingresos de conversaciones. |
| Rentabilidad | Conectar ingresos con gastos y orientar decisiones. | Fuentes confiables de ambos, reglas contables acordadas y cobertura visible. |
| Recomendaciones por negocio | Explicar oportunidades y patrones transversales. | Contexto configurable, datos representativos, fuentes, frecuencia, muestra y evaluación por sector. |

Cada módulo requiere hipótesis, validación con usuarios, diseño de datos, consentimiento, costo y criterio de éxito. Priorizar después de observar uso real; no convertir Pendiva en un sistema de registro pesado por acumular funciones.

## 8. Siguientes decisiones y autorizaciones

- Confirmar que el equipo fue aceptado y su categoría en la hackathon; verificar especificaciones de entrega y trabajo previo.
- El usuario introduce su clave de Meta Model API en la terminal local, nunca en el chat. Las llamadas reales y su costo dependen de créditos y condiciones de la cuenta.
- Para probar WhatsApp, seleccionar un teléfono propio o consentido y completar la configuración de Meta. Para habilitar un webhook HTTPS o modificar Hostinger se requiere la autorización explícita correspondiente.
- Confirmar qué personas usarán la demo y qué datos pueden mostrarse o enviarse a Muse. No confundir un número de prueba con conexión lista para cualquier negocio.
