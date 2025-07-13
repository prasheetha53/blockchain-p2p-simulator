import hashlib
import json
import time
from typing import List, Dict, Optional


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }


class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 10
        self.difficulty = 4
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, [], "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add a transaction to pending transactions"""
        if transaction.sender == transaction.recipient:
            return False
        if transaction.amount <= 0:
            return False
        
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, mining_reward_address: str) -> Block:
        """Mine a new block with pending transactions"""
        # Add mining reward transaction
        reward_transaction = Transaction(None, mining_reward_address, self.mining_reward)
        self.pending_transactions.append(reward_transaction)
        
        # Create new block
        new_block = Block(
            len(self.chain),
            self.pending_transactions.copy(),
            self.get_latest_block().hash
        )
        
        # Proof of work
        new_block = self.proof_of_work(new_block)
        
        # Add to chain and clear pending
        self.chain.append(new_block)
        self.pending_transactions = []
        
        return new_block
    
    def proof_of_work(self, block: Block) -> Block:
        """Simple proof of work algorithm"""
        target = "0" * self.difficulty
        
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()
        
        return block
    
    def is_chain_valid(self, chain: List[Block] = None) -> bool:
        """Validate the entire blockchain"""
        if chain is None:
            chain = self.chain
        
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check proof of work
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                return False
        
        return True
    
    def get_balance(self, address: str) -> float:
        """Get balance for a specific address"""
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        
        return balance
    
    def to_dict(self) -> Dict:
        return {
            'chain': [block.to_dict() for block in self.chain],
            'length': len(self.chain)
        }
    
    def replace_chain(self, new_chain_data: List[Dict]) -> bool:
        """Replace current chain with new chain if valid and longer"""
        try:
            # Convert dict data back to Block objects
            new_chain = []
            for block_data in new_chain_data:
                transactions = []
                for tx_data in block_data['transactions']:
                    tx = Transaction(tx_data['sender'], tx_data['recipient'], tx_data['amount'])
                    tx.timestamp = tx_data['timestamp']
                    transactions.append(tx)
                
                block = Block(
                    block_data['index'],
                    transactions,
                    block_data['previous_hash'],
                    block_data['nonce']
                )
                block.timestamp = block_data['timestamp']
                block.hash = block_data['hash']
                new_chain.append(block)
            
            # Validate new chain
            if len(new_chain) > len(self.chain) and self.is_chain_valid(new_chain):
                self.chain = new_chain
                return True
            
            return False
        except Exception as e:
            print(f"Error replacing chain: {e}")
            return False