import os
import json
from typing import Tuple

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config.json"))


def _load_config() -> dict:
    default = {"require_token": False, "token": "changeme"}
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            default.update(cfg)
    except Exception:
        pass
    return default


_CFG = _load_config()


def authorize(raw_text: str) -> Tuple[bool, str, str]:
    """Verifica si la acción está autorizada.

    Devuelve (allowed, cleaned_text, reason).
    - Si `require_token` es False, devuelve True.
    - Si la variable de entorno JARVIS_TOKEN coincide con el token del config, True.
    - Si el comando empieza con 'token <token>' o 'clave <token>', compara y elimina ese prefijo.
    """
    if not _CFG.get("require_token", False):
        return True, raw_text, ""

    env_token = os.environ.get("JARVIS_TOKEN")
    cfg_token = str(_CFG.get("token", ""))
    if env_token and env_token == cfg_token:
        return True, raw_text, "autorizado por variable de entorno"

    t = (raw_text or "").strip()
    for prefix in ("token ", "clave "):
        if t.lower().startswith(prefix):
            parts = t.split(maxsplit=2)
            if len(parts) >= 2:
                supplied = parts[1]
                remainder = parts[2] if len(parts) > 2 else ""
                if supplied == cfg_token:
                    return True, remainder, "autorizado por prefijo"
                return False, raw_text, "token incorrecto"

    return False, raw_text, "se requiere token"
