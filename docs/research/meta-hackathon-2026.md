# Investigación y guion — posible hackathon de Meta

**Actualización:** 2026-10-27. La convocatoria localizada es **Meta Global AI Developer Hackathon**; el usuario aún debe confirmar que sea esa. Las reglas oficiales completas del organizador se consultaron después de este primer informe; ver [plan actualizado](../plan-hackathon-muse-whatsapp.md).

## Información verificada en la convocatoria pública

La [página oficial de Meta](https://dev.meta.ai/events/global-hackathon) describe un evento virtual para participantes seleccionados, con categoría de desarrolladores independientes y categoría de startups. La primera menciona creatividad, ambición técnica y funcionamiento; la segunda menciona ejecución técnica y preparación para producción. Propone los temas **Build for Your World** y **Push the Frontier**, y presenta Meta Model API, modelos de Meta y Muse Code entre las herramientas disponibles.

La página indica que la postulación cerraba el **25 de octubre de 2026 a las 11:59 p. m. ET**, o antes si se llenaban los cupos; la entrega del proyecto figura para el **4 de noviembre de 2026 a las 9:00 p. m. ET**, equivalente a las **9:00 p. m. en Bogotá** ese día. La página advierte que las fechas pueden cambiar.

**Pendiente:** confirmar admisión y categoría del usuario, requisitos exactos de entrega, tratamiento del trabajo previo y uso de datos, y características exigidas al repositorio y video. Las [reglas oficiales](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver) se pudieron leer en el navegador y están resumidas en el [plan actualizado](../plan-hackathon-muse-whatsapp.md).

## Propuesta de Pendiva para Build for Your World

**Problema por validar:** una empresa pequeña que vende servicios por WhatsApp puede perder contexto entre conversaciones y dejar seguimientos pendientes. El usuario reportó dos entrevistas y una señal de interés; no se cuenta aún con evidencia suficiente de impacto ni con cifras de ventas.

**Propuesta:** Pendiva presenta conversaciones relevantes, señala qué se puede hacer después y permite revisar el mensaje que sustenta la sugerencia. El asesor decide si procede; un pago declarado sigue pendiente de verificación.

**Uso de Meta a demostrar:** ejecutar Muse Spark sobre una conversación de prueba y mostrar su resumen, siguiente paso y mensaje fuente. Hay un adaptador preparado conforme a la [documentación de Meta](https://dev.meta.ai/docs/quickstart), pero se requieren una clave autorizada, créditos o facturación y una prueba real antes de afirmar que funciona con el modelo. El número de prueba WhatsApp ya existe; token, destinatario y prueba real siguen pendientes. Son integraciones separadas.

## Guion sugerido de demostración

1. Presentar a **Brilla Hogar**, una empresa ficticia que atiende solicitudes de limpieza a domicilio.
2. Abrir el caso de Ana: pidió una cotización. Mostrar la conversación, el mensaje fuente y la acción sugerida.
3. Mostrar a Luisa: dijo que pagó, pero el panel pide verificarlo en lugar de dar el pago por confirmado.
4. Marcar una oportunidad como revisada y mostrar cómo cambian los indicadores. Volverla a pendiente si se desea repetir la demo.
5. Si está habilitada y probada la clave, usar **Analizar caso con Meta AI** y comparar el resultado con la evidencia original. De lo contrario, explicar que se muestra una simulación de producto y que falta la prueba real con Meta.
6. Cerrar con lo que queda para un piloto: integración WhatsApp probada, privacidad y autorización, aislamiento por empresa, y validación con clientes reales.

No presentar datos ficticios como métricas reales, ni el adaptador preparado como una integración validada. Las dos entrevistas reportadas son una señal preliminar, no prueba de demanda o ventas.
