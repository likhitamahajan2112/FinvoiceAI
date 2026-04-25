from core.session import Session
from core.state_manager import StateManager
from engine.voice_engine import listen, speak
import time

if __name__ == "__main__":
    session = Session()
    state_manager = StateManager(session, speak)

    silent_count = 0

    while True:
        transcript = listen()

        if transcript is None or transcript.strip() == "":
            silent_count += 1

            if silent_count >= 3:
                speak("Please say something or say exit to quit.")
                silent_count = 0

            continue

        silent_count = 0

        result = state_manager.handle_command(transcript)

        time.sleep(1)

        if result == "EXIT":
            break