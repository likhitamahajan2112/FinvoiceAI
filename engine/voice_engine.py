import speech_recognition as sr
import pyttsx3
import threading

recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.pause_threshold = 0.8

def create_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    return engine

tts_lock = threading.Lock()

def speak(message):
    print("System:", message)

    def run_tts(msg):
        with tts_lock:
            engine = create_engine()
            engine.say(msg)
            engine.runAndWait()
            engine.stop()

    threading.Thread(target=run_tts, args=(message,), daemon=True).start()


def listen():
    try:
        with microphone as source:
            recognizer.energy_threshold = 250
            recognizer.adjust_for_ambient_noise(source, duration=0.25)

            if not hasattr(listen, "is_listening"):
                print("Listening...")
                listen.is_listening = True

            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

        transcript = recognizer.recognize_google(audio)
        print("You:", transcript)

        listen.is_listening = False

        return transcript.lower()

    except sr.WaitTimeoutError:
        return None

    except sr.UnknownValueError:
        return None

    except sr.RequestError:
        speak("Speech recognition service error.")
        return None

    except OSError:
        speak("Microphone not detected.")
        return None