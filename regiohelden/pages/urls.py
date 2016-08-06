from django.conf.urls import url
from pages import views


urlpatterns = [
    url(r'^login/$', views.LoginPage.as_view(), name='login'),
    url(r'^$', views.DashboardPage.as_view(), name='dashboard'),
]