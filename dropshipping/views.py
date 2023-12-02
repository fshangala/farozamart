from django.shortcuts import render, redirect, reverse
from dropshipping import forms
from dashboard.function import getOptions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages

# Create your views here.


class SteadfastConfiguration(LoginRequiredMixin,View):
  template_name='dashboard/steadfast-configuration.html'
  
  def get(self,request):
    context={
      'form':forms.SteadfastConfiguration(data=getOptions())
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.SteadfastConfiguration(data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Steadfast configuration updated!')
      return redirect(reverse('dropshipping:steadfast-configuration'))
    
    context={'form':form}
    return render(request,self.template_name,context)

# Steadfast
steadfast_context = {
  'sidebar_menu_steadfast_class':'active'
}

class SteadfastDelivery(LoginRequiredMixin,View):
  template_name='dashboard/dropshipping/steadfast.html'
  
  def get(self,request):
    context=steadfast_context
    
    return render(request,self.template_name,context)