class Session:
    def __init__(self):
        self.is_authenticated = False
        self.account_number = None
        self.user_name = None
        self.transfer_receiver = None
        self.transfer_amount = None

    def reset(self):
        self.is_authenticated = False
        self.account_number = None
        self.user_name = None
        self.transfer_receiver = None
        self.transfer_amount = None