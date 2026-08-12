from jarvis import knowledge


def test_kb_reload_and_search():
    n = knowledge.reload_index()
    assert n >= 0
    res = knowledge.search("Bienvenido")
    assert isinstance(res, str)
