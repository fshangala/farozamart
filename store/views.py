from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from store import forms
from store import models

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

# dashboard inventory
inventory_context = {
  'sidebar_menu_inventory_class':'active'
}
class Inventory(LoginRequiredMixin,View):
  template_name='store/inventory.html'
  
  def get(self,request):
    context=inventory_context
    
    inventory_items = models.Inventory.objects.filter(store=request.user.store)
    context['inventory_items']=inventory_items
    return render(request,self.template_name,context)

class EditInventory(LoginRequiredMixin,View):
  template_name='store/edit_inventory.html'
  
  def get(self,request,id):
    inventory = models.Inventory.objects.get(pk=id)
    form = forms.InventoryForm(user=request.user,instance=inventory)
    
    context=inventory_context
    context['form']=form
    return render(request,self.template_name,context)
  
  def post(self,request,id):
    inventory = models.Inventory.objects.get(pk=id)
    form = forms.InventoryForm(user=request.user,instance=inventory,data=request.POST)
    
    if form.is_valid():
      form.save()
      return redirect(reverse("store:edit-inventory",kwargs={'id':id}))
    
    context=inventory_context
    context['form']=form
    return render(request,self.template_name,context)

class NewInventory(LoginRequiredMixin,View):
  template_name='store/new_inventory.html'
  
  def get(self,request):
    form = forms.InventoryForm(user=request.user)
    
    context=inventory_context
    context['form']=form
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.InventoryForm(user=request.user,data=request.POST)
    
    if form.is_valid():
      form.save()
      return redirect(reverse("store:inventory"))
    
    context=inventory_context
    context['form']=form
    return render(request,self.template_name,context)

class DeleteInventory(LoginRequiredMixin,View):
  def get(self,request,id):
    inventory = models.Inventory.objects.get(pk=id)
    inventory.delete()
    return redirect(reverse("store:inventory"))

# dashboard purchases
purchases_context = {
  'sidebar_menu_purchases_class':'active'
}

class Purchases(LoginRequiredMixin,View):
  template_name='store/purchases.html'
  
  def get(self,request):
    context=purchases_context
    
    inventory = request.user.store.inventory.all()
    qs = []
    for a in inventory:
      qs.append(models.Purchase.objects.filter(inventory=a))
      
    purchases = models.Purchase.objects.union(*qs)
    context['purchases']=purchases
    
    return render(request,self.template_name,context)

class NewPurchase(LoginRequiredMixin,View):
  template_name='store/new_purchase.html'
  
  def get(self,request):
    form = forms.PurchaseForm(user=request.user)
    
    context=purchases_context
    context['form']=form
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.PurchaseForm(user=request.user,data=request.POST)
    
    if form.is_valid():
      form.save()
      return redirect(reverse("store:purchases"))
    
    context=purchases_context
    context['form']=form
    return render(request,self.template_name,context)

class EditPurchase(LoginRequiredMixin,View):
  template_name='store/edit_purchase.html'
  
  def get(self,request,id):
    purchase = models.Purchase.objects.get(pk=id)
    form = forms.PurchaseForm(user=request.user,instance=purchase)
    
    context=purchases_context
    context['form']=form
    return render(request,self.template_name,context)
  
  def post(self,request,id):
    purchase = models.Purchase.objects.get(pk=id)
    form = forms.PurchaseForm(user=request.user,instance=purchase,data=request.POST)
    
    if form.is_valid():
      form.save()
      return redirect(reverse("store:edit-purchase",kwargs={'id':id}))
    
    context=purchases_context
    context['form']=form
    return render(request,self.template_name,context)

class DeletePurchase(LoginRequiredMixin,View):
  def get(self,request,id):
    purchase = models.Purchase.objects.get(pk=id)
    purchase.delete()
    return redirect(reverse("store:purchases"))