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

from datetime import date, datetime, timedelta
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


def get_hist_data_from_sql(from_: date,
                           to_: date,
                           idxs: list,
                           type: str = "o",
                           ffill: bool = True) -> pd.DataFrame:

    server = MSSQL.instance()
    server.login(
        id=get_token('id'),
        pw=get_token('pw')
    )

    # 시작일이 공휴일이면 ffill 할 수가 없어 넉넉하게 과거 10일 데이터 불러와서 출력은 시작일부터
    # DB에 2000/01/04 부터 들어가 있어 CSI300은 처음엔 NaN으로 나옴
    if from_ < date(2000, 1, 4):
        from_ = date(2000, 1, 4)

    from_ = from_ - timedelta(10)

    # query 조건
    cond_name = [f"NAME = '{idx}'" for idx in idxs]
    cond_name = " or ".join(cond_name)

    cond = [
        f"DATE >= '{from_.strftime('%Y%m%d')}'",
        f"DATE <= '{to_.strftime('%Y%m%d')}'",
        f"({cond_name})"
    ]

    cond = ' and '.join(cond)

    # data 불러오기
    col = ['DATE', 'NAME', 'TICKER', 'TYPE', 'VALUE']
    d = server.select_db(
        database='WSOL',
        schema='dbo',
        table='drvprc',
        column=col,
        condition=cond
    )

    # data 가공
    d = pd.DataFrame(d)
    d = pd.pivot_table(d, values=d.columns[4], index=d.columns[0], columns=d.columns[1])
    d.index = pd.Series([datetime.strptime(day, "%Y%m%d") for day in d.index])
    d.index.name = "Date"

    # DB에서 받아온 index는 datetime 형태, date만 있는 object 타입으로 바꿔줌(class_els와의 호환 위해)
    d.index = d.index.date

    # type = 'w'인 경우도 db에 있는 날까지 나오도록
    to_ = d.index[-1]

    # 공휴일, 휴일제외 original version
    if type == "o":
        if ffill is True:
            d.fillna(method='ffill', inplace=True)
            return d.iloc[10:, :]
        else:
            return d.iloc[10:, :]

    # 모든 날 추가한 version
    elif type == "w":
        dt_rng = pd.date_range(from_, to_).date
        d_weekend = pd.DataFrame(index=dt_rng, columns=idxs)

        for day in d.index:
            try:
                d_weekend.loc[day] = d.loc[day]

            except KeyError as e:
                d_weekend.loc[day] = [np.nan] * len(idxs)

        if ffill is True:
            d_weekend.fillna(method='ffill', inplace=True)

            return d_weekend.iloc[10:, :]
        else:
            return d_weekend.iloc[10:, :]


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
                datetime.today() - timedelta(days=1),
                datetime.today() - timedelta(days=5)
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

    def get_bdh_data(self) -> pd.DataFrame:

        print("Get Stock Indices")
        r0 = self.__get_stockind()

        return r0

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

    @staticmethod
    def create_insertible(dat:pd.DataFrame):
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

def Create_excel():

    def get_data() -> pd.DataFrame:
        start = date(2018, 1, 1)
        end = date.today() - timedelta(days=1)

        underlyings = [
            'KOSPI200', 'HSCEI', 'HSI', 'NIKKEI225', 'S&P500', 'EUROSTOXX50', 'CSI300',
            'S&P500(Q)', 'EUROSTOXX50(Q)',
            'S&P500(KRW)', 'EUROSTOXX50(KRW)', 'HSCEI(KRW)'
        ]

        df = get_hist_data_from_sql(start, end, underlyings, type='w', ffill=True)

        return df

    def update_excel(dataframe: pd.DataFrame):
        with xw.App(visible=False)as app:
            ex = xw.Book(r'\\172.31.1.222\GlobalD\Derivatives\DB 종가데이터\DB 종가데이터.xlsx')
            sh1 = ex.sheets['DB종가']

            sh1.range("A1:M8000").clear_contents()

            sh1[0, 0].options(index=True).value = dataframe

            ex.save()
            ex.close()

    df = get_data()
    update_excel(df)

    return


if __name__ == '__main__':
    # 넉넉하게 5일전부터 어제까지의 데이터 받는 걸로 daily 설정. 중복PK는 알아서 걸러지니깐
    indat = InsertData(work='daily')
    indat.run()

    Create_excel()
