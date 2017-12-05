from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        else:
            return {"error":"Store not found"},404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"error":"Store with this name {} is already exist".format(name)}, 400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
                return store.json(), 201
            except:
                return {"error":"An error occur"}, 500

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return "Store deleted", 200

class StoreList(Resource):
    def get(self):
        return {"stores" : [ store.json() for store in StoreModel.query.all() ]}
