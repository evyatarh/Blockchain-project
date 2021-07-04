
class MerkleLeaf:

    def __init__(self,transaction):
        self.transaction = transaction


    def __str__(self):
        return str(self.transaction)


    def get_transaction(self):
        return self.transaction
