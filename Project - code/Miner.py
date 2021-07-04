import hashlib
import math
from random import random

from MerkleLeaf import MerkleLeaf
from RegUser import RegUser
from BlockChain import BlockChain
from Cryptodome.Signature.pkcs1_15 import PKCS115_SigScheme
from Cryptodome.Hash import SHA256

class Miner(RegUser):

    def __init__(self, private_key,public_key, amount, id):
       super().__init__(private_key,public_key, amount, id)


    def validate_transactions(self, pool_of_transactions,reg_users):
        approved_transactions = []
        total_fees = 0
        transaction_volume = 0
        #sorting the transactions by fees. if the fee is higher, the transcation will be added quicker to the block
        pool_of_transactions.sort(key=lambda transaction: transaction.get_fees(),reverse = True)
        for trans in pool_of_transactions:
            last_used_block_index = trans.get_sender_address().get_element_from_path(0)
            transaction_index = trans.get_sender_address().get_element_from_path(1)
            transaction_neighbour_index = trans.get_sender_address().get_element_from_path(2)
            rc = self.proof_of_membership(trans,reg_users,last_used_block_index, transaction_index, transaction_neighbour_index)

            if rc:
                total_fees += trans.get_fees()
                transaction_volume += trans.get_value()
                print("Transaction from User ", trans.get_sender_address().get_id(),end=" ")
                print("To User ",trans.get_recipient_address().get_id()," with ",trans.get_value()," HERL - Approved!")
                approved_transactions.append(trans)
            else:
                print("Transaction from User ", trans.get_sender_address().get_id(), end=" ")
                print("To User ", trans.get_recipient_address().get_id(), " with ", trans.get_value(),
                      " HERL - Declined!")
                print("Reason : User Have " , trans.get_sender_address(). get_wallet_amount() , " HERL Left!\n")

        return (approved_transactions,total_fees,transaction_volume)


    def proof_of_membership(self,trans,reg_users, block_index, transaction_index, neighbour_index):
        block = BlockChain.get_block(block_index)
        prev_transaction = block.get_transaction_list()[transaction_index]

        sender = trans.get_sender_address()
        #check if the user with the signature on the transaction is really him with verification
        if self.hash_pointers_check(block_index) is False : return False
        if self.sig_verification(sender,trans) is False : return False
        if self.amount_verification(reg_users,sender, trans) is False : return False


        transaction_neighbour = block.get_transaction_list()[neighbour_index]
        trans_hash = self.hash(MerkleLeaf(prev_transaction).__str__().encode('utf-8'))
        neighbour_hash = self.hash(MerkleLeaf(transaction_neighbour).__str__().encode('utf-8'))
        if (lambda varX: varX % 2 == 1)(transaction_index):
            addition_hash = self.hash_on_two_args(str(neighbour_hash),str(trans_hash))
        else:
            addition_hash = self.hash_on_two_args(str(trans_hash),str(neighbour_hash))

        merkle_nodes = block.get_nodes()
        node_hash_index = int(((len(merkle_nodes) + transaction_index) / 2))
        node_hash_index_new = [node_hash_index, node_hash_index - 1][(lambda varX: varX % 2 == 1)(transaction_index)]

        left_hash = merkle_nodes[node_hash_index_new].get_left()
        right_hash = merkle_nodes[node_hash_index_new].get_right()

        node_hash = self.hash_on_two_args(str(left_hash), str(right_hash))

        if node_hash != addition_hash : return False


        for i in range(int(math.log(len(merkle_nodes),2))):
            if (lambda varX: varX % 2 == 0)(node_hash_index_new):
                second_hash = node_hash_index_new - 1
                next_index = int(second_hash / 2)
                l = self.hash(str(merkle_nodes[second_hash]).encode('utf-8'))
                r = self.hash(str(merkle_nodes[node_hash_index_new]).encode('utf-8'))
            else:
                second_hash = node_hash_index_new + 1
                next_index = int(second_hash / 2) - 1
                l = self.hash(str(merkle_nodes[node_hash_index_new]).encode('utf-8'))
                r = self.hash(str(merkle_nodes[second_hash]).encode('utf-8'))

            addition_hash = self.hash_on_two_args(str(l),str(r))
            node_hash_index_new = next_index

            left_hash = merkle_nodes[next_index].get_left()
            right_hash = merkle_nodes[next_index].get_right()
            tempHash = self.hash_on_two_args(str(left_hash), str(right_hash))
            if tempHash != addition_hash : return False

        return True


    def hash_on_two_args(self,arg1,arg2):
        hash_function = getattr(hashlib, 'sha256')
        arg3 = arg1 + arg2
        arg3 = arg3.encode('utf-8')
        return hash_function(arg3).hexdigest()


    def hash(self, arg):
        hash_function = getattr(hashlib, 'sha256')
        return hash_function(arg).hexdigest()


    def sig_verification(self, sender, transaction):
        hash = SHA256.new(str(transaction.to_dict()).encode('utf-8'))
        verifier = PKCS115_SigScheme(sender.get_public_key())
        try:
            verifier.verify(hash, transaction.get_signature())
            print("Signature is valid.")
            return True
        except:
            print("Signature is invalid.")
            return False


    def amount_verification(self,reg_users, sender, transaction):
        if sender.get_wallet_amount() < transaction.get_value() :  return False

        reg_users[transaction.get_recipient_address().get_id()].set_amount(transaction.get_value() + transaction.get_recipient_address().get_wallet_amount())
        reg_users[sender.get_id()].set_amount(sender.get_wallet_amount() - transaction.get_value())
        return True

    def hash_pointers_check(self,block_index):

        # if this is the first block, he is point to the genesis block
        if(block_index == 0) : return True
        blocks_to_scan = random.randrange(block_index)
        while(blocks_to_scan > 0):
            if(BlockChain.get_block(block_index).get_prev_block_hash()
                    != BlockChain.get_block(block_index-1).get_hash()):
                return False
            blocks_to_scan-=1
            block_index-=1
        return True