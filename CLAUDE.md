# Contexto del proyecto para Claude

## Producto

Planificación de un SaaS de inteligencia comercial para empresas de servicios que atienden oportunidades por WhatsApp Business. La hipótesis es ayudar al equipo a dar seguimiento a cotizaciones y conversaciones, con evidencia trazable y sin quitarle al negocio el canal que ya usa.

El alcance funcional propuesto está en [`docs/product/mvp.md`](docs/product/mvp.md). La arquitectura de Hostinger VPS + Docker Compose y el stack descrito allí siguen siendo propuestas hasta que una fase de diseño las valide.

## Estado y fuentes

- Lee [`README.md`](README.md) y [`docs/roadmap.md`](docs/roadmap.md) para el estado actual.
- Las decisiones están en [`docs/decisions/`](docs/decisions/); la matriz técnica, descubrimiento y bloqueos están en [`docs/research/`](docs/research/) y [`docs/validation/`](docs/validation/).
- Trata el roadmap fuente como referencia de alcance, no como prueba de que las capacidades o recursos externos estén disponibles.
- Evidencia comercial reportada por el usuario: dos entrevistas previas; una persona expresó interés en un panel que ayude a vender más y mejor. Es una señal inicial autoinformada, no validación de mercado, compromiso de compra ni una entrevista documentada en detalle.
- WhatsApp Cloud API dispone de recursos de prueba de Meta para mensajes básicos. Un envío con `hello_world` no demuestra coexistencia con WhatsApp Business App, sincronización de historial ni cobertura de mensajes enviados desde la app.

## Cómo colaborar

Usa criterio y avanza de forma autónoma en el alcance que pidió el usuario. Inspecciona el estado del proyecto antes de editar; conserva trabajo existente; consulta fuentes oficiales actuales antes de una integración; separa hechos, inferencias y pendientes. Mantén las decisiones importantes documentadas y deja código nuevo acompañado de pruebas útiles.

No incluyas secretos o datos reales de clientes en archivos del proyecto. Antes de compras, mensajes a terceros, conexión de cuentas reales, despliegues productivos o cambios destructivos, confirma que la petición autoriza esa acción concreta. Las instrucciones más detalladas están en [`AGENTS.md`](AGENTS.md).

## Prueba de envío Cloud API

Meta documenta una cuenta/número de test y la plantilla `hello_world`. La guía de pasos y el script local están en [`docs/validation/meta-cloud-api-test.md`](docs/validation/meta-cloud-api-test.md) y [`scripts/whatsapp_test_smoke.py`](scripts/whatsapp_test_smoke.py). Ejecutar el script sin `--send` es modo seco. El envío real requiere credenciales temporales del entorno de test y un destinatario propio añadido/permitido en Meta; no se deben pegar tokens en el chat ni guardarlos en Git.
