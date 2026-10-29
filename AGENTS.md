# Guía para agentes

Este archivo da contexto compartido, no reemplaza la petición actual del usuario ni impone un flujo rígido. Usa criterio para completar el trabajo solicitado, resolver decisiones reversibles y mantener el avance visible.

## Antes de cambios importantes

- Revisa `README.md`, `docs/roadmap.md`, las decisiones relevantes y `git status`; identifica instrucciones locales adicionales.
- Inspecciona el código y conserva el trabajo existente. Haz cambios pequeños y coherentes con la tarea.
- Usa el roadmap como contexto de dependencias. El usuario puede autorizar varias fases o una excepción de alcance; sigue esa autorización y señala dependencias que sigan sin evidencia.

## Calidad y seguridad

- Para servicios externos, verifica la documentación oficial vigente y anota enlaces, límites y supuestos relevantes.
- No guardes secretos, tokens, claves privadas ni datos personales/de clientes en Git. Prefiere fixtures sintéticos o anonimizados.
- No realices compras, envíes comunicaciones a terceros, conectes cuentas reales, cambies infraestructura productiva ni ejecutes operaciones destructivas sin autorización explícita para esa acción.
- Acompaña código nuevo con pruebas automatizadas adecuadas y documentación. Distingue siempre entre pruebas simuladas y validaciones contra el servicio real.
- No conviertas hipótesis, señales verbales o muestras pequeñas en hechos concluyentes; registra fuente y nivel de evidencia.

## Entrega

Resume archivos y decisiones importantes, verificaciones realizadas, límites/riesgos y el siguiente paso útil. Pide aclaración sólo si la información faltante cambia materialmente el resultado o requiere una acción externa no autorizada.
