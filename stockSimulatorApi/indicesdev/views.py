from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.decorators import api_view
import yfinance as yahooFinance
from rest_framework.response import Response
from datetime import date

Dict = {'^NSEI': 0, '^CNX100': 1, '^NSMIDCP': 2, '^NSEMDCP50': 3, '^NSEBANK': 4, '^CNXAUTO': 5, '^CNXIT': 6,
        'NIFTY_HEALTHCARE.NS': 7}


@api_view(['POST'])
def returnDataOfIndices(request):
    if request.method == "POST":
        symbol = request.POST.get('symbol')
        indData = yahooFinance.Ticker(symbol)
        i = 0
        indDataGraph = yahooFinance.download(symbol, start=(datetime.now() - timedelta(i)).strftime('%Y-%m-%d'),
                                             end=date.today(), interval="1m")
        isEmpty = indDataGraph["Close"].empty
        while isEmpty and i < 10:
            indDataGraph = yahooFinance.download(symbol, start=(datetime.now() - timedelta(i)).strftime('%Y-%m-%d'),
                                                 end=date.today(), interval="1m")
            i = i + 1
            isEmpty = indDataGraph["Close"].empty
        change = 100 - ((indData.info['previousClose'] * 100) / indData.info['regularMarketPrice'])
        context = {
            'uid': Dict[indData.info['symbol']],
            'name': indData.info['shortName'],
            'symbol': indData.info['symbol'],
            'high': indData.info['dayLow'],
            'low': indData.info['dayHigh'],
            'change': change,
            'current': indData.info['regularMarketPrice'],
            'graphData': indDataGraph["Close"],
            'hasNext': False,
            'code': status.HTTP_200_OK
        }
        return Response(context, status=status.HTTP_200_OK)
