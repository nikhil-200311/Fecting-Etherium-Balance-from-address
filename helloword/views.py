from django.shortcuts import render
from web3 import Web3

def get_wallet_balance(wallet_address):
    # Connect to Ethereum network using Infura API
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a6551b993013458ab3670308d647e5eb'))

    # Convert wallet address to checksum format
    checksum_address = w3.to_checksum_address(wallet_address)

    # Fetch current balance of wallet
    balance_wei = w3.eth.get_balance(checksum_address)

    # Convert balance from wei to ether
    balance_eth = w3.from_wei(balance_wei, 'ether')

    return balance_eth

def get_recent_transactions(wallet_address):
    # Connect to Ethereum network using Infura API
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a6551b993013458ab3670308d647e5eb'))

    # Convert wallet address to checksum format
    checksum_address = w3.to_checksum_address(wallet_address)

    # Fetch the five most recent transactions involving this wallet
    transactions = [w3.eth.get_transaction_count(checksum_address, 'latest')]

    return transactions[:5]

def fetch_wallet(request):
    if request.method == 'POST':
        # Get the Ethereum address entered by the user
        wallet_address = request.POST.get('wallet_address')

        # Fetch the current balance of the wallet
        balance = get_wallet_balance(wallet_address)
        
        # Fetch the five most recent transactions involving this wallet
        transactions = get_recent_transactions(wallet_address)

        # Render the template with the wallet balance and transaction history
        return render(request, 'wallet.html', {'balance': balance, 'transactions': transactions})

    # If the request method is not POST, just render the empty form
    return render(request, 'fetch.html')