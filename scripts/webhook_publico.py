"""Local listener exposing only the signed Meta webhook, for a temporary tunnel."""
from pathlib import Path
from src.live_app import create_server
from src.local_config import load_local_config


def main():
    root = Path(__file__).resolve().parents[1]
    config = load_local_config(root / ".env")
    port = int(config.get("PENDIVA_WEBHOOK_PORT", "8772"))
    server = create_server(host="127.0.0.1", port=port, db_path=config.get("PENDIVA_LIVE_DB") or None,
                           environ=config, webhook_only=True)
    print(f"Receptor de webhook limitado a http://127.0.0.1:{port}/webhooks/meta", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
