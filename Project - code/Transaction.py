from collections import OrderedDict



class Transaction:
    def __init__(self, sender_address,recipient_address, value,fees):
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.value = value
        self.signature = None
        self.fees = fees


    # Use orderedDict method to encode it at the same order all the time
    def to_dict(self):
        return OrderedDict({'sender_address': self.sender_address,
                            'recipient_address': self.recipient_address,
                            'value': self.value,
                            'fees': self.fees
                            })


    def get_sender_address(self):
        return self.sender_address


    def get_fees(self):
        return self.fees

    def set_signature(self,sig):
        self.signature = sig


    def get_signature(self):
        return self.signature


    def get_recipient_address(self):
        return self.recipient_address


    def get_value(self):
        return self.value