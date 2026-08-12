try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    import speech_recognition as sr
except Exception:
    sr = None


class TTS:
    def __init__(self):
        if pyttsx3 is None:
            raise RuntimeError("pyttsx3 no está instalado")
        self.engine = pyttsx3.init()

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()


class STT:
    def __init__(self):
        if sr is None:
            raise RuntimeError("speech_recognition no está instalado")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self, timeout: int = 5):
        with self.microphone as source:
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=timeout)
        try:
            text = self.recognizer.recognize_google(audio, language="es-ES")
            return text
        except Exception as e:
            print("No se entendió:", e)
            return None
