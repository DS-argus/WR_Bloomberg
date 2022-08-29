import config as cfg
from xbbg import blp
import xlwings as xw
import pandas as pd

import numpy as np

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
    start = date(2010, 1, 1)
    to = date.today()
    tickers = ['ECGQUS Q123 Index']
    fields = ['PX_Last']
    df = getbldata(tickers, fields, start, to)
    xw.view(df)
    print(df)

