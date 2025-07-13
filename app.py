from flask import Flask, jsonify, request, render_template
import requests
import argparse
import uuid
from blockchain import Blockchain, Transaction
from urllib.parse import urlparse


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Generate unique node identifier
node_identifier = str(uuid.uuid4()).replace('-', '')

# Initialize blockchain
blockchain = Blockchain()

# Set of peer nodes
peers = set()


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         node_id=node_identifier[:8], 
                         port=app.config.get('PORT', 5000))


@app.route('/mine', methods=['GET'])
def mine():
    """Mine a new block"""
    try:
        # Check if there are pending transactions
        if not blockchain.pending_transactions:
            return jsonify({
                'success': False,
                'message': 'No pending transactions to mine'
            }), 400
        
        # Mine the block
        new_block = blockchain.mine_pending_transactions(node_identifier)
        
        response = {
            'success': True,
            'message': 'New block mined successfully',
            'block': new_block.to_dict(),
            'chain_length': len(blockchain.chain)
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Mining failed: {str(e)}'
        }), 500


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Add a new transaction"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['sender', 'recipient', 'amount']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: sender, recipient, amount'
            }), 400
        
        # Create transaction
        transaction = Transaction(
            data['sender'],
            data['recipient'],
            float(data['amount'])
        )
        
        # Add to blockchain
        if blockchain.add_transaction(transaction):
            return jsonify({
                'success': True,
                'message': 'Transaction added successfully',
                'transaction': transaction.to_dict()
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid transaction'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Transaction failed: {str(e)}'
        }), 500


@app.route('/chain', methods=['GET'])
def full_chain():
    """Return the full blockchain"""
    response = {
        'chain': blockchain.to_dict()['chain'],
        'length': len(blockchain.chain),
        'valid': blockchain.is_chain_valid()
    }
    return jsonify(response), 200


@app.route('/pending', methods=['GET'])
def pending_transactions():
    """Return pending transactions"""
    return jsonify({
        'transactions': [tx.to_dict() for tx in blockchain.pending_transactions],
        'count': len(blockchain.pending_transactions)
    }), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """Register new peer nodes"""
    try:
        data = request.get_json()
        nodes = data.get('nodes', [])
        
        if not nodes:
            return jsonify({
                'success': False,
                'message': 'No nodes provided'
            }), 400
        
        for node in nodes:
            # Parse and validate node URL
            parsed_url = urlparse(node if node.startswith('http') else f'http://{node}')
            if parsed_url.netloc:
                peers.add(parsed_url.netloc)
        
        return jsonify({
            'success': True,
            'message': 'Nodes registered successfully',
            'total_nodes': list(peers)
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500


@app.route('/nodes', methods=['GET'])
def get_nodes():
    """Get all registered peer nodes"""
    return jsonify({
        'nodes': list(peers),
        'count': len(peers)
    }), 200


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """Resolve conflicts using longest chain rule"""
    try:
        replaced = False
        max_length = len(blockchain.chain)
        new_chain = None
        
        # Check all peer nodes
        for peer in peers:
            try:
                response = requests.get(f'http://{peer}/chain', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    length = data['length']
                    chain = data['chain']
                    
                    # Check if chain is longer and valid
                    if length > max_length:
                        if blockchain.replace_chain(chain):
                            max_length = length
                            new_chain = chain
                            replaced = True
                            
            except requests.exceptions.RequestException:
                continue  # Skip unreachable peers
        
        if replaced:
            return jsonify({
                'success': True,
                'message': 'Chain was replaced',
                'new_chain': new_chain,
                'chain_length': max_length
            }), 200
        else:
            return jsonify({
                'success': True,
                'message': 'Chain is authoritative',
                'chain_length': len(blockchain.chain)
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Consensus failed: {str(e)}'
        }), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get node statistics"""
    return jsonify({
        'node_id': node_identifier[:8],
        'chain_length': len(blockchain.chain),
        'pending_transactions': len(blockchain.pending_transactions),
        'connected_nodes': len(peers),
        'mining_difficulty': blockchain.difficulty,
        'mining_reward': blockchain.mining_reward
    }), 200


@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """Get balance for a specific address"""
    balance = blockchain.get_balance(address)
    return jsonify({
        'address': address,
        'balance': balance
    }), 200


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run blockchain node')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the node on')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to run the node on')
    args = parser.parse_args()
    
    # Store port in app config
    app.config['PORT'] = args.port
    
    print(f"Starting blockchain node on {args.host}:{args.port}")
    print(f"Node ID: {node_identifier[:8]}")
    print(f"Dashboard: http://{args.host}:{args.port}")
    
    app.run(host=args.host, port=args.port, debug=True)