import datetime
import webbrowser
import urllib.parse
import re
from typing import Tuple

from jarvis import storage
from jarvis import knowledge
from jarvis import auth


class IntentClassifier:
    @staticmethod
    def classify(text: str) -> str:
        t = (text or "").lower()
        if re.search(r"\bhora\b|\btime\b", t):
            return "time"
        if re.search(r"\babrir\b", t):
            return "open"
        if re.search(r"\bbuscar\b", t):
            return "search"
        if re.match(r"^(decir|di)\b", t):
            return "say"
        if re.search(r"\bsalir\b|\badiós\b|\badios\b", t):
            return "exit"
        if re.search(r"\bnota\b|\bguardar nota\b|\bguardar\b", t):
            return "note"
        if re.search(r"\brecordar\b|\blistar notas\b|\bnotas\b", t):
            return "list_notes"
        if re.search(r"\btarea\b|\bcrear tarea\b|\bagregar tarea\b", t):
            return "add_task"
        if re.search(r"\blistar tareas\b|\btareas\b", t):
            return "list_tasks"
        if re.search(r"\bcompletar tarea\b|\bmarcar tarea\b|\bterminar tarea\b", t):
            return "complete_task"
        if re.search(r"\bayuda\b|\bhelp\b", t):
            return "help"
            if re.search(r"\bexplicar\b|\bqué es\b|\bque es\b|\binfo\b|\bbuscar en base\b|\bdocumentaci[oó]n\b|\bdefinir\b", t):
                return "kb_search"
            if re.search(r"\brecargar\b|\breload\b|\brecargar kb\b|\brecargar base\b|\brecargar conocimiento\b", t):
                return "reload_kb"
        return "fallback"


def _open_target(text: str) -> Tuple[str, bool]:
    parts = text.split(maxsplit=1)
    if len(parts) <= 1:
        return "¿Qué quieres que abra? Ej: 'abrir ejemplo.com'", False
    target = parts[1].strip()
    if not re.match(r"^https?://", target):
        target = "https://" + target
    webbrowser.open(target)
    return f"Abriendo {target}", False


def _search_web(text: str) -> Tuple[str, bool]:
    parts = text.split(maxsplit=1)
    if len(parts) <= 1:
        return "¿Qué quieres buscar? Ej: 'buscar recetas de paella'", False
    q = urllib.parse.quote(parts[1])
    url = f"https://www.google.com/search?q={q}"
    webbrowser.open(url)
    return f"Buscando {parts[1]}", False


def _say(text: str) -> Tuple[str, bool]:
    parts = text.split(maxsplit=1)
    phrase = parts[1] if len(parts) > 1 else ""
    return phrase, False


def _time() -> Tuple[str, bool]:
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return f"Son las {now}", False


def _add_note(text: str) -> Tuple[str, bool]:
    ok, cleaned, reason = auth.authorize(text)
    if not ok:
        return f"Acceso denegado: {reason}", False

    parts = re.split(r"nota\b|guardar nota\b|guardar\b", cleaned, flags=re.IGNORECASE)
    body = parts[-1].strip() if len(parts) > 1 else ""
    if not body:
        return "Dime la nota tras 'nota' o 'guardar nota'. Ej: 'nota comprar leche'", False
    note = storage.add_note(body)
    return f"Nota guardada (id={note['id']}).", False


def _list_notes() -> Tuple[str, bool]:
    notes = storage.get_notes()
    if not notes:
        return "No hay notas guardadas.", False
    lines = [f"{n['id']}: {n['text']} ({n['created']})" for n in notes]
    return "\n".join(lines), False


def _add_task(text: str) -> Tuple[str, bool]:
    ok, cleaned, reason = auth.authorize(text)
    if not ok:
        return f"Acceso denegado: {reason}", False

    parts = re.split(r"tarea\b|crear tarea\b|agregar tarea\b", cleaned, flags=re.IGNORECASE)
    body = parts[-1].strip() if len(parts) > 1 else ""
    if not body:
        return "Dime la tarea tras 'tarea'. Ej: 'tarea comprar pan'", False
    task = storage.add_task(body)
    return f"Tarea creada (id={task['id']}).", False


def _list_tasks() -> Tuple[str, bool]:
    tasks = storage.list_tasks()
    if not tasks:
        return "No hay tareas.", False
    lines = [f"{t['id']}: {t['title']} - {'hecha' if t.get('done') else 'pendiente'}" for t in tasks]
    return "\n".join(lines), False


def _complete_task(text: str) -> Tuple[str, bool]:
    ok, cleaned, reason = auth.authorize(text)
    if not ok:
        return f"Acceso denegado: {reason}", False

    m = re.search(r"(\d+)", cleaned)
    if not m:
        return "Indica el id de la tarea a completar. Ej: 'completar tarea 2'", False
    tid = int(m.group(1))
    ok = storage.complete_task(tid)
    if ok:
        return f"Tarea {tid} marcada como hecha.", False
    return f"No encontré la tarea {tid}.", False


def _help() -> Tuple[str, bool]:
    txt = (
        "Comandos disponibles:\n"
        "- hora: Muestra la hora\n"
        "- abrir <url>: Abre una URL\n"
        "- buscar <texto>: Busca en la web\n"
        "- decir <texto>: Repite el texto\n"
        "- nota <texto>: Guarda una nota\n"
        "- recordar / notas: Lista notas\n"
        "- tarea <texto>: Crea una tarea\n"
        "- listar tareas: Lista tareas\n"
        "- completar tarea <id>: Marca tarea como hecha\n"
        "- salir: Cierra J.A.R.V.I.S\n"
    )
    return txt, False


def _kb_search(text: str) -> Tuple[str, bool]:
    # extraer consulta después de palabras clave
    q = re.sub(r"(?i)explicar|que es|qué es|info sobre|buscar en base|documentaci[oó]n|definir", "", text).strip()
    if not q:
        return "Dime qué quieres buscar en la base de conocimiento. Ej: 'explicar VLAN'", False
    # primero intento un resumen extractivo
    summary = knowledge.summarize(q, max_sentences=3)
    # además aporto referencias si el resumen es muy corto
    if len(summary) < 40:
        refs = knowledge.search(q, top=2)
        return (summary + "\n\n" + refs).strip(), False
    return summary, False


def _reload_kb() -> Tuple[str, bool]:
    ok, cleaned, reason = auth.authorize("recargar" )
    # allow reload if env token present or require_token is false; authorize will check config
    if not ok:
        return f"Acceso denegado: {reason}", False
    n = knowledge.reload_index()
    return f"Índice recargado: {n} documentos indexados.", False


def handle_command(text: str) -> Tuple[str, bool]:
    intent = IntentClassifier.classify(text)
    if intent == "time":
        return _time()
    if intent == "open":
        return _open_target(text)
    if intent == "search":
        return _search_web(text)
    if intent == "say":
        return _say(text)
    if intent == "note":
        return _add_note(text)
    if intent == "list_notes":
        return _list_notes()
    if intent == "add_task":
        return _add_task(text)
    if intent == "list_tasks":
        return _list_tasks()
    if intent == "complete_task":
        return _complete_task(text)
    if intent == "help":
        return _help()
    if intent == "kb_search":
        return _kb_search(text)
    if intent == "exit":
        return "Adiós.", True

    return (
        "No entiendo ese comando. Escribe 'ayuda' para ver comandos disponibles.",
        False,
    )
