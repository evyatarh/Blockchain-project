
import secrets
import math
import time

from random import random
from random import uniform
from Cryptodome.PublicKey import RSA
from datetime import datetime
from RegUser import RegUser
from Miner import Miner
from BlockChain import BlockChain
from Block import Block

"""
This is a Simulator on - How does Bloackchain and Transactions work
Created By Evyatar Hai & Lior Reinitz
 """

class TimeOutException(Exception):
    pass


class Simulator:

    def alarm_handler(signum):
        print("finish to create transactions")
        raise TimeOutException()

    def run_simulator(self):

        print("Today 1 HERL currency is : ",
              (int(datetime.now().strftime("%Y")) + uniform(0, math.pow(2,10))),"$ - Please Wait.." )

        reg_users = []
        miners = []

        #each user starting with amount of 10 HERL
        amount = 10
        num_of_participates = 5#secrets.randbelow(int(math.pow(2,6))) + 1
        num_of_simulations = secrets.randbelow(int(math.pow(2,7))) + 1

        # create regular users and miners
        for id in range(num_of_participates):
            private_key_reg_user,public_key_reg_user = self.generate_private_public_key()
            private_key_miner,public_key_miner = self.generate_private_public_key()
            reg_users.append(RegUser(private_key_reg_user,public_key_reg_user,amount,id))
            miners.append(Miner(private_key_miner,public_key_miner,amount,(id)))


        for simulations in range(num_of_simulations):
            print("\nSimulation ", simulations, ": ")
            fees_per_simulation = random()
            total_fees = 0
            transaction_volume = 0
            pool = []
            #first simulation, all the users get a 10 HERL
            if simulations == 0:
                e_l_private_key,e_l_public_key =  self.generate_private_public_key() #Evyatar Hai & Lior Reinitz Keys
                sender_address = Miner(e_l_private_key,e_l_public_key,int(math.pow(2,16)),int(math.pow(2,31)))
                for user in range(num_of_participates):
                    pool.append(sender_address.create_transaction(amount,reg_users[user],fees_per_simulation))
                    pool.append(sender_address.create_transaction(amount, miners[user],fees_per_simulation))
                    transaction_volume += amount*2

                list_of_transactions = pool
                rand_miner = int(math.pow(2,31))
                first_simulation = True
            else:
                pool = self.generate_pool_of_transactions(reg_users, num_of_participates,secrets.randbelow(20))
                if not len(pool):
                    print("No Transactions Generated!")
                    continue
                #some miner will do validation for the transactions who generated
                temp = secrets.randbelow(num_of_participates)
                rand_miner = miners[temp].get_id()
                list_of_transactions,total_fees,transaction_volume = miners[temp].validate_transactions(pool,reg_users)
                if not len(list_of_transactions):
                    print("All The Transactions Declined!")
                    continue
                first_simulation = False
                #The miner that mine the block, getting reward on his hard work - the transactions fees for mining this block
                miners[temp].set_amount(miners[temp].get_wallet_amount() + total_fees)

            list_of_transactions.reverse()
            new_block = Block(list_of_transactions, datetime.now(),BlockChain.get_num_of_blocks(),total_fees,transaction_volume)
            new_block.create_merkle_tree(BlockChain.get_num_of_blocks())
            new_block.set_root(new_block.get_nodes()[0])
            self.update_users(reg_users,miners, new_block.get_transaction_list(),first_simulation)
            print("Miner ",rand_miner," Created a new Block at",new_block.get_timestamp().strftime("%c"))

            BlockChain.add_block(new_block)
            BlockChain.print_details()
            BlockChain.print_the_chain()





    def update_users(self,reg_users,miners, list_of_transactions,sim):

        for id in (list_of_transactions):

            if sim:
                user = id.get_recipient_address()
                temp = user.get_id()
                if isinstance(user, Miner):
                    miners[temp].append_to_path_of_proof(user.get_path_of_proof())

                else:
                    reg_users[temp].append_to_path_of_proof(user.get_path_of_proof())

            else:
                user = id.get_sender_address()
                temp = user.get_id()
                if isinstance(user, Miner):
                    miners[temp].append_to_path_of_proof(user.get_path_of_proof())
                    miners[temp].append_to_path_of_proof(id.get_recipient_address().get_path_of_proof())
                else:
                    reg_users[temp].append_to_path_of_proof(user.get_path_of_proof())
                    reg_users[temp].append_to_path_of_proof(id.get_recipient_address().get_path_of_proof())


    def generate_pool_of_transactions(self,reg_users, num_of_participates,timer):

        pool = []

        while timer:
                rand_user = secrets.randbelow(num_of_participates)
                rand_recipient = secrets.randbelow(num_of_participates)
                if rand_user == rand_recipient: continue
                fees_per_simulation = random()

                #sending other user amount of HERL, could be more than actual the user have,
                #so we can see the option to do double spending, the user cannot create a transcation
                #if he dosnt have enough HERL

                value = uniform(0.001,math.pow(2,4))
                pool.append(reg_users[rand_user].create_transaction(value,reg_users[rand_recipient],fees_per_simulation))
                timer-=1
                time.sleep(1)
        return pool


    def generate_private_public_key(self):
        new_key = RSA.generate(1024, e=65537)
        public_key = new_key.publickey()
        private_key = new_key
        return private_key, public_key



if __name__ == "__main__":
    sim = Simulator()
    sim.run_simulator()
    print("The Simulations Finished!")



