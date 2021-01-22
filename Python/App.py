# using flask_restful
from flask import Flask, Response, request, jsonify
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError
from BehaviouralToken import *

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

BehaviouralToken = BehaviouralToken(ganache_url, abi, address)

@app.route('/BehaviouralToken/AccountPassword', methods=['GET'])
def get_account_password():
    return jsonify({'username': 'password'})

@app.route('/BehaviouralToken/TotalSupply/', methods=['GET'])
def get_total_supply():
    try:
        result = BehaviouralToken.get_total_supply()
    except Exception as ex:
        return jsonify({'Error': str(ex)}), 400
    return jsonify({'Total_Supply:': result})

@app.route('/BehaviouralToken/ABI', methods=['GET'])
def get_abi():
    try:
        result = BehaviouralToken.get_abi()
    except Exception as ex:
        return jsonify({'Error': str(ex)}), 400
    return jsonify({'ABI:': result})

#Metodo invocato tramite una Dapp per acquistare un servizio tramite Meta-Transaction
@app.route('/BehaviouralToken/BuyServiceWithMetaTransaction', methods=['POST'])
def buy_service_with_meta_transaction():
    data = request.get_json()
    customer_address = data['customer_address']
    provider_address = data['provider_address']
    nonce = data['nonce']
    amount = data['amount']
    signature = data['signature']
    try:
        result = BehaviouralToken.buy_service_with_metaTransaction(customer_address=customer_address, provider_address=provider_address, nonce=nonce, amount=amount, signature=signature)
    except Exception as ex:
        return jsonify({'Error': str(ex)}), 400
    return jsonify({'Transaction Receipt': result}), 200

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Hello(Resource):
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
        return jsonify({'message': 'Hello World...!!!'})

        # Corresponds to POST request

    def post(self):
        data = request.get_json()  # status code
        return jsonify({'data': data}), 200


api.add_resource(Hello, '/')

# driver function
if __name__ == '__main__':
    app.run(debug=True)