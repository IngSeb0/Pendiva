# ADR 003 — Prototipo mínimo para demostración de hackathon

- **Estado:** aceptada para prototipo local
- **Fecha:** 2026-10-23
- **Contexto:** el usuario pidió código ejecutable para demostrar el MVP mientras Meta aún no provisiona el número de prueba.

## Decisión

Construir un panel de una sola aplicación con Python estándar, `http.server`, SQLite y HTML/CSS/JavaScript sin build step. Ejecutarlo localmente o empaquetarlo en un contenedor Docker; Compose enlaza el puerto sólo a loopback. El panel muestra fixtures sintéticos y permite enviar texto de ejemplo al clasificador de reglas local.

## Motivos

- El demo puede correr en un portátil sin claves, servicios pagos o configuración de nube.
- Las etiquetas son explicables y cada sugerencia muestra el mensaje que la disparó.
- Mantiene bajo el coste de preparación para una hackathon y permite probar el recorrido del panel con usuarios.
- Los eventos de demostración tienen claves únicas para que reintentar no cree duplicados.

## Límites y consecuencias

- No implementa autenticación, multiempresa, autorización, integración Meta, envío de mensajes ni webhook.
- Las reglas no son IA y no prueban precisión comercial; los nombres y mensajes incluidos son ficticios.
- `http.server` y SQLite son sólo para el demo local. No exponer el contenedor a Internet ni instalarlo en el VPS como servicio público.
- No cierra F01, F02 ni los requisitos de arquitectura F03/F04. La conexión Meta requiere completar su número sandbox y diseñar manejo de credenciales, webhooks y privacidad antes de conectarla.
- Al pasar a una demo compartida, sustituir este servidor por el backend que se decida en la fase de arquitectura, con autenticación y controles de datos.

## Reconsiderar cuando

El objetivo pase de validar el recorrido visual a procesar mensajes de Meta o datos de una empresa; o cuando el prototipo vaya a quedar accesible por Internet.
