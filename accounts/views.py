from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView

# Create your views here.
class Login(LoginView):
  template_name='registration/login.html'