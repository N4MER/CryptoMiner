from BlockChain import Block

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

    def mine(self, block, nonce, block_chain):
        block.nonce = nonce
        if block.compare_hash():
            self._wallet += block.reward
            block_chain.append(Block(block.hash))
        else:
            nonce += 1