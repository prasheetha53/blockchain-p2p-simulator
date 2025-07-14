# Blockchain Network Implementation

## Overview

This project is a comprehensive implementation of a blockchain network using Python and Flask. It provides a functional blockchain with features such as mining, transaction handling, peer-to-peer networking, and consensus algorithms. The project is designed to be both educational and practical, demonstrating core blockchain concepts in a real-world application.

## Features

- **Blockchain Implementation**: A complete blockchain with blocks, transactions, and cryptographic hashing.
- **Proof of Work**: Mining algorithm to secure the blockchain.
- **Transaction Handling**: Creation and management of transactions within the network.
- **Peer-to-Peer Networking**: Nodes can register and communicate with each other to maintain a distributed ledger.
- **Consensus Algorithm**: Implementation of the longest chain rule to resolve conflicts and ensure consistency across the network.
- **Web Interface**: A dashboard to interact with the blockchain, view transactions, mine blocks, and manage nodes.
- **RESTful API**: Endpoints to interact with the blockchain programmatically.

## Project Structure

```
BLOCKCHAIN-NETWORK/
│
├── app.py                  # Main application file with Flask routes
├── blockchain.py           # Core blockchain implementation
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Web interface for the blockchain dashboard
└── README.md               # Project documentation
```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/blockchain-network.git
   cd blockchain-network
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Blockchain Node**:
   ```bash
   python app.py --port 5000 --host 127.0.0.1
   ```

2. **Access the Dashboard**:
   Open your web browser and navigate to `http://127.0.0.1:5000` to access the blockchain dashboard.

3. **Interact with the Blockchain**:
   - **Mine Blocks**: Click the "Mine Block" button to mine a new block.
   - **Add Transactions**: Use the form to add new transactions to the pending transactions pool.
   - **Register Nodes**: Add new peer nodes to the network.
   - **View Blockchain**: See the full blockchain and pending transactions.

## API Endpoints

- `GET /`: Main dashboard page.
- `GET /mine`: Mine a new block.
- `POST /transactions/new`: Add a new transaction.
- `GET /chain`: Get the full blockchain.
- `GET /pending`: Get pending transactions.
- `POST /nodes/register`: Register new peer nodes.
- `GET /nodes`: Get all registered peer nodes.
- `GET /nodes/resolve`: Resolve conflicts using the consensus algorithm.
- `GET /stats`: Get node statistics.
- `GET /balance/<address>`: Get balance for a specific address.

## Demo

Watch the demo of the blockchain network:

[![Blockchain Network Demo](https://img.youtube.com/vi/H2M96z8Mo2o/0.jpg)](https://www.youtube.com/watch?v=H2M96z8Mo2o)

## Technical Details

### Blockchain Implementation

The blockchain is implemented as a chain of blocks, where each block contains a list of transactions, a timestamp, the hash of the previous block, and a nonce for proof of work. The `Blockchain` class handles the creation of new blocks, validation of the chain, and mining of pending transactions.

### Proof of Work

The proof of work algorithm requires miners to find a nonce such that the hash of the block starts with a certain number of zeros (determined by the difficulty level). This ensures that mining a block requires computational effort, securing the network against attacks.

### Transactions

Transactions are created by users and added to the pending transactions pool. Each transaction includes a sender, recipient, and amount. Transactions are validated before being added to the pool to ensure they are properly formatted and contain valid data.

### Peer-to-Peer Networking

Nodes in the network can register with each other to form a peer-to-peer network. Each node maintains a list of peer nodes and can communicate with them to synchronize the blockchain and resolve conflicts.

### Consensus Algorithm

The consensus algorithm ensures that all nodes in the network agree on the state of the blockchain. The longest chain rule is used to resolve conflicts, where the longest valid chain is considered the authoritative version of the blockchain.
