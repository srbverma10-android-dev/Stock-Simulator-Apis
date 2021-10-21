from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage

from .models import ReportDevModel

fs = FileSystemStorage()


@api_view(['POST'])
def SaveReport(request):
    if request.method == "POST":
        email = request.POST['email']
        secondParam = request.POST['secondParam']
        screenShotFile = request.FILES['screenShot']
        logCsvFile = request.FILES['logCsvFile']
        urlScreenShot = ''
        urlLogCsv = ''
        if screenShotFile.content_type == 'image/png' and logCsvFile.content_type == 'text/csv':
            nameScreenShot = fs.save(screenShotFile.name, screenShotFile)
            urlScreenShot = fs.url(nameScreenShot)

            nameLogCsvFile = fs.save(logCsvFile.name, logCsvFile)
            urlLogCsv = fs.url(nameLogCsvFile)

            ins = ReportDevModel(email=email, secondParam=secondParam, screenShot=urlScreenShot, logCsvFile=urlLogCsv)
            ins.full_clean()
            ins.save()

        if urlScreenShot != '' and urlScreenShot != '':
            context = {
                'data': {
                    'email': email,
                    'secondParam': secondParam,
                    'screenShot': urlScreenShot,
                    'logCsvFile': urlLogCsv,
                },
                'hasNext': False,
                'code': status.HTTP_201_CREATED
            }
        else:
            context = {
                'data': {
                    'email': email,
                    'secondParam': secondParam,
                    'screenShot': urlScreenShot,
                    'logCsvFile': urlLogCsv,
                },
                'hasNext': False,
                'code': status.HTTP_412_PRECONDITION_FAILED
            }
        return Response(context, status=status.HTTP_200_OK)