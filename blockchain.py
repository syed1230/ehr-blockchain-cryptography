import hashlib
import json
from datetime import datetime


class Block:

    def __init__(
        self,
        index,
        encrypted_data,
        data_hash,
        previous_hash
    ):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.encrypted_data = encrypted_data
        self.data_hash = data_hash
        self.previous_hash = previous_hash

        # Calculate current block hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):

        block_data = (
            str(self.index)
            + self.timestamp
            + self.encrypted_data
            + self.data_hash
            + self.previous_hash
        )

        return hashlib.sha256(
            block_data.encode("utf-8")
        ).hexdigest()


class Blockchain:

    def __init__(self):

        self.chain = []

        # Create first block
        self.create_genesis_block()

    def create_genesis_block(self):

        genesis_block = Block(
            0,
            "Genesis Block",
            hashlib.sha256(
                b"Genesis Block"
            ).hexdigest(),
            "0"
        )

        self.chain.append(genesis_block)

    def add_block(self, encrypted_data, data_hash):

        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            encrypted_data,
            data_hash,
            previous_block.hash
        )

        self.chain.append(new_block)

    def verify_chain(self):

        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check current block hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check connection to previous block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True