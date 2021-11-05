from rest_framework import status
from rest_framework.decorators import api_view
import yfinance as yahooFinance
from rest_framework.response import Response


@api_view(['POST'])
def returnDataOfIndices(request):
    if request.method == "POST":
        symbol = request.POST.get('symbol')
        indData = yahooFinance.Ticker(symbol)
        context = {
            'name': indData.info['shortName'],
            'symbol': indData.info['symbol'],
            'high': indData.info['dayLow'],
            'low': indData.info['dayHigh'],
            'graphData': indData.history(period="1d", interval="15m"),
            'current': indData.info['regularMarketPrice'],
            'hasNext': False,
            'code': status.HTTP_412_PRECONDITION_FAILED
        }
        return Response(context, status=status.HTTP_200_OK)
