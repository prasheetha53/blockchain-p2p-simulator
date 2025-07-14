# Blockchain Node Dashboard

## Overview

The **Blockchain Node Dashboard** is a web-based application that enables users to interact with a decentralized blockchain network. It provides functionalities for managing nodes, creating and viewing transactions, mining new blocks, and monitoring various statistics related to the blockchain. This project is implemented using Python with Flask for the backend and HTML/CSS for the frontend, showcasing a practical application of blockchain technology.

## Features

- **Node Management**: Register and view peer nodes in the network, facilitating decentralized communication.
- **Transaction Handling**: Create and add new transactions to the blockchain, ensuring secure and transparent transfers.
- **Mining**: Mine new blocks and receive mining rewards, demonstrating the proof-of-work mechanism.
- **Blockchain Viewer**: Visualize the entire blockchain, including block details and transactions.
- **Statistics Panel**: Monitor node statistics such as chain length, pending transactions, connected nodes, and mining difficulty.

## Project Structure

```
BLOCKCHAIN-NETWORK/
├── implementation_screenshots/     # Folder containing screenshots of the application
├── app.py                          # Main application file with Flask routes
├── blockchain.py                   # Core blockchain implementation
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                  # Web interface for the blockchain dashboard
└── README.md                       # Project documentation
```

### File Descriptions

- **app.py**: The main application file that contains the Flask web server and defines all the routes for handling requests related to transactions, mining, node management, and blockchain data retrieval. Key routes include:
  - `/`: Renders the main dashboard.
  - `/mine`: Initiates the mining process, creating a new block with pending transactions.
  - `/transactions/new`: Handles new transaction submissions via a POST request.
  - `/chain`: Returns the full blockchain in JSON format.
  - `/pending`: Returns pending transactions in JSON format.
  - `/nodes/register`: Registers new peer nodes by accepting a list of node addresses.
  - `/nodes`: Retrieves all registered peer nodes in JSON format.
  - `/nodes/resolve`: Resolves conflicts in the blockchain by adopting the longest valid chain.
  - `/stats`: Provides node statistics such as chain length, pending transactions, and connected nodes.

- **blockchain.py**: Contains the core logic for the blockchain, including the `Transaction`, `Block`, and `Blockchain` classes. This file handles the creation of blocks, transaction validation, mining processes, and consensus mechanisms. Key components include:
  - **Transaction Class**: Represents a transaction with attributes for sender, recipient, amount, and timestamp. It includes a method to convert the transaction to a dictionary format for JSON serialization.
  - **Block Class**: Represents a block in the blockchain, containing transactions, previous hash, nonce, and methods to calculate its hash. It includes a method to convert the block to a dictionary format for JSON serialization.
  - **Blockchain Class**: Manages the chain of blocks, handles transactions, mining, and validation of the blockchain. It includes methods for creating the genesis block, adding transactions, mining blocks, validating the chain, and calculating balances.

- **requirements.txt**: Lists all the Python dependencies required to run the application, including Flask and any other necessary libraries.

- **templates/index.html**: The HTML file that serves as the user interface for the blockchain dashboard. It includes:
  - A header displaying the node ID and port.
  - Panels for node statistics, new transactions, mining, and blockchain viewing.
  - Forms for submitting transactions and registering nodes.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/blockchain-network.git
   cd blockchain-network
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py --port 5000
   ```

4. **Access the dashboard**:
   Open your web browser and navigate to `http://127.0.0.1:5000`.

## Blockchain Implementation Details

### Core Components

#### Transaction Class

- **Attributes**:
  - `sender`: The address of the sender.
  - `recipient`: The address of the recipient.
  - `amount`: The amount being transferred.
  - `timestamp`: The time when the transaction was created.

- **Methods**:
  - `to_dict()`: Converts the transaction object to a dictionary format for JSON serialization.

#### Block Class

- **Attributes**:
  - `index`: The position of the block in the blockchain.
  - `timestamp`: The time when the block was created.
  - `transactions`: A list of transactions included in the block.
  - `previous_hash`: The hash of the previous block in the chain.
  - `nonce`: A number used in the mining process to find a valid hash.
  - `hash`: The hash of the block, calculated using SHA-256.

- **Methods**:
  - `calculate_hash()`: Computes the hash of the block based on its attributes.
  - `to_dict()`: Converts the block object to a dictionary format for JSON serialization.

#### Blockchain Class

- **Attributes**:
  - `chain`: A list that holds all the blocks in the blockchain.
  - `pending_transactions`: A list of transactions that are waiting to be included in a block.
  - `mining_reward`: The reward given to miners for successfully mining a block.
  - `difficulty`: The difficulty level for the proof-of-work algorithm.

- **Methods**:
  - `create_genesis_block()`: Initializes the blockchain with the first block (genesis block).
  - `add_transaction(transaction)`: Adds a new transaction to the list of pending transactions after validating it.
  - `mine_pending_transactions(mining_reward_address)`: Mines a new block with the pending transactions and rewards the miner.
  - `proof_of_work(block)`: Implements the proof-of-work algorithm to find a valid hash for the block.
  - `is_chain_valid(chain)`: Validates the entire blockchain to ensure integrity.
  - `get_balance(address)`: Calculates the balance of a given address based on transactions in the blockchain.
  - `replace_chain(new_chain_data)`: Replaces the current chain with a new chain if it is longer and valid.

### Mining Process

- The mining process involves creating a new block that includes all pending transactions. The miner must solve a proof-of-work challenge, which requires finding a hash that meets the specified difficulty level (i.e., a certain number of leading zeros).
- Once a valid hash is found, the new block is added to the blockchain, and the miner receives a reward in the form of a transaction.

### Consensus Mechanism

- The application implements a consensus mechanism to resolve conflicts in the blockchain. If a node detects that another node has a longer chain, it will request the longer chain and replace its own if the new chain is valid.
- This ensures that all nodes in the network maintain a consistent view of the blockchain.

## Usage

- **Add Transaction**: Fill in the sender, recipient, and amount in the form and click "Add Transaction". The transaction will be validated and added to the pending transactions.
  
- **Mine Block**: Click the "Mine Block" button to mine a new block containing all pending transactions. The miner will receive a reward for their efforts.

- **View Pending Transactions**: Click "View Pending" to see all transactions waiting to be mined. This provides transparency into the current state of the network.

- **Register Node**: Enter a peer node address (e.g., `localhost:5001`) and click "Register Node" to add it to the network. This enables decentralized communication and collaboration.

- **Sync Chain**: Click "Sync Chain" to resolve conflicts with other nodes by adopting the longest valid chain.

## Demo

Watch the demo of the Blockchain Node Dashboard:

[![Watch the demo](https://img.youtube.com/vi/H2M96z8Mo2o/0.jpg)](https://youtu.be/H2M96z8Mo2o?si=0yRezApP99jmSD6Y)
