from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from dashboard.forms import GeneralOptionsForm
from dashboard.function import getOptions
from django.contrib import messages

# Create your views here.
class Dashboard(LoginRequiredMixin,UserPassesTestMixin,View):
  template_name='dashboard/dashboard.html'
  
  def test_func(self):
    return self.request.user.profile.is_seller or self.request.user.is_staff
  
  def get(self, request):
    context={
      'sidebar_menu_dashboard_class':'active'
    }
    messages.info(request,'Welcome to the dashboard!')
    return render(request,self.template_name,context)

class GeneralSettings(LoginRequiredMixin,View):
  template_name='dashboard/general-settings.html'
  
  def get(self,request):
    context={
      'form':GeneralOptionsForm(data=getOptions())
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = GeneralOptionsForm(data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'General options updated!')
      return redirect(reverse('dashboard:general-settings'))
    
    context={'form':form}
    return render(request,self.template_name,context)