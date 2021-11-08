from datetime import date, timedelta

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from nsepy.history import get_price_list


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
            prices = prices.drop(['SERIES', 'ISIN', 'TIMESTAMP'], axis=1)
            context = {
                'data': prices,
                'hasNext': False,
                'code': status.HTTP_200_OK
            }
        except:
            context = {
                'data': "",
                'hasNext': False,
                'code': status.HTTP_200_OK
            }
        return Response(context, status=status.HTTP_200_OK)
