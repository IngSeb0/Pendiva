"""Inspect or subscribe Pendiva's existing test account to its own app.

The default is read-only. --subscribe adds only the Pendiva app to its
Meta-provisioned sandbox account after verifying the account's test sender.
Secrets stay in memory and no messages are sent.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.local_config import load_local_config

ROOT = Path(__file__).resolve().parents[1]
PENDIVA_APP_ID = "889989257436890"
PENDIVA_TEST_ACCOUNT_ID = "1656900775878774"


class SandboxError(ValueError):
    pass


def request_json(url, token, opener, *, data=None):
    request = Request(url, data=data, headers={"Authorization": f"Bearer {token}"})
    with opener(request, timeout=20) as response:
        return json.load(response)


def inspect_sandbox(config, *, subscribe=False, opener=urlopen):
    if config.get("WHATSAPP_APP_ID", PENDIVA_APP_ID) != PENDIVA_APP_ID:
        raise SandboxError("La herramienta sólo admite la app Pendiva.")
    version = config.get("WHATSAPP_TEST_GRAPH_VERSION", "")
    secret = config.get("WHATSAPP_APP_SECRET", "")
    token = config.get("WHATSAPP_TEST_ACCESS_TOKEN", "")
    phone_id = config.get("WHATSAPP_TEST_PHONE_NUMBER_ID", "")
    if not secret or not token or not re.fullmatch(r"v[0-9]+\.[0-9]+", version) or not phone_id.isascii() or not phone_id.isdigit():
        raise SandboxError("Faltan las variables de la app y del sandbox de prueba.")
    if config.get("WHATSAPP_PHONE_NUMBER_ID") != phone_id:
        raise SandboxError("El número del sandbox y el filtro del webhook no coinciden.")
    base = f"https://graph.facebook.com/{version}"
    query = urlencode({"input_token": token})
    details = request_json(f"{base}/debug_token?{query}", f"{PENDIVA_APP_ID}|{secret}", opener).get("data", {})
    if details.get("app_id") != PENDIVA_APP_ID or details.get("is_valid") is not True:
        raise SandboxError("El token no es válido para la app Pendiva.")
    if "whatsapp_business_management" not in details.get("scopes", []):
        raise SandboxError("El token no tiene permiso de gestión de WhatsApp.")
    expires = details.get("expires_at")
    if not isinstance(expires, int):
        raise SandboxError("Meta no devolvió la caducidad del token.")
    account_url = f"{base}/{PENDIVA_TEST_ACCOUNT_ID}"
    phones = request_json(account_url + "/phone_numbers?fields=id", token, opener)
    if phones.get("paging", {}).get("next"):
        raise SandboxError("La lista de números es incompleta; no se puede verificar el sandbox.")
    if phone_id not in {str(item.get("id", "")) for item in phones.get("data", [])}:
        raise SandboxError("El número configurado no pertenece a la cuenta sandbox esperada.")

    def read_subscription():
        result = request_json(account_url + "/subscribed_apps", token, opener)
        if result.get("paging", {}).get("next"):
            raise SandboxError("La lista de suscripciones es incompleta.")
        apps = [item.get("whatsapp_business_api_data", {}).get("id") for item in result.get("data", [])]
        return PENDIVA_APP_ID in apps

    active = read_subscription()
    created = False
    if subscribe and not active:
        result = request_json(account_url + "/subscribed_apps", token, opener, data=b"")
        if result.get("success") is not True:
            raise SandboxError("Meta no confirmó la suscripción.")
        active = read_subscription()
        if not active:
            raise SandboxError("Meta no confirmó la suscripción en la lectura posterior.")
        created = True
    return {"app": "Pendiva", "scope": "sandbox", "token_valid": True,
            "expires_at_utc": datetime.fromtimestamp(expires, timezone.utc).isoformat() if expires else None,
            "test_sender_matches": True, "app_subscribed": active, "subscription_added": created}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subscribe", action="store_true", help="subscribe Pendiva if it is not already subscribed")
    args = parser.parse_args(argv)
    try:
        report = inspect_sandbox(load_local_config(ROOT / ".env"), subscribe=args.subscribe)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["app_subscribed"] else 2
    except HTTPError as error:
        if error.code == 401:
            print("Meta rechazó el token de prueba. Renueva WHATSAPP_TEST_ACCESS_TOKEN localmente.", file=sys.stderr)
        else:
            print(f"Meta devolvió HTTP {error.code}; revisa permisos y configuración.", file=sys.stderr)
    except (OSError, URLError):
        print("No fue posible conectar con Meta.", file=sys.stderr)
    except SandboxError as error:
        print(str(error), file=sys.stderr)
    except (ValueError, TypeError, KeyError, AttributeError):
        print("No se pudo validar el token, la cuenta o el número sandbox de Pendiva.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
