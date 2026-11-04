# Plan de desarrollo de Pendiva: hackathon y SaaS

**Estado:** plan por entregas verificables, sin fechas obligatorias ni duración total fijada.
La velocidad se obtiene reutilizando lo construido, reduciendo trabajo simultáneo y entregando
recorridos completos. Complementa el [roadmap existente](roadmap.md), el [plan de inteligencia
comercial](plan-inteligencia-comercial/plan.md) y la [validación multimedia](validation/estudio-multimodal.md).

## 1. Objetivo y posicionamiento

Pendiva ayuda a una empresa de servicios a identificar situaciones comerciales que podrían
necesitar atención, explicar la recomendación con sus fuentes y facilitar que una persona decida
qué hacer. El primer sector de la demo es **limpieza a domicilio**; la arquitectura debe permitir
adaptarse después a otros servicios.

Hipótesis que hay que comprobar: un dueño o asesor puede encontrar y resolver pendientes útiles
con menos esfuerzo y suficiente precisión frente a su proceso actual y a alternativas como Bolten.
Tener un CRM, WhatsApp, IA, voz o multimedia no es una ventaja exclusiva. La documentación de
[Bolten](https://www.bolten.io/es) anuncia estas categorías y su [FAQ](https://bolten.gitbook.io/bolten-docs/faq/principais-duvidas)
describe conexiones por QR y API oficial; su comportamiento en los casos específicos de Pendiva
requiere una prueba comparativa, no se debe asumir que no los resuelve.

La propuesta para la hackathon es un **caso completo y comprobable**; la propuesta para el SaaS es
convertir ese recorrido en un servicio confiable, aislado, útil y económicamente viable.

## 2. Punto de partida verificado

| Capacidad | Situación actual | Límite o siguiente comprobación |
|---|---|---|
| Texto WhatsApp | Se recibió un texto real de prueba mediante webhook firmado; hay deduplicación. | No acredita cobertura del historial ni mensajes salientes. |
| Imagen y audio WhatsApp | Una imagen JPEG y un audio OGG de prueba se recibieron, descargaron y analizaron realmente con autorización; resultados guardados. | La exactitud completa de las salidas y el recorrido visual final aún requieren revisión. |
| Muse | Probados con datos sintéticos: imagen, video estático, transcripción, respuesta con evidencia y propuesta de vista. | No presentar las salidas sintéticas como prueba del recorrido completo por WhatsApp. |
| Atención y clientes | Panel local, prioridades, filtros, fichas y revisión con evidencia. | Las fichas y varias fechas/responsables son manuales; no equivalen a un CRM multiempresa completo. |
| Seguimientos | Inicio reúne oportunidades abiertas registradas por el equipo y clasifica sus fechas según el dispositivo; permite abrir la ficha y su respaldo. | No detecta promesas automáticamente ni confirma que se haya contactado al cliente. |
| Asistente | Preguntas por texto/dictado y respuesta escrita; interfaz animada y voz del navegador. | El dictado físico y la nueva animación no han sido verificados en el dispositivo; no es una llamada de voz en tiempo real. |
| Herramientas | Muse propone vistas dentro de tres plantillas, con aclaración, vista previa y aprobación. | No crea ni ejecuta código arbitrario, no programa citas ni envía mensajes. |
| Seguridad y operación | Autenticación local y partes de aislamiento, pruebas y webhook aislado. | No hay aislamiento completo, despliegue público, Coexistence real ni SaaS listo para clientes. |

## 3. Horizonte A: demo diferenciable de hackathon

### Experiencia que verá el jurado

1. Una empresa ficticia de limpieza recibe una solicitud. Se muestra un mensaje real del
   sandbox si está disponible y, por separado, los datos sintéticos de presentación.
2. Una foto o un audio de prueba se procesa con Muse, con autorización; la ficha muestra lo
   observado o transcrito y lo que no se sabe. El adjunto original queda disponible como fuente.
3. Pendiva muestra una situación que necesita revisión: qué se observó, qué falta, fuente y
   siguiente paso. Una persona puede corregir o resolver la recomendación.
4. El dueño pregunta al asistente por texto o voz: «¿Qué falta para cotizar este servicio?».
   Se muestran respuesta, fuentes y cobertura. La animación representa el estado de la interacción.
5. En Mejoras se previsualiza una lista de datos faltantes o cotizaciones para seguimiento y se
   abre la ficha correspondiente. Las fechas declaradas faltantes no se inventan.

**Caso de compromiso del asesor:** si el canal todavía no entrega mensajes salientes, mostrarlo
únicamente como **escenario sintético** y no como vigilancia real de todos los asesores. El
objetivo de producción depende de comprobar Coexistence y la cobertura real del proveedor.

### Prioridades y criterios de aceptación

| ID | Prioridad | Trabajo | Criterio de salida |
|---|---|---|---|
| H0 | Antes de publicar | Confirmar evento, aceptación, categoría, reglas y formato de entrega. | Evidencia de inscripción o bloqueo; lista de entrega y condiciones. No bloquea desarrollo local. |
| H1 | P0 | Comprobar los envíos de imagen y audio autorizados. | Recepción, descarga y análisis registrados para ambos; revisar las salidas y su presentación visual. |
| H2 | P0 | Enlazar mensaje, archivo, observación, recomendación y revisión. | El usuario puede ir de cada sugerencia a evidencia pertinente y corregirla; faltantes y cobertura parcial visibles. |
| H3 | P0 | Caso comercial de limpieza con datos verificados o explícitamente sintéticos. | Enseñar al menos una señal útil, una incertidumbre y una acción humana sin inventar precio, pago o resultado. |
| H4 | P0 | Ensayar voz, accesibilidad, español/inglés y modo oscuro. | Dictado y audio probados en el dispositivo si es posible; si fallan, entrada/salida por texto; interfaz no afirma que funciona en tiempo real. |
| H5 | P0 | Pruebas y plan B. | Firma inválida, duplicados, modelo caído y datos faltantes con resultados legibles; demo grabada o sintética etiquetada si falla la red. |
| H6 | P1 | Plantillas de seguimiento y creador con Muse. | Al menos una plantilla se previsualiza y ejecuta con fuente y requisitos; activación explícita. |
| H7 | P1 | Video, presentación y paquete del evento. | Guion ensayado, enlace/documentación requeridos y revisión de derechos; enviar sólo con autorización. |

### Orden de entrega sin calendario obligatorio

La convocatoria se revisará antes de publicar o presentar. Sus fechas no son dependencias del
desarrollo. El avance se mide por recorridos que funcionan y criterios de salida cumplidos.

1. Cerrar el recorrido de una conversación y su evidencia.
2. Añadir extracción estructurada y una recomendación útil de seguimiento.
3. Resolver, corregir y volver a consultar el resultado desde el asistente.
4. Enseñar personalización mediante una herramienta que use esos mismos datos.
5. Ensayar presentación, voz, errores y alternativa sin red.

Si se necesita una demostración antes, se presenta el último recorrido completo y se identifica
su cobertura. Los módulos incompletos no entran en el recorrido principal.

## 4. Horizonte B: SaaS, por fases y con puertas de salida

El núcleo de la demo y el SaaS se desarrolla en la misma base. El aislamiento se incorpora a las
nuevas entidades desde su creación; no se deja como una reescritura posterior. La conexión
comercial, el piloto y cualquier despliegue o compra conservan sus autorizaciones correspondientes.

No se fija una duración global sin medir el ritmo real. Se estimarán tareas pequeñas después
de implementar el primer recorrido, registrando
esfuerzo real, bloqueos y retrabajo. El tiempo de espera de Meta se registra por separado del
esfuerzo de desarrollo. La prioridad se ajusta al valor, riesgo y dependencias, no a un calendario.

### B1. Datos comerciales y motor de oportunidades

- Modelar por empresa: contacto, canal, conversación, mensajes, archivos, **varias
  oportunidades por contacto**, cotizaciones, compromisos, responsables, recomendaciones,
  evidencias, correcciones y actividades. Conservar origen y fecha de cada dato.
- Extraer candidatos con Muse en esquema validado; marcar cada campo como observado,
  inferido, corregido o desconocido. Las reglas calculan plazos desde fechas identificadas y
  zona horaria configurada; una frase ambigua genera una pregunta, no una fecha inventada.
- Distinguir promesa del asesor, solicitud del cliente, objeción, rechazo y silencio. Un pago
  declarado no es un pago verificado; silencio no es oportunidad perdida.
- Mostrar cobertura: número/canal, periodo, mensajes entrantes/salientes disponibles, último
  evento y fallos. Nunca convertir ausencia de evidencia en evidencia de ausencia.

**Salida B1:** una muestra anotada por humanos cubre los casos anteriores; cada recomendación
tiene fuente válida y fecha interpretada de forma verificable; errores y límites están visibles.

### B2. Conexión WhatsApp y operación confiable

**Solicitud adicional:** bandeja que permita responder por WhatsApp y automatización configurable.
La primera pieza local guarda borradores por conversación, con respuesta inicial bilingüe; no envía
mensajes ni activa un bot. Los borradores se pueden editar y cada cambio se registra en auditoría.
Antes de enviar al sandbox faltan implementar y verificar la identidad de
la conexión, ventana de servicio o plantilla aplicable, autorización por rol, confirmación de envío,
idempotencia y estados aceptado/entregado/fallido. Antes de automatizar para clientes se requieren
pausa y transferencia a una persona, límites, consentimiento y cobertura del canal. La prueba de
extracción documenta errores de próximos pasos y no justifica automatización sin supervisión.

Meta describe la sesión iniciada por el cliente en su [guía de pruebas](https://whatsapp.github.io/WhatsApp-Nodejs-SDK/);
ese SDK está archivado, por lo que se deben verificar los requisitos actuales de Cloud API y plantillas
antes de implementar envíos en producción. Ningún histórico completo se da por garantizado.

- Evaluar Meta directo frente a proveedor oficial y verificar Embedded Signup/Coexistence con
  un número elegible y consentimiento. Probar entrada, salida, eco, historial permitido,
  multimedia, desconexión, reconexión y comportamiento ante permisos o token vencidos.
- Persistir eventos firmados de manera idempotente; gestionar duplicados, reordenamiento,
  reintentos con límites y errores visibles. Usar cola/worker y almacenamiento de archivos
  apropiados fuera del proceso web, con cuotas y políticas de retención.
- Cada conexión debe indicar **lo que realmente sincroniza**. No prometer historial completo ni
  continuidad de WhatsApp Business App hasta verificar condiciones y cobertura.

**Salida B2:** matriz de pruebas por proveedor/cuenta y una conexión de prueba recuperable,
con logs sin secretos, deduplicación y fuentes de verdad documentadas.

### B3. Seguridad, aislamiento y arquitectura de producto

- Auditar todas las consultas, claves únicas y accesos por empresa: mensajes, análisis,
  revisiones, archivos, informes, búsqueda, herramientas y sesiones. Resolver la colisión
  actual de análisis por remitente antes de cualquier acceso multiempresa.
- Roles y autorización en servidor; pruebas cruzadas entre dos empresas y para el mismo número
  de cliente, incluidas tareas asíncronas y archivos. Verificar CSRF, límites de acceso y sesiones.
- Diseñar migración versionada desde SQLite y respaldo recuperable a una base adecuada para el
  piloto, normalmente PostgreSQL; probar copia, restauración y rollback con datos ficticios.
  El stack de despliegue se decide con ADR y capacidad del equipo: no se asume Hostinger,
  proveedor ni framework como requisito inmutable.
- Definir consentimiento, minimización de datos, permisos de acceso, exportación, retención y
  eliminación de originales, derivados y backups. Revisar obligaciones legales con asesoría
  adecuada antes de tratar datos reales; no registrar claves ni contenidos en telemetría.
- Limitar costo y frecuencia de IA, revisar permisos por proveedor, defender contra instrucciones
  en mensajes/archivos y usar respuestas estructuradas. El modo Standard de Muse y las políticas
  vigentes deben verificarse antes de procesar información de clientes.

**Salida B3:** revisión de seguridad, aislamiento adversarial automatizado, restauración
ensayada y checklist de privacidad/operación. No exponer el servidor local actual a Internet.

### B4. Producto, personalización y voz

- Onboarding guiado: sector, servicios, horarios, zonas, políticas y fuente de tarifas; datos
  modificables y revisables. Empezar por limpieza y añadir otros sectores a partir de pilotos.
- Evolucionar el creador hacia **componentes declarativos permitidos**: preguntar objetivo,
  fuente, reglas, permisos y datos faltantes; previsualizar, aprobar, auditar y desactivar.
  No ejecutar código generado en producción ni conceder acceso amplio por una instrucción de IA.
- Voz de ida y vuelta con animación de estado, interrupción, consentimiento de proveedores y
  alternativa por texto. La voz continua en tiempo real es una fase independiente que requiere
  evaluar latencia, permisos, costo y disponibilidad; no está implementada hoy.
- Audio, imagen y video: presentar observaciones con referencia al archivo y etiqueta de IA.
  La [documentación de Muse](https://dev.meta.ai/docs/video-understanding) advierte limitaciones
  en audio de Spark 1.3; elegir el modelo de transcripción comprobado y no prometer interpretación
  perfecta del audio de video.

**Salida B4:** un negocio de prueba completa onboarding y revisa sus recomendaciones sin ayuda;
los límites de datos y acciones son comprensibles y medidos.

### B5. Piloto y sostenibilidad

- Reclutar 3–5 empresas sólo con consentimiento, acuerdo de datos y procedimiento de soporte;
  este número es una meta de reclutamiento, no evidencia de demanda existente.
- Registrar: alertas mostradas, confirmadas, corregidas o descartadas; tiempo hasta revisión;
  seguimiento declarado; respuesta y resultado comercial confirmado por una fuente explícita.
- Evaluar costo por empresa y por caso: WhatsApp, almacenamiento, cómputo, IA de texto y
  multimedia, soporte y margen. Los precios de proveedores cambian; usar mediciones reales y
  verificar condiciones antes de fijar precios comerciales.
- Comparar con el proceso actual y con Bolten usando los mismos casos y una configuración
  razonable. Documentar dónde Pendiva gana, empata o pierde antes de prometer superioridad.

**Salida B5:** informe con uso, calidad, incidentes, costos, interés de pago y decisión de seguir,
ajustar o detener. Ventas posteriores no se atribuyen causalmente a Pendiva sin comparación.

## 5. Cómo producir más valor con menos trabajo

### Reutilización y decisiones de alcance

| Decisión | Implementación prevista | Ahorro o beneficio |
|---|---|---|
| Conservar Python y la interfaz existente | Separar módulos donde ayude a probarlos; evitar reescritura inicial de frontend. | Menos migración y más tiempo en el motor comercial. |
| Una sola definición de oportunidad | Compartida por extracción, ficha, filtros, asistente e informes. | Evitar reglas diferentes para el mismo dato. |
| IA para interpretar; reglas para calcular | Muse propone candidatos con fuentes; consultas calculan antigüedad, vencimientos y totales. | Reducir costo y errores en cálculos repetitivos. |
| Analizar cambios relevantes | Versionar mensajes/contexto, invalidar derivados y evitar repetir análisis idénticos. | Menos latencia y gasto; requiere comprobar idempotencia y cobertura. |
| Personalización declarativa | Configurar campos, reglas y vistas dentro de permisos conocidos. | Nuevos casos de uso sin generar código arbitrario por empresa. |
| Evidencia compartida | Una referencia al mensaje o archivo sirve a ficha, recomendación y asistente. | Menos duplicación y mejor trazabilidad. |
| Un sector de validación, configuración reutilizable | Limpieza valida el recorrido; mantenimiento es el siguiente escenario de prueba. | Evitar diseñar diez procesos antes de comprobar uno. |
| Despliegue modular sencillo | Una aplicación y un worker cuando sea necesario; evitar microservicios prematuros. | Menos operación y fallos entre servicios. |

No se reduce el trabajo necesario de aislamiento, protección de datos o validación. Se reduce el
trabajo de migraciones prematuras, módulos accesorios y funcionalidades duplicadas.

### Método de ejecución

- Elegir una entrega vertical: datos → regla → pantalla → acción → prueba. No completar primero
  todo el backend y después descubrir que el usuario necesita otro flujo.
- Mantener **una entrega de producto en curso** y una tarea independiente de diagnóstico o
  preparación. Si hay más colaboradores, repartir sólo módulos con contratos claros y sin editar
  el mismo archivo; con una sola persona, alternar trabajo útil mientras espera un servicio externo.
- Dividir tareas que no puedan demostrarse de forma independiente. Al terminar cada entrega,
  registrar qué cambió, cómo se probó y qué sigue pendiente.
- Añadir pruebas de comportamiento y riesgo, no de apariencia interna. Conservar un conjunto
  pequeño de casos de regresión y ampliarlo cuando se encuentre una clase nueva de error.
- Resolver decisiones reversibles dentro del alcance. Agrupar las decisiones del dueño sobre
  cuentas, datos reales, publicación y gasto al final de la preparación técnica.

## 6. Backlog detallado por entregas

Las estimaciones relativas **S / M / L** indican complejidad: S es acotada; M requiere coordinar
datos, interfaz y pruebas; L tiene incertidumbre o dependencia externa. No equivalen a días.
Las fases anteriores describen el destino; esta tabla y los bloques siguientes definen el orden
de implementación. Una fase puede necesitar varias entregas y no se considera terminada por
completar una sola.

| Entrega | Tamaño inicial | Depende de | Beneficio visible |
|---|---|---|---|
| E1 · Base reproducible y cobertura | S/M | Estado actual | Saber qué mensajes llegaron y repetir la demo. |
| E2 · Oportunidad y evidencia | M | E1 | Dos servicios del mismo cliente se consultan por separado. |
| E3 · Extracción revisable | M | E2 | Menos transcripción manual de datos comerciales. |
| E4 · Compromisos y prioridades | M | E3 | Saber qué revisar y qué plazo lo sustenta. |
| E5 · Acción y resultado | M | E4 | Resolver pendientes con historial y medir qué pasó después. |
| E6 · Asistente y voz sobre el mismo motor | S/M | E2–E5 | Consultar el negocio con fuentes coherentes. |
| E7 · Herramientas y documentos del negocio | M | E2–E5 | Personalizar vistas con reglas y datos propios. |
| E8 · Presentación y comparación | S/M | E1 y un recorrido E2–E6 completo | Demo sólida y evaluación frente a alternativas. |
| E9 · Aislamiento integral | M/L | Empieza en E2; cierre antes de piloto multiempresa | Empresas y usuarios separados de verdad. |
| E10 · Conexión comercial y operación | L | Diagnóstico desde E1; cierre con E9 | Operar con una cuenta elegible y recuperarse de fallos. |
| E11 · Piloto medido | M + observación | E9 y E10 aprobadas | Saber si existe utilidad y disposición de pago. |
| E12 · Comercialización gradual | M | Evidencia de E11 | Contratar, controlar uso, soportar y cancelar el servicio. |

### E1. Base reproducible y cobertura

**Tareas:** comprobar estado del receptor y credenciales sin exponer valores; recuperar la foto
y audio autorizados si están disponibles; verificar formato, firma y duplicados; añadir una
forma de conocer la última recepción y los errores de cada etapa. Conservar los fixtures y
datos reales en recorridos identificables, sin borrados para reiniciar una demo.

**Salida:** se puede seguir mensaje → almacenamiento → archivo → análisis. Si falla Meta, el
error queda identificado y el recorrido sintético sigue siendo reproducible. No dar por cumplida
la prueba real de los archivos ya enviados hasta comprobarla.

### E2. Oportunidad y evidencia como núcleo

**Avance implementado:** la conversación de una empresa autenticada permite registrar y editar
varios servicios por separado con valor, etapa, fecha y próximo paso declarados por la persona,
seleccionando un mensaje de respaldo del mismo contacto y empresa. El asistente puede recuperar
esos registros como datos declarados. Hay pruebas de separación de oportunidades y rechazo de
evidencias de otro contacto. Siguen pendientes extracción automática, asociación de archivos,
resolución de ambigüedades y aislamiento integral de las rutas anteriores.

**Tareas:** revisar primero las entidades ya presentes en el dominio y reutilizarlas; crear las
migraciones necesarias; vincular una oportunidad con contacto, servicio, conversación, estado,
responsable y fuentes; permitir varias oportunidades del mismo contacto. La asignación sugerida
por IA se mantiene pendiente cuando es ambigua. Toda entidad nueva incluye empresa en su clave
y autorización de acceso desde la primera implementación.

**Pantallas:** lista de clientes conserva su función; el detalle permite abrir las oportunidades
de ese cliente sin mezclar una limpieza de sofá con otro servicio posterior.

**Salida:** un fixture con dos solicitudes del mismo cliente mantiene importes, fechas y próximos
pasos independientes. Un usuario de otra empresa no puede acceder a las entidades nuevas.

### E3. Extracción estructurada con corrección

**Avance local:** Muse puede proponer hasta cinco servicios a partir de los últimos 30 mensajes de
texto disponibles, con consentimiento por búsqueda y una fuente por propuesta. La propuesta es
temporal: se revisa y edita antes de crear una oportunidad. Se descartan importes que no aparecen
literalmente en el mensaje citado. La validación automatizada usa respuestas simuladas; falta evaluar
precisión con ejemplos anotados y atribución por campo. Documentación
oficial: [salida estructurada de Meta](https://dev.meta.ai/docs/structured-output).

**Evidencia multimedia:** opcionalmente se incluyen hasta diez observaciones ya guardadas, no los
archivos, con aceptación explícita. Una propuesta multimedia conserva al guardarse la observación
existente, su fecha y enlace al archivo, y rechaza una observación modificada desde la búsqueda.
El borrado del archivo elimina la copia de evidencia; la oportunidad permanece. Las pruebas usan
respuestas simuladas. Aún no se dispone de una evaluación de precisión revisada por personas ni se
verifica automáticamente que el servicio propuesto esté respaldado semánticamente por la fuente.

**Tareas:** definir un esquema para servicio, cantidad/alcance, zona, fecha solicitada, importe
mencionado y compromiso; distinguir quién lo dijo y cuándo; conservar la evidencia de texto o
archivo. Mostrar sugerencias campo por campo y permitir aceptar, editar o rechazar. Las
correcciones humanas sobreviven a un nuevo análisis; los conflictos se presentan para revisión.

**Reglas:** no estimar material, tamaño, precio, pago ni disponibilidad a partir de una foto
sin evidencia adecuada. Un importe preliminar se conserva como preliminar. Las frases sobre
fechas se interpretan respecto al mensaje y la zona horaria, con incertidumbre explícita.

**Salida:** una ficha se completa desde sugerencias verificables; los datos ambiguos quedan
pendientes y un reanálisis no reemplaza silenciosamente una corrección humana.

### E4. Compromisos y motor de atención

**Tareas:** representar compromiso con actor, acción, fecha cuando exista, oportunidad, evidencia
y estado; comenzar con tres detectores: solicitud de cotización pendiente, compromiso con fecha
para revisar y cotización enviada que requiere seguimiento según una política configurable.
Incorporar rechazo explícito y oportunidad resuelta como condiciones para retirar alertas.

**Prioridad:** reglas transparentes por plazo, petición explícita y estado, sin probabilidades
inventadas de compra. Identificar qué datos causan cada prioridad. Si no hay cobertura saliente,
mostrar «No encontramos confirmación en los mensajes disponibles; revisar».

**Salida:** el panel diferencia ausencia de respuesta, rechazo y compromiso con fecha. Un mensaje
nuevo invalida o recalcula la alerta pertinente; las alertas resueltas no reaparecen sin causa.

### E5. Pasar de alerta a acción y resultado

**Tareas:** acciones internas de revisar, asignar, crear recordatorio, preparar borrador y resolver;
registrar actor, momento, evidencia y motivo de corrección. El borrador no se envía automáticamente.
Separar estado de recomendación, estado de oportunidad y resultado comercial declarado.

**Avance local:** se guardan y editan borradores de respuesta con empresa, conversación, mensaje de
origen, persona que los modificó y eventos de auditoría. No se consideran mensajes enviados; no hay
estado de entrega ni informe de venta ligado al borrador.

**Medición:** alerta → revisión → acción declarada o registrada → respuesta disponible → resultado
confirmado. Marcar qué pasos se observan en la conexión y cuáles los registró una persona.

**Salida:** se puede reconstruir qué cambió y por qué; «recomendación completada» no se cuenta
automáticamente como venta ni como ingreso causado por Pendiva.

### E6. Asistente de negocio y experiencia de voz

**Tareas:** consultar las oportunidades y compromisos de E2–E5 mediante funciones autorizadas;
usar consultas deterministas para totales y Muse para explicarlos. Comenzar con «qué reviso hoy»,
«qué falta para cotizar», «qué compromisos necesitan revisión» y «qué cambió desde mi última visita».
Mostrar alcance, fuentes y acción propuesta, con confirmación para cambios que lo requieran.

**Voz:** probar el indicador animado, inicio/fin/interrupción, cierre del panel y permisos;
mantener texto como alternativa. La voz del navegador no crea un archivo de respuesta.
Evaluar conversación continua sólo después de medir la utilidad y latencia del recorrido actual.

**Salida:** preguntar por texto o dictado devuelve los mismos datos comerciales. No se habla
con autoridad sobre mensajes inaccesibles ni se ejecutan funciones fuera del rol del usuario.

### E7. Personalización y documentos de empresa

**Tareas:** ampliar el creador existente con una especificación de objetivo, campos, fuente,
regla, permisos y vista. Si faltan datos, preguntar y ofrecer formulario o importación con vista
previa. Cargar primero CSV y texto; evaluar otros formatos después de resolver el recorrido.
Versionar tarifas, zonas y políticas con vigencia y procedencia. La IA propone; el dueño revisa.

**Ejemplo:** «Avísame de cotizaciones de limpieza de oficinas sin respuesta después de dos días».
El creador pregunta qué cuenta como cotización enviada, qué fecha usar y quién revisa la lista;
si faltan fechas, ofrece completarlas antes de activar la regla.

**Salida:** la herramienta explica qué hará, con qué datos y qué le falta; se puede previsualizar,
aprobar, desactivar y auditar sin ejecutar código arbitrario. Un documento cargado se trata como
información, nunca como autorización para cambiar permisos o enviar mensajes.

### E8. Demo diferenciable y prueba competitiva

**Tareas:** preparar un caso positivo y uno ambiguo; enseñar fuente, corrección y efecto en el
panel; comparar con el mismo caso en Bolten y con un proceso manual cuando haya acceso autorizado.
Medir pasos, configuración necesaria, errores y tiempo de revisión. Grabar un respaldo identificado
y verificar el dispositivo de presentación; confirmar las condiciones del evento al preparar entrega.

**Salida:** la presentación demuestra utilidad concreta y límites. Los criterios de evaluación
son iguales para los productos y no se presentan funciones no verificadas de Bolten como ausentes.

### E9. Cierre de aislamiento y seguridad

**Tareas:** completar la auditoría de rutas, búsquedas, claves únicas, revisiones, jobs, archivos y
herramientas; resolver las tablas antiguas con claves globales. Probar dos empresas con el mismo
remitente y sesiones de distintos roles. Preparar migración, exportación y restauración verificadas.

**Salida:** cero accesos cruzados en los casos de aislamiento definidos, autorización en servidor
y recuperación ensayada. Es una condición para un piloto multiempresa, aunque la demo local pueda
avanzar antes con datos ficticios.

### E10. Conexión comercial y operación

**Tareas:** comprobar con una cuenta elegible la cobertura del proveedor; gestionar permisos,
renovación de credenciales, desconexión y reconexión. Pasar la recepción a persistencia y trabajo
asíncrono con reintentos acotados, cuotas y errores recuperables. Preparar HTTPS, secretos, backups,
retención y monitorización en un entorno aprobado.

**Salida:** un fallo de modelo no pierde el mensaje; un evento repetido no duplica una acción;
un reinicio no depende de rehacer manualmente todo el recorrido. La interfaz expone la cobertura
real de cada cuenta. Las aprobaciones externas no bloquean el trabajo independiente de E2–E9.

### E11. Piloto con aprendizaje útil

**Tareas:** incorporar gradualmente empresas consentidas, observar el uso y revisar alertas con
los usuarios; documentar motivos de descarte, datos faltantes, costo por cuenta y soporte. Empezar
con un negocio y ampliar hacia la meta de 3–5 sólo si la operación lo permite.

**Salida:** evidencia para decidir qué mejorar y si tiene sentido cobrar. Una entrevista positiva,
una demo exitosa o varias ventas posteriores no sustituyen una validación de utilidad recurrente.

### E12. Comercialización gradual

**Tareas:** definir planes a partir de costo medido y disposición de pago; añadir límites de uso,
avisos, contratación, soporte, facturación mediante proveedor elegido y cancelación/exportación.
Separar acceso al producto de permisos para conectar canales y datos. Habilitar cambios a grupos
pequeños y documentar recuperación y atención de incidentes.

**Salida:** alta, uso, cobro y cancelación probados con cuentas de test; activar pagos y publicar
requiere decisión del dueño. Expandir sectores o integraciones sólo con demanda observada.

## 7. Evaluación de calidad y diferenciación

Crear un conjunto independiente de conversaciones sintéticas y, sólo con autorización, una
muestra anonimizada de casos reales. Etiquetar por personas con instrucciones compartidas:
evento, responsable, fecha, fuente, cobertura y acción esperada. Incluir dos oportunidades del
mismo contacto, promesa ambigua, cotización rechazada, silencio, pago declarado, archivos no
analizados, mensajes incompletos y texto adversarial.

Medir por tipo de caso: **precisión** de alertas revisadas, **cobertura** sobre casos positivos
identificados, fuentes válidas, errores de fecha/responsable, alertas por usuario y tiempo hasta
revisión. Registrar denominadores y mostrar muestras; con pocas observaciones, los porcentajes
son exploratorios. Definir metas antes de evaluar y revisar desacuerdos humanos. La calidad de
una alerta no se deduce solamente de que cite un mensaje existente.

### Alcance mínimo de cada versión

| Versión | Alcance que se termina primero | Se amplía después |
|---|---|---|
| Demo diferenciable | Un caso de limpieza; dos oportunidades del mismo contacto en fixture; cuatro campos sugeridos; una alerta explicada; corregir/resolver; dos consultas del asistente; una plantilla existente. | Más detectores, más sectores, personalización ampliada y conversación continua. |
| Alfa privada | Ese mismo flujo con persistencia, roles y datos de test; errores recuperables y cobertura visible. | Cuentas comerciales reales y acceso multiempresa público. |
| Piloto SaaS | Aislamiento integral, conexión elegible, onboarding, recuperación, cuotas, política de datos y seguimiento de resultados. | Cobro y difusión amplia hasta contar con evidencia de operación y demanda. |
| Comercial | Piloto satisfactorio, soporte, condiciones y ciclo de contratación/cancelación probados. | Nuevos sectores e integraciones según uso y economía observados. |

La demo puede demostrar el diferencial con un corte pequeño de E2–E6; no necesita terminar
todas las variantes de cada entrega. Los recorridos con datos sintéticos siguen identificados.

### Primera lista de trabajo para comenzar la implementación

1. Registrar qué funciones y tablas existentes ya cubren cada entrega y reutilizarlas; conservar
   los cambios locales. Identificar la colisión de análisis por remitente y las rutas pendientes.
2. Preparar fixtures y respuestas esperadas para solicitud, promesa ambigua, rechazo y dos
   oportunidades del mismo cliente. Guardar la versión de esas expectativas.
3. Cerrar el diagnóstico de los archivos autorizados y documentar el resultado real o bloqueo.
   Si falta acceso externo, seguir con el resto usando fixtures identificados.
4. Implementar el mínimo de E2 y E3: oportunidades separadas y sugerencias con fuente, sin
   ampliar todavía todo el CRM ni rehacer la interfaz.
5. Añadir un detector de E4 y las acciones revisar/corregir/resolver de E5. Mostrar su efecto
   desde una consulta del asistente y medir el recorrido completo.
6. Revisar resultados y esfuerzo real; escoger el siguiente incremento por utilidad demostrada.
   Después fijar estimaciones pequeñas basadas en ese ritmo, sin convertirlas en fechas obligatorias.

### Condición común de una entrega terminada

El recorrido se puede repetir; usa las mismas reglas en pantalla y asistente; los datos tienen
fuente; los accesos están autorizados; los errores son visibles; las pruebas cubren el comportamiento
nuevo; y la documentación distingue probado, simulado y pendiente. Un mock sólo acredita el
contrato simulado, nunca la disponibilidad de un servicio real.

## 8. Qué no se promete

- No conectar números comerciales reales, enviar mensajes a clientes ni publicar el producto sin
  autorización y condiciones de uso apropiadas.
- No presentar el prototipo, los resultados simulados o una muestra pequeña como SaaS validado.
- No afirmar que Bolten carece de una función sin probarla, ni que usar la API oficial sea exclusivo.
- No afirmar ingresos recuperados por una alerta sin una evaluación causal adecuada.
- No sustituir la revisión humana con acciones automáticas de IA ni código generado sin controles.

## Referencias y decisiones abiertas

- [Página del evento de Meta](https://dev.meta.ai/events/global-hackathon): confirmar evento,
  admisión, categoría, fecha y condiciones aplicables en el portal de participación.
- [Meta Model API: modelos](https://dev.meta.ai/docs/models), [multimedia](https://dev.meta.ai/docs/video-understanding)
  y [precios y límites](https://dev.meta.ai/docs/pricing-rate-limits): revisar antes de cada integración.
- [WhatsApp Cloud API: obtener URL multimedia](https://www.postman.com/meta/whatsapp-business-platform/request/ptjyi84/retrieve-media-url):
  referencia de la recuperación de medios; validar condiciones actuales de conexión y convivencia.
- [Bolten](https://www.bolten.io/es) y [conexiones WhatsApp](https://bolten.gitbook.io/bolten-docs/faq/principais-duvidas):
  capacidades anunciadas, no sustituyen una prueba práctica comparativa.
- Pendientes de decisión: alcance de la entrega concreta, proveedor definitivo, infraestructura,
  política de datos, presupuesto, precio, integración opcional con otros CRM y condiciones de piloto.
