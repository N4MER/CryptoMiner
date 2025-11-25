import hashlib
import time

class Block:
    def __init__(self, previous_hash):
        """
        Constructor for Block class.
        :param previous_hash: Hash of the previous block.
        """
        self.previous_hash = previous_hash
        self.reward = 1
        self.timestamp = time.time()
        self.nonce = 0
        self.difficulty = 5
        self.hash = None

    def get_value(self):
        """
        Converts variable values in block to string.
        :return: variable values of the block converted to string.
        """
        return f"{self.previous_hash} | {self.timestamp} | {self.nonce}".encode()

    def hash(self):
        """
        Hashes string made from variable values of the block.
        :return: Hash of the string made from variable values.
        """
        return hashlib.sha256(self.get_value()).hexdigest()

    def compare_hash(self):
        """
        Compares values of the hashed block with a difficulty based target.

        The target is a 64-character hex string.
        It starts with number of zeros equal to difficulty of the block, and all remaining characters are f.
        :return: True if int value of the block is smaller than int value of the target, and False otherwise.
        """
        target = ("0" * self.difficulty) + ("f" * (64 - self.difficulty))
        hash = self.hash()
        if int(hash, 16) < int(target, 16):
            self.hash = hash
            return True
        return False


class BlockChain:
    def __init__(self):
        """
        Constructor for Block class.
        """
        self.chain = []

    def append(self, block):
        """
        Appends a block to the BlockChain.
        :param block:
        :return:
        """
        self.chain.append(block)

