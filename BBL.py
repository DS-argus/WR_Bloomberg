import config as cfg
from xbbg import blp
import xlwings as xw

from datetime import date


def getbldata(tkrs, flds, start_date, end_date):

    res = blp.bdh(
        tkrs,
        flds,
        start_date=start_date,
        end_date=end_date,
    )

    return res



if __name__ == "__main__":
    start = date(2020, 1, 1)
    to = date(2022, 6, 3)
    tickers = ['KWCDC BOKR Curncy', 'KWDCD KSDA Curncy', 'KWCDC LAST Curncy',
               'KWCDC CMPN Curncy']
    fields = ['PX_Last']
    print(getbldata(tickers, fields, start, to))

    xw.view(getbldata(tickers, fields, start, to))
