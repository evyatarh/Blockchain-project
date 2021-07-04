
class Wallet:

    def __init__(self, private_key,public_key, amount):
        self.private_key = private_key
        self.amount = amount
        self.public_key = public_key


    def get_amount(self):
        return self.amount


    def get_public_key(self):
        return self.public_key


    def get_private_key(self):
        return self.private_key


    def set_amount(self,val):
        self.amount = val


