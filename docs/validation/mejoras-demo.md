# Mejoras de demo y límites verificados

## Cambios implementados

- La interfaz local usa únicamente Muse (Meta Model API). El proveedor heredado en `.env` ya no
  controla las llamadas de la aplicación. Muse necesita `MODEL_API_KEY`; la credencial de WhatsApp
  es independiente.
- El idioma elegido se manda en cada pregunta y análisis nuevos. Al cambiar a English, respuestas
  nuevas de Muse deben estar en inglés; resultados almacenados anteriormente conservan su idioma.
- La búsqueda del asistente examina localmente todas las conversaciones del tenant y envía como
  máximo 36 fuentes relevantes, con cada fragmento limitado. No manda la base completa al modelo.
  El asistente muestra cobertura y límites; una respuesta no debe presentarse como análisis de
  cada mensaje si sólo se adjuntó una muestra.
- Finanzas incluye una gráfica mensual de barras para ventas y gastos registrados, con máximos
  de 12 meses y fuente declarada como CSV local. No equivale a Power BI conectado ni a una fuente
  contable/bancaria. Los agregados siguen disponibles para todos los meses.

## Estado de voz

El botón «Iniciar conversación por voz» activa turnos manos libres: el navegador reconoce voz,
Pendiva envía cada transcripción a Muse, lee la respuesta con la voz del dispositivo y vuelve a
escuchar. Requiere permiso de micrófono, `SpeechRecognition` del navegador y consentimiento de IA;
la nota junto al selector advierte que el servicio de reconocimiento puede recibir el audio.
El usuario puede terminar la sesión o detener una respuesta. Esto no es voz a voz de baja latencia:
Muse Voice Transcribe ofrece transcripción realtime por WebSocket, pero no sintetiza ni conversa
por sí solo. El reconocimiento y la voz actuales dependen del navegador/dispositivo.

## Error de envío WhatsApp

La prueba registrada devolvió HTTP 401 desde Cloud API. Eso indica que Meta rechazó la credencial
o autorización presentada; no afecta las credenciales de Muse ni implica que el panel esté roto.
El script de prueba no imprime el token ni el cuerpo sensible del error. En el dashboard hay que
crear un token vigente con permisos para el WABA/número de prueba y reemplazar sólo
`WHATSAPP_TEST_ACCESS_TOKEN` en `.env`; después verificar la app/número/recipiente configurados.
No guardar tokens en Git ni pegarlos en el chat. La siguiente prueba `--send` al mismo destinatario
sandbox requiere ser una acción autorizada; aceptación HTTP 2xx tampoco prueba entrega al teléfono.

## Pendiente para una demo excelente

- Revisar el recorrido visual en el dispositivo y probar ES/EN, tema oscuro, pantallas pequeñas,
  micrófono, texto a voz, errores de red y reducción de movimiento.
- Probar Muse en ambos idiomas con casos ficticios representativos y revisar salidas por una persona;
  registrar calidad por caso, no sólo éxito HTTP.
- Para una vista ejecutiva de negocio: diferenciar importe mencionado, presupuesto del cliente,
  venta facturada y gasto; añadir moneda y periodo antes de comparar márgenes. Hoy el CSV no define
  moneda y no se deben mostrar conclusiones de margen como datos contables verificados.
- La evaluación competitiva, prueba sandbox de entrega, aislamiento integral y publicación todavía
  requieren sus accesos y validaciones externos.

## Fuentes de producto Meta

- [Modelos y capacidades](https://dev.meta.ai/docs/models)
- [Tarifas y límites](https://dev.meta.ai/docs/pricing-rate-limits)
- [Transcripción de voz y endpoint realtime](https://dev.meta.ai/docs/speech-to-text)
- [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api/)
