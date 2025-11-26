import hashlib
import threading
import time

class Block:
    def __init__(self, previous_hash):
        """
        Constructor for Block class.
        :param previous_hash: Hash of the previous block.
        """
        self._previous_hash = previous_hash
        self.reward = 1
        self._timestamp = time.time()
        self._nonce = 0
        self._difficulty = 5
        self._hash = None

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value):
        if value is None or type(value) is not str or len(value) != 64:
            raise TypeError("Hash must be a 64-character hex string.")

        try:
            int(value, 16)
        except ValueError:
            raise TypeError("Hash must contain valid hexadecimal characters.")
        self._hash = value

    @property
    def nonce(self):
        return self._nonce

    @nonce.setter
    def nonce(self, value):
        self._nonce = value

    @property
    def previous_hash(self):
        return self._previous_hash

    @previous_hash.setter
    def previous_hash(self, value):
        """
        Setter for previous hash.
        Value must be a 64-character hex string.
        :param value:
        :return:
        """
        if value is None or type(value) is not str or len(value) != 64:
            raise TypeError("Previous hash must be a 64-character hex string.")

        try:
            int(value, 16)
        except ValueError:
            raise TypeError("Previous hash must contain valid hexadecimal characters.")

        self.previous_hash = value

    def increment_nonce(self):
        """
        Increments the nonce.
        :return:
        """
        self._nonce += 1

    def get_value(self):
        """
        Converts variable values in block to string.
        :return: variable values of the block converted to string.
        """
        return f"{self.previous_hash} | {self._timestamp} | {self._nonce}".encode()

    def hash_block(self):
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
        target = ("0" * self._difficulty) + ("f" * (64 - self._difficulty))
        hash = self.hash_block()
        if int(hash, 16) < int(target, 16):
            self.hash = hash
            return True
        return False


class Blockchain:
    def __init__(self):
        """
        Constructor for Block class.
        """
        self.chain = []
        self.lock = threading.Lock()


    def append(self, block):
        """
        Appends a block to the BlockChain.
        :param block:
        :return:
        """
        with self.lock:
            self.chain.append(block)