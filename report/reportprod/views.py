from django.http import JsonResponse


def showTempDataProd(request):
    data = {
        'name': 'PRODUCTION REPORT SERVER'
    }
    return JsonResponse(data)
