import time


list_of_blocks = []


class BlockChain:

    @staticmethod
    def add_block(block):
        if len(list_of_blocks) == 0:
            #the genesis block won't hold prev block hash cause he is the first block in the Blockchain.
            block.set_prev_block_hash(0)
        else:
            block.set_prev_block_hash(list_of_blocks[-1].get_hash())
        list_of_blocks.append(block)


    @staticmethod
    def get_block(index):
        return list_of_blocks[index]


    @staticmethod
    def get_num_of_blocks():
        return len(list_of_blocks)


    @staticmethod
    def print_details():
        for block in range(len(list_of_blocks)):
            time.sleep(0.5)
            print("\nDetails on Block number ",block,":")
            print("Previous Hash : ",list_of_blocks[block].get_prev_block_hash())
            print("Block Hash : ",list_of_blocks[block].get_hash())
            print("Fee Reward : ", list_of_blocks[block].get_total_fees()," HERL")
            print("Transaction Volume : ", list_of_blocks[block].get_transaction_volume()," HERL")
            print("Created at : ", list_of_blocks[block].get_timestamp().strftime("%c"))


    @staticmethod
    def print_the_chain():

        for block in range(0,len(list_of_blocks)):
            if block == 0:
                print("\nGenesis Block")

            print("*******")
            print("*     *")
            if block < 10:
                print("* ", block, " *")
            else:
                print("* ", block, "*")
            print("*     *")
            print("*******")

            if block != (len(list_of_blocks)-1):
                print("   | ")
                print("   V ")
            else:
                print("<New Block Added!>")
            if block == (len(list_of_blocks)-2):
                print("                         <Please wait until the block will be added to the BlockChain>")
                time.sleep(2)
