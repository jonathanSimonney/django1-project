from django.urls import include, path
from rest_framework import routers
from . import views as apiViews

router = routers.DefaultRouter()
router.register(r'users', apiViews.UserViewSet)
router.register(r'groups', apiViews.GroupViewSet)


app_name = 'pastebinApi'
urlpatterns = [
    path('', include(router.urls)),
]
