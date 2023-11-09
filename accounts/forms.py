from django import forms
from accounts.models import gender_options
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator

class RegistrationForm(forms.Form):
  username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={
    'class':'form-control'
  }),validators=[UnicodeUsernameValidator])
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
  password=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={
    'class':'form-control',
    'placeholder':'********'
  }))
  repeat_password=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={
    'class':'form-control',
    'placeholder':'********'
  }))
  
  def clean_username(self):
    """Reject usernames that differ only in case."""
    username = self.cleaned_data.get("username")
    if username and User.objects.filter(username__iexact=username).exists():
      self.add_error('username','This username is taken')
    
    return username
  
  def clean(self):
    cleaned_data = super().clean()
    if(cleaned_data['password'] != cleaned_data['repeat_password']):
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
    user.save()

class BecomeSellerForm(forms.Form):
  def save(self,user:User):
    user.profile.is_seller = True
    user.save()