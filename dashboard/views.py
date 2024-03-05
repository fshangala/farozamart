from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from dashboard.forms import GeneralOptionsForm, MailingForm
from dashboard.function import getOptions
from django.contrib import messages
from store import models as store_models
from store import functions as store_functions
from django.contrib.auth.models import User

# Create your views here.
class Dashboard(LoginRequiredMixin,UserPassesTestMixin,View):
  template_name='dashboard/dashboard.html'
  
  def test_func(self):
    return self.request.user.profile.is_seller or self.request.user.is_staff or self.request.user.profile.is_reseller
  
  def get(self, request):
    context={
      'sidebar_menu_dashboard_class':'active'
    }
    if request.user.is_staff:
      context['new_orders']=store_models.Order.objects.filter(draft=False,transaction=None).count()
      context['products']=store_models.Inventory.objects.all().count()
      context['sellers']=User.objects.filter(profile__is_seller=True).count()
      context['resellers']=User.objects.filter(profile__is_reseller=True).count()
    if request.user.profile.is_seller:
      context['sales']=store_functions.getUserSales(request.user).count()
      context['inventory']=request.user.store.inventory.all().count()
      context['active_purchases']=store_functions.getUserActivePurchases(request.user).count()
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

class Mailing(LoginRequiredMixin,View):
  template_name='dashboard/mailing-settings.html'
  
  def get(self,request):
    context={
      'form':MailingForm(data=getOptions())
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = MailingForm(data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Mailing options updated!')
      return redirect(reverse('dashboard:mailing-settings'))
    
    context={'form':form}
    return render(request,self.template_name,context)