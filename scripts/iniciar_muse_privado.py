"""Start the local dashboard after the user enters their own API key."""
import getpass
import os
import runpy


def main() -> None:
    key = getpass.getpass("Pega tu clave de Meta Model API y pulsa Enter (no se mostrará): ")
    if not key.strip():
        print("No se ingresó una clave. Vuelve a ejecutar el comando.")
        return
    os.environ["MODEL_API_KEY"] = key
    os.environ["PENDIVA_AI_PROVIDER"] = "meta"
    os.environ["PENDIVA_PORT"] = "8767"
    print("Clave cargada en esta sesión. Abre http://127.0.0.1:8767/.")
    print("Muse no se llamará automáticamente. Pulsa Ctrl+C para cerrar el servidor.")
    runpy.run_module("src.live_app", run_name="__main__")


if __name__ == "__main__":
    main()
