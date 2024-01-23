from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.conf import settings
from accounts import forms
from django.contrib import messages

# Create your views here.
class Login(View):
  template_name='registration/login.html'
  def get(self,request):
    context={
      'get_parameters':request.GET,
      'form':forms.LoginForm()
    }
    messages.info(request,'Please login or sign up')
    return render(request,self.template_name,context)
  def post(self,request):
    context={
      'get_parameters':request.GET
    }
    nextPage = request.GET.get('next')
    if not nextPage:
      nextPage = reverse('home:home')
    form = forms.LoginForm(data=request.POST)
    if form.is_valid():
      user = authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
      if user is not None:
        login(request,user)
        messages.success(request,'Login successful!')
        return redirect(nextPage)
      else:
        messages.error(request, 'invalid credentials!')
    context['form']=form
    return render(request,self.template_name,context)

class Logout(LoginRequiredMixin,LogoutView):
  pass

class Register(View):
  template_name='registration/register.html'
  def get(self,request):
    form = forms.RegistrationForm()
    context={
      'form':form,
      'get_parameters':request.GET
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.RegistrationForm(data=request.POST)
    
    nextPage = request.GET.get('next')
    if not nextPage:
      nextPage = reverse('home:home')
    if form.is_valid():
      form.save()
      messages.success(request,'Registration successful!')
      user = authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
      if user is not None:
        login(request,user)
        messages.success(request,'Login successful!')
        return redirect(nextPage)
      else:
        messages.error(request, 'invalid credentials!')
    
    context={
      'form':form,
      'get_parameters':request.GET
    }
    return render(request,self.template_name,context)

class Profile(LoginRequiredMixin,View):
  template_name='accounts/profile.html'
  def get(self,request):
    context={}
    picture_form=forms.UpdatePictureForm(user=request.user)
    context['picture_form']=picture_form
    return render(request,self.template_name,context)

class EditProfile(LoginRequiredMixin,View):
  template_name='accounts/edit-profile.html'

  def get(self,request):
    context={
      'form':forms.EditProfileForm(user=request.user)
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.EditProfileForm(user=request.user,data=request.POST)
    context={
      'form':form
    }
    if form.is_valid():
      form.save()
      messages.success(request,'Profile successfully updated!')
      return redirect(reverse('accounts:profile'))
    return render(request,self.template_name,context)

class UpdateProfilePicture(LoginRequiredMixin,View):
  template_name='accounts/update-picture.html'
  def get(self,request):
    context={}
    form=forms.UpdatePictureForm(user=request.user)
    context['form']=form
    return render(request,self.template_name,context)
  def post(self,request):
    context={}
    form=forms.UpdatePictureForm(user=request.user,data=request.POST,files=request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request,'Profile picture successfully updated!')
      return redirect(reverse('accounts:profile'))
    context['form']=form
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

class BecomeReseller(LoginRequiredMixin,View):
  def get(self,request):
    form = forms.BecomeResellerForm()
    form.save()
    messages.success(request,'You are now a reseller!')
    context={
      'form':form
    }
    return redirect(reverse('dashboard:dashboard'))
    