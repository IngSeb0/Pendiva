# Viabilidad de WhatsApp Business para el SaaS

**Corte de investigación:** 2026-10-15. Precios publicados observados en esa fecha; pueden cambiar. Esta fase es investigación y contrato simulado: no se conectó Meta, un BSP, un número, el VPS ni una cuenta real.

## Conclusión ejecutiva

La viabilidad técnica es **plausible, aún no probada para el caso comercial**. Meta documenta Embedded Signup para proveedores tecnológicos y socios, pero exige revisión de la app y acceso avanzado para permisos de negocio antes de publicarla. La convivencia permite usar WhatsApp Business App y Cloud API en el mismo número cuando Meta lo habilita; la elegibilidad y la cobertura real del historial requieren validación con un número de prueba autorizado. La señal técnica más crítica es `smb_message_echoes`, que debe incluir los mensajes enviados desde la app del negocio.

Para una primera prueba de costo, **Kapso Platform** parece el camino menos pesado de los dos planes públicos revisados: publica USD 299/mes, 50 números incluidos y onboarding white-label; las tarifas Meta se trasladan aparte. Es una hipótesis de evaluación, no una selección ni compra. Meta directo podría quitar tarifa de BSP, pero exige implementar y operar Embedded Signup, revisión/permisos, facturación y cambios de plataforma. 360dialog tiene una oferta explícita multi-cliente pero mayor costo fijo público. Antes de decidir debe confirmarse por escrito elegibilidad de Colombia, WAAC/PMA, convivencia, límites/retención, exportación/desconexión, impuestos, SLA y contrato de tratamiento.

## Cambio de modelo de cuentas 2026

Meta publicó el 16 de junio de 2026 una evolución que separa WAAC (números telefónicos) y PMA (plantillas y facturación); permite que un número sea compartido por varias integraciones con facturación separada. Por tanto, el modelo de datos no debe suponer que WABA equivale a un único número o a una sola unidad de cobro. Guardaremos referencias opacas de proveedor/Meta y capacidad facturable por separado. La guía de migración y versiones concretas de endpoints deben revalidarse directamente en la documentación para desarrolladores antes de integrar: la documentación web de referencia sufrió limitación de acceso durante esta revisión.

## Comparativa

| Opción | Requisitos/costo de plataforma publicado | Onboarding SaaS | Convivencia, historia y ecosistema | Evaluación |
|---|---|---|---|---|
| Meta Cloud API directo | Sin tarifa de BSP en esta comparación; siguen las tarifas Meta por mensajería. Embedded Signup requiere App Review y Advanced Access a `business_management` y `whatsapp_business_management`. | Sí, flujo oficial para Tech Providers/Partners y Solution Partners; el SaaS asume la integración, permisos, soporte, facturación y evolución de API. | Coexistence debe confirmarse para la cuenta y el flujo elegibles. Configurar webhooks y conservar/normalizar eventos es responsabilidad propia. | Coste proveedor potencialmente menor al escalar; mayor inversión técnica y carga de cumplimiento. No es el camino más corto del spike. |
| Kapso | Free: USD 0 con límite publicado de 1 número y 2.000 mensajes de plataforma/mes; Pro USD 25/mes, 3 números y 100k mensajes; Platform USD 299/mes, 50 números, 1M mensajes, onboarding white-label y facturación Meta centralizada. Tarifas Meta aparte, según proveedor. | La página publica links de setup/Embedded Signup y Platform white-label. La documentación de coexistencia existe, pero compatibilidad exacta, Colombia, límites de sincronización, retención/exportación y obligaciones contractuales quedan por confirmar con el proveedor. | No se considera acreditada la cobertura de historial ni todos los ecosistemas de dispositivos por la oferta comercial. Debe probarse webhook y desconexión. | Candidato recomendado para solicitar una cotización y ejecutar spike autorizado, no decisión final. Coste de entrada público más sencillo para SaaS que el plan partner de 360dialog. |
| 360dialog Partner Platform | Starter €250/mes + €49 por canal estándar (incluye 5); Growth €500 + €25/canal (incluye 10); Premium €1.000 + €15/canal (incluye 20). Fee de licencia por número, más cargos de mensajería Meta. | Oferta explícita de plataforma multi-cliente, onboarding administrado y modelos Direct-Paid o Partner-Paid documentados. Se requiere alta de partner y método de pago; no se hizo. | Documenta `history`, `smb_app_state_sync` (contactos) y `smb_message_echoes` (mensajes enviados desde Business App). Ciertas apps/dispositivos acompañantes no generan ecos; limitaciones y actividad de la app móvil pueden afectar continuidad. Rango y completitud de historia no quedan garantizados. | Alternativa clara para comparar soporte y coste total. El mínimo fijo público hace falta justificarlo con demanda y pruebas. |

Los importes no incluyen impuestos, conversión FX ni tarifas Meta. Las cifras de Kapso son tarifa de proveedor, y la tabla de 360dialog corresponde a sus precios públicos consultados, no una oferta negociada. No se usa ninguna cifra de mensajería como presupuesto firme para Colombia: confirmar la rate card oficial y su vigencia directamente con Meta/proveedor antes de modelar margen.

## Embedded Signup, permisos y modelo de operación

- La colección oficial Meta indica que Embedded Signup sirve a Solution Partners, Tech Providers y Tech Partners. Para publicar, pide App Review y Advanced Access para `business_management` y `whatsapp_business_management`. Usar Cloud API; Meta marca On-Premises API como deprecada.
- El usuario empresarial debe consentir conexión y seleccionar/autorizar sus activos. Persistir únicamente identificadores necesarios, estado, alcance y marcas de tiempo; retirar tokens y datos al desconectar conforme al contrato y retención definida en F03.
- No copiar lógica de endpoints, permisos o formatos del ejemplo del proveedor como si fuera garantía de Meta. F06 debe basarse en las versiones documentadas vigentes de Graph API y Embedded Signup.
- Segmentar onboarding y facturación como recursos separados (WAAC/PMA y números) por el cambio anunciado en 2026.

## Coexistence y límites de cobertura

La documentación vigente de 360dialog para convivencia describe tres familias relevantes: eventos `history`, actualizaciones de contactos `smb_app_state_sync` y ecos de mensajes enviados desde WhatsApp Business App mediante `smb_message_echoes`. El evento de historia comunica aceptación/rechazo, chunks y progreso; un rechazo está representado con error. Esto hace técnicamente viable intentar analizar ambas direcciones del trabajo comercial **si** Meta habilita convivencia y el webhook de ecos está configurado correctamente.

Límites documentados por el BSP: elegibilidad controlada por Meta; no debe prometerse historia completa ni un rango fijo; el cliente puede declinar historial. Mantener WhatsApp Business App activa con regularidad. Algunos dispositivos acompañantes se desvinculan durante el alta y ciertos clientes (incluidos Windows/WearOS según la guía consultada) no tienen soporte completo; mensajes enviados desde aplicaciones no soportadas pueden no producir webhooks. Confirmar restricciones actualizadas para cada número antes de onboarding. Registrar el hueco de cobertura y mostrarlo en producto: “datos sincronizados desde…” y última sincronización, no “todas las conversaciones”.

Al desconectar, revocar/limpiar vínculo y detener ingestión; documentar qué ocurre con los activos Meta y con historial ya importado. La eliminación de nuestros datos, exportación y tiempos de purga son requisitos del SaaS que no quedan resueltos por la API del proveedor.

## Política de producto e IA

Los términos de WhatsApp Business Solution (actualizados 6 de marzo de 2026) prohíben a proveedores de IA ofrecer en WhatsApp su asistente general cuando esa sea la función principal, salvo excepciones por jurisdicción (EEE/Brasil). Colombia no aparece entre las excepciones del texto revisado. Los términos permiten que una empresa contrate un proveedor de IA como tercero para ejecutar instrucciones de su negocio, pero restringen usar datos de Business Solution para entrenar o mejorar modelos de terceros; el ajuste fino queda limitado al uso exclusivo descrito en términos.

Por eso el alcance aquí es analítica/inteligencia comercial de conversaciones de negocios, con salidas para la empresa y evidencia verificable, no distribución de un asistente general de IA dentro de WhatsApp. Requiere revisión legal de términos, tratamiento, transferencias, base/consentimiento y contrato con cada subprocesador antes de datos reales.

## Matriz de costos de evaluación

| Escenario mensual, antes de tarifas Meta | Kapso Platform | 360dialog Starter Partner |
|---|---:|---:|
| 5 números conectados | USD 299 (50 números incluidos) | €250 + 5 × €49 = €495 |
| 10 números conectados | USD 299 (50 incluidos) | €500 + 10 × €25 = €750 (Growth, 10 incluidos) |

Esto compara sólo los importes publicados de plataforma/canales. No se equiparan mensaje incluido, monedas, alcance de soporte, créditos ni obligaciones. Solicitar cotización y modelar tasa/categoría/país usando rate card oficial vigente antes de selección.

## Fuentes consultadas

- [Meta: Embedded Signup, colección oficial de WhatsApp Business Platform](https://www.postman.com/meta/whatsapp-business-platform/documentation/du6gzjv/embedded-signup) — permisos y publicación.
- [Meta: colección oficial Cloud API](https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api) — Cloud API y permisos.
- [Meta: evolución del modelo de cuentas WAAC/PMA, 16-06-2026](https://developers.meta.com/resources/videos/whatsapp-account-model-evolution/) — separación entre números, plantillas y facturación.
- [Meta: WhatsApp Business Solution Terms](https://www.whatsapp.com/legal/business-solution-terms) — IA, datos y terceros; modificación 06-03-2026.
- [Kapso: planes y precios](https://kapso.com/pricing) y [documentación](https://docs.kapso.ai/llms.txt) — oferta y árbol de documentación, fuente comercial/de proveedor.
- [360dialog: Partner Platform](https://360dialog.com/es/partners) — precio SaaS para socios.
- [360dialog: convivencia](https://docs.360dialog.com/docs/hub/embedded-signup/coexistence-onboarding), [webhooks de convivencia](https://docs.360dialog.com/partner/onboarding/whatsapp-coexistence/coexistence-webhooks) y [restricciones del modo Coexistence](https://docs.360dialog.com/docs/resources/phone-numbers/coexistence.md) — documentación BSP, no sustituto de aceptación por Meta.
- [360dialog: precios directos por canal](https://docs.360dialog.com/docs/get-started/pricing) — tarifa de licencia; distinta del plan Partner Platform.

## Desconocido hasta prueba real autorizada

Elegibilidad de un número colombiano concreto; alta con Companion Device existente; aceptación/declinación de historia; rango y orden del histórico exportado; presencia y latencia de cada eco saliente; duplicación/reorden; reconexión tras desconexión; exportación/borrado; tarifas Meta efectivas y elegibilidad/soporte contractual de Kapso o 360dialog para Colombia y el modelo WAAC/PMA.
