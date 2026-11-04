# Guion de demo: negocio de limpieza

**For an English recording**, use the current [Pendiva English Demo Recording Pack](demo-recording-pack-en.md)
and start the isolated seed with `--demo-language en`. This older page is retained as a Spanish
reference.

## Antes de comenzar

Inicia `python -m scripts.iniciar_demo --demo`. El comando muestra las credenciales del
usuario ficticio. Comprueba que la voz del navegador esté disponible y que las credenciales
de los proveedores necesarios estén configuradas. Para usar micrófono, concede el permiso
del navegador cuando lo solicite. Ninguna llamada de IA o de voz se realiza al iniciar.
Mantén abierto este guion y ten una alternativa escrita si falla el dictado o la voz.

## Presentación

1. **0:00–0:35 · El problema.** En Clientes, abre a Ana. Muestra su consulta sobre un sofá,
   el siguiente paso sugerido y la evidencia. Explica que el dueño conserva la decisión.
2. **0:35–1:15 · La imagen.** En los archivos de Ana enseña la ilustración ficticia. Si se
   cuenta con consentimiento para enviarla a Meta y créditos, pulsa «Analizar con Muse» y
   revisa la observación. Si la red falla, describe la función sin fingir un resultado.
3. **1:15–2:05 · El asistente.** Abre la burbuja, elige un proveedor y acepta el envío del
   contexto. Dicta o escribe «¿Qué información falta para cotizar el sofá de Ana?». Revisa
   la transcripción antes de enviarla y muestra la respuesta y sus fuentes. El indicador animado
   refleja escucha, procesamiento y habla, pero no es una onda de audio real. La voz del
   navegador depende del dispositivo y no crea un archivo; ElevenLabs para dictado requiere
   consentimiento y puede usar créditos.
4. **2:05–3:00 · Acción concreta.** En Mejoras, ejecuta «Datos por completar · ejemplo» y
   abre un cliente. Muestra que la vista usa datos de la ficha manual. Opcionalmente abre la
   vista previa de seguimiento: una cotización sin fecha aparece como información faltante.

## Lo que esta demo no demuestra

- Los nueve clientes, las conversaciones y los archivos incluidos son ficticios.
- La recepción de texto real desde el sandbox se verificó por separado; la recepción de
  imagen y audio de WhatsApp aún no se ha validado de extremo a extremo.
- Pendiva no recupera necesariamente el historial previo ni los mensajes salientes.
- Las observaciones de IA son sugerencias. No confirman precios, pagos ni reservas.
- Las herramientas actuales son vistas de reglas limitadas y no ejecutan código generado ni
  envían mensajes a clientes. La aplicación local no está lista para acceso público.

Documentación de la plataforma: [reconocimiento de voz](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition)
(disponibilidad limitada y posible procesamiento remoto) y [evento de fin de voz](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/end_event).
