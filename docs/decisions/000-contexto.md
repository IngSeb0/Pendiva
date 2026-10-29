# ADR 000 — Contexto inicial del proyecto

- **Estado:** propuesta contextual; no autoriza implementación de las fases posteriores.
- **Fecha:** 2026-10-15.
- **Fase:** F00.
- **Fuente principal:** `C:/Users/Acer/Downloads/ROADMAP_AGENTE_SAAS_WHATSAPP_HOSTINGER.md`, roadmap v1.0 con fecha de referencia 2026-10-13.

## Contexto inspeccionado

La carpeta de trabajo estaba vacía al iniciar. `git rev-parse`, `git status` y `git remote -v` confirmaron que no era un repositorio Git; no había README, AGENTS, código, pruebas, configuración, ramas, remotos ni nombres de variables de entorno para inventariar. Para preparar el trabajo F00 se inicializó Git con rama `main`. No se pudo crear el commit: falta identidad de autor y el sandbox deniega actualizar `.git/index`. La conexión a GitHub tampoco se completó. Al inicio no se habían proporcionado entrevistas, credenciales, estado de cuentas, proveedor, VPS, dominio ni evidencias de pilotos. Posteriormente, el usuario informó que ya realizó dos entrevistas y que una persona expresó interés general en la idea; aún no se recibieron notas que permitan analizar la muestra. La existencia o estado de otros recursos externos queda **desconocido**, no se interpreta como inexistencia.

El documento de referencia declara como hipótesis Hostinger VPS + Docker Compose para Colombia y propone Next.js, FastAPI, PostgreSQL, Redis/worker y proxy TLS. También establece límites de producto, restricciones sobre datos e integraciones y una secuencia F00–F15.

## Decisiones para F00

1. **Adoptar el roadmap recibido como línea base documental.** Motivo: instrucción del usuario y ausencia de artefactos previos en la carpeta. Su alcance comercial/técnico sigue siendo propuesta hasta su validación.
2. **Preparar únicamente documentación de planificación.** Motivo: autorización exclusiva para F00 y DoD de esa fase; no se crea aplicación, esquema, infraestructura ni integración.
3. **Preparar un repositorio privado `IngSeb0/pendiva` en GitHub.** Motivo: el usuario lo pidió explícitamente y el nombre coincide con la carpeta de trabajo. Sigue pendiente porque el conector de GitHub no expone creación de repositorios y el navegador integrado de esta sesión solicita iniciar sesión. Se conserva visibilidad privada como intención del ADR; no se comparte código en público por defecto.
4. **No fijar decisiones de proveedor, identidad, cola o proxy.** El propio roadmap las deja para investigación/mini-spikes posteriores; quedan abiertas.
5. **Dejar creación/enlace de GitHub pendiente de completar con sesión autenticada.** La autorización del usuario ya está dada; el bloqueo es la capacidad disponible, no una aprobación pendiente.
6. **Preparar el acceso SSH a Hostinger sin conectarse todavía.** La llave pública local `~/.ssh/hostinger_nueva.pub` y su pareja privada existen; el usuario afirma que la pública está instalada en Hostinger. Aún no se ha verificado el VPS, host key ni usuario SSH.

## Opciones técnicas propuestas, pendientes de aprobación

- VPS KVM 2 como hipótesis inicial, no capacidad validada ni servicio comprado.
- Monolito modular y contenedores propuestos en el roadmap, sin implementación en F00.
- Elegibilidad y capacidades de WhatsApp Coexistence dependen de Meta, número y proveedor; pendientes de verificar en F02 con documentación actual.
- No seleccionar Kapso/BSP, Auth.js/proveedor de identidad, RQ/Dramatiq, Caddy/Traefik ni proveedor de IA en esta fase.

## Consecuencias

Se crean documentos funcionales, roadmap/backlog, decisión contextual y registro de bloqueos, además de instrucciones mínimas para preservar el alcance en futuras fases. No hay pruebas de producto que ejecutar porque no hay código ni suite. La aceptación de F00 y la creación/remoto de GitHub deben reportarse por separado.
