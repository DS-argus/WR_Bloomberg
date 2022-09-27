class YourNameIs:
    TICKER_NAME = {
    'GDP CYOY Index': 'GDP US Chained 2012 Dollars YoY SA',
    'EHPIUS Index': 'US Consumer Price Index (YoY%)',
    'EHUPUS Index': 'US Unemployment Rate (%)',
    'ECGQUS Q123 Index': 'US GDP Economic Forecast SA YoY%',
    'ECPIUS Q123 Index': 'US CPI Ecinomic Forecast (YoY%)',
    'ECUPUS Q123 Index': 'US Unemployment Rate Forecast (%)',

    'KOGDPQOQ Index': 'South Korea GDP at Chained 2015 Year Prices QoQ SA',
    'EHPIKR Index': 'South Korea Consumer Price Index (YoY%)',
    'EHUPKR Index': 'South Korea Unemployment Rate (%)',
    'ECGQKR Q123 Index': 'South Korea GDP Economic Forecast SA QoQ%',
    'ECPIKR Q123 Index': 'South Korea CPI Economic Forecast (YoY%)',
    'ECUPKR Q123 Index': 'South Korea Unemployment Rate Forecast (%)'






    }


# 종가와 30D implied volatility update에 사용됨 --> 다른 implied vol 필요하면 List 분리
TICKER_MACRO = [
    'GDP CYOY Index',
    'EHPIUS Index',
    'EHUPUS Index',
    'ECGQUS Q123 Index',
    'ECPIUS Q123 Index',
    'ECUPUS Q123 Index',

    'KOGDPQOQ Index',
    'EHPIKR Index',
    'EHUPKR Index',
    'ECGQKR Q123 Index',
    'ECPIKR Q123 Index',
    'ECUPKR Q123 Index'
]
