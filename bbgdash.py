import config as cfg

from dbms.DBmssql import MSSQL
from util.token import get_token

import pandas as pd
import numpy as np

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class MReportDataExtract:
    def __init__(self):
        self.server = MSSQL.instance()
        self.server.login(
            id=get_token('id'),
            pw=get_token('pw')
        )

    @staticmethod
    def rpt_extract_date(target_year:int, target_month:int, type_:str):
        date_end = datetime(target_year, target_month + 1, 1)
        date_end = date_end - timedelta(days=1)
        if type_ == '5months':
            raise NotImplementedError

        elif type_ == '3years':
            date_start = date_end - relativedelta(years=3)

            return (date_start.strftime('%Y%m%d'),
                    date_end.strftime('%Y%m%d'))


    def mnt_data(self):
        print("조회하고자 하는 연도와 월을 입력하세요")
        print("연도?")
        y = int(input())
        print("달?")
        m = int(input())

        ds, de = self.rpt_extract_date(y, m, type_='3years')
        condition = f'date >= {ds} and date <= {de}'
        col = ['date', 'ind_name', 'ind_bbg', 'typ', 'value']
        r = self.server.select_db(
            database="WSOL",
            schema="dbo",
            table="bbgind",
            column=col,
            condition=condition
        )

        r = pd.DataFrame(r, columns=col)
        r = r.set_index('date')

        r = r.pivot_table(
            values='value',
            index='date',
            columns='ind_bbg'
        )
        return r.sort_index()


if __name__ == '__main__':
    blm = MReportDataExtract()
    g = blm.mnt_data()
    print(g)