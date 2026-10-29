# Bloqueos y verificaciones pendientes

**Última revisión del sandbox:** 2026-10-28. Los demás hallazgos conservan su fecha y nivel de evidencia. «No verificado» no significa «no existe».

| Área | Estado observado | Qué falta / cómo resolver | Fase |
|---|---|---|---|
| Entrevistas y evidencia comercial | El usuario reporta dos entrevistas; una persona expresó interés general en un panel para vender más y mejor. No hay fichas ni detalles en el workspace | Si se comparten detalles, registrar fichas anonimizadas; ampliar muestra y documentar problema, herramientas, impactos y disposición a pagar | F01 |
| Sector, dolor y disposición a pagar | Hipótesis del roadmap | Validar por ciudad/segmento y cotizar precio concreto sin inducir respuestas | F01 |
| Hostinger VPS | Usuario informa que hay VPS Hostinger KVM 2, Ubuntu 24.04 + EasyPanel, host `srv1230927.hstgr.cloud`, IP `46.202.191.56`, activo hasta 2026-12-27 | F02/F01 no requieren SSH. En F04/F12 tomar usuario/IP exactos de hPanel, confirmar fingerprint y contar con permiso específico para acciones allí. No se conectó ni desplegó | F04/F12 |
| Dominio/DNS/TLS | Estado desconocido; roadmap menciona dominios orientativos | Confirmar propiedad/control y decidir nombres después; compra y cambios requieren autorización | F05 |
| Meta Business / App / número | No usado ni conectado en F02; elegibilidad de número colombiano desconocida | Para pruebas A–E falta proveedor y número de prueba elegible; consentimiento de historia y autorización operativa separada | F02/F06 |
| Sandbox Cloud API de Meta | El 2026-10-28 Meta aceptó un `hello_world`, Pendiva recibió un texto de prueba y Nebius y Muse lo analizaron con evidencia válida en comprobaciones separadas | Confirmar entrega del `hello_world` y mostrar y revisar el resultado Muse en el panel. El sandbox no valida Coexistence/historial/echo | F02 / HACK-02–03 |
| Proveedor oficial / BSP | Candidato provisional Kapso Platform; alternativa 360dialog; ninguno contratado | Confirmar por escrito Colombia, WAAC/PMA, coexistencia, Webhooks, historial, exportación/borrado, facturación, términos y precio total. Decisión no habilita compra | F02/F06 |
| Historial y eventos | Docs de BSP describen `history`, `smb_app_state_sync` y `smb_message_echoes`; cobertura no probada | Validar aceptación/rechazo, rango, completitud, latencia y eco de mensajes salientes desde Business App con número autorizado | F02 |
| Identidad, cola, proxy, IA | Decisiones abiertas | Mini-spike o evaluación cuando dependencias de F01/F02 se conozcan; registrar ADR | F03/F04 |
| Privacidad, tratamiento y transferencias | Requiere revisión contextual y jurídica | Definir retención, roles, consentimientos, terceros, exportación/borrado y revisión legal en Colombia antes de datos reales | F03/F11 |
| Repositorio Git local | No existía al iniciar; se está preparando estructura F00 | Inicializar historial solo después de documentar y confirmar alcance; no hay cambios previos que proteger | F00 |
| Repositorio GitHub | El usuario autorizó crear `IngSeb0/pendiva`; el conector instalado no expone la operación de crear repositorios y el navegador integrado solicita iniciar sesión | Completar creación autenticada del repo privado, añadir remote y publicar el estado preparado; no exponer secretos | F00 |
| Git local | El commit requiere `user.name`/`user.email`; además, el sandbox deniega escritura a `.git/index` al actualizar el staging | Habilitar escritura de Git en `.git` y definir la identidad de autor; crear commit F00 y luego enlazar/push cuando exista remoto | F00 |
| Conexión SSH a Hostinger | Llave `hostinger_nueva` generada en Windows e instalada según el usuario. `Acer` es su usuario Windows, no necesariamente el de VPS. Hostinger indica que `root` suele ser el usuario SSH predeterminado de VPS ([guía](https://support.hostinger.com/en/articles/9969102-how-to-troubleshoot-ssh-connection-issues-on-vps)); no se verificó servidor, usuario exacto ni fingerprint | En fase que requiera VPS, usar los datos copiados de hPanel (usuario/IP exactos), clave privada local sin exponerla y contrastar fingerprint con fuente confiable antes de aceptar. No conectarse para F01/F02 | F04/F12 |
| Descubrimiento comercial F01 | Guía y ficha anonimizante creadas; usuario informa dos entrevistas y una señal verbal de interés | Documentar las entrevistas previas con notas anonimizadas y ampliar la muestra; se requiere autorización específica para contactar terceros | F01 |

## Condiciones siguientes

- F01 tiene instrumentos listos y una señal inicial reportada por el usuario (dos entrevistas, una persona interesada en el concepto); aún faltan fichas de evidencia y una muestra mayor. Las notas deben anonimizarse y no deben recogerse chats/identificadores de clientes.
- F03 requiere F01 y F02. F02 documental/simulado se completó, pero el pilotaje real de coexistencia queda pendiente de número elegible y autorización operativa. No se debe anunciar cobertura total.
- SSH: el usuario indicó que instaló la clave pública local `hostinger_nueva.pub`. No se expuso el contenido de la llave ni se estableció conexión. En F04/F12 se verificará el usuario que muestra hPanel y fingerprint; nunca se usará el servidor para el spike F02.
- El usuario autorizó crear el repo GitHub; la publicación sigue pendiente de una sesión autenticada y una herramienta de creación disponible.
