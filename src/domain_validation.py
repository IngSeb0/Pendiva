"""Validation contracts shared by the commercial domain."""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
import re

EVIDENCE_STATES = ("confirmed", "inferred", "pending")
OPPORTUNITY_STAGES = (
    "new_inquiry", "information_pending", "to_quote", "quote_sent",
    "negotiation", "appointment_pending", "appointment_booked",
    "service_completed", "payment_to_verify", "won", "lost_confirmed",
    "unclassified",
)
ROLES = ("owner", "manager", "advisor", "viewer")
MONEY_RE = re.compile(r"^\d{1,12}(?:[.,]\d{1,2})?$")


def validate_evidence_state(value: str) -> str:
    if value not in EVIDENCE_STATES:
        raise ValueError("Estado de evidencia no válido")
    return value


def validate_stage(value: str) -> str:
    if value not in OPPORTUNITY_STAGES:
        raise ValueError("Etapa comercial no válida")
    return value


def validate_role(value: str) -> str:
    if value not in ROLES:
        raise ValueError("Rol no válido")
    return value


def validate_date(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("La fecha debe usar YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValueError("La fecha debe usar YYYY-MM-DD") from None
    return value


def validate_money(value: str | int | float | Decimal) -> str:
    text = str(value).strip().replace(",", ".")
    if not MONEY_RE.fullmatch(text):
        raise ValueError("El precio debe ser un importe positivo válido")
    try:
        amount = Decimal(text)
    except InvalidOperation:
        raise ValueError("El precio no es válido") from None
    if amount < 0:
        raise ValueError("El precio no puede ser negativo")
    return format(amount, "f")


def validate_tenant_name(value: str) -> str:
    value = value.strip() if isinstance(value, str) else ""
    if not value or len(value) > 160:
        raise ValueError("El nombre de la empresa debe tener entre 1 y 160 caracteres")
    return value
