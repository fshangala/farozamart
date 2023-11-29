from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import View
from store import forms
from store import models
from store import functions

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
      
    purchases = functions.getUserPurchases(request.user)
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

# dashboard sales
sales_context = {
  'sidebar_menu_sales_class':'active'
}

class Sales(LoginRequiredMixin,View):
  template_name='store/sales.html'
  
  def get(self,request):
    context=sales_context
      
    context['sales']=functions.getUserSales(request.user)
    
    return render(request,self.template_name,context)

class NewSale(LoginRequiredMixin,View):
  template_name='store/new_sale.html'
  
  def get(self,request):
    form = forms.SaleForm(user=request.user)
    
    context=sales_context
    context['form']=form
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.SaleForm(user=request.user,data=request.POST)
    
    if form.is_valid():
      form.save()
      return redirect(reverse("store:sales"))
    
    context=sales_context
    context['form']=form
    return render(request,self.template_name,context)

class EditSale(LoginRequiredMixin,View):
  template_name='store/edit_sale.html'
  
  def get(self,request,id):
    sale = models.Sale.objects.get(pk=id)
    form = forms.SaleForm(user=request.user,instance=sale)
    
    context=sales_context
    context['form']=form
    return render(request,self.template_name,context)
  
  def post(self,request,id):
    sale = models.Sale.objects.get(pk=id)
    form = forms.SaleForm(user=request.user,instance=sale,data=request.POST)
    
    if form.is_valid():
      form.save()
      return redirect(reverse("store:edit-sale",kwargs={'id':id}))
    
    context=sales_context
    context['form']=form
    return render(request,self.template_name,context)

class DeleteSale(LoginRequiredMixin,View):
  def get(self,request,id):
    sale = models.Sale.objects.get(pk=id)
    sale.delete()
    return redirect(reverse("store:sales"))

# shop
shop_context={
  'nav_shop_class':'active'
}
class Shop(View):
  template_name='store/shop.html'
  def get(self,request):
    context=shop_context

    listings = models.Purchase.objects.all()
    context['listings']=listings
    return render(request,self.template_name,context)

class Listing(LoginRequiredMixin,View):
  template_name='store/listing.html'

  def get(self,request,id):
    context=shop_context
    listing=models.Purchase.objects.get(pk=id)
    form=forms.ListingForm(user=request.user,listing=listing)

    context['listing']=listing
    context['form']=form

    return render(request, self.template_name, context)
  
  def post(self,request,id):
    context=shop_context
    listing=models.Purchase.objects.get(pk=id)
    form=forms.ListingForm(user=request.user,listing=listing,data=request.POST)
    if form.is_valid():
      if request.POST['submit_type'] == 'buy':
        form.buy()
      elif request.POST['submit_type'] == 'cart':
        form.cart()
        messages.success(request,'Added to cart!')
      else:
        form.add_error(field=None,error='Invalid request')

    context['listing']=listing
    context['form']=form

    return render(request, self.template_name, context)

# cart
cart_context={}
class Cart(LoginRequiredMixin,View):
  template_name='store/cart.html'
  
  def cartCurrency(self,items)->str:
    return items[0].purchase.currency.code
  
  def cartTotal(self,items)->float:
    cart_total = 0.0
    for item in items:
      cart_total += item.quantity * item.sale_price
    return cart_total

  def get(self,request):
    context=cart_context
    
    cart_items = request.user.orders.filter(cart=True)
    context['cart_items']=cart_items
    context['cart_total']=self.cartTotal(cart_items)
    context['cart_currency']=self.cartCurrency(cart_items)

    return render(request,self.template_name,context)

class DeleteCartItem(LoginRequiredMixin,View):
  def get(self,request,id):
    context=cart_context
    item = models.Sale.objects.get(pk=id)
    item.delete()
    return redirect(reverse('store:cart'))

# settings currency
class Currencies(LoginRequiredMixin,View):
  template_name='store/currencies.html'
  def get(self,request):
    context={}
    context['currencies']=models.Currency.objects.all()
    return render(request,self.template_name,context)
  
class NewCurrency(LoginRequiredMixin,View):
  template_name='store/new-currency.html'
  def get(self,request):
    context={
      'form':forms.CurrencyForm()
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    context={}
    form=forms.CurrencyForm(data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'New currency successfully created!')
      return redirect(reverse('store:currencies'))
    context['form']=form
    return render(request,self.template_name,context)

class EditCurrency(LoginRequiredMixin,View):
  template_name='store/edit-currency.html'
  def get(self,request,id):
    instance=models.Currency.objects.get(pk=id)
    context={'form':forms.CurrencyForm(instance=instance)}
    return render(request,self.template_name,context)
  
  def post(self,request,id):
    instance=models.Currency.objects.get(pk=id)
    context={}
    form=forms.CurrencyForm(data=request.POST,instance=instance)
    if form.is_valid():
      form.save()
      messages.success(request,'Successfully updated!')
      return redirect(reverse('store:currencies'))
    context['form']=form
    return render(request,self.template_name,context)

class DeleteCurrency(LoginRequiredMixin,View):
  def get(self,request,id):
    context=cart_context
    item = models.Currency.objects.get(pk=id)
    item.delete()
    messages.success(request,f"{item.name_singular} successfully deleted!")
    return redirect(reverse('store:currencies'))