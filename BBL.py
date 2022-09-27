import config as cfg
from xbbg import blp
import xlwings as xw
import pandas as pd

import numpy as np

from datetime import date


def getbldata(tkrs, flds, start_date, end_date, per='D'):

    res = blp.bdh(
        tkrs,
        flds,
        start_date=start_date,
        end_date=end_date,
        Per=per
    )

    return res



if __name__ == "__main__":
    start = date(2022, 9, 5)
    to = date.today()
    tickers = ['US0003M Curncy']
    fields = ['PX_Last']
    df = getbldata(tickers, fields, start, to, 'M')
    print(df)

