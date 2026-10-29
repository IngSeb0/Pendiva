# Prueba local de Nemotron en NVIDIA

**Estado:** integración preparada con pruebas simuladas; aún falta ejecutar una llamada real con una clave del usuario. Esta guía usa específicamente una clave de **NVIDIA API Catalog**; otras plataformas que ofrezcan Nemotron pueden usar endpoints y claves diferentes.

## Primera prueba de la clave

1. Obtén una clave en el [catálogo oficial de NVIDIA](https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b?nim=hosted&section=deploy) o usa una que ya controles. Revisa las condiciones y créditos de tu cuenta.
2. Abre PowerShell en la raíz del proyecto y ejecuta:

   ```powershell
   python -m scripts.iniciar_nemotron_privado
   ```

3. Pega la clave cuando el programa la solicite y pulsa Enter. El prompt oculta lo que escribes; no pegues la clave en el chat. El programa realiza **una llamada real breve a NVIDIA** con el texto `Responde: listo.` y puede consumir créditos.
4. Si recibe una respuesta de chat válida, informa de la aceptación y abre el servidor local en `http://127.0.0.1:8768/`. Mantén la terminal abierta. Si devuelve error, informa únicamente el código o mensaje sanitizado, nunca la clave.

El panel muestra el proveedor NVIDIA. La clave vive en el proceso y se pierde al cerrarlo. Una clave correcta para NVIDIA no habilita por sí sola el webhook de WhatsApp; hay que configurarlo y verificarlo por separado conforme a [live-sandbox](live-sandbox.md).

## Privacidad y límites

El botón de análisis requiere confirmar que se pueden enviar los mensajes a **NVIDIA**, que es distinto de Meta. La llamada sólo ocurre al pulsar el botón con el consentimiento correspondiente. Consultar las condiciones de NVIDIA, la disponibilidad del modelo y costos de la cuenta antes de usar datos reales de clientes. La llamada de prueba de conectividad no envía conversaciones. No hay cambio automático a otro proveedor si falla el elegido.

La preparación con Nemotron sirve para probar el flujo, pero no demuestra uso de Muse ni acredita por sí misma el cumplimiento de la hackathon de Meta. La integración con Muse sigue disponible como ruta separada. Ver [ADR 005](../decisions/005-proveedor-nemotron.md).
