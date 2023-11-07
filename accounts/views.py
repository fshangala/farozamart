from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
class Login(LoginView):
  template_name='registration/login.html'

class Logout(LogoutView):
  pass

class Profile(View):
  template_name='accounts/profile.html'
  def get(self,request):
    context={}
    return render(request,self.template_name,context)