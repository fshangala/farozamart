from django import forms
from accounts.models import gender_options
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from dashboard.function import getOptions, saveOption
import random

class RegistrationForm(forms.Form):
  username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control'
  }),validators=[UnicodeUsernameValidator])
  email=forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={
    'class':'form-control'
  }))
  phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control',
    'placeholder':'+000 (000) 000000'
  }),help_text='Please enter phone with country code.')
  first_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control'
  }))
  last_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control'
  }))
  gender=forms.ChoiceField(choices=gender_options,widget=forms.Select(attrs={
    'class':'form-control'
  }))
  address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control'
  }))
  password=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={
    'class':'form-control',
    'placeholder':'********'
  }))
  repeat_password=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={
    'class':'form-control',
    'placeholder':'********'
  }))
  
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    
    self.initial['phone']="+880"
  
  def clean_phone(self):
    """Check for country code"""
    phone = self.cleaned_data.get("phone")
    if phone and phone[0] != "+":
      self.add_error('phone','Please enter phone with country code')
    
    return phone
  
  def clean_username(self):
    """Reject usernames that differ only in case."""
    username = self.cleaned_data.get("username")
    if username and User.objects.filter(username__iexact=username).exists():
      self.add_error('username','This username is taken')
    
    return username
  
  def clean(self):
    cleaned_data = super().clean()
    if(cleaned_data.get('password') != cleaned_data.get('repeat_password') and cleaned_data.get('password')):
      self.add_error(error='Password and Repeat password must match')
    
    return cleaned_data
  
  def save(self) -> bool:
    user = User.objects.create(
      username=self.cleaned_data['username'],
      email=self.cleaned_data['email'],
      first_name=self.cleaned_data['first_name'],
      last_name=self.cleaned_data['last_name']
    )
    user.set_password(raw_password=self.cleaned_data['password'])
    user.profile.phone = self.cleaned_data['phone']
    user.profile.gender = self.cleaned_data['gender']
    user.profile.address = self.cleaned_data['address']
    user.save()
    
    options = getOptions()
    send_mail(
      f"{options['name']} - User registration",
      f"Thank you for your registration to {options['name']}. You may login anytime with the username {user.username}.",
      options['site_mail'],
      [user.email]
    )

class LoginForm(forms.Form):
  username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control'
  }))
  password=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={
    'class':'form-control',
    'placeholder':'********'
  }))

class BecomeSellerForm(forms.Form):
  def save(self,user:User):
    user.profile.is_seller = True
    user.save()

class BecomeResellerForm(forms.Form):
  def save(self,user:User):
    user.profile.is_reseller = True
    user.save()

class EditProfileForm(forms.Form):
  email=forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={
    'class':'form-control'
  }))
  phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control',
    'placeholder':'+1 (234) 567890'
  }))
  first_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control'
  }))
  last_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control'
  }))
  gender=forms.ChoiceField(choices=gender_options,widget=forms.Select(attrs={
    'class':'form-control'
  }))
  address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control'
  }))
  
  def save(self):
    self.user.email=self.cleaned_data['email']
    self.user.first_name=self.cleaned_data['first_name']
    self.user.last_name=self.cleaned_data['last_name']
    self.user.profile.phone = self.cleaned_data['phone']
    self.user.profile.gender = self.cleaned_data['gender']
    self.user.profile.address = self.cleaned_data['address']
    self.user.save()
  
  def __init__(self,*args,user:User,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    
    self.initial['email']=self.user.email
    self.initial['first_name']=self.user.first_name
    self.initial['last_name']=self.user.last_name
    self.initial['phone']=self.user.profile.phone
    self.initial['gender']=self.user.profile.gender
    self.initial['address']=self.user.profile.address

class UpdatePictureForm(forms.Form):
  picture=forms.ImageField()
  
  def save(self):
    self.user.profile.picture = self.cleaned_data['picture']
    self.user.profile.save()
  
  def __init__(self,*args,user:User,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    
    self.initial['picture']=self.user.profile.picture

class VerifyUserEmailForm(forms.Form):
  code=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
  
  def __init__(self,user:User,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    
  def clean_code(self):
    data = self.cleaned_data.get('code')
    options=getOptions()
    if options['otp'] != str(data):
      self.add_error('code','Invalid OTP Code')
    
    return data
  
  def save(self):
    self.user.profile.user_email_verified=True
    self.user.profile.save()

class GetPasswordResetCode(forms.Form):
  email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
  
  def clean_email(self):
    data=self.cleaned_data['email']
    if not User.objects.filter(email=data).exists():
      self.add_error('email','This email is not associated with any account!')
    
    return data
  
  def save(self):
    otp=random.randint(1000,9999)
    saveOption('otp',otp)
    options = getOptions()
    send_mail(
      f"{options['name']} - User password reset code",
      f"{otp} is your password reset code.",
      options['site_mail'],
      [self.cleaned_data['email']]
    )

class ResetPassword(forms.Form):
  reset_code=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
  password=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={
    'class':'form-control',
    'placeholder':'********'
  }))
  repeat_password=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={
    'class':'form-control',
    'placeholder':'********'
  }))
  
  def __init__(self,email:str,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.email=email
  
  def clean_reset_code(self):
    code=self.cleaned_data['reset_code']
    options=getOptions()
    if code != options['otp']:
      self.add_error('reset_code','Invalid code.')
    
    return code
  
  def clean(self):
    cleaned_data = super().clean()
    
    if not User.objects.filter(email=self.email).exists():
      self.add_error(error='User email not associated with any account.')
      
    if(cleaned_data.get('password') != cleaned_data.get('repeat_password') and cleaned_data.get('password')):
      self.add_error(error='Password and Repeat password must match')
    
    return cleaned_data
  
  def save(self):
    user=User.objects.filter(email=self.email).first()
    user.set_password(self.cleaned_data['password'])
    save()