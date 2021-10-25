import simplejson as json
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.mail import EmailMultiAlternatives
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

        msg = EmailMultiAlternatives(body="...", from_email="srbverma10@gmail.com",
                                     to=[removeDoubleQuotes(email)])
        if removeDoubleQuotes(typeForContext) == "report":
            msg.subject = "Reported a bug"
            html_content = "<html><body><h2>We are glad to receive feedback.\n</h2><p>We strive to create a platform that ensures user comfort and proper management and we assure you to look into your report and get back to you as soon as possible.\n</p><b>Report:-</b><a>" + secondParam +"\n</a></body></html> "
        elif removeDoubleQuotes(typeForContext) == "suggestion":
            msg.subject = "Suggested an improvement"
            html_content = "<html><body><h2>We are glad to receive suggestions from you.\n</h2><p>We strive to create a platform that ensures user comfort and proper management and we assure you to look into your suggestion and get back to you as soon as possible.\n</p><b>Suggestions:-</b><a>" + secondParam +"\n</a></body></html> "
        else:
            msg.subject = "Asked questions"
            html_content = "<html><body><h2>We will be glad to answer you.\n</h2><p>We strive to create a platform that ensures user comfort and proper management and we assure you to look into your queries and get back to you as soon as possible.\n</p><b>Query:-</b><a>" + secondParam +"\n</a></body></html> "
        msg.attach_alternative(html_content, "text/html")
        for f in request.FILES.getlist('screenShot'):
            if f.content_type == 'image/png':
                msg.attach(f.name, f.read(), f.content_type)
                nameScreenShot = fs.save(f.name, f)
                urlScreenShot = fs.url(nameScreenShot)
                listOfUrls.append(urlScreenShot)

        if logCsvFile.content_type == 'text/csv':
            msg.attach(logCsvFile.name, logCsvFile.read(), logCsvFile.content_type)
            nameLogCsvFile = fs.save(logCsvFile.name, logCsvFile)
            urlLogCsv = fs.url(nameLogCsvFile)

        temp2 = json.loads(buildJson)
        build = Build(buildName=temp2['buildName'])
        build.save()

        ins = ReportDevModel(email=removeDoubleQuotes(email), type=removeDoubleQuotes(typeForContext),
                             secondParam=removeDoubleQuotes(secondParam),
                             screenShot=listOfUrls, logCsvFile=urlLogCsv, build=build)
        ins.save()
        msg.send(fail_silently=True)
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
