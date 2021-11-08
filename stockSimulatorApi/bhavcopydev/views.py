from datetime import date, timedelta

from nsepy.history import get_price_list
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def getBhavCopy(request):
    if request.method == "GET":
        i = 0
        did_not_got_data = True
        while did_not_got_data:
            try:
                prices = get_price_list(dt=date.today() - timedelta(i))
                did_not_got_data = False
            except:
                i = i + 1
        try:
            prices = prices.drop(
                ['SERIES', 'ISIN', 'TIMESTAMP', 'HIGH', 'LOW', 'OPEN', 'LAST', 'TOTTRDQTY', 'TOTTRDVAL'], axis=1)
            listOfChange = []
            for index, row in prices.iterrows():
                change = (((row['CLOSE'] - row['PREVCLOSE']) * 100) / row['CLOSE'])
                listOfChange.append(change)
            prices['CHANGE'] = listOfChange
            context = {
                'top_gainer': prices.sort_values(by='CHANGE', ascending=False).head(20).drop(['TOTALTRADES', 'PREVCLOSE'], axis=1),
                'top_looser': prices.sort_values(by='CHANGE', ascending=True).head(20).drop(['TOTALTRADES', 'PREVCLOSE'], axis=1),
                'most_traded': prices.sort_values(by='TOTALTRADES', ascending=False).head(20).drop(['TOTALTRADES', 'PREVCLOSE'], axis=1),
                'hasNext': False,
                'code': status.HTTP_200_OK
            }
        except Exception as e:
            context = {
                'data': str(e),
                'hasNext': False,
                'code': status.HTTP_400_BAD_REQUEST
            }
        return Response(context, status=status.HTTP_200_OK)
