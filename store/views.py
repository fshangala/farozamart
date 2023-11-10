from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from store import forms

# Create your views here.
class BecomeSeller(LoginRequiredMixin,UserPassesTestMixin,View):
  template_name='store/become-seller.html'
  
  def test_func(self):
    return not (self.request.user.profile.is_seller and self.request.method == 'GET')
  
  def get(self,request):
    form = forms.BecomeSellerForm(user=request.user)
    context={
      'form':form
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.BecomeSellerForm(user=request.user,data=request.POST)
    if form.is_valid():
      form.save()
      return redirect(reverse('dashboard:dashboard'))
    context={
      'form':form
    }
    return render(request,self.template_name,context)