from jarvis.commands import IntentClassifier, _time, _say


def test_intent_and_handlers():
    assert IntentClassifier.classify("¿Qué hora es?") == "time"
    out, _ = _time()
    assert "Son las" in out

    out2, _ = _say("decir hola mundo")
    assert out2 == "hola mundo"
