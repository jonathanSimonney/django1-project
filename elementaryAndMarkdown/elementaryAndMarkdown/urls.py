"""elementaryAndMarkdown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from . import views

from pastebinApi import views as apiViews
router = routers.DefaultRouter()
router.register(r'users', apiViews.UserViewSet)
router.register(r'groups', apiViews.GroupViewSet)

# print(include(router.urls))
# print(include('pastebinApi.urls'))

urlpatterns = [
    path('wolfram/', include('elementaryCellularAutomata.urls')),
    path('markdown/', include('pasteAsMarkdown.urls')),
    path('admin/', admin.site.urls),
    path('', views.home_display),
    path('api/', include(router.urls)),
    # path('api/', include('pastebinApi.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
