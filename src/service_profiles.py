"""Editable sector profiles used to configure service businesses."""
from __future__ import annotations

from copy import deepcopy

SERVICE_PROFILES = {
    "home_services": {
        "name": "Servicios para el hogar",
        "currency": "COP",
        "timezone": "America/Bogota",
        "stages": ["new_inquiry", "information_pending", "to_quote", "quote_sent",
                   "appointment_pending", "appointment_booked", "service_completed",
                   "payment_to_verify", "won", "lost_confirmed"],
        "services": [
            {"key": "installation", "name": "Instalación", "required_fields": ["location", "preferred_date"]},
            {"key": "maintenance", "name": "Mantenimiento", "required_fields": ["location", "preferred_date"]},
        ],
        "follow_up_days": 2,
    },
    "professional_services": {
        "name": "Servicios profesionales",
        "currency": "COP",
        "timezone": "America/Bogota",
        "stages": ["new_inquiry", "information_pending", "to_quote", "quote_sent",
                   "negotiation", "won", "lost_confirmed"],
        "services": [
            {"key": "consulting", "name": "Consultoría", "required_fields": ["scope", "preferred_date"]},
            {"key": "training", "name": "Capacitación", "required_fields": ["attendees", "preferred_date"]},
        ],
        "follow_up_days": 3,
    },
}


def get_profile(key: str) -> dict:
    try:
        return deepcopy(SERVICE_PROFILES[key])
    except KeyError:
        raise ValueError("Perfil sectorial no válido") from None


def validate_profile(profile: dict) -> dict:
    if not isinstance(profile, dict) or not isinstance(profile.get("stages"), list):
        raise ValueError("La configuración sectorial no es válida")
    if not profile["stages"] or not all(isinstance(item, str) for item in profile["stages"]):
        raise ValueError("Debe existir al menos una etapa válida")
    if not isinstance(profile.get("services"), list):
        raise ValueError("La configuración debe incluir servicios")
    return deepcopy(profile)
