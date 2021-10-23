import json
from collections import namedtuple

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ReportDevModel, Build

fs = FileSystemStorage()


def customBuildDecoder(build):
    return namedtuple('X', build.keys())(*build.values())


@api_view(['POST'])
def SaveReport(request):
    if request.method == "POST":
        email = request.POST['email']
        typeForContext = request.POST['type']
        secondParam = request.POST['secondParam']
        buildJson = request.POST['build']
        logCsvFile = request.FILES['logCsvFile']
        urlLogCsv = ''
        listOfUrls = []

        for f in request.FILES.getlist('screenShot'):
            print(f.name)
            if f.content_type == 'image/png':
                nameScreenShot = fs.save(f.name, f)
                urlScreenShot = fs.url(nameScreenShot)
                listOfUrls.append(urlScreenShot)

        if logCsvFile.content_type == 'text/csv':
            nameLogCsvFile = fs.save(logCsvFile.name, logCsvFile)
            urlLogCsv = fs.url(nameLogCsvFile)

        buildObj = json.loads(buildJson, object_hook=customBuildDecoder)
        print('buildName:- ' + buildObj.buildName)
        build = Build(buildName=buildObj.buildName)
        build.save()
        ins = ReportDevModel(email=email, type=typeForContext, secondParam=secondParam,
                             screenShot=listOfUrls, logCsvFile=urlLogCsv, build=build)
        ins.full_clean()
        ins.save()
        send_mail(
            'Subject here',
            'Here is the message.',
            'srbverma10@gmail.com',
            [email],
            fail_silently=False,
        )

        if listOfUrls != '' and urlLogCsv != '':
            context = {
                'data': {
                    'email': email,
                    'type': typeForContext,
                    'secondParam': secondParam,
                    'screenShot': listOfUrls,
                    'logCsvFile': urlLogCsv,
                },
                'hasNext': False,
                'code': status.HTTP_201_CREATED
            }
        else:
            context = {
                'data': {
                    'email': email,
                    'type': type,
                    'secondParam': secondParam,
                    'screenShot': listOfUrls,
                    'logCsvFile': urlLogCsv,
                },
                'hasNext': False,
                'code': status.HTTP_412_PRECONDITION_FAILED
            }
        return Response(context, status=status.HTTP_200_OK)
