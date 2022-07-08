import xbbg.blp

from dbms.DBmssql import MSSQL
from config import YourNameIs
import config as cfg

from xbbg import blp
import pandas as pd
import numpy as np
import xlwings as xw
import pymssql
import json

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def get_token(target:str) -> str:
    """
    Keys are saved in separate json file
        for extra security.
    :param target: type in the name for certain api
    :return: api key in str
    """
    loc = "./security/idpw.json"  # refract this file to add subtract info.
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()

    return dat['sql'][target]


class InsertData:
    def __init__(self, work:str='initial'):
        """
        :param work:
            if work == 'initial':
                initial state of inserting data
                the class will insert historical data from 2016 ~ present
            elif work == 'daily:
                data will be inserted daily
                the class will insert daily data
            elif work == 'amend':
                designated period of data will be inserted into the server

        """
        assert work in {'initial', 'daily', 'amend'}

        self.server = MSSQL.instance()
        self.server.login(
            id=get_token('id'),
            pw=get_token('pw')
        )
        self.ds, self.de = self.__get_dateinfo(work)

    def __get_dateinfo(self, status:str, dfmt:str= '%Y%m%d'):
        chg = False
        if status == 'initial':
            chg = True
            # Initialize Database
            date_end = datetime.today() - timedelta(days=2)
            date_start = date_end - relativedelta(years=4)

        elif status == 'daily':
            chg = True
            # Update Database Daily
            date_end, date_start = (
                datetime.today() - timedelta(days=2),
                datetime.today() - timedelta(days=2)
            )

        else:
            # Amend Database Occasionally
            print(
                "데이터베이스에 삽입할 시작날짜, 종료날짜를 적으세요 (yyyymmdd 형태)"
            )
            print(
                "ex) 20211201, 20211211"
            )
            dates = map(str, list(input().split(', ')))
            date_start, date_end = dates
        if chg is True:
            return date_start.strftime(dfmt), date_end.strftime(dfmt)
        else:
            return date_start, date_end

    # 삽입하고 싶은 데이터 종류에 해당하는 코드만 주석 해제하고 return 부분 변경한 뒤 run
    # 1. Index, 2. Implied volatility, 3. Interest rates는 매일 DB에 업데이트 중
    def get_bdh_data(self):

        ## 1. Index
        # print("Get Stock Indices")
        # r0 = self.__get_stockind()

        ## 2. Implied volatility
        # print("Get Implied Volatility")
        # r1 = self.__get_implied_vol()

        ## 3. Interest rates
        # print("Get Interest rates")
        # r2 = self.__get_interest_rates()

        # 4. 개별 주식
        print("Get Individual Stocks")
        r3 = self.__get_idvstock()

        return r3

    def __get_stockind(self):
        tkrs = cfg.TICKER_IDXS
        flds = ['PX_Last']

        res = blp.bdh(
            tkrs,
            flds,
            start_date=self.ds,
            end_date=self.de,
        )

        return res

    def __get_idvstock(self):
        tkrs = cfg.TICKER_STOCKS
        flds = ['PX_Last']

        res = blp.bdh(
            tkrs,
            flds,
            start_date=self.ds,
            end_date=self.de,
        )

        return res

    def __get_implied_vol(self):
        tkrs = cfg.TICKER_IDXS
        flds = ['30DAY_IMPVOL_100.0%MNY_DF']

        res = blp.bdh(
            tkrs,
            flds,
            start_date=self.ds,
            end_date=self.de,
        )

        return res

    def __get_interest_rates(self):
        tkrs = cfg.TICKER_RATES
        flds = ['PX_Last']

        res = blp.bdh(
            tkrs,
            flds,
            start_date=self.ds,
            end_date=self.de,
        )

        return res

    @staticmethod
    def create_insertible(dat:pd.DataFrame) -> list:
        yn = YourNameIs().TICKER_NAME
        result = list()
        for date in dat.index:
            seg = dat.loc[date]

            for types, val in zip(seg.index, seg):
                if np.isnan(val):
                    continue
                ins_ = (
                    date.strftime('%Y%m%d'),
                    yn[types[0]],
                    types[0],
                    types[1],
                    val
                )
                result.append(ins_)

        return result

    def run(self):
        print("Inserting Data from Bloomberg")
        dats = self.get_bdh_data()

        if isinstance(dats, tuple) is False:  # dataframe 1개일 때
            insert_ = self.create_insertible(dats)

            duples = 0
            for line in insert_:
                try:
                    self.server.insert_row(
                        table_name='price',
                        schema='drv',
                        database='WSOL',
                        col_=['DATE', 'NAME', 'TICKER', 'TYPE', 'VALUE'],
                        rows_=[line]
                    )

                except pymssql._pymssql.IntegrityError as e:
                    print(f"{duples + 1}. {line[0]} & {line[1]} 은 이미 있는 정보입니다")
                    duples += 1
                    continue

        else:   # dataframe 2개 이상일 때
            for dfs in dats:
                insert_ = self.create_insertible(dfs)

                duples = 0
                for line in insert_:
                    try:
                        self.server.insert_row(
                            table_name='price',
                            schema='drv',
                            database='WSOL',
                            col_=['DATE', 'NAME', 'TICKER', 'TYPE', 'VALUE'],
                            rows_=[line]
                        )

                    except pymssql._pymssql.IntegrityError as e:
                        print(f"{duples + 1}. {line[0]} & {line[1]} 은 이미 있는 정보입니다")
                        duples += 1
                        continue



if __name__ == '__main__':
    mrd = InsertData(work='amend')
    mrd.run()
