import json
import os
import datetime
from typing import Dict, List, Any


DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "jarvis_data.json"))


def _load() -> Dict[str, Any]:
    if not os.path.exists(DATA_PATH):
        return {"notes": [], "tasks": []}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"notes": [], "tasks": []}


def _save(data: Dict[str, Any]):
    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def add_note(text: str) -> Dict[str, Any]:
    data = _load()
    nid = (data.get("notes") and max((n.get("id", 0) for n in data["notes"]), default=0) + 1) or 1
    note = {"id": nid, "text": text, "created": datetime.datetime.now().isoformat()}
    data.setdefault("notes", []).append(note)
    _save(data)
    return note


def get_notes() -> List[Dict[str, Any]]:
    data = _load()
    return data.get("notes", [])


def add_task(title: str) -> Dict[str, Any]:
    data = _load()
    tid = (data.get("tasks") and max((t.get("id", 0) for t in data["tasks"]), default=0) + 1) or 1
    task = {"id": tid, "title": title, "created": datetime.datetime.now().isoformat(), "done": False}
    data.setdefault("tasks", []).append(task)
    _save(data)
    return task


def list_tasks() -> List[Dict[str, Any]]:
    data = _load()
    return data.get("tasks", [])


def complete_task(task_id: int) -> bool:
    data = _load()
    for t in data.get("tasks", []):
        if t.get("id") == task_id:
            t["done"] = True
            _save(data)
            return True
    return False
