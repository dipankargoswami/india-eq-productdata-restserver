import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

import MiscProductDataUtility
from InvalidReqException import InvalidReqException


class NSEBhavCopyRequestHandler:
    def __init__(self):
        self.newdf = None
        self.current_filename = MiscProductDataUtility.get_nse_bhavcopy_filename()
        self.download_file()

    def get_product_data(self, product):

        print("Retrieving details for the product [{}]".format(product))

        new_filename = MiscProductDataUtility.get_nse_bhavcopy_filename()
        if new_filename != self.current_filename:
            self.current_filename = new_filename
            self.download_file()

        product_detail = {"product": product}
        try:
            sd = self.newdf.loc[product]
            product_detail["open"] = sd["OPEN"]
            product_detail["high"] = sd["HIGH"]
            product_detail["low"] = sd["LOW"]
            product_detail["close"] = sd["CLOSE"]
            product_detail["last"] = sd["LAST"]
        except KeyError:
            print("No detail found for the product [{}]".format(product))
            raise InvalidReqException('No Product Found')
        resp = {"NSE": product_detail}
        return resp

    def download_file(self):
        month = self.current_filename[4:7]
        year = self.current_filename[7:11]
        file_download_url = f'https://archives.nseindia.com/content/historical/EQUITIES/' \
                            f'{year}/{month}/{self.current_filename}.zip'
        print("Downloading {}".format(file_download_url))
        url = urlopen(file_download_url)
        zipfile = ZipFile(BytesIO(url.read()))

        cereal_df = pd.read_csv(zipfile.open(self.current_filename), index_col=0)
        self.newdf = cereal_df.loc[(cereal_df.SERIES == "EQ")]
