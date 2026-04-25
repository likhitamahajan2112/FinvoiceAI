from core.constants import States
from services.intent_service import classify_intent
from services.auth_service import authenticate
from services.banking_service import get_balance, get_transactions, transfer_money

class StateManager:
    def __init__(self, session, speak):
        self.session = session
        self.current_state = States.IDLE
        self.speak = speak

    def reset(self):
        self.session.reset()
        self.current_state = States.IDLE

    def handle_command(self, transcript):
        if transcript.strip() == "":
            return None

        intent = classify_intent(transcript)

        if intent == "exit":
            self.speak("Thank you for using FinVoice AI. Goodbye.")
            return "EXIT"

        if self.current_state == States.IDLE:
            if intent == "login":
                self.current_state = States.LOGIN_ACCOUNT
                self.speak("Please say your account number")
            elif intent in ["balance", "transactions", "transfer"]:
                self.speak("Please login first.")
            else:
                self.speak("Command not recognized.")

        elif self.current_state == States.LOGIN_ACCOUNT:
            self.session.account_number = transcript.strip()
            self.current_state = States.LOGIN_PIN
            self.speak("Please say your PIN")

        elif self.current_state == States.LOGIN_PIN:
            pin = transcript.strip()
            result = authenticate(self.session.account_number, pin)

            if result["success"]:
                self.session.is_authenticated = True
                self.session.user_name = result["name"]
                self.current_state = States.AUTHENTICATED
                self.speak(f"Welcome {self.session.user_name}")
            else:
                self.reset()
                self.speak("Login failed. Please say login again.")

        elif self.current_state == States.AUTHENTICATED:
            if intent == "logout":
                self.reset()
                self.speak("You have been logged out.")

            elif intent == "balance":
                balance = get_balance(self.session.account_number)
                self.speak(f"Your balance is {balance}")

            elif intent == "transactions":
                txs = get_transactions(self.session.account_number)
                msg = "Recent transactions: " + ", ".join(
                    [f"{t['type']} ₹{t['amount']} - {t['description']}" for t in txs]
                )
                self.speak(msg)

            elif intent == "transfer":
                self.current_state = States.TRANSFER_ACCOUNT
                self.speak("Please say receiver account number")

            else:
                self.speak("Command not recognized.")

        elif self.current_state == States.TRANSFER_ACCOUNT:
            self.session.transfer_receiver = transcript.strip()
            self.current_state = States.TRANSFER_AMOUNT
            self.speak("Please say amount")

        elif self.current_state == States.TRANSFER_AMOUNT:
            self.session.transfer_amount = transcript.strip()
            self.current_state = States.TRANSFER_CONFIRM
            self.speak("Do you confirm?")

        elif self.current_state == States.TRANSFER_CONFIRM:
            if intent == "confirm" or "yes" in transcript:
                msg = transfer_money(
                    self.session.account_number,
                    self.session.transfer_receiver,
                    self.session.transfer_amount
                )
                self.speak(msg)
                self.current_state = States.AUTHENTICATED

            elif intent == "cancel" or "no" in transcript:
                self.speak("Transfer cancelled.")
                self.current_state = States.AUTHENTICATED

            else:
                self.speak("Please say yes or no.")

        return None