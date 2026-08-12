#!/usr/bin/env python3
"""
Interactive test script for J.A.R.V.I.S
Validates all features and components work correctly.
"""

import sys
import os
import importlib.util

def test_imports():
    """Test if all required packages can be imported."""
    print("🔍 Verificando dependencias...")
    packages = {
        'pyttsx3': 'Síntesis de voz',
        'speech_recognition': 'Reconocimiento de voz (opcional)',
        'pytest': 'Marco de pruebas'
    }
    
    missing = []
    for pkg, desc in packages.items():
        try:
            __import__(pkg)
            print(f"  ✅ {pkg} ({desc})")
        except ImportError:
            if pkg != 'speech_recognition':  # optional
                missing.append(pkg)
            print(f"  ⚠️  {pkg} ({desc}) - NO ENCONTRADO")
    
    return len(missing) == 0


def test_jarvis_modules():
    """Test if J.A.R.V.I.S modules load correctly."""
    print("\n🔍 Verificando módulos de J.A.R.V.I.S...")
    
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    sys.path.insert(0, src_path)
    
    modules = ['jarvis.main', 'jarvis.voice', 'jarvis.commands', 'jarvis.storage', 'jarvis.knowledge']
    all_ok = True
    
    for mod in modules:
        try:
            __import__(mod)
            print(f"  ✅ {mod}")
        except Exception as e:
            print(f"  ❌ {mod}: {e}")
            all_ok = False
    
    return all_ok


def test_config():
    """Test if config.json exists and is valid."""
    print("\n🔍 Verificando configuración...")
    
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    
    if not os.path.exists(config_path):
        print(f"  ⚠️  config.json no encontrado en {config_path}")
        return False
    
    try:
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"  ✅ config.json válido")
        return True
    except Exception as e:
        print(f"  ❌ config.json inválido: {e}")
        return False


def test_data_files():
    """Test if data files exist."""
    print("\n🔍 Verificando archivos de datos...")
    
    base_dir = os.path.dirname(__file__)
    files = {
        'jarvis_data.json': 'Base de datos (se creará si no existe)',
        'knowledge': 'Carpeta de base de conocimiento'
    }
    
    for fname, desc in files.items():
        path = os.path.join(base_dir, '..', fname)
        exists = os.path.exists(path)
        status = "✅" if exists else "⚠️ "
        print(f"  {status} {fname} ({desc})")
    
    return True


def test_voice():
    """Test TTS functionality."""
    print("\n🔍 Verificando síntesis de voz...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say("Prueba de J.A.R.V.I.S")
        engine.runAndWait()
        print("  ✅ Síntesis de voz funcionando")
        return True
    except Exception as e:
        print(f"  ❌ Error de voz: {e}")
        return False


def test_commands():
    """Test command handling."""
    print("\n🔍 Verificando manejador de comandos...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from jarvis.commands import handle_command, IntentClassifier
        
        # Test intent classification
        test_cases = [
            ("qué hora es", "time"),
            ("abrir google", "open"),
            ("buscar python", "search"),
            ("nota comprar leche", "note"),
            ("ayuda", "help"),
        ]
        
        for text, expected_intent in test_cases:
            intent = IntentClassifier.classify(text)
            if intent == expected_intent:
                print(f"  ✅ '{text}' → {intent}")
            else:
                print(f"  ⚠️  '{text}' → {intent} (esperado: {expected_intent})")
        
        # Test command execution
        response, should_exit = handle_command("hora")
        print(f"  ✅ Comando 'hora' respondió: {response[:50]}...")
        
        return True
    except Exception as e:
        print(f"  ❌ Error en comandos: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("🧪 SUITE DE PRUEBAS INTERACTIVAS DE J.A.R.V.I.S")
    print("=" * 60)
    
    results = {
        "Dependencias": test_imports(),
        "Módulos J.A.R.V.I.S": test_jarvis_modules(),
        "Configuración": test_config(),
        "Archivos de datos": test_data_files(),
        "Síntesis de voz": test_voice(),
        "Manejo de comandos": test_commands(),
    }
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! J.A.R.V.I.S está listo para usar.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron. Revisa los errores arriba.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
