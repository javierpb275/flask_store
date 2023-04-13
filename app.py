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
    return {"stores": stores}


@app.post("/api/stores")
def create_store():
    body = request.get_json()
    new_store = {"name": body["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


app.run()
