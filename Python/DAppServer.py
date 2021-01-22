# using flask_restful
from flask import Flask, Response, request, jsonify
from flask_restful import Resource, Api
from BehaviouralToken import *

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

behaviouralToken = BehaviouralToken(ganache_url, abi, address)

# Metodo che restituisce il numero di Token associati ad un Customer
@app.route('/BehaviouralToken/Supply/<int:customer_index>', methods=['GET'])
def get_supply(customer_index):
    try:
        result = behaviouralToken.get_address_balance(customer_index)
    except Exception as ex:
        return jsonify({'Error': str(ex)}), 400
    return jsonify({'Address_Supply:': behaviouralToken.get_address_balance(customer_index)})

#Metodo che restituisce l'hash da firmare che verra' utilizzato nella Meta-Transaction
@app.route('/BehaviouralToken/hash', methods=['POST'])
def get_hash():
    data = request.get_json()
    customer_address = data['customer_address']
    provider_address = data['provider_address']
    nonce = data['nonce']
    amount = data['amount']
    try:
        hash = behaviouralToken.get_hash(customer_address, provider_address, nonce, amount)
    except Exception as ex:
        return jsonify({'Error': str(ex)}), 400
    return jsonify({'customer_address': customer_address,
                    'provider_address': provider_address,
                    'nonce': nonce,
                    'amount': amount,
                    'hash': hash.hex()})

#Metodo utilizzato per firmare un hash, che verra' utilizzato all'interno di una Meta-Transaction
@app.route('/BehaviouralToken/sign', methods=['POST'])
def get_sign():
    data = request.get_json()
    hash = data['hash']
    private_key = data['private_key']
    try:
        result = behaviouralToken.get_signature(hash=hash, private_key=private_key)
    except Exception as ex:
        return jsonify({'Error': str(ex)}), 400
    return jsonify({'Signature': result})

#Metodo utilizzato per ottenere il nonce associato ad un account
@app.route('/BehaviouralToken/Nonce/<customer_address>')
def get_nonce(customer_address):
    try:
        result = behaviouralToken.get_address_nonce(customer_address)
    except Exception as ex:
        return jsonify({'Error': str(ex)}), 400
    return jsonify({'Nonce': result})

#Metodo invocato tramite una Dapp per acquistare un servizio tramite Transaction
@app.route('/BehaviouralToken/BuyService', methods=['POST'])
def buy_service():
    data = request.get_json()
    customer_address = data['customer_address']
    provider_address = data['provider_address']
    amount = data['amount']
    try:
        result = behaviouralToken.buy_service(customer_address=customer_address, provider_address=provider_address, amount=amount)
    except Exception as ex:
        return jsonify({'Error': str(ex)}), 400

    return jsonify({'Transaction Receipt': result})

# driver function
if __name__ == '__main__':
    app.run(debug=True)