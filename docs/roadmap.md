# Roadmap y backlog

**Línea base:** `ROADMAP_AGENTE_SAAS_WHATSAPP_HOSTINGER.md` v1.0 (13-10-2026), recibido como documento de referencia. Las prioridades reflejan dependencias/riesgo descritos en él; no son compromisos de fechas. El roadmap fuente estima tiempos orientativos, no los confirma.

## Estado

- **F00 — Auditoría y planificación:** entregables preparados y publicados en `IngSeb0/Pendiva`, rama `e`.
- **F01 — Validación comercial:** instrumentos listos. El usuario reportó dos entrevistas previas y una señal verbal de interés por un panel que ayude a vender más y mejor. Falta documentar detalles anonimizados de esas entrevistas y ampliar la muestra; no hay base para decidir segmento, precio o mercado.
- **F02 — Viabilidad de WhatsApp:** investigación, adaptador simulado, smoke-test y spike local de Embedded Signup preparados. El 2026-10-28 Meta aceptó un envío `hello_world` y el webhook de Pendiva recibió un texto del teléfono sandbox autorizado. La entrega del `hello_world` y Coexistence siguen sin validarse.
- **F03–F15:** no iniciadas. La fundación técnica de Fase 0 y Fase 1 del plan de inteligencia comercial está implementada localmente, pero no sustituye la validación comercial, la migración a PostgreSQL ni un despliegue cloud.
- **Trabajo encontrado al inicio de F00:** ninguno. Durante F02 se añadió un adaptador simulado, no una integración real.
- **Excepción de prototipo solicitada:** se añadió un demo local para hackathon con fixtures sintéticos. No declara F03/F04 completos ni habilita despliegue público. Ver [ADR 003](decisions/003-hackathon-prototype.md).
- **Entrega actual elegida el 2026-10-28:** demo de hackathon con sandbox, sólo Pendiva. Arranque unificado, túnel aislado, suscripción y callback comprobados; texto ficticio recibido desde el teléfono autorizado y analizado realmente con Nebius. La recomendación quedó pendiente de decisión humana. Muse analizó el mismo mensaje por separado y ahora el panel permite seleccionar el proveedor configurado; la bandeja de prioridades, el resumen del dueño, autenticación local y el análisis de ventas/gastos importados están implementados localmente. Mostrar y revisar una recomendación real con Muse, además de los requisitos del concurso, siguen pendientes. Ver [ADR 007](decisions/007-operacion-demo-sandbox.md) y [validación de Muse](validation/muse.md).
- **Fundación SaaS local — 2026-10-28:** Fase 0 y Fase 1 del plan de inteligencia comercial implementadas de forma aditiva: contrato de dominio, perfiles sectoriales, validadores, tenants, usuarios, membresías, roles, sesiones revocables, auditoría y pruebas de aislamiento. Falta integrar todas las rutas existentes con el tenant de sesión, conectar cada número de WhatsApp a un tenant y migrar la persistencia a PostgreSQL antes de cloud.

## Backlog priorizado

| ID | Prioridad | Fase / tarea | Dependencias | Criterio de aceptación resumido | Estado |
|---|---|---|---|---|---|
| F00-01 | P0 | Inventariar archivos, Git, stack, entornos y nombres de variables sin leer valores secretos | Ninguna | Hallazgos y desconocidos registrados; cambios preexistentes preservados | Hecho: workspace vacío y sin Git |
| F00-02 | P0 | Especificar límites funcionales y reglas del MVP | F00-01 | Documento diferencia dentro/fuera, evidencia, cobertura y aislamiento; hipótesis marcadas | Hecho: borrador para aprobación |
| F00-03 | P0 | Crear backlog con IDs, dependencias, prioridades y criterios por fase | Roadmap fuente | Cada fase tiene hito y criterio verificable; dependencias F01/F02 explícitas | Hecho |
| F00-04 | P0 | Registrar decisiones y bloqueos externos | F00-01–03 | Desconocidos no se presentan como hechos; no se asume cuenta/proveedor/contratación | Hecho |
| F00-05 | P1 | Crear repositorio privado de GitHub y enlazar al directorio local | F00-01–04 | URL/owner confirmados, remote configurado y archivos del proyecto publicados | Pendiente: el conector no ofrece creación de repositorios y la sesión de navegador disponible no está autenticada |
| F01-01 | P1 | Documentar y completar entrevistas de descubrimiento | F00 aprobado | Evidencia anonimizada, ciudad/sector/tamaño/dolor/herramientas/ejemplos/precio registrados; ninguna respuesta inventada | 2 entrevistas reportadas por el usuario; 1 señal verbal de interés; detalles por documentar y muestra pendiente |
| F01-02 | P1 | Analizar patrones y elegir sector/propuesta económica | F01-01 | Hipótesis priorizadas, cinco candidatos a piloto y disposición a pagar a precio concreto documentada | No iniciada |
| F01-03 | P1 | Recomendar seguir, pivotar o detener | F01-01–02 | Recomendación sustentada en muestra real, limitaciones y economía preliminar | No iniciada |
| F02-01 | P1 | Verificar Embedded Signup/Coexistence y política Meta vigente | F00 aprobado | Requisitos, permisos, elegibilidad, límites y fuentes oficiales fechadas; incertidumbre explícita | Hecho documental; integración pendiente |
| F02-02 | P1 | Comparar Meta directo, Kapso y BSPs posibles | F02-01 | Costos/planes SaaS, país, webhooks, historial, echo, exportación y desconexión respaldados por fuentes/contratos | Hecho con límites; confirmar país, contrato y cobertura |
| F02-03 | P1 | Diseñar contrato de adaptador y pruebas con mocks | F02-01–02 | Contrato cubre connect/status/verify/normalize/disconnect/capabilities; mocks no se describen como validación real | Hecho simulado |
| F02-04 | P1 | Validar límites de mensajes, historial y reconexión | F02-01–03; acceso a activos de test y número elegible para coexistence | Casos A–E documentados; mensajes salientes reflejados y completitud probados o bloqueo claro | Un envío sandbox fue aceptado y un texto entrante se recibió; entrega del envío y Coexistence real pendientes |
| F02-05 | P1 | Probar onboarding Embedded Signup con línea propia de WhatsApp Business App | Configuración Meta con ruta Coexistence, App ID, Config ID, secreto local y origen permitido | El botón abre el flujo, Meta comparte WABA/número y la línea permanece accesible desde Business App; registrar resultado o bloqueo | Harness local implementado; valores y prueba real pendientes |
| META-TEST-01 | P1 | Provisionar número de prueba y probar Cloud API | App Meta Pendiva y acceso al dashboard | Meta muestra número de prueba y se verifica envío/recepción con destinatario autorizado | `hello_world` aceptado y texto entrante recibido el 2026-10-28; entrega del mensaje saliente no confirmada |
| HACK-01 | P1 | Prototipo local del panel para demo de hackathon | Alcance MVP; fixtures sintéticos | Panel y endpoint local muestran señal, evidencia y acción; deduplican evento y no requieren cuenta externa | Hecho; no conectado a Meta ni desplegado |
| HACK-02 | P1 | Recorrido sin datos precargados: webhook WhatsApp + análisis Muse + revisión | Número sandbox, claves, webhook HTTPS y consentimiento | Un mensaje real de prueba aparece una vez y Muse devuelve evidencia validada que una persona revisa | El mensaje fue analizado con Nebius y con Muse por separado; falta mostrar el resultado Muse en el panel y la decisión humana |
| HACK-03 | P1 | Operar y verificar la demo sandbox de un solo negocio | HACK-01–02; configuración local y cloudflared autorizado | Arranque único, receptor separado, callback verificado y análisis sintético real; evidencia de recepción distinta a presencia de credenciales | Recorrido con Nebius y análisis separado del mensaje sandbox con Muse verificados el 2026-10-28; recomendación pendiente de revisión |
| F03-01 | P1 | Diseñar arquitectura modular, flujos de datos y ADRs | F01 y F02 | Decisiones de stack/proveedor con evidencia y límites de confianza documentados | No iniciada |
| F03-02 | P1 | Diseñar aislamiento, consentimiento, retención, borrado y auditoría | F01 y F02 | Requisitos tenant-aware y política de datos propuesta; revisión legal pendiente claramente identificada | No iniciada |
| F04-01 | P1 | Preparar entorno local reproducible | F03 | Compose de desarrollo levanta servicios mínimos; healthchecks, datos sintéticos y pruebas documentados | No iniciada |
| F05-01 | P1 | Implementar multiempresa, identidad y plan comercial inicial | F03–04 | Roles y aislamiento verificados con pruebas de acceso entre empresas | No iniciada |
| F06-01 | P1 | Implementar onboarding con proveedor seleccionado | F02–05; credenciales y autorización según alcance | Estados, errores, desconexión y permisos claros; pruebas automatizadas y mocks separados | No iniciada |
| F07-01 | P1 | Ingestar, normalizar e idempotentizar mensajes/eventos | F06 | Duplicados/fuera de orden tratados; cobertura y última sync expuestas; fixtures sintéticos | No iniciada |
| F08-01 | P1 | Detectar etapas, compromisos y tareas con evidencia | F07 | Salidas con fuente, fecha, confianza; revisión humana y pruebas de escenarios adversos | No iniciada |
| F09-01 | P1 | Construir panel comercial responsive | F05–08 | Búsqueda/filtros y vistas de contacto/oportunidad; cobertura parcial visible | No iniciada |
| F10-01 | P2 | Generar resúmenes y consultas verificables | F07–09 | Totales reproducibles desde datos fuente; no inventa causalidad ni información faltante | No iniciada |
| F11-01 | P1 | Revisar seguridad, confiabilidad y piloto | F04–10 | Controles, restauración, monitoreo, límites, exportación y borrado con evidencias y pruebas | No iniciada |
| F12-01 | P1 | Desplegar staging y preparar Hostinger VPS | F11; compra/acciones externas con autorización | Staging con datos sintéticos, TLS/redes/respaldos/observabilidad comprobados; sin exposición DB/Redis | No iniciada |
| F13-01 | P1 | Ejecutar piloto cerrado de 3–5 empresas | F12; consentimiento y autorizaciones | Uso y señales medidos; incidentes/casos fallidos y costos reales documentados | No iniciada |
| F14-01 | P2 | Preparar comercialización v1 | F13 con señal suficiente | Alta, conexión elegible, valor, pago, cancelación y exportación entendibles | No iniciada |
| F15-01 | P3 | Evaluar módulos posteriores uno a uno | Validación nueva por módulo | Cada adición dispone de hipótesis y decisión basada en evidencia; sin expansión automática de alcance | No iniciada |

## Ruta de dependencias

```text
F00 → (F01 || F02) → F03 → F04 → F05 → F06 → F07 → F08 → F09 → F10 → F11 → F12 → F13 → F14 → F15
```

El roadmap permite F01 y F02 en paralelo. F01 tiene guía de campo, pero no evidencia primaria suficiente. Meta aceptó un envío sandbox y Pendiva recibió un texto desde el teléfono autorizado; faltan confirmación de entrega del envío y Coexistence. La demo no cierra F01–F04. El [plan actualizado](plan-hackathon-muse-whatsapp.md) conserva esas limitaciones.

## Hechos, hipótesis y bloqueos

- Hecho de contexto: no había artefactos en el workspace al comienzo de F00.
- Hecho de contexto comunicado por el usuario: VPS Hostinger KVM 2 activo con Ubuntu 24.04 + EasyPanel. No se verificó por SSH ni se desplegó.
- Hipótesis pendientes: problema y segmento, elegibilidad de números, alcance de historial, costos, proveedor, presupuesto e ingresos.
- Los bloqueos externos completos y sus condiciones están en [bloqueos](validation/bloqueos.md).

## Aprobación

F00 está preparada. F02 tiene su [matriz de proveedores](research/whatsapp-provider-matrix.md), [contrato simulado](validation/coexistence-spike.md), [guía Cloud API de test](validation/meta-cloud-api-test.md), [spike de Embedded Signup](validation/embedded-signup-spike.md) y [script de smoke test](../scripts/whatsapp_test_smoke.py). El sandbox aceptó un envío y recibió un texto mediante HTTPS; la entrega del mensaje saliente sigue sin confirmarse. F01 tiene dos entrevistas reportadas y una señal verbal de interés, además de [guía de descubrimiento](research/customer-discovery-f01.md) y [plantilla anonimizante](validation/interview-template.csv); falta documentar fichas y ampliar la muestra. La [demo sandbox](validation/live-sandbox.md) no completa F01–F04. El repo GitHub permanece pendiente.
