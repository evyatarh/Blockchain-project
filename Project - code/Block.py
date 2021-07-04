import hashlib
from MerkleTree import MerkleTree

class Block:

    def __init__(self, transactions_list,timestamp,index,total_fees,transaction_volume):
        self.index = index
        self.transactions_list = transactions_list
        self.prev_block_hash = None
        self.timestamp = timestamp
        self.hash = self.generate_hash()
        self.root = None
        self.nodes = None
        self.total_fees = total_fees
        self.transaction_volume = transaction_volume


    def create_merkle_tree(self,block_index):
        merkle_tree = MerkleTree(self.transactions_list)
        self.nodes = merkle_tree.create_merkle_tree(block_index)
        self.transactions_list = merkle_tree.get_transaction_list()


    def get_total_fees(self):
        return self.total_fees


    def get_transaction_volume(self):
        return self.transaction_volume


    def get_nodes(self):
        return self.nodes


    def get_transaction_list(self):
        return self.transactions_list


    def set_transaction_list(self,li):
        self.transactions_list = li


    def get_prev_block_hash(self):
        return self.prev_block_hash


    def set_prev_block_hash(self,prev_hash):
        self.prev_block_hash = prev_hash


    def get_timestamp(self):
        return self.timestamp


    def get_hash(self):
        return self.hash


    def get_index(self):
        return self.index


    def set_root(self,root):
        self.root = root


    def generate_hash(self):
        hash_function = getattr(hashlib, 'sha256')
        return hash_function(str(self).encode('utf-8')).hexdigest()
