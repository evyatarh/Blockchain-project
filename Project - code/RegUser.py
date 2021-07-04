from Cryptodome.Signature.pkcs1_15 import PKCS115_SigScheme
from Cryptodome.Hash import SHA256
from Wallet import Wallet
from Transaction import Transaction



class RegUser:

    def __init__(self, private_key,public_key, amount,id):
        self.my_wallet = Wallet(private_key,public_key, amount)
        self.id = id
        self.path_of_proof = []


    def create_transaction(self,value,recipient_address,fees):
        print("User ",self.id, " Made a transaction with User ",recipient_address.get_id()," on a ",value, " HERL")
        print("Waiting for approval from a Miner...")
        trans = Transaction(self, recipient_address, value,fees)
        trans.set_signature(self.sign_transaction(trans))
        return trans


    def set_index_of_the_transaction(self, index):
        self.index_of_the_transaction = index


    def get_id(self):
        return self.id


    def get_element_from_path(self,index):
        return self.path_of_proof[index]


    def get_index_of_the_transaction(self):
        return self.index_of_the_transaction


    def set_num_of_last_block(self, num_of_block):
        self.num_of_the_last_used_block = num_of_block


    def get_num_of_last_block(self):
        return self.num_of_the_last_used_block


    def append_to_path_of_proof(self,li):
        self.path_of_proof = li


    def get_path_of_proof(self):
        return self.path_of_proof


    def get_wallet_amount(self):
        return self.my_wallet.get_amount()


    def set_amount(self,val):
        self.my_wallet.set_amount(val)


    def get_public_key(self):
        return self.my_wallet.get_public_key()


    def get_index_and_last_use_block(self):
        return self.index_of_the_transaction, self.num_of_the_last_used_block


    # Sign transaction with private key
    def sign_transaction(self, trans):
        h = SHA256.new(str(trans.to_dict()).encode('utf8'))
        signer = PKCS115_SigScheme(self.my_wallet.get_private_key())  # RSA digital signature protocol called RSASSA-PKCS1-v1_5.
        return signer.sign(h)
