"""Reproducible, fictional data for the local demo."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from contextlib import closing
import json
import secrets

from src.live_pipeline import LiveStore

DEMO_EMAIL = "demo@pendiva.local"
DEMO_PASSWORD = "demo-password-local-2026"
DEMO_TENANT = "demo-tenant-pendiva"
DEMO_PHONE = "573000000000"

CASES = (
    ("demo-ana", "Ana Rojas", "573000000101", "Limpieza profunda de sofá",
     ["Hola, necesito limpiar un sofá de tres puestos.", "Es en Chapinero y lo necesito esta semana.", "¿Me envías la cotización, por favor?"],
     "quote_sent", "alta", "Ana espera una cotización y no hay seguimiento posterior."),
    ("demo-juan", "Juan Torres", "573000000102", "Limpieza de dos colchones",
     ["Quisiera limpiar dos colchones dobles.", "La propuesta para los dos sería de $240.000 COP.", "Me parece caro. ¿Tienen una opción más económica?"],
     "negotiation", "alta", "Juan planteó una objeción de precio después de recibir la propuesta."),
    ("demo-luisa", "Luisa Méndez", "573000000103", "Lavado de alfombra",
     ["Quiero reservar el servicio para el viernes.", "Ya pagué la reserva y te envío el comprobante."],
     "payment_to_verify", "media", "Luisa declara un pago, pero la confirmación sigue pendiente."),
    ("demo-carlos", "Carlos Díaz", "573000000104", "Limpieza de sala",
     ["¿Tienen disponibilidad el sábado por la mañana?", "Te confirmo mañana después de revisar la agenda."],
     "appointment_pending", "media", "El asesor prometió revisar disponibilidad y falta confirmar."),
    ("demo-mariana", "Mariana Silva", "573000000105", "Servicio de limpieza",
     ["Hola, quisiera conocer sus servicios."],
     "information_pending", "baja", "Faltan servicio, ubicación y fecha para poder cotizar."),
)


def seed_demo(store: LiveStore, phone_number_id: str = "") -> dict:
    """Insert synthetic data without replacing real messages or financial records."""
    store.initialize()
    identity = store.identity()
    row = identity.db.execute("SELECT id FROM tenants WHERE id=?", (DEMO_TENANT,)).fetchone()
    if not row:
        now = datetime.now(timezone.utc).isoformat()
        with identity.db:
            identity.db.execute("INSERT INTO tenants(id,name,sector,settings,created_at) VALUES(?,?,?,?,?)",
                                (DEMO_TENANT, "Servicios Hogar Demo", "home_services", "{}", now))
            user_id = secrets.token_hex(16)
            from src.auth import hash_password
            identity.db.execute("INSERT INTO users(id,email,password_hash,created_at) VALUES(?,?,?,?)",
                                (user_id, DEMO_EMAIL, hash_password(DEMO_PASSWORD), now))
            identity.db.execute("INSERT INTO memberships(user_id,tenant_id,role,created_at) VALUES(?,?,?,?)",
                                (user_id, DEMO_TENANT, "owner", now))
    if phone_number_id:
        with identity.db:
            identity.db.execute("INSERT OR REPLACE INTO tenant_connections(tenant_id,phone_number_id,verified,created_at) "
                                "VALUES(?,?,1,datetime('now'))", (DEMO_TENANT, phone_number_id))
    profile = {
        "nombre": "Servicios Hogar Demo", "sector": "Limpieza y mantenimiento a domicilio",
        "servicios": "Sofás, colchones, alfombras y salas", "horario": "Lunes a sábado, 8:00 a 18:00",
        "objetivos": "Responder rápido, dar seguimiento a cotizaciones y llenar la agenda",
    }
    store.save_business_profile(profile)
    now = datetime.now(timezone.utc)
    seeded = 0
    with closing(store.connect()) as db, db:
        for case_index, (case_id, name, phone, service, texts, stage, priority, reason) in enumerate(CASES):
            contact_id = f"{case_id}-contact"
            db.execute("INSERT OR IGNORE INTO contacts(id,tenant_id,phone,name,created_at) VALUES(?,?,?,?,?)",
                       (contact_id, DEMO_TENANT, phone, name, now.isoformat()))
            message_ids = []
            for index, text in enumerate(texts):
                message_id = f"{case_id}-message-{index + 1}"
                message_ids.append(message_id)
                timestamp = int((now - timedelta(hours=case_index * 5 + len(texts) - index)).timestamp())
                author = "cliente" if index % 2 == 0 else "asesor"
                db.execute("INSERT OR IGNORE INTO live_messages(id,sender,name,timestamp,text,kind,raw,tenant_id) "
                           "VALUES(?,?,?,?,?,?,?,?)",
                           (message_id, phone, name, timestamp, text, "text",
                            json.dumps({"demo": True, "author": author}, ensure_ascii=False), DEMO_TENANT))
            result = {
                "model": "pendiva-demo-rules-1", "resumen": f"{name} consulta por {service}.",
                "incertidumbre": "Datos sintéticos para demostración; validar antes de actuar.",
                "recomendaciones": [{
                    "tipo": stage, "accion": reason, "motivo": reason, "prioridad": priority,
                    "evidencia_ids": message_ids[-1:],
                }],
                "profile_hash": store._profile_hash(profile),
            }
            db.execute("INSERT OR IGNORE INTO live_analyses(sender,result,message_ids,created_at,reviewed,tenant_id) "
                       "VALUES(?,?,?,?,0,?)",
                       (phone, json.dumps(result, ensure_ascii=False), json.dumps(message_ids),
                        now.isoformat(), DEMO_TENANT))
            seeded += 1
        finance = (
            ("2026-09-05", "venta", 1800000, "Servicios a domicilio"),
            ("2026-09-10", "gasto", 420000, "Publicidad"),
            ("2026-09-18", "gasto", 280000, "Transporte"),
            ("2026-10-04", "venta", 1450000, "Servicios a domicilio"),
            ("2026-10-09", "gasto", 620000, "Publicidad"),
            ("2026-10-16", "gasto", 410000, "Insumos"),
        )
        existing_finance = db.execute("SELECT COUNT(*) FROM financial_records WHERE tenant_id=?", (DEMO_TENANT,)).fetchone()[0]
        if not existing_finance:
            for date, kind, amount, category in finance:
                db.execute("INSERT INTO financial_records(date,kind,amount,category,imported_at,tenant_id) "
                           "VALUES(?,?,?,?,?,?)", (date, kind, amount, category, now.isoformat(), DEMO_TENANT))
    identity.close()
    return {"tenant_id": DEMO_TENANT, "email": DEMO_EMAIL, "password": DEMO_PASSWORD,
            "conversations": seeded, "synthetic": True}
