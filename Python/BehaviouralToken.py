from web3 import Web3
from eth_account.messages import encode_defunct
from eth_account import Account
import json

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

account_1 = "account_1"  # Fill me in
account_2 = "account_2"  # Fill me in
account_3 = "account_3"
private_key = "private_key"  # Fill me in

# OMG ABI
abi = json.loads(
    '[{"inputs":[{"internalType":"uint256","name":"initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"customer","type":"address"},{"indexed":false,"internalType":"address","name":"serviceProvider","type":"address"},{"indexed":false,"internalType":"uint256","name":"nonce","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"signature","type":"bytes"},{"indexed":false,"internalType":"address","name":"msgSender","type":"address"}],"name":"serviceBuyedWithMetaTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"customer","type":"address"},{"indexed":false,"internalType":"address","name":"serviceProvider","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"serviceBuyedWithTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"customer","type":"address"},{"indexed":false,"internalType":"address","name":"serviceProvider","type":"address"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"quantity","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"signature","type":"bytes"},{"indexed":false,"internalType":"address","name":"msgSender","type":"address"}],"name":"signatureNotValid","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SERVICE_CUSTOMER","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SERVICE_PROVIDER","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"},{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"addAddressToCircuit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"serviceProvider","type":"address"}],"name":"buyService","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"serviceCustomer","type":"address"},{"internalType":"address","name":"serviceProvider","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"name":"buyServiceWithMetaTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"buyTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_rateOfTokenForEth","type":"uint256"}],"name":"changeRateOfTokenForEth","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"increaseTotalSupply","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"nonceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pauseToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"removeAddressFromCircuit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpauseToken","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

# OMG Address
address = 'address'

class BehaviouralToken:

	#Costruttore che riceve in input i dati di connessione per Ganache, l'ABI
	#dello Smart Contract e l'indirizzo di quest'ultimo
    def __init__(self, ganache_url, abi, contract_address):
        self.abi = abi
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        self.contract = web3.eth.contract(address=contract_address, abi=abi)

	#Restituisce il numero di token emessi dal Contract Owner
    def get_total_supply(self):
        try:
            result = self.contract.functions.totalSupply().call()
        except:
            raise Exception("Errore durante esecuzione get_total_supply")
        print(result)
        return result

	#Restituisce il numero di token associati ad un account
    def get_address_balance(self, customer_index):
        try:
            result = self.contract.functions.balanceOf(web3.eth.accounts[customer_index]).call()
        except:
            raise Exception("Errore durante esecuzione get_address_balance")
        print(result)
        return result

	#Restituisce l'ABI dello Smart Contract
    def get_abi(self):
        try:
            result = self.abi
        except:
            raise Exception("Errore durante esecuzione get_abi")
        print(result)
        return result

	#Invocando il metodo viene restituito l'hash dei campi passati in input:
	#cusomer_address: e' l'address del customer che vuole comprare un servizio
	#provider_address: address del fornitore di servizi (Relayer)
	#nonce: nonce associato ad un utente
	#amount: quantita' di token che un account desidera spendere per comprare un servizio
    def get_hash(self, customer_address, provider_address, nonce, amount):
        try:
            result = web3.solidityKeccak(['address', 'address', 'uint256', 'uint256'], [customer_address, provider_address, nonce, amount])
        except:
            raise Exception("Errore durante esecuzione get_hash")
        print(result)
        return result

	#Metodo necessario per ottenere la firma necessaria per una Meta-Transaction
    def get_signature(self, hash, private_key):
        print(hash)
        print(private_key)
        print(encode_defunct(hexstr=hash))
        try:
            result = Account.sign_message(encode_defunct(hexstr=hash), private_key=private_key)
        except:
            raise Exception("Errore durante esecuzione get_signature")
        print(result)
        return result.signature.hex()

	#Metodo che restituisce il nonce associato ad un account
    def get_address_nonce(self, customer_address):
        return self.contract.functions.nonceOf(customer_address).call()

	#Metodo invocato per inviare una Meta-Transaction per comprare un Servizio da un Provider
    def buy_service_with_metaTransaction(self, customer_address, provider_address, nonce, amount, signature):
        web3.eth.defaultAccount = provider_address
        print(web3.eth.defaultAccount)
        try:
            tx_hash = self.contract.functions.buyServiceWithMetaTransaction(customer_address, provider_address, nonce, amount, signature).transact()
            tx_receipt= web3.eth.waitForTransactionReceipt(tx_hash)
        except:
            raise Exception("Errore durante esecuzione buy_service_with_metaTransaction")
        print(tx_receipt)
        return toDict(tx_receipt)

	#Metodo invocato da parte di un Customer per comprare un servizio
    def buy_service(self, customer_address, provider_address, amount):
        web3.eth.defaultAccount = customer_address
        print(web3.eth.defaultAccount)
        try:
            tx_hash = self.contract.functions.buyService(amount, provider_address).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        except:
            raise Exception("Errore durante esecuzione buy_service")
        print(tx_receipt)
        return toDict(tx_receipt)

#https://github.com/ethereum/web3.py/issues/782
def toDict(dictToParse):
    # convert any 'AttributeDict' type found to 'dict'
    parsedDict = dict(dictToParse)
    for key, val in parsedDict.items():
        if 'list' in str(type(val)):
            parsedDict[key] = [_parseValue(x) for x in val]
        else:
            parsedDict[key] = _parseValue(val)
    return parsedDict

def _parseValue(val):
    # check for nested dict structures to iterate through
    if 'dict' in str(type(val)).lower():
        return toDict(val)
    # convert 'HexBytes' type to 'str'
    elif 'HexBytes' in str(type(val)):
        return val.hex()
    else:
        return val
