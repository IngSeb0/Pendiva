"""Reproducible, fictional data for the local demo."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from contextlib import closing
import base64
import json
from pathlib import Path
import secrets

from src.live_pipeline import LiveStore

DEMO_EMAIL = "demo@pendiva.local"
DEMO_PASSWORD = "demo-password-local-2026"
DEMO_TENANT = "demo-tenant-pendiva"
DEMO_PHONE = "573000000000"

CASES = (
    ("demo-ana", "Ana Rojas", "573000000101", "Limpieza profunda de sofá",
     ["Hola, necesito limpiar un sofá de tres puestos.", "Es en Chapinero y lo necesito esta semana.", "¿Me envías la cotización, por favor?"],
     "information_pending", "alta", "Ana espera una cotización; confirma la dirección y la fecha para prepararla."),
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
    ("demo-andres", "Andrés Vega", "573000000106", "Limpieza de oficina",
     ["Necesito limpiar una oficina de 80 metros cuadrados.", "Estamos en Usaquén y buscamos servicio semanal."],
     "information_pending", "alta", "Andrés necesita una propuesta recurrente; confirma el alcance y el horario."),
    ("demo-valentina", "Valentina Ruiz", "573000000107", "Lavado de muebles",
     ["Tengo dos sillas y un sofá para lavar.", "¿Podrían venir el próximo martes?"],
     "appointment_pending", "media", "Valentina consulta disponibilidad para varios muebles; confirma la agenda."),
    ("demo-felipe", "Felipe Castro", "573000000108", "Limpieza posobra",
     ["Terminamos una remodelación y queremos limpieza posobra.", "El apartamento tiene 65 metros cuadrados."],
     "information_pending", "media", "Felipe compartió el tamaño; falta confirmar ubicación y fecha para cotizar."),
    ("demo-sofia", "Sofía Morales", "573000000109", "Limpieza de colchón",
     ["Quiero limpiar un colchón doble.", "¿Tienen un horario después de las cinco de la tarde?"],
     "appointment_pending", "baja", "Sofía solicita una visita al final de la tarde; revisa disponibilidad."),
)

CASES_EN = (
    ("demo-ana", "Ana Rojas", "573000000101", "Deep sofa cleaning",
     ["Hi, I need a three-seat sofa cleaned.", "It is in Chapinero and I need it this week.", "Could you send me a quote?"],
     "information_pending", "alta", "Ana is waiting for a quote; confirm the service address and preferred date first."),
    ("demo-juan", "Juan Torres", "573000000102", "Two mattress cleaning",
     ["I would like two double mattresses cleaned.", "The quote for both would be 240,000 COP.", "That is a bit expensive. Do you have a lower-cost option?"],
     "negotiation", "alta", "Juan raised a price objection after receiving the quote; review scope or offer a suitable alternative."),
    ("demo-luisa", "Luisa Méndez", "573000000103", "Rug cleaning",
     ["I would like to book the service for Friday.", "I paid the deposit and will send the receipt."],
     "payment_to_verify", "media", "Luisa says she paid a deposit, but the payment still needs verification."),
    ("demo-carlos", "Carlos Díaz", "573000000104", "Living room cleaning",
     ["Do you have availability on Saturday morning?", "I will check the schedule and confirm tomorrow."],
     "appointment_pending", "media", "The advisor promised to check availability; follow up with a confirmed time."),
    ("demo-mariana", "Mariana Silva", "573000000105", "Home cleaning",
     ["Hi, I would like to learn about your services."],
     "information_pending", "baja", "Ask which service, location, and date she has in mind before preparing a quote."),
    ("demo-andres", "Andrés Vega", "573000000106", "Weekly office cleaning",
     ["I need an 80-square-meter office cleaned.", "We are in Usaquén and need service every week."],
     "information_pending", "alta", "Confirm the cleaning scope and preferred schedule before quoting recurring service."),
    ("demo-valentina", "Valentina Ruiz", "573000000107", "Upholstery cleaning",
     ["I have two chairs and a sofa to clean.", "Could you come next Tuesday?"],
     "appointment_pending", "media", "Check the schedule and confirm availability for all three items."),
    ("demo-felipe", "Felipe Castro", "573000000108", "Post-renovation cleaning",
     ["We finished a renovation and need a post-construction clean.", "The apartment is 65 square meters."],
     "information_pending", "media", "Felipe shared the property size; confirm location and preferred date before quoting."),
    ("demo-sofia", "Sofía Morales", "573000000109", "Mattress cleaning",
     ["I need a double mattress cleaned.", "Do you have an appointment after 5 p.m.?"],
     "appointment_pending", "baja", "Check evening availability and confirm the date with Sofía."),
)


def seed_demo(store: LiveStore, phone_number_id: str = "", language: str = "es", include_finance: bool = True) -> dict:
    """Insert synthetic data without replacing real messages or financial records."""
    if language not in ("es", "en"):
        raise ValueError("Demo language must be 'es' or 'en'.")
    cases = CASES_EN if language == "en" else CASES
    store.initialize()
    identity = store.identity()
    row = identity.db.execute("SELECT id FROM tenants WHERE id=?", (DEMO_TENANT,)).fetchone()
    if not row:
        now = datetime.now(timezone.utc).isoformat()
        with identity.db:
            identity.db.execute("INSERT INTO tenants(id,name,sector,settings,created_at) VALUES(?,?,?,?,?)",
                                (DEMO_TENANT, "Home Services Demo" if language == "en" else "Servicios Hogar Demo", "home_services", "{}", now))
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
    profile = ({
        "nombre": "Home Services Demo", "sector": "Residential cleaning and home services",
        "servicios": "Sofas, mattresses, rugs, and living rooms", "horario": "Monday to Saturday, 8:00 a.m.–6:00 p.m.",
        "objetivos": "Reply faster, follow up on quotes, and keep the schedule full",
    } if language == "en" else {
        "nombre": "Servicios Hogar Demo", "sector": "Limpieza y mantenimiento a domicilio",
        "servicios": "Sofás, colchones, alfombras y salas", "horario": "Lunes a sábado, 8:00 a 18:00",
        "objetivos": "Responder rápido, dar seguimiento a cotizaciones y llenar la agenda",
    })
    existing_profile = store.business_profile(DEMO_TENANT)
    profile = existing_profile if any(existing_profile.values()) else store.save_business_profile(profile, DEMO_TENANT)
    now = datetime.now(timezone.utc)
    seeded = 0
    with closing(store.connect()) as db, db:
        for case_index, (case_id, name, phone, service, texts, stage, priority, reason) in enumerate(cases):
            contact_id = f"{case_id}-contact"
            db.execute("INSERT OR IGNORE INTO contacts(id,tenant_id,phone,name,created_at) VALUES(?,?,?,?,?)",
                       (contact_id, DEMO_TENANT, phone, name, now.isoformat()))
            demo_workflows = {
                "demo-ana": {"stage": "missing", "service": service, "location": "Chapinero", "date": "This week" if language == "en" else "Esta semana", "scope": "Three-seat sofa" if language == "en" else "Sofá de tres puestos"},
                "demo-juan": {"stage": "quoted", "service": service},
                "demo-carlos": {"stage": "scheduled", "service": service},
            }
            workflow = demo_workflows.get(case_id, {"stage": "new", "service": service})
            db.execute("INSERT OR IGNORE INTO conversation_workflows(scope,sender,data) VALUES(?,?,?)",
                       (DEMO_TENANT, phone, json.dumps(workflow, ensure_ascii=False)))
            message_ids = []
            for index, text in enumerate(texts):
                message_id = f"{case_id}-message-{index + 1}"
                message_ids.append(message_id)
                timestamp = int((now - timedelta(hours=case_index * 5 + len(texts) - index)).timestamp())
                advisor_messages = {"demo-juan": {1}, "demo-carlos": {1}}
                author = "asesor" if index in advisor_messages.get(case_id, set()) else "cliente"
                db.execute("INSERT OR IGNORE INTO live_messages(id,sender,name,timestamp,text,kind,raw,tenant_id) "
                           "VALUES(?,?,?,?,?,?,?,?)",
                           (message_id, phone, name, timestamp, text, "text",
                            json.dumps({"demo": True, "author": author}, ensure_ascii=False), DEMO_TENANT))
            result = {
                "model": "pendiva-demo-rules-1", "resumen": f"{name} asked about {service}." if language == "en" else f"{name} consulta por {service}.",
                "incertidumbre": "Fictional demo data; verify before taking action." if language == "en" else "Datos sintéticos para demostración; validar antes de actuar.",
                "recomendaciones": [{
                    "tipo": stage, "accion": reason, "motivo": reason, "prioridad": priority,
                    "commitment": ({
                        "description": "Check the schedule and confirm Saturday morning availability" if language == "en" else "Revisar la agenda y confirmar disponibilidad el sábado por la mañana",
                        "responsible_party": "business_representative",
                        "timing_text": "Tomorrow" if language == "en" else "Mañana",
                        "due_date": None,
                        "evidence_ids": [message_ids[-1]],
                        "suggested_next_action": "Check whether availability was confirmed and follow up with Carlos if needed." if language == "en" else "Verificar si se confirmó la disponibilidad y responderle a Carlos si hace falta.",
                    } if case_id == "demo-carlos" else None),
                    "missing_information": ([
                        "The exact service address is not in the available messages.",
                        "The customer said 'this week'; no exact appointment date is recorded.",
                    ] if case_id == "demo-ana" and language == "en" else
                    ["No aparece la dirección exacta del servicio en los mensajes disponibles.",
                     "La clienta dijo 'esta semana'; no hay una fecha exacta de cita registrada."]
                     if case_id == "demo-ana" else []),
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
            (("2026-09-05", "sale", 1800, "Home cleaning"),
             ("2026-09-10", "expense", 420, "Marketing"),
             ("2026-09-18", "expense", 280, "Travel"),
             ("2026-10-04", "sale", 1450, "Home cleaning"),
             ("2026-10-09", "expense", 620, "Marketing"),
             ("2026-10-16", "expense", 410, "Supplies")) if language == "en" else (
            ("2026-09-05", "venta", 1800000, "Servicios a domicilio"),
            ("2026-09-10", "gasto", 420000, "Publicidad"),
            ("2026-09-18", "gasto", 280000, "Transporte"),
            ("2026-10-04", "venta", 1450000, "Servicios a domicilio"),
            ("2026-10-09", "gasto", 620000, "Publicidad"),
            ("2026-10-16", "gasto", 410000, "Insumos")))
        existing_finance = db.execute("SELECT COUNT(*) FROM financial_records WHERE tenant_id=?", (DEMO_TENANT,)).fetchone()[0]
        if include_finance and not existing_finance:
            for date, kind, amount, category in finance:
                stored_kind = {"sale": "venta", "expense": "gasto"}.get(kind, kind)
                db.execute("INSERT INTO financial_records(date,kind,amount,category,imported_at,tenant_id) "
                           "VALUES(?,?,?,?,?,?)", (date, stored_kind, amount, category, now.isoformat(), DEMO_TENANT))
    identity.close()
    # A ready-to-run example is seeded once; deactivating it stays respected on restart.
    from src.custom_tools import init_tools
    init_tools(store)
    example_view = {"name": "Missing details · demo" if language == "en" else "Datos por completar · ejemplo", "template": "missing_info", "days": 1}
    with closing(store.connect()) as db, db:
        db.execute("INSERT OR IGNORE INTO custom_views(id,scope,config,active,created_at) VALUES(?,?,?,?,?)",
                   ("d" * 32, DEMO_TENANT, json.dumps(example_view, ensure_ascii=False), 1, now.isoformat()))
    # Optional synthetic files are deterministic and never analyzed automatically.
    from src.multimodal import add_media, init_media
    init_media(store)
    fixtures = Path(__file__).resolve().parents[1] / "fixtures" / "demo"
    for fixture_name, display_name, mime in (("sofa-ficticio.png", "sofa-reference.png", "image/png"),
                                              ("solicitud-ficticia.wav", "voice-request.wav", "audio/wav"),
                                              ("video-ficticio.mp4", "video-walkthrough.mp4", "video/mp4")):
        filename = fixture_name if language == "es" else display_name
        path = fixtures / fixture_name
        if path.is_file():
            add_media(store, DEMO_TENANT, "573000000101", filename, mime,
                      base64.b64encode(path.read_bytes()).decode(), "fixture:" + fixture_name)
    return {"tenant_id": DEMO_TENANT, "email": DEMO_EMAIL, "password": DEMO_PASSWORD,
            "conversations": seeded, "synthetic": True}
