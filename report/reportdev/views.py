from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serialize import ReportSerialize


@api_view(['POST'])
def SaveReport(request):
    if request.method == "POST":
        serialize = ReportSerialize(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
