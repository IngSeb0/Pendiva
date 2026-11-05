# Pendiva — Hackathon demo recording script

**Recording target:** 3 minutes. The instructions are in Spanish; speak only the quoted English narration. Set the interface to English and use the fictional English demo data. This script shows Pendiva calling its configured AI service after explicit consent; the UI brands the assistant as Pendiva.

## Preparación

1. Desde la raíz del repo, ejecuta en PowerShell:

   ```powershell
   python -m scripts.iniciar_demo --demo --demo-language en --demo-no-finance --demo-db data/pendiva-hackathon-en.sqlite3
   ```

2. Deja esa ventana abierta. Cuando aparezca `Panel: http://127.0.0.1:8000`, abre esa dirección. Si el puerto ya está ocupado, detén la otra demo con `Ctrl+C` y vuelve a ejecutar el comando.
3. Inicia sesión con `demo@pendiva.local` y `demo-password-local-2026`. El cargador vuelve a sincronizar esta contraseña demo al iniciar. Si antes viste 429, reiniciar el proceso limpia el límite temporal.
4. Verifica que **Pendiva · AI configured** aparezca arriba. Esto confirma que hay una variable `MODEL_API_KEY` en el `.env`, pero no verifica que el servicio remoto responda. Antes de grabar, envía una pregunta escrita de prueba. Si dice **AI setup needed**, detén la grabación y revisa la clave en el `.env` local. No la pegues en el chat ni la muestres en pantalla.
5. Entra a **Ana Rojas** y confirma que se ve el hilo largo de 14 mensajes. Cierra DevTools y deja el navegador a 100–110% de zoom.
6. Abre el asistente de Pendiva y marca el consentimiento antes de la pregunta: se envían a Meta la pregunta, el contexto del negocio, hasta 36 fragmentos pertinentes y hasta 3 turnos previos. Puede consumir créditos. No se envía toda la base de datos. Prueba el micrófono antes de grabar.

## Recorrido y narración exacta

| Tiempo | Instrucciones para mostrar (español) | Narración (inglés) |
|---|---|---|
| 0:00–0:20 | En **Overview**, muestra el resumen y **Needs Attention**. No te detengas en indicadores financieros. | “Service businesses run on conversations. But when a quote takes message after message, the owner spends time chasing details instead of serving customers. Pendiva turns the conversations it has received into clear, reviewable next steps.” |
| 0:20–0:55 | Abre **Customers → Ana Rojas**. Desplázate por sus 14 mensajes y muestra el conteo de cliente y negocio, los intercambios repetidos, la pregunta por una cotización y los datos que aún faltan. | “Here, Ana has already shared the service, the sofa size, the neighborhood, and the stain. After several back-and-forth messages, she is still waiting for a quote. The exact service address is still missing, and Thursday afternoon availability has not been confirmed. Pendiva makes those gaps visible instead of guessing a price or promising a time.” |
| 0:55–1:15 | Muestra **Prepare reply**. Explica que abre un borrador editable. No lo envíes por WhatsApp. Vuelve al asistente. | “The owner can prepare an editable reply, check it, and decide what to do. Pendiva does not send a message without the business owner.” |
| 1:15–2:25 | En el asistente, marca el consentimiento. Pulsa **Start voice conversation**, permite el micrófono y di con claridad la pregunta exacta de abajo. Deja de hablar y espera diez segundos completos sin seguir hablando. Pendiva enviará la pregunta y leerá la respuesta. Muestra citas y cobertura; si el audio no inicia, escribe la misma pregunta y pulsa **Ask Pendiva**. | “I’m asking Pendiva to review this long conversation, separate what we know from what is still missing, and recommend one useful next step. I can speak naturally; after ten seconds of silence, Pendiva sends the question, answers, and reads the response aloud. The cited messages let the owner verify the recommendation.” |
| 2:25–2:45 | Señala un mensaje citado y el icono de altavoz. No afirmes que la transcripción contiene todo WhatsApp: la cobertura muestra únicamente lo guardado en la demo. | “This is grounded in a limited set of stored messages. I can open the cited evidence or replay the answer with the speaker button. The owner stays in control.” |
| 2:45–3:00 | Regresa al overview. | “Pendiva is more than a chatbot attached to a CRM. It connects conversation history, evidence, and the next decision—so service-business owners can spend less time repeating follow-ups and more time doing the work.” |

### Pregunta exacta para Pendiva

> “Review Ana Rojas’s conversation. Count the messages in this thread, separate what is already known from what is still missing before a quote, and recommend one next question that confirms the exact service address and Thursday availability together. Cite the supporting messages.”

**Revisa la respuesta que produzca la IA antes de grabar.** El texto puede variar. Debe responder en inglés, mencionar sólo hechos respaldados por mensajes citados, indicar el alcance mostrado y evitar inventar un precio o una reserva. Si devuelve error, no grabes un resultado falso como respuesta real: usa el borrador guardado o corrige la configuración del modelo.

## Qué hacen los botones

- **Start voice conversation:** inicia el micrófono. Al detectar diez segundos sin voz reconocida, envía la transcripción a Pendiva y lee la respuesta. Si sigues hablando, el contador vuelve a empezar.
- **Ask Pendiva:** envía la pregunta escrita o transcrita después de marcar el consentimiento.
- **Prepare reply:** crea texto editable con contexto guardado; hay que revisarlo y guardarlo. No lo envía por WhatsApp.
- **View evidence:** lleva a los mensajes que respaldan la recomendación.
- **Speaker icon:** reproduce la respuesta ya escrita usando la voz del dispositivo; no genera ni envía otro archivo de audio.
- **Consent checkbox:** autoriza una consulta a Meta AI con la pregunta, el contexto del negocio, hasta 36 fuentes pertinentes y hasta 3 preguntas previas. Puede consumir créditos.

## Límites que debes decir si preguntan

- Los clientes y mensajes de este walkthrough son ficticios.
- La demo no recupera automáticamente mensajes anteriores al webhook ni garantiza que tenga toda la conversación de WhatsApp.
- La llamada a la IA revisa una selección limitada de hasta 36 fuentes pertinentes; el panel muestra la cobertura y las citas disponibles.
- La respuesta es una recomendación que debe revisar una persona. No prueba que se envió un mensaje, se confirmó una cita o se obtuvo una venta.
- La voz usa reconocimiento del navegador y síntesis de voz del dispositivo; el recorrido es por turnos y tiene una espera de silencio de 10 segundos.
- Nunca muestres `.env`, claves, chats reales, datos de clientes ni DevTools.

## Respaldo

Si la respuesta por voz falla, prueba una sola vez con la pregunta escrita. Si falla la respuesta de IA, no la presentes como lista: muestra los mensajes, el ejemplo sintético etiquetado y el borrador editable, y continúa con el pitch dejando claro que la conexión de IA no respondió. El video y su URL los graba y entrega el propietario; todavía no se han grabado ni subido.
