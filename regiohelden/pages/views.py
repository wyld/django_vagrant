from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginPage(TemplateView):
    template_name = 'pages/login.html'


class DashboardPage(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboard.html'
