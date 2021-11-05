from rest_framework import status
from rest_framework.decorators import api_view
import yfinance as yahooFinance
from rest_framework.response import Response


@api_view(['POST'])
def returnDataOfIndices(request):
    if request.method == "POST":
        symbol = request.POST.get('symbol')
        indData = yahooFinance.Ticker(symbol)
        # print(indData.history(period="1d", interval="15m"))
        context = {
            'name': indData.info['shortName'],
            'symbol': indData.info['symbol'],
            'high': indData.info['regularMarketDayHigh'],
            'low': indData.info['regularMarketDayLow'],
            'graphData': indData.history(period="1d", interval="15m"),
            'hasNext': False,
            'code': status.HTTP_412_PRECONDITION_FAILED
        }
        return Response(context, status=status.HTTP_200_OK)
