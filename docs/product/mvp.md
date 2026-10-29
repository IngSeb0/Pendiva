# Definición funcional del MVP — propuesta por validar

**Estado:** alcance transcrito y organizado desde el roadmap de referencia; pendiente de validación comercial en F01. No implica entrevistas realizadas, producto implementado ni aprobación de proveedores.

## Usuario y objetivo

Responsable comercial o dueño de una empresa colombiana de servicios con 1–5 asesores que atiende cotizaciones por WhatsApp. Los segmentos iniciales de investigación son limpieza de muebles, impermeabilización, reparaciones, aire acondicionado y cámaras de seguridad. No se presume que compartan necesidad o presupuesto.

El producto busca conectar, cuando el número sea elegible y con integración oficial, el WhatsApp Business que la empresa ya usa, mantener la atención en la aplicación y presentar contexto comercial verificable: clientes, oportunidades, cotizaciones pendientes, compromisos, evidencia y siguientes acciones.

## Capacidades dentro del alcance propuesto

- Registro de empresa, acceso seguro y roles básicos.
- Onboarding con Embedded Signup / Coexistence solo si el número y el proveedor lo permiten.
- Estado de conexión, cobertura e historial realmente disponible; mostrar límites y última sincronización.
- Ingesta de mensajes entrantes, salientes y eventos admitidos por el proveedor.
- Contactos separados de oportunidades; una persona puede tener varias oportunidades.
- Etapas comerciales, pendientes y promesas sugeridas por reglas/IA con enlace a mensaje fuente, fecha y confianza.
- Corrección manual, historial de cambios y marcación de tareas completadas.
- Tabla con búsqueda/filtros, detalle del cliente, resumen de pendientes y consultas limitadas a datos verificables.
- Exportación, desconexión, proceso de eliminación, monitoreo, control de costos y aislamiento entre empresas.

## Fuera de alcance

- Respuestas automáticas de chatbot, campañas o envío masivo.
- Confirmar pagos sin integración bancaria o verificación humana.
- Inferir abandono por silencio; importar grupos, medios o historial no disponible en la plataforma oficial.
- Diagnóstico de humedades/filtraciones mediante imágenes o presupuestos definitivos de obra.
- CRM empresarial completo, omnicanal, llamadas, ERP, app móvil nativa, Kubernetes o microservicios.

## Reglas de interpretación y seguridad

1. Contacto, conversación, oportunidad y actividad son entidades distintas.
2. Falta de respuesta significa «sin respuesta», no «perdido», salvo confirmación explícita o decisión manual.
3. «Dijo que pagó» significa «pago por verificar».
4. Conclusiones automáticas muestran fuente, fecha y confianza y admiten corrección.
5. Ante evidencia insuficiente: `sin_clasificar`, `incierto` o `requiere_revision`.
6. La interfaz declara cobertura/completitud y última sincronización; nunca promete sincronización íntegra sin evidencia.
7. Los datos de una empresa no son visibles a otra.
8. El asesor debe poder seguir atendiendo desde WhatsApp Business en el MVP.

## Criterios de producto derivados del roadmap

- Una promesa de cotización vencida sin evidencia de envío genera una tarea con referencia al mensaje que contiene la promesa.
- Una objeción de precio puede registrarse como tal, sin concluir que sea la causa única de pérdida.
- Un pago declarado por el cliente queda pendiente de verificar.
- La cobertura parcial se comunica y evita afirmaciones absolutas sobre el historial.
- Eventos repetidos no producen mensajes/tareas duplicados (a validar en la fase de ingesta).
- Un usuario de otra empresa no puede consultar conversación ni metadatos ajenos.
- Tras reinicio, el procesamiento debe recuperarse conforme a la estrategia de confiabilidad que se defina.

## Validación pendiente

F01 debe confirmar problema, sector inicial, volumen, disposición de pago y pilotos con entrevistas reales. F02 debe verificar capacidades y restricciones actuales de Meta/proveedores con fuentes oficiales. Hasta entonces, el usuario, la propuesta de valor, la elegibilidad, precios y cobertura de datos son hipótesis del roadmap.
