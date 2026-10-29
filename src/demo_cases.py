"""Fictional conversations for the local Pendiva demonstration."""

CASES = [
    {
        "id": "demo-case-ana", "name": "Ana Rojas", "service": "Limpieza de sofá", "stage": "Cotización solicitada", "signal": "cotizacion_pendiente", "priority": "Alta",
        "summary": "Ana pidió una cotización para limpiar un sofá de tres puestos y compartió la zona de servicio.",
        "action": "Preparar y enviar la cotización para el sofá.", "evidence_index": 2,
        "messages": [
            {"author": "cliente", "time": "Hoy · 9:12", "text": "Hola, ¿hacen limpieza de sofás a domicilio?"},
            {"author": "asesor", "time": "Hoy · 9:16", "text": "¡Hola! Sí, cuéntame cuántos puestos tiene y en qué zona estás."},
            {"author": "cliente", "time": "Hoy · 9:20", "text": "Es de tres puestos, en Chapinero. ¿Me envías una cotización?"},
        ],
    },
    {
        "id": "demo-case-juan", "name": "Juan Torres", "service": "Limpieza de colchón", "stage": "Conversación sobre precio", "signal": "objecion_precio", "priority": "Alta",
        "summary": "Juan recibió una propuesta y preguntó si existe una alternativa que se ajuste mejor a su presupuesto.",
        "action": "Consultar con Juan qué alcance y presupuesto necesita.", "evidence_index": 2,
        "messages": [
            {"author": "cliente", "time": "Hoy · 8:35", "text": "Quisiera limpiar dos colchones dobles."},
            {"author": "asesor", "time": "Hoy · 8:42", "text": "Para los dos, la propuesta de ejemplo es de $240.000 COP."},
            {"author": "cliente", "time": "Hoy · 8:50", "text": "Me parece caro. ¿Tienen una opción más económica?"},
        ],
    },
    {
        "id": "demo-case-luisa", "name": "Luisa Méndez", "service": "Lavado de alfombra", "stage": "Pago por verificar", "signal": "pago_por_verificar", "priority": "Media",
        "summary": "Luisa afirma haber enviado el anticipo. La confirmación requiere revisión humana.",
        "action": "Revisar el comprobante y confirmar el pago manualmente.", "evidence_index": 2,
        "messages": [
            {"author": "asesor", "time": "Ayer · 16:20", "text": "Para reservar el servicio, compartimos los datos del anticipo."},
            {"author": "cliente", "time": "Hoy · 8:05", "text": "Listo, quiero reservar para el viernes."},
            {"author": "cliente", "time": "Hoy · 8:07", "text": "Ya pagué la reserva. Te envío el comprobante."},
        ],
    },
    {
        "id": "demo-case-carlos", "name": "Carlos Díaz", "service": "Limpieza de sala", "stage": "Seguimiento prometido", "signal": "promesa_de_seguimiento", "priority": "Media",
        "summary": "El asesor ofreció confirmar la disponibilidad. Falta revisar si ya lo hizo por otro medio.",
        "action": "Revisar la agenda y confirmar la disponibilidad con Carlos.", "evidence_index": 1,
        "messages": [
            {"author": "cliente", "time": "Ayer · 15:10", "text": "¿Tienen disponibilidad el sábado por la mañana?"},
            {"author": "asesor", "time": "Ayer · 15:14", "text": "Te confirmo mañana después de revisar la agenda."},
        ],
    },
    {
        "id": "demo-case-mariana", "name": "Mariana Silva", "service": "Consulta general", "stage": "Por revisar", "signal": "sin_clasificar", "priority": "Normal",
        "summary": "Hay una consulta inicial, pero no suficiente información para sugerir una etapa comercial.",
        "action": "Preguntar qué servicio necesita Mariana.", "evidence_index": 0,
        "messages": [{"author": "cliente", "time": "Ayer · 11:05", "text": "Hola, quisiera conocer sus servicios."}],
    },
]
