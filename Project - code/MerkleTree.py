from Node import Node
from MerkleLeaf import MerkleLeaf
import math
import hashlib

class MerkleTree:

    def __init__(self, transactions_list):
        self.transactions_list = transactions_list


    def is_power_of_two(self, num):
        ans = bin(num & num-1)
        if not num : num+=1
        power = int(math.log(num,2)) #the closest power
        if not ans : return (True, None)
        return (False, math.pow(2,power+1)-num)


    def set_path_for_user(self,transaction,neighbour, block_index):
        temp = []
        temp.append(block_index);temp.append(transaction);temp.append(neighbour)
        return temp


    def create_leafs(self,block_index):
        leafs = []
        for transaction in range((len(self.transactions_list)-1),-1,-1) :
            neighbour = [transaction -1, transaction + 1][(lambda varX: varX % 2 == 0)(transaction)]
            self.transactions_list[transaction].get_recipient_address().append_to_path_of_proof(
                self.set_path_for_user(transaction, neighbour, block_index))
            self.transactions_list[transaction].get_sender_address().append_to_path_of_proof(
                self.set_path_for_user(transaction, neighbour, block_index))
            leafs.append(MerkleLeaf(self.transactions_list[transaction]))
        leafs.reverse()
        (power, diff) = self.is_power_of_two(len(leafs))
        if not power:
            for _ in range(int(diff)):
                leafs.append(leafs[-1])
                self.transactions_list.append(leafs[-1].get_transaction())
        return leafs


    def build_list(self,list,hash_function):
        levelI = []
        for i in range(1,len(list),2):
            hash_node_left = hash_function(str(list[i-1]).encode('utf-8')).hexdigest()
            hash_node_right = hash_function(str(list[i]).encode('utf-8')).hexdigest()
            levelI.append(Node(hash_node_left,hash_node_right))
        return levelI


    def create_nodes(self, leafs):
        nodes = []
        hash_function = getattr(hashlib, 'sha256')
        firstLevel = []

        for i in range (1,len(leafs),2): # initialize the first level
            left_data = leafs[i-1].__str__().encode('utf-8')
            left_hash = hash_function(left_data).hexdigest()
            right_data = leafs[i].__str__().encode('utf-8')
            right_hash= hash_function(right_data).hexdigest()
            firstLevel.append(Node(left_hash, right_hash))
        cur_node_len = len(firstLevel)
        retList = firstLevel
        tempNodes = []
        tempNodes.append(firstLevel)

        while int(cur_node_len) > 1:# initialize the second level
            retList = self.build_list(retList,hash_function)
            tempNodes.append(retList)
            cur_node_len /=2

        tempNodes.reverse()
        for n in tempNodes : nodes += n

        return nodes


    def create_merkle_tree(self,block_index):
        leafs = self.create_leafs(block_index)
        return self.create_nodes(leafs)


    def get_transaction_list(self):
        return self.transactions_list
