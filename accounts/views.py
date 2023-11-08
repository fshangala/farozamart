from django.shortcuts import render
from django.views.generic import View, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class Login(LoginView):
  template_name='registration/login.html'

class Logout(LogoutView):
  pass

class Register(FormView):
  template_name='registration/register.html'
  form_class=UserCreationForm

class Profile(View):
  template_name='accounts/profile.html'
  def get(self,request):
    context={}
    return render(request,self.template_name,context)