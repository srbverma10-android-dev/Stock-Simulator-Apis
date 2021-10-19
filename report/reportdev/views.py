from django.http import JsonResponse


def showTempDataDev(request):
    data = {
        'name': 'TEST REPORT SERVER'
    }
    return JsonResponse(data)
