# Demo de estudio multimedia y herramientas personalizadas

## Alcance

El prototipo local permite asociar un archivo de hasta 4 MB a una conversación, mostrarlo y
analizarlo previa confirmación por el usuario. Para imágenes PNG/JPG y video MP4 se utiliza
Muse Spark 1.3 en modo estándar; para WAV se usa Muse Voice Transcribe. El WAV debe ser mono,
PCM de 16 bits, a 16 o 24 kHz. Si el audio es OGG, FFmpeg lo convierte localmente y solo se
transcriben los primeros 60 segundos. Para audio en un video, la documentación de Meta advierte
que la comprensión de audio de Spark 1.3 puede degradarse: no se debe presentar como garantizada.

El webhook puede guardar el identificador de multimedia, pero descargar el archivo requiere la
acción del usuario y una credencial sandbox válida. La descarga consulta la API oficial, restringe
el host de destino, no sigue redirecciones, comprueba tamaño/formato e integridad cuando Meta da
un hash, y guarda el archivo en SQLite. Luego se requiere otra confirmación para enviarlo a Meta
Model API. El prototipo incluye acceso por empresa a estas nuevas tablas, pero no es un servicio
multiempresa de producción: el modelo de análisis previo todavía tiene claves globales y el resto
de las rutas necesita una auditoría completa. No exponer el panel a internet.

El asistente utiliza como fuentes textos y resultados multimedia existentes; las descripciones y
transcripciones son salidas de IA, no hechos verificados. Eliminar un archivo local elimina su
análisis asociado, pero no elimina respuestas anteriores del asistente ni archivos en Meta/WhatsApp.

Muse propone únicamente vistas de seguimiento, datos faltantes y servicios por confirmar. Se exige
al menos una aclaración; las propuestas se validan contra un esquema cerrado, se previsualizan con
datos locales, y el dueño las activa expresamente. Los cálculos no ejecutan código generado. La
fecha de cotización es declarada por el usuario mediante la ficha o CSV y no se deduce del silencio.
El creador no envía mensajes ni programa citas.

## Evidencia de pruebas — 2026-10-29

- **Real:** Muse Spark 1.3 describió una ilustración de sofá y un video MP4 estático ficticio;
  Muse Voice Transcribe transcribió un WAV sintético. Se comprobó además una nota OGG ficticia
  convertida a WAV con FFmpeg y transcrita por el servicio. Se utilizaron créditos de API.
- **Real:** Muse realizó una pregunta de aclaración y generó una propuesta de lista de seguimiento;
  se verificó su vista previa y activación en el navegador con una base de datos ficticia.
- **Real:** el asistente respondió una pregunta ficticia sobre el sofá de Ana con Muse y fuentes
  de la demo; ElevenLabs generó automáticamente el audio de esa respuesta. El permiso físico de
  micrófono y el dictado desde este dispositivo no se comprobaron en esa prueba.
- **Simulado:** recuperación del adjunto de WhatsApp, rechazos de URL externa, comprobación de
  integridad, autorización explícita, reglas, importación CSV e aislamiento de las tablas nuevas.
- **Simulado, recorrido integrado:** firma y normalización del webhook con imagen y audio OGG,
  deduplicación, descarga desde respuestas ficticias de Graph, conversión y respuestas ficticias
  de Muse, persistencia del resultado y recuperación como evidencia del asistente. No constituye
  una recepción o transcripción real del sandbox.
- **Pendiente:** evaluación de la exactitud de las observaciones y transcripciones. No se ha
  probado contenido de clientes ni se ha verificado un despliegue comercial o captura completa
  del historial de WhatsApp.

Actualización: tras renovar la credencial y con autorización del usuario, se descargaron desde
el sandbox una imagen JPEG y una nota de voz OGG realmente recibidas. Muse analizó la imagen y
Muse Voice Transcribe procesó el audio convertido localmente; ambos resultados quedaron guardados
en la conversación. Se verificó persistencia y tipos, no la exactitud completa de las salidas.

Referencias oficiales: [imágenes](https://dev.meta.ai/docs/image-understanding),
[video y audio](https://dev.meta.ai/docs/video-understanding),
[transcripción y formatos WAV](https://dev.meta.ai/docs/speech-to-text),
[obtención de URL multimedia de WhatsApp](https://www.postman.com/meta/whatsapp-business-platform/request/ptjyi84/retrieve-media-url),
[precios y límites](https://dev.meta.ai/docs/pricing-rate-limits).
