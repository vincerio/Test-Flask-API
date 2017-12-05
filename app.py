# virtaulenv [folder] --python=python3.6

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
# from security.py
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, StoreList
#items = []

# JWT = JSON Web Token -> for authentication

# Flask_resetful make a flask could response to request without app.route :)
# Every Resource must be a class

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "iyo" # This would to be secret in Production
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity) # I have to identity my user in my app to work with this jwt T^T
# jwt will create new endpoint = /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__": # to prevent python run the below statement when import this file from other file
	from db import db
	db.init_app(app)
	app.run(port=6969, debug=True)

# It is a good example to design the endpoints first before start working...
# JSON = 'String of dictionary T^T'
# JSON always use double quote
# JSON always start with dictionary... not a list T^T
# I'm skip too many inportant principle T^T

"""
stores = [
	{
		'name' : 'iyo store',
		'items' : [
			{
				'name' : 'First item',
				'price' : 1.00
			}
		]
	}
]

# stores is a list of dictionary

# POST /store data: {name:}
# GET /store/<string:name>
# GET /store
# POST /store/<string:name>/item {name:,price:}
# GET /store/<string:name>/item

@app.route('/store',methods=['POST'])
def create_store():
	request_data = request.get_json() # browser send a JSON data to server
	new_store = {
		'name' : request_data['name'],
		'items' : []
	}
	stores.append(new_store)
	return jsonify(new_store)

@app.route('/store/<string:name>')
def get_store(name):
	# Iterate over store if the name matches, return it
	# If none match, return an error message
	for store in stores:
		if store['name'] == name:
			return jsonify(store)
	return jsonify({'error' : 'store not found'})

@app.route('/store')
def get_stores():
	# JSON is dictionary
	return jsonify({ 'stores' : stores })

@app.route('/store/<string:name>/item',methods=['POST'])
def create_item_in_store(name):
	for store in stores:
		request_data = request.get_json()
		if store['name'] == name:
			new_item = {
				'name' : request_data['name'],
				'price' : request_data['price']
			}
			store['items'].append(new_item)
			return jsonify(new_item)
	return jsonify({ 'error' : 'store not found' })

@app.route('/store/<string:name>/item')
def get_item_in_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify(store['items'])
"""
