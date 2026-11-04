# Bloqueos y verificaciones pendientes

**Última revisión del sandbox:** 2026-11-04. La app local quedó configurada para usar sólo Muse; la prueba de red falló por resolución DNS. El usuario reportó HTTP 401 en la ejecución anterior del smoke test; la validez del token sigue sin verificar. Los demás hallazgos conservan su fecha y nivel de evidencia. «No verificado» no significa «no existe».

| Área | Estado observado | Qué falta / cómo resolver | Fase |
|---|---|---|---|
| Entrevistas y evidencia comercial | El usuario reporta dos entrevistas; una persona expresó interés general en un panel para vender más y mejor. No hay fichas ni detalles en el workspace | Si se comparten detalles, registrar fichas anonimizadas; ampliar muestra y documentar problema, herramientas, impactos y disposición a pagar | F01 |
| Sector, dolor y disposición a pagar | Hipótesis del roadmap | Validar por ciudad/segmento y cotizar precio concreto sin inducir respuestas | F01 |
| Hostinger VPS | El usuario informa que mantiene un VPS con Ubuntu 24.04 y EasyPanel; se omiten hostname, IP y fechas de cuenta de esta documentación pública | F02/F01 no requieren SSH. En F04/F12 tomar usuario/IP exactos de hPanel, confirmar fingerprint y contar con permiso específico para acciones allí. No se conectó ni desplegó | F04/F12 |
| Dominio/DNS/TLS | Estado desconocido; roadmap menciona dominios orientativos | Confirmar propiedad/control y decidir nombres después; compra y cambios requieren autorización | F05 |
| Meta Business / App / número | No usado ni conectado en F02; elegibilidad de número colombiano desconocida | Para pruebas A–E falta proveedor y número de prueba elegible; consentimiento de historia y autorización operativa separada | F02/F06 |
| Sandbox Cloud API de Meta | El 2026-10-28 Meta aceptó un `hello_world`, Pendiva recibió un texto de prueba y Nebius y Muse lo analizaron con evidencia válida en comprobaciones separadas | Confirmar entrega del `hello_world` y mostrar y revisar el resultado Muse en el panel. El sandbox no valida Coexistence/historial/echo | F02 / HACK-02–03 |
| Proveedor oficial / BSP | Candidato provisional Kapso Platform; alternativa 360dialog; ninguno contratado | Confirmar por escrito Colombia, WAAC/PMA, coexistencia, Webhooks, historial, exportación/borrado, facturación, términos y precio total. Decisión no habilita compra | F02/F06 |
| Historial y eventos | Docs de BSP describen `history`, `smb_app_state_sync` y `smb_message_echoes`; cobertura no probada | Validar aceptación/rechazo, rango, completitud, latencia y eco de mensajes salientes desde Business App con número autorizado | F02 |
| Identidad, cola, proxy, IA | Decisiones abiertas | Mini-spike o evaluación cuando dependencias de F01/F02 se conozcan; registrar ADR | F03/F04 |
| Privacidad, tratamiento y transferencias | Requiere revisión contextual y jurídica | Definir retención, roles, consentimientos, terceros, exportación/borrado y revisión legal en Colombia antes de datos reales | F03/F11 |
| Repositorio GitHub | El usuario confirmó posteriormente que el repo ya está publicado | No es bloqueo de desarrollo; comprobar sincronización sólo si solicita publicar cambios nuevos | F00 |
| Conexión SSH a Hostinger | El usuario informó que generó e instaló una llave pública local; no se incluye su nombre ni material de llave. No se verificó servidor, usuario exacto ni fingerprint. Hostinger indica que `root` suele ser el usuario SSH predeterminado de VPS ([guía](https://support.hostinger.com/en/articles/9969102-how-to-troubleshoot-ssh-connection-issues-on-vps)) | En fase que requiera VPS, usar los datos copiados de hPanel (usuario/IP exactos), clave privada local sin exponerla y contrastar fingerprint con fuente confiable antes de aceptar. No conectarse para F01/F02 | F04/F12 |
| Descubrimiento comercial F01 | Guía y ficha anonimizante creadas; usuario informa dos entrevistas y una señal verbal de interés | Documentar las entrevistas previas con notas anonimizadas y ampliar la muestra; se requiere autorización específica para contactar terceros | F01 |

## Condiciones siguientes

- F01 tiene instrumentos listos y una señal inicial reportada por el usuario (dos entrevistas, una persona interesada en el concepto); aún faltan fichas de evidencia y una muestra mayor. Las notas deben anonimizarse y no deben recogerse chats/identificadores de clientes.
- F03 requiere F01 y F02. F02 documental/simulado se completó, pero el pilotaje real de coexistencia queda pendiente de número elegible y autorización operativa. No se debe anunciar cobertura total.
- SSH: el usuario indicó que instaló una clave pública local. No se expuso el contenido ni el nombre de la llave y no se estableció conexión. En F04/F12 se verificará el usuario que muestra hPanel y fingerprint; nunca se usará el servidor para el spike F02.
- El usuario confirmó que el repo de GitHub ya está publicado. Esta revisión sólo toca el workspace local; no hizo push.

## Estado del alcance de hackathon y SaaS

- Localmente hay ingesta y deduplicación de mensajes entrantes, oportunidades manuales y sugeridas con fuente, evidencia multimedia enlazada, bandeja de seguimientos, asistente, vistas configurables y borradores de respuestas bilingües. Muse prepara borradores con consentimiento y fuentes, pero no hay entrega saliente ni bot automático.
- La evaluación exploratoria de Muse de ocho casos sintéticos se registra en [evaluación de extracción](evaluacion-extraccion.md). Detectó una confusión entre presupuesto del cliente e importe cotizado y próximos pasos mejorables. No es una evaluación independiente ni demuestra precisión productiva.
- El código local incluye tenants, roles y algunas pruebas de aislamiento; eso no equivale a una auditoría completa. La colisión de análisis por remitente, la cobertura transversal de rutas y los archivos requieren resolución/verificación antes de un SaaS multiempresa.
- La URL abierta localmente no prueba que el proceso esté ejecutando la última versión; reiniciar la demo actualiza el código servido. No se realizó inspección visual integral en esta sesión.
- Para marcar el plan entero completado siguen haciendo falta, como mínimo: prueba de envío/estado de entrega en el sandbox; usuario confirma el destinatario sandbox y un texto de prueba exacto cuando toque enviar; auditoría integral de aislamiento; validación comercial con empresas y consentimiento; términos/retención y revisión legal; respaldos y recuperación; staging autorizado con TLS/observabilidad; y prueba de facturación/cancelación. No se han hecho envíos a clientes, despliegues, compras ni publicaciones de cambios nuevos.
