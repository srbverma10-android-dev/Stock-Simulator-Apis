from datetime import date, timedelta
from nsepy import get_history
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def getDetails(request):
    if request.method == "POST":
        symbol = request.POST.get('symbol')
        index = request.POST.get('index')
        i = 0
        did_not_got_data = True
        while did_not_got_data:
            if index == "True":
                data = get_history(symbol=symbol,
                                   start=date.today() - timedelta(i),
                                   end=date.today(),
                                   index=True)
            else:
                data = get_history(symbol=symbol,
                                   start=date.today() - timedelta(i),
                                   end=date.today(),
                                   index=False)
            if data.shape[0] == 0:
                i = i + 1
            else:
                did_not_got_data = False
        context = {
            'data': data,
            'hasNext': False,
            'code': status.HTTP_200_OK
        }
        return Response(context, status=status.HTTP_200_OK)
