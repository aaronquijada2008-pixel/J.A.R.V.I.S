#!/usr/bin/env python3
import argparse
import sys

from jarvis.voice import TTS, STT
from jarvis.commands import handle_command


def main():
    parser = argparse.ArgumentParser(description="J.A.R.V.I.S prototipo")
    parser.add_argument("--voice", action="store_true", help="Habilitar TTS")
    parser.add_argument("--listen", action="store_true", help="Usar micrófono para entrada")
    args = parser.parse_args()

    tts = TTS() if args.voice else None
    stt = None
    if args.listen:
        try:
            stt = STT()
        except Exception as e:
            print("No se pudo inicializar reconocimiento de voz:", e)
            stt = None

    print("J.A.R.V.I.S listo. Escribe un comando o usa --listen para hablar. (escribe 'salir' para terminar)")
    try:
        while True:
            if stt:
                text = stt.listen()
                if text is None:
                    continue
                print("Tú:", text)
            else:
                try:
                    text = input("> ").strip()
                except EOFError:
                    break

            if not text:
                continue

            response, should_exit = handle_command(text)
            if response:
                print("JARVIS:", response)
                if tts:
                    tts.speak(response)
            if should_exit:
                break
    except (KeyboardInterrupt, SystemExit):
        print("\nAdiós.")


if __name__ == "__main__":
    main()
