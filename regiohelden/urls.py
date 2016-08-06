from django.conf.urls import include, url
from django.contrib import admin

from accounts.views import UserViewSet


from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/1.0/', include(router.urls)),

    url(r'^accounts/', include('allauth.urls')),
    url(r'', include('pages.urls')),
]