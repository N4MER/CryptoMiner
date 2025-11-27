import multiprocessing
import time

from Block import Block

class MiningGroup:
    def __init__(self):
        #self.nonce = multiprocessing.Value("i", 0)
        self.timestamp = multiprocessing.Value("d", time.time())
        self.blockchain = multiprocessing.Manager().list()
        self.miners = []
        self.lock = multiprocessing.Lock()
        self.processes = []

    def run(self):
        self.create_threads()
        self.start_all()
        self.join_all()

    def add_miner(self, miner):
        self.miners.append(miner)

    def create_threads(self):
        for miner in self.miners:
            p = multiprocessing.Process(target=miner.mine, args=(self.blockchain, self.lock, self.timestamp, len(self.miners)))
            self.processes.append(p)

    def start_all(self):
        for p in self.processes:
            p.start()

    def join_all(self):
        for p in self.processes:
            p.join()


class Miner:
    def __init__(self, username, miner_id):
        self._name = username
        self._wallet = 0
        self.miner_id = miner_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None or type(value) is not str:
            raise TypeError("Name must be a string")
        self._name = value

    @property
    def wallet(self):
        return self._wallet

    @wallet.setter
    def wallet(self, value):
        self._wallet = value

    def mine(self, blockchain, lock, timestamp, total_miners):
        k = 0
        last_seen_hash = len(blockchain)
        while True:
            if blockchain[-1].hash != last_seen_hash:
                last_seen_hash = blockchain[-1].hash
                k = 0

            nonce = self.miner_id + k * total_miners

            with lock:
                blockchain_length = len(blockchain)
                last_block_in_blockchain = blockchain[-1]
                new_block = Block(last_block_in_blockchain.hash, timestamp.value)
                #print(f'{self.name}: {nonce} block: {str(new_block)}')

            #new_block = Block(last_block_in_blockchain.hash, timestamp.value)
            hashed_new_block = new_block.hash_block(nonce)
            k+=1


            if new_block.compare_hash(hashed_new_block):
                with lock:

                    if blockchain[-1].hash != last_seen_hash:
                        last_seen_hash = blockchain[-1].hash
                        k = 0
                        continue

                    self._wallet += new_block.reward
                    print(f'{self.name} mined crypto! wallet: {self.wallet} nonce: {nonce} time to find: {time.time() - timestamp.value}')
                    k = 0
                    timestamp.value = time.time()
                    new_block.hash = hashed_new_block
                    blockchain.append(new_block)
                    #Miner.print_blockchain(blockchain)

    @staticmethod
    def print_blockchain(blockchain):
        for block in blockchain:
            print(block)

if __name__ == '__main__':

    max_processes = multiprocessing.cpu_count()
    print(max_processes)

    mining_group = MiningGroup()

    m1 = Miner('m1', 0)
    m2 = Miner('m2', 1)
    m3 = Miner('m3', 2)
    m4 = Miner('m4', 3)
    m5 = Miner('m5', 4)
    m6 = Miner('m6', 5)
    m7 = Miner('m7', 6)
    m8 = Miner('m8', 7)
    m9 = Miner('m9', 8)
    m10 = Miner('m10', 9)

    starting_block = Block('0'*64, time.time())
    starting_block.hash = '0'*64

    mining_group.blockchain.append(starting_block)

    mining_group.add_miner(m1)
    mining_group.add_miner(m2)
    mining_group.add_miner(m3)
    mining_group.add_miner(m4)
    mining_group.add_miner(m5)
    mining_group.add_miner(m6)
    mining_group.add_miner(m7)
    mining_group.add_miner(m8)
    mining_group.add_miner(m9)
    mining_group.add_miner(m10)

    mining_group.run()