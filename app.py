from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

# You would set this as an environment variable in production
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_eth_balance(address):
    """Get the ETH balance for an address using Etherscan API"""
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "1":
        # Convert from Wei to ETH (1 ETH = 10^18 Wei)
        balance_eth = int(data["result"]) / 10**18
        return balance_eth
    else:
        return None

def get_transactions(address, limit=5):
    """Get the last transactions for an address using Etherscan API"""
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset={limit}&sort=desc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "1":
        return data["result"]
    else:
        return []

def format_transaction(tx, address):
    """Format a transaction for display"""
    timestamp = datetime.fromtimestamp(int(tx["timeStamp"]))
    date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    # Convert values from Wei to ETH
    value_eth = float(tx["value"]) / 10**18
    gas_price_gwei = float(tx["gasPrice"]) / 10**9
    gas_used = int(tx["gasUsed"])
    
    # Determine if this is an incoming or outgoing transaction
    tx_type = "IN" if tx["to"].lower() == address.lower() else "OUT"
    
    return {
        "hash": tx["hash"],
        "date": date_str,
        "from": tx["from"],
        "to": tx["to"],
        "type": tx_type,
        "value_eth": value_eth,
        "gas_used": gas_used,
        "gas_price_gwei": gas_price_gwei,
        "confirmation": tx["confirmations"]
    }

def get_eth_price():
    """Get the current ETH price in USD"""
    url = f"https://api.etherscan.io/api?module=stats&action=ethprice&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "1":
        return float(data["result"]["ethusd"])
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/wallet', methods=['POST'])
def wallet_info():
    data = request.json
    address = data.get('address', '')
    
    if not address:
        return jsonify({"error": "Address is required"}), 400
    
    # Get wallet balance
    balance = get_eth_balance(address)
    if balance is None:
        return jsonify({"error": "Failed to fetch balance"}), 500
    
    # Get transactions
    transactions = get_transactions(address, 5)
    formatted_transactions = [format_transaction(tx, address) for tx in transactions]
    
    # Get ETH price
    eth_price = get_eth_price()
    usd_balance = balance * eth_price if eth_price else None
    
    # Get transaction history for chart (last 10 transactions)
    chart_transactions = get_transactions(address, 10)
    chart_data = []
    
    for tx in chart_transactions:
        timestamp = int(tx["timeStamp"]) * 1000  # Convert to milliseconds for JS
        value = float(tx["value"]) / 10**18
        tx_type = "in" if tx["to"].lower() == address.lower() else "out"
        
        chart_data.append({
            "timestamp": timestamp,
            "value": value,
            "type": tx_type
        })
    
    return jsonify({
        "address": address,
        "balance": balance,
        "usd_balance": usd_balance,
        "transactions": formatted_transactions,
        "chart_data": chart_data
    })

if __name__ == '__main__':
    app.run(debug=True)
