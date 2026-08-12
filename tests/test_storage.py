import os
from jarvis import storage


def test_notes_tasks_lifecycle():
    # limpiar estado anterior
    try:
        if os.path.exists(storage.DATA_PATH):
            os.remove(storage.DATA_PATH)
    except Exception:
        pass

    note = storage.add_note("nota de prueba")
    assert note["id"] == 1
    notes = storage.get_notes()
    assert any(n["text"] == "nota de prueba" for n in notes)

    task = storage.add_task("tarea de prueba")
    assert task["id"] == 1
    tasks = storage.list_tasks()
    assert any(t["title"] == "tarea de prueba" for t in tasks)

    ok = storage.complete_task(task["id"])
    assert ok

    # cleanup
    try:
        if os.path.exists(storage.DATA_PATH):
            os.remove(storage.DATA_PATH)
    except Exception:
        pass
