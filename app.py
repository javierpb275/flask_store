from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]


@app.get("/api/stores")
def get_stores():
    return {"stores": stores}, 200


@app.get("/api/stores/<string:store_name>")
def get_store(store_name):
    for store in stores:
        if store["name"] == store_name:
            return store, 200
    return {"message": "Store Not Found"}, 404


@app.post("/api/stores")
def create_store():
    body = request.get_json()
    new_store = {"name": body["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/api/items/<string:store_name>")
def add_item(store_name):
    body = request.get_json()
    for store in stores:
        if store["name"] == store_name:
            new_item = {
                "name": body["name"],
                "price": body["price"]
            }
            store["items"].append(new_item)
            return store, 201
    return {"message": "Store Not Found"}, 404


app.run()
