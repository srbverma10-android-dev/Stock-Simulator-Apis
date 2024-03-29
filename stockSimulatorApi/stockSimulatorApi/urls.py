"""report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from reportdev.views import SaveReport
from reportprod.views import showTempDataProd
from indicesdev.views import returnDataOfIndices
from bhavcopydev.views import getBhavCopy
from detailsdev.views import getDetails

from . import settings
TEST = 'dev/'
PROD = 'v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(TEST+'report', SaveReport, name='SaveReport'),
    path(TEST+'indices', returnDataOfIndices, name='returnDataOfIndices'),
    path(TEST+'bhavcopy', getBhavCopy, name='getBhavCopy'),
    path(TEST+'details', getDetails, name='getDetails'),
    path(PROD+'report', showTempDataProd)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
