# server.py
# %%  İmporting a some library for useable
import uuid
from flask import Flask, request, jsonify
from flask_smorest import abort
from db import items,stores

app = Flask(__name__)


# Store GET and POST İnformation
@app.route("/store", methods=["GET"])
def get_stores():
    return {"stores":list(stores.values())}

@app.route("/store", methods=["POST"])
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload"
        )
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(
            400,
            message="Store already exist",
        )
        
    store_id = uuid.uuid4().hex
    store = {**store_data,"id":store_id}
    stores[store_id] = store
    return store, 201

# İtems GET and POST İnformation

@app.route("/item", methods=["GET"])
def get_all_items():
    # return "Hello World"
    return {"items":list(items.values())}


@app.route("/item", methods=["POST"])
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id' and 'name' are include in JSON payload.",
        )
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(
                400,messagge = f"Item already exist"
            )
    if item_data["store_id"] not in stores:
        abort(404,message="Store not found.")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id":item_id}
    items[item_id] = item
    return item, 201


# Spesific store gettin code
@app.route("/store/<string:store_id>", methods=["GET"])
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404,message="Store not found.")


# Spesific item getting code
@app.route("/item/<string:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        
        return items[item_id]
    except KeyError:
        abort(404,message="İtem not found.")
        
        
        

## DELETE and PUT (update) methods

#### DELETE
# Item Delete
@app.route("/item/<string:item_id>", methods=["DELETE"])
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"Item deleted."}
    except KeyError:
        abort(404,message="Item not found.")
        
# Store Delete
@app.route("/store/<string:store_id>", methods=["DELETE"])
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"Store deleted."}
    except KeyError:
        abort(404,message="Store not found.")


#### PUT (update)

# Item Update
@app.route("/item/<string:item_id>", methods=["PUT"])
def update_item(item_id):
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id' are include in JSON payload.",
        )
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404,message="Item not found.")

# Store Update
@app.route("/store/<string:store_id>", methods=["PUT"])
def update_store(store_id):
    store_data = request.get_json()
    if ("name" not in store_data):
        abort(
            400,
            message="Bad request. Ensure 'name' is include in JSON payload.",
        )
    try:
        store = stores[store_id]
        store |= store_data
        return store
    except KeyError:
        abort(404,message="Store not found.")

# Run and debuging flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=8080)

# %%
