"""Local-first identity, tenant membership and revocable sessions."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import hmac
import secrets
import sqlite3
import time

from src.domain_validation import ROLES, validate_role, validate_tenant_name

SESSION_TTL = 8 * 60 * 60


def hash_password(password: str, salt: bytes | None = None) -> str:
    if not isinstance(password, str) or not 12 <= len(password) <= 256:
        raise ValueError("La contraseña debe tener entre 12 y 256 caracteres")
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return f"pbkdf2_sha256$310000${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, rounds, salt_hex, digest_hex = encoded.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        expected = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(rounds))
        return hmac.compare_digest(expected.hex(), digest_hex)
    except (AttributeError, ValueError):
        return False


class IdentityStore:
    def __init__(self, db):
        self.db = db

    def close(self):
        self.db.close()

    def bootstrap(self, name: str, email: str, password: str, sector: str = "professional_services") -> dict:
        name = validate_tenant_name(name)
        email = email.strip().lower()
        if "@" not in email or len(email) > 254:
            raise ValueError("El correo no es válido")
        with self.db:
            tenant_id = secrets.token_hex(16)
            user_id = secrets.token_hex(16)
            now = datetime.now(timezone.utc).isoformat()
            self.db.execute("INSERT INTO tenants(id,name,sector,created_at) VALUES(?,?,?,?)",
                            (tenant_id, name, sector, now))
            self.db.execute("INSERT INTO users(id,email,password_hash,created_at) VALUES(?,?,?,?)",
                            (user_id, email, hash_password(password), now))
            self.db.execute("INSERT INTO memberships(user_id,tenant_id,role,created_at) VALUES(?,?,?,?)",
                            (user_id, tenant_id, "owner", now))
            self.db.execute("INSERT INTO tenant_connections(tenant_id,phone_number_id,verified,created_at) VALUES(?,?,1,?)",
                            (tenant_id, f"local-{tenant_id}", now))
        return {"tenant_id": tenant_id, "user_id": user_id, "email": email, "role": "owner"}

    def login(self, email: str, password: str) -> dict | None:
        row = self.db.execute("SELECT id,email,password_hash FROM users WHERE email=?",
                              (email.strip().lower(),)).fetchone()
        if not row or not verify_password(password, row["password_hash"]):
            return None
        memberships = self.db.execute(
            "SELECT tenant_id,role FROM memberships WHERE user_id=? ORDER BY created_at", (row["id"],)
        ).fetchall()
        if not memberships:
            return None
        token = secrets.token_urlsafe(32)
        expires = time.time() + SESSION_TTL
        with self.db:
            csrf_token = secrets.token_urlsafe(24)
            self.db.execute("INSERT INTO sessions(token,user_id,tenant_id,expires_at,csrf_token,created_at) VALUES(?,?,?,?,?,?)",
                            (token, row["id"], memberships[0]["tenant_id"], expires, csrf_token,
                             datetime.now(timezone.utc).isoformat()))
            self.db.execute("INSERT INTO audit_events(id,tenant_id,user_id,action,created_at) VALUES(?,?,?,?,?)",
                            (secrets.token_hex(16), memberships[0]["tenant_id"], row["id"], "login",
                             datetime.now(timezone.utc).isoformat()))
        return {"token": token, "csrf_token": csrf_token, "user_id": row["id"],
                "tenant_id": memberships[0]["tenant_id"], "role": memberships[0]["role"], "expires_at": expires}

    def session(self, token: str | None) -> dict | None:
        if not token:
            return None
        row = self.db.execute("""SELECT s.token,s.user_id,s.tenant_id,s.expires_at,s.csrf_token,m.role,u.email
                                FROM sessions s JOIN memberships m ON m.user_id=s.user_id AND m.tenant_id=s.tenant_id
                                JOIN users u ON u.id=s.user_id
                                WHERE s.token=? AND s.expires_at>?""", (token, time.time())).fetchone()
        return dict(row) if row else None

    def revoke(self, token: str) -> bool:
        with self.db:
            return self.db.execute("DELETE FROM sessions WHERE token=?", (token,)).rowcount == 1

    @staticmethod
    def can(role: str, operation: str) -> bool:
        permissions = {
            "owner": {"read", "write", "manage_users", "manage_billing"},
            "manager": {"read", "write", "manage_users"},
            "advisor": {"read", "write"},
            "viewer": {"read"},
        }
        return operation in permissions.get(role, set())
