import requests
import json
from datetime import datetime

def get_eth_balance(address, api_key):
    """Get the ETH balance for an address using Etherscan API"""
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "1":
        # Convert from Wei to ETH (1 ETH = 10^18 Wei)
        balance_eth = int(data["result"]) / 10**18
        return balance_eth
    else:
        return f"Error: {data['message']}"

def get_transactions(address, api_key, limit=5):
    """Get the last transactions for an address using Etherscan API"""
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset={limit}&sort=desc&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "1":
        return data["result"]
    else:
        return []

def format_transaction(tx):
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
        "gas_price_gwei": gas_price_gwei
    }

# Replace with your Etherscan API key
ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY"

# Example Ethereum address (Vitalik Buterin's address)
address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

# You can replace this with any Ethereum address you want to check
print(f"Checking Ethereum address: {address}")

# Get balance
balance = get_eth_balance(address, ETHERSCAN_API_KEY)
print(f"\nBalance: {balance:.4f} ETH")

# Get last 5 transactions
print("\nLast 5 transactions:")
transactions = get_transactions(address, ETHERSCAN_API_KEY, 5)

if transactions:
    for i, tx in enumerate(transactions, 1):
        tx_formatted = format_transaction(tx)
        print(f"\nTransaction {i}:")
        print(f"  Hash: {tx_formatted['hash']}")
        print(f"  Date: {tx_formatted['date']}")
        print(f"  Type: {tx_formatted['type']}")
        print(f"  From: {tx_formatted['from']}")
        print(f"  To: {tx_formatted['to']}")
        print(f"  Value: {tx_formatted['value_eth']:.4f} ETH")
        print(f"  Gas Used: {tx_formatted['gas_used']}")
        print(f"  Gas Price: {tx_formatted['gas_price_gwei']:.2f} Gwei")
else:
    print("No transactions found or API error")
