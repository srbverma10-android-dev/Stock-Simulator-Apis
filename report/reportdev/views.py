from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage

from .models import ReportDevModel


@api_view(['POST'])
def SaveReport(request):
    if request.method == "POST":
        print(request.data)
        email = request.POST['email']
        secondParam = request.POST['secondParam']
        screenShotFile = request.FILES['screenShot']

        fs = FileSystemStorage()
        name = fs.save(screenShotFile.name, screenShotFile)
        url = fs.url(name)

        ins = ReportDevModel(email=email, secondParam=secondParam, screenShot=url, logCsvFile='')
        ins.save()

        context = {
            'email': email,
            'secondParam': secondParam,
            'screenShot': url
        }
        return Response(context, status=status.HTTP_201_CREATED)
