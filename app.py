from flask import Flask, jsonify, request
from flask import render_template


app = Flask(__name__)

resp = {"A": 1, "B": "Hi"}

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/api/v1/bhavcopy/')
def get_all():
    market = ""
    product = ""

    if 'market' not in request.args or 'product' not in request.args:
        return "Error: No market or product field provided. Please specify a market and a product."
    if 'product' in request.args:
        market = request.args['market']
        product = request.args['product']

    resp["market"] = market
    resp["product"] = product
    return jsonify(resp)
