from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from paymentgateway import forms
from dashboard.function import getOptions
from django.contrib import messages

# Create your views here.
payment_method_context={}
class PaymentMethods(LoginRequiredMixin,View):
  template_name='dashboard/payment-methods.html'
  def get(self,request):
    context=payment_method_context
    options=getOptions()
    cod_form=forms.CashOnDeliveryConfiguration(data=options)
    context['cod_form']=cod_form
    return render(request,self.template_name,context)
  
  def post(self,requeust):
    context=payment_method_context
    options=getOptions()
    cod_form=forms.CashOnDeliveryConfiguration(data=options)
    context['cod_form']=cod_form
    return render(request,self.template_name,context)

class CODPayment(LoginRequiredMixin,View):
  template_name='dashboard/cod-payment.html'
  def get(self,request):
    context=payment_method_context
    options=getOptions()
    form=forms.CashOnDeliveryConfiguration(data=options)
    context['form']=form
    return render(request,self.template_name,context)
  
  def post(self,request):
    context=payment_method_context
    form=forms.CashOnDeliveryConfiguration(data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Cash on delivery payment configuration updated')
      
    context['form']=form
    return render(request,self.template_name,context)
    