# ADR 001: estrategia de proveedor de WhatsApp (F02)

- **Estado:** candidato para spike; no aprobado para compra ni integración real.
- **Fecha:** 2026-10-15.
- **Contexto:** el SaaS necesita conectar negocios a WhatsApp y analizar mensajes entrantes y salientes. Embedded Signup requiere proceso de revisión/acceso avanzado y el modelo de cuentas Meta cambia en 2026. Coexistence depende de elegibilidad y puede no sincronizar todo el historial o todos los dispositivos.
- **Decisión provisional:** mantener una interfaz propia por proveedor y no acoplar dominio a WABA o a un BSP. Para un spike futuro, pedir acceso/cotización a Kapso Platform primero; incluir 360dialog como comparación. No iniciar onboarding/compra. Meta directo permanece como opción de largo plazo.
- **Razones:** Kapso publica oferta SaaS white-label e importe Platform menor al coste fijo público de 360dialog Starter; 360dialog documenta explícitamente ecos de mensajes de Business App y flujos históricos; ambas opciones tienen preguntas operativas aún abiertas. Un simulador permite probar dominio/contratos sin afirmar integración.
- **Consecuencias:** referencias de cuenta y unidades facturables deben ser opacas y desacopladas; representar permisos, consentimiento, estado de sincronización, cobertura parcial, idempotencia y desconexión. No diseñar producto con garantía de historial total. El proveedor podría intercambiarse sólo si el normalizador evita formatos del BSP en dominio.
- **Revisitar cuando:** número elegible y autorizado para pruebas; confirmación por escrito de Colombia, WAAC/PMA, SLA, retención/exportación/borrado, pricing completo y contrato de tratamiento; evidencia de ecos de mensajes enviados desde la app y matriz A–E completada.

## Alternativas consideradas

1. **Meta Cloud API directo:** evita una licencia BSP pública, pero impone alta carga de App Review, Advanced Access, Embedded Signup, soporte, cambios API, facturación y validación de convivencia. No es el primer spike sugerido.
2. **Kapso:** mejor coste público de entrada para validar un SaaS con onboarding de marca. Debe validar cobertura de Coexistence y garantías comerciales antes de elegirse.
3. **360dialog:** BSP con flujo partner y coexistence webhooks documentados, pero su coste fijo público merece validación comercial antes de comprometerse.

## Implicaciones del modelo Meta

Tratar WAAC, PMA, número y proveedor como entidades con referencias separadas. No asumir que identificador de WABA, número y cartera de cobro tienen una relación 1:1. Revalidar guía técnica y versiones de endpoint Meta en F06.
