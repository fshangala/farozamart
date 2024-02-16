from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.conf import settings
from accounts import forms
from django.contrib import messages
from dashboard.function import saveOption, getOptions
import random
from django.core.mail import send_mail

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

class VerifyUserEmail(LoginRequiredMixin,View):
  template_name='accounts/verify-user-email.html'
  def get(self,request):
    context={
      'form':forms.VerifyUserEmailForm(user=request.user)
    }
    otp=random.randint(1000,9999)
    options=getOptions()
    send_mail(
        f"{options['name']} - Email verification",
        f"{otp} is your email verification code.",
        options['site_mail'],
        [request.user.email]
    )
    messages.info(request,f"A new verification code has been sent to your email address {request.user.email}. Use it to verify your email.")
    saveOption('otp',otp)
    return render(request,self.template_name,context)
  def post(self,request):
    context={}
    form = forms.VerifyUserEmailForm(user=request.user,data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Email successfully verified!')
      return redirect(reverse('accounts:profile'))
    context['form']=form
    return render(request,self.template_name,context)

class ForgotPassword(View):
  template_name='registration/forgot-password.html'
  def get(self,request):
    form = forms.GetPasswordResetCode()
    context={
      'form':form,
      'get_parameters':request.GET
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.GetPasswordResetCode(data=request.POST)
    
    nextPage = request.GET.get('next')
    if not nextPage:
      nextPage = reverse('home:home')
    if form.is_valid():
      form.save()
      messages.success(request,'The password reset code has been sent to your email.')
      return redirect(reverse('accounts:forgot-password-reset',kwargs={'email':request.POST['email']})) # TODO: redirect to reset password
    
    context={
      'form':form,
      'get_parameters':request.GET
    }
    return render(request,self.template_name,context)

class ForgotPasswordReset(View):
  template_name='registration/forgot-password.html'
  def get(self,request,email):
    form = forms.ResetPassword(email=email)
    context={
      'form':form,
      'get_parameters':request.GET
    }
    return render(request,self.template_name,context)
  
  def post(self,request,email):
    form = forms.ResetPassword(email=email,data=request.POST)
    
    nextPage = request.GET.get('next')
    if not nextPage:
      nextPage = reverse('home:home')
    if form.is_valid():
      form.save()
      messages.success(request,'The password reset was successfull, you can login with your new password.')
      return redirect(nextPage)
    
    context={
      'form':form,
      'get_parameters':request.GET
    }
    return render(request,self.template_name,context)