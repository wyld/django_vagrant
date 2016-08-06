from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from pages import views


urlpatterns = [
    url(r'^login/$', views.LoginPage.as_view(), name='login'),
    url(r'^$', views.DashboardPage.as_view(), name='dashboard'),
]

urlpatterns += staticfiles_urlpatterns()
