from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from accounts import forms

# Create your views here.
class Login(LoginView):
  template_name='registration/login.html'

class Logout(LoginRequiredMixin,LogoutView):
  pass

class Register(View):
  template_name='registration/register.html'
  def get(self,request):
    form = forms.RegistrationForm()
    context={
      'form':form
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.RegistrationForm(data=request.POST)
    
    if form.is_valid():
      form.save()
      return redirect(reverse('accounts:login'))
    
    context={
      'form':form
    }
    return render(request,self.template_name,context)

class Profile(LoginRequiredMixin,View):
  template_name='accounts/profile.html'
  def get(self,request):
    context={}
    return render(request,self.template_name,context)

class EditProfile(LoginRequiredMixin,View):
  template_name='accounts/edit-profile.html'

  def get(self,request):
    context={}
    return render(request,self.template_name,context)

class BecomeSeller(LoginRequiredMixin,UserPassesTestMixin,View):
  template_name='accounts/become-seller.html'
  
  def test_func(self):
    return not self.request.user.profile.is_seller
  
  def get(self,request):
    form = forms.BecomeSellerForm()
    context={
      'form':form
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.BecomeSellerForm(data=request.POST)
    if form.is_valid():
      form.save(request.user)
      return redirect(reverse('dashboard:dashboard'))
    context={
      'form':form
    }
    return render(request,self.template_name,context)