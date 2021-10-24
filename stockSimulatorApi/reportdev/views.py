import simplejson as json
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ReportDevModel, Build

fs = FileSystemStorage()


def removeDoubleQuotes(string):
    return string[1:(len(string)-1)]


@api_view(['POST'])
def SaveReport(request):
    if request.method == "POST":
        email = request.POST.get('email')
        typeForContext = request.POST.get('type')
        secondParam = request.POST.get('secondParam')
        build = request.POST['build']
        logCsvFile = request.FILES['logCsvFile']

        temp = json.loads(build)
        buildJson = json.dumps(temp['nameValuePairs'])

        urlLogCsv = ''
        listOfUrls = []

        for f in request.FILES.getlist('screenShot'):
            if f.content_type == 'image/png':
                nameScreenShot = fs.save(f.name, f)
                urlScreenShot = fs.url(nameScreenShot)
                listOfUrls.append(urlScreenShot)

        if logCsvFile.content_type == 'text/csv':
            nameLogCsvFile = fs.save(logCsvFile.name, logCsvFile)
            urlLogCsv = fs.url(nameLogCsvFile)

        temp2 = json.loads(buildJson)
        build = Build(buildName=temp2['buildName'])
        build.save()

        ins = ReportDevModel(email=removeDoubleQuotes(email), type=removeDoubleQuotes(typeForContext),
                             secondParam=removeDoubleQuotes(secondParam),
                             screenShot=listOfUrls, logCsvFile=removeDoubleQuotes(urlLogCsv), build=build)
        ins.save()
        send_mail(
            'Subject here',
            'Here is the message.',
            'srbverma10@gmail.com',
            [removeDoubleQuotes(email)],
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
                    'build': temp2
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
                    'build': temp2
                },
                'hasNext': False,
                'code': status.HTTP_412_PRECONDITION_FAILED
            }
        return Response(context, status=status.HTTP_200_OK)
