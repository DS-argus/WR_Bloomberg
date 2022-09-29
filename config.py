class YourNameIs:
    TICKER_NAME = {
        "SPX Index": "S&P500",
        "DJI Index": "DJIA30",
        "NDX Index": "NASDAQ",
        "SX5E Index": "EUROSTOXX50",
        "DAX Index": "DAX",
        "KOSPI Index": "KOSPI",
        "KOSPI2 Index": "KOSPI200",
        "SHSZ300 Index": "CSI300",
        "HSI Index": "HSI",
        "HSCEI Index": "HSCEI",
        "NKY Index": "NIKKEI225",
        "SP5QUKAP Index": "S&P500(Q)",
        "IX5QEKKP Index": "EUROSTOXX50(Q)",
        "SPXNKH Index": "S&P500(KRW)",
        "IX5MKHKP Index": "EUROSTOXX50(KRW)",
        "HSCEKRWH Index": "HSCEI(KRW)",
        "VIX Index": "VIX",

        "TSLA US Equity": "TESLA",
        "AMD US Equity": "AMD",

        # 11개/ call과 cd91는 전일 데이터가 다음날 조회되는지 확인( 토요일날 금요일껀 안보임)
        "KWCR1T BOKR Curncy": "KW CALL", # ALLQ에서 데이터소스 선택가능, 체크 2551과 일치하는 금리
        "KWCDC BOKR Curncy": "KW CD91", # CMPN과 동일, 공백없이 산출되는 것으로 보임
        "KWSWOF Curncy": "KW SWAP 6M",
        "KWSWOI Curncy": "KW SWAP 9M",
        "KWSWO1 Curncy": "KW SWAP 1Y",
        "KWSWO2 Curncy": "KW SWAP 2Y",
        "KWSWO3 Curncy": "KW SWAP 3Y",
        "KWSWO4 Curncy": "KW SWAP 4Y",
        "KWSWO5 Curncy": "KW SWAP 5Y",
        "KWSWO7 Curncy": "KW SWAP 7Y",
        "KWSWO10 Curncy": "KW SWAP 10Y",


        # for DLF report
        "USSW2 CURNCY": "US CMS 2Y",
        "USSW10 CURNCY": "US CMS 10Y",
        "USSW30 CURNCY": "US CMS 30Y",
        "US0003M Curncy": "LIBOR 3M"

    }


# 종가 update에 사용됨 --> 다른 implied vol 필요하면 List 분리
TICKER_IDXS = [
    "SPX Index",
    "DJI Index",
    "NDX Index",
    "SX5E Index",
    "DAX Index",
    "KOSPI Index",
    "KOSPI2 Index",
    "SHSZ300 Index",
    "HSI Index",
    "HSCEI Index",
    "NKY Index",
    "SP5QUKAP Index",
    "IX5QEKKP Index",
    "SPXNKH Index",
    "IX5MKHKP Index",
    "HSCEKRWH Index",
    "VIX Index"
]

TICKER_IVOL = [
    "SPX Index",
    "SX5E Index",
    "KOSPI2 Index",
    "SHSZ300 Index",
    "NKY Index",
    "HSCEI Index"
]

TICKER_STOCKS = [
    "TSLA US Equity",
    "AMD US Equity"
]

TICKER_RATES = [
    "KWCR1T BOKR Curncy",
    "KWCDC BOKR Curncy",
    "KWSWOF Curncy",
    "KWSWOI Curncy",
    "KWSWO1 Curncy",
    "KWSWO2 Curncy",
    "KWSWO3 Curncy",
    "KWSWO4 Curncy",
    "KWSWO5 Curncy",
    "KWSWO7 Curncy",
    "KWSWO10 Curncy",
    "US0003M Curncy"

]

TICKER_DLF = [
    "USSW2 CURNCY",
    "USSW10 CURNCY",
    "USSW30 CURNCY"
]