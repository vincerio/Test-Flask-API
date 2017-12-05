from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank")
    parser.add_argument('store_id',type=int,required=True,help="Every item need a store ID")

    @jwt_required()
    def get(self,name):
        # retrive from object in memory
        # item = next(filter(lambda x: x['name'] == name,items), None)
        # return {'item' : item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return { "message" : "item not found" }, 404

    def post(self,name):
        # some conflict in resource URL and request_data about name T^T
        #if next(filter(lambda x: x['name'] == name,items), None):
        #    return {'error' : 'item with this name {} is already exist'.format(name) },400
        if ItemModel.find_by_name(name):
            return {'error' : 'item with this name {} is already exist'.format(name) },400

        data = Item.parser.parse_args()

        #request_data = request.get_json(force=True) # If the request is not JSON it will throw the error
        # force = True -> doesn't care about applicate-type JSON header
        # somehow dangerous because it just care about processing the text but ignore the header ^^''
        item = ItemModel(name, **data)

        #items.append(item)
        try:
            item.save_to_db()
        except Exception as e:
            print (str(e))
            return { "error" : "unknown error occur T^T" }, 500

        return item.json(), 201 # 201 is for create!
        # 202 is for accept... but delay in creation
        # accept the request but not working on it yet!
        #pass

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message" : "Item deleted"}

    def put(self,name):
        data = Item.parser.parse_args() #request.get_json()
        #item = next(filter(lambda x: x['name'] == name,items), None)
        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {"error":"An error occured inserting an item T__T"}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {"error":"An error occured inserting an item T__T"}, 500
        item.save_to_db()

        return item.json(), 200

class Items(Resource):
    def get(self):
        return {'items' : [ item.json() for item in ItemModel.query.all() ]} # More Pythonic and more faster ^^
        # return {'items' : list(map(lambda x: x.json(), ItemModel.query.all())) }
