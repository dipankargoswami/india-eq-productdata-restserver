from flask import Flask, jsonify, request
from flask import render_template

from NSEBhavCopyRequestHandler import NSEBhavCopyRequestHandler
from InvalidReqException import InvalidReqException

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

nseBhavCopyReqHandler = NSEBhavCopyRequestHandler()


@app.errorhandler(InvalidReqException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


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

    if market.upper() == "NSE":
        resp = nseBhavCopyReqHandler.get_product_data(product)
        return jsonify(resp)
    else:
        raise InvalidReqException('Invalid Market specified in the request')
