import multiprocessing

from Block import Block

class MiningGroup:
    def __init__(self):
        self.nonce = multiprocessing.Value("i", 0)
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
            p = multiprocessing.Process(target=miner.mine, args=(self.blockchain, self.lock, self.nonce))
            self.processes.append(p)

    def start_all(self):
        for p in self.processes:
            p.start()

    def join_all(self):
        for p in self.processes:
            p.join()


class Miner:
    def __init__(self, username):
        self._name = username
        self._wallet = 0

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

    def mine(self, blockchain, lock, nonce):
        while True:
            with lock:
                block = blockchain[-1]
                old_block = block
                nonce.value += 1
                blockchain[-1] = block

            if block.compare_hash(nonce.value):
                self._wallet += old_block.reward
                print(f'{self.name} mined crypto! wallet: {self.wallet} nonce: {nonce.value}')
                with lock:
                    blockchain[-1] = old_block
                    blockchain.append(Block(old_block.hash))

if __name__ == '__main__':
    mining_group = MiningGroup()
    m1 = Miner('m1')
    m2 = Miner('m2')
    m3 = Miner('m3')
    m4 = Miner('m4')

    starting_block = Block('0'*64)

    mining_group.blockchain.append(starting_block)

    mining_group.add_miner(m1)
    mining_group.add_miner(m2)
    mining_group.add_miner(m3)
    mining_group.add_miner(m4)

    mining_group.run()