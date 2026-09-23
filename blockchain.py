import hashlib
from datetime import datetime


# ============================================================
# BLOCK
# ============================================================

class Block:

    def __init__(
        self,
        index,
        encrypted_data,
        data_hash,
        previous_hash,
        timestamp=None
    ):

        self.index = index

        self.timestamp = (
            timestamp
            if timestamp
            else datetime.now().isoformat()
        )

        self.encrypted_data = encrypted_data

        self.data_hash = data_hash

        self.previous_hash = previous_hash

        self.hash = self.calculate_hash()


    # ========================================================
    # CALCULATE BLOCK HASH
    # ========================================================

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


# ============================================================
# BLOCKCHAIN
# ============================================================

class Blockchain:

    def __init__(self):

        self.chain = []

        self.create_genesis_block()


    # ========================================================
    # GENESIS BLOCK
    # ========================================================

    def create_genesis_block(self):

        genesis_data = "Genesis Block"

        genesis_hash = hashlib.sha256(
            genesis_data.encode("utf-8")
        ).hexdigest()

        genesis_block = Block(
            index=0,
            encrypted_data=genesis_data,
            data_hash=genesis_hash,
            previous_hash="0",
            timestamp="GENESIS"
        )

        self.chain.append(
            genesis_block
        )


    # ========================================================
    # ADD NEW BLOCK
    # ========================================================

    def add_block(
        self,
        encrypted_data,
        data_hash
    ):

        previous_block = self.chain[-1]

        new_block = Block(
            index=len(self.chain),
            encrypted_data=encrypted_data,
            data_hash=data_hash,
            previous_hash=previous_block.hash
        )

        self.chain.append(
            new_block
        )

        return new_block


    # ========================================================
    # VERIFY BLOCKCHAIN
    # ========================================================

    def verify_chain(self):

        for i in range(
            1,
            len(self.chain)
        ):

            current_block = self.chain[i]

            previous_block = self.chain[i - 1]


            # ------------------------------------------------
            # CHECK DATA HASH
            # ------------------------------------------------

            calculated_data_hash = hashlib.sha256(
                current_block.encrypted_data.encode("utf-8")
            ).hexdigest()

            if (
                current_block.data_hash
                != calculated_data_hash
            ):

                return False


            # ------------------------------------------------
            # CHECK CURRENT BLOCK HASH
            # ------------------------------------------------

            if (
                current_block.hash
                != current_block.calculate_hash()
            ):

                return False


            # ------------------------------------------------
            # CHECK PREVIOUS BLOCK CONNECTION
            # ------------------------------------------------

            if (
                current_block.previous_hash
                != previous_block.hash
            ):

                return False


        return True


    # ========================================================
    # LOAD BLOCK FROM STORED DATA
    # ========================================================

    def add_existing_block(
        self,
        encrypted_data,
        data_hash,
        block_hash,
        previous_hash,
        timestamp
    ):

        new_block = Block(
            index=len(self.chain),
            encrypted_data=encrypted_data,
            data_hash=data_hash,
            previous_hash=previous_hash,
            timestamp=timestamp
        )

        # Keep the stored blockchain hash.
        # This allows us to detect if the stored
        # block hash was changed.

        new_block.hash = block_hash

        self.chain.append(
            new_block
        )

        return new_block