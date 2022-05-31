from flask import Flask, jsonify, request
from flask import render_template

from NSEBhavCopyRequestHandler import NSEBhavCopyRequestHandler
from BSEBhavCopyRequestHandler import BSEBhavCopyRequestHandler
from InvalidReqException import InvalidReqException

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

nseBhavCopyReqHandler = NSEBhavCopyRequestHandler()
bseBhavCopyReqHandler = BSEBhavCopyRequestHandler()


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

    if 'exchange' not in request.args or 'stock' not in request.args:
        return "Error: No exchange or stock field provided. Please specify a market and a product."
    market = request.args['exchange']
    product = request.args['stock']

    if market.upper() == "NSE":
        resp = nseBhavCopyReqHandler.get_product_data(product.upper())
        return jsonify(resp)
    elif market.upper() == "BSE":
        if not product.isnumeric():
            raise InvalidReqException('Must provide numeric scripcode')
        resp = bseBhavCopyReqHandler.get_product_data(int(product))
        return jsonify(resp)
    else:
        raise InvalidReqException('Invalid Market specified in the request')
