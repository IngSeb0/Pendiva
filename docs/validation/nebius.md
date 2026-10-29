# Nemotron de NVIDIA mediante Nebius Token Factory

**Estado al 2026-10-28:** Nebius analizó una cotización ficticia recibida realmente desde WhatsApp y devolvió una recomendación con evidencia válida, que quedó pendiente de revisión. La prueba sintética aislada más reciente también pasó. Esto no verifica calidad general. El modelo es de NVIDIA y el servicio que recibe y procesa los datos es Nebius. No confundir la clave de Nebius con la de NVIDIA API Catalog.

Desde PowerShell en la carpeta del proyecto:

```powershell
python -m scripts.iniciar_nebius_privado
```

Pega la clave de Nebius en el prompt oculto, nunca en el chat. Se hace una solicitud neutral real, que puede consumir créditos; sólo si responde correctamente se abre el panel en http://127.0.0.1:8769/. El webhook de WhatsApp requiere configuración adicional. No se envían conversaciones en la solicitud de prueba.

El proveedor `nebius` requiere `NEBIUS_API_KEY` y se conecta a `https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions` usando `nvidia/nemotron-3-super-120b-a12b`. Es el endpoint y modelo del [ejemplo oficial de Nebius](https://github.com/nebius/token-factory-cookbook/blob/main/models/nemotron/nemotron3-super-120B.md); la disponibilidad y región deben verificarse en la cuenta. Las recomendaciones se validan en servidor y el operador autoriza expresamente el envío a Nebius; no hay cambio automático de proveedor. La clave se conserva sólo en el proceso. Consulta las [condiciones de procesamiento](https://docs.tokenfactory.nebius.com/legal/subprocessors) y precios antes de analizar conversaciones reales.

Para usar la clave ya configurada en `.env`, ejecuta `python -m scripts.iniciar_demo --check-model --provider nebius`. Hace una llamada real con texto ficticio y registra sólo metadatos en `data/model-check-nebius.json`, excluido de Git. No carga ejemplos en el panel. El arranque completo es `python -m scripts.iniciar_demo --tunnel`; consulta la [guía del sandbox](live-sandbox.md).

El recorrido con el teléfono autorizado, el callback público y Nebius se comprobó el 2026-10-28. Por separado, [Muse analizó el mensaje sandbox autorizado](muse.md) sin cambiar ni sobrescribir el panel Nebius.
