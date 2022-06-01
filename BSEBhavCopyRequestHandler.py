import urllib

import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

import MiscProductDataUtility
from InvalidReqException import InvalidReqException


class BSEBhavCopyRequestHandler:
    def __init__(self):
        self.newdf = None
        self.current_filename = MiscProductDataUtility.get_bse_bhavcopy_filename()
        self.download_file()

    def get_product_data(self, product):

        print("Retrieving details for the product [{}]".format(product))

        new_filename = MiscProductDataUtility.get_bse_bhavcopy_filename()
        if new_filename != self.current_filename:
            self.current_filename = new_filename
            self.download_file()

        product_detail = {"market": "BSE", "product": product}
        try:
            sd = self.newdf.loc[product]
            product_detail["name"] = sd["SC_NAME"].rstrip()
            product_detail["open"] = sd["OPEN"]
            product_detail["high"] = sd["HIGH"]
            product_detail["low"] = sd["LOW"]
            product_detail["close"] = sd["CLOSE"]
            product_detail["last"] = sd["LAST"]
        except KeyError:
            print("No detail found for the product [{}]".format(product))
            raise InvalidReqException('No Product Found')
        return product_detail

    def download_file(self):
        file_download_url = f'https://www.bseindia.com/download/BhavCopy/Equity/{self.current_filename}_CSV.ZIP'
        print("Downloading {}".format(file_download_url))
        page = urllib.request.Request(file_download_url, headers={'User-Agent': 'Mozilla/5.0'})
        url = urlopen(page)
        zipfile = ZipFile(BytesIO(url.read()))

        self.newdf = pd.read_csv(zipfile.open(f'{self.current_filename}.CSV'), index_col=0)
