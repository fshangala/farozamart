from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import View
from store import forms
from store import models
from store import functions
from dropshipping.functions import steadfastCreateOrder
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from dropshipping.models import SteadFastDelivery
from django.utils import timezone

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

class BecomeReseller(LoginRequiredMixin,View):
  def get(self,request):
    form = forms.BecomeResellerForm(user=request.user)
    form.save()
    messages.success(request,'You are now a reseller!')
    context={
      'form':form
    }
    return redirect(reverse('dashboard:dashboard'))

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
      messages.success(request,'Inventory successfully updated!')
      return redirect(reverse("store:inventory"))
    
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

# dashboard resales
resale_purchases_context = {
  'sidebar_menu_resale_purchases_class':'active'
}
class Resales(LoginRequiredMixin,View):
  template_name='store/resales.html'
  def get(self,request):
    context=resale_purchases_context
    resales = functions.getUserResalePurchases(request.user)
    context['resales']=resales
    return render(request,self.template_name,context)

class ResalePurchases(LoginRequiredMixin,View):
  template_name='store/resale-purchases.html'
  def get(self,request):
    context=resale_purchases_context
    purchases=models.Purchase.objects.filter(resale_price__gt=0.0)
    context['purchases']=purchases
    return render(request,self.template_name,context)

class NewResale(LoginRequiredMixin,View):
  template_name='store/new-resale.html'
  def get(self,request,id):
    context=resale_purchases_context
    purchase=get_object_or_404(models.Purchase,pk=id)
    form = forms.ResaleForm(reseller=request.user,purchase=purchase)
    context['form']=form
    context['purchase']=purchase
    return render(request,self.template_name,context)
  def post(self,request,id):
    context=resale_purchases_context
    purchase=get_object_or_404(models.Purchase,pk=id)
    form = forms.ResaleForm(reseller=request.user,purchase=purchase,data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'New resale successfully added!')
      return redirect(reverse('store:resales'))
    context['form']=form
    context['purchase']=purchase
    return render(request,self.template_name,context)

class DeleteResale(LoginRequiredMixin,View):
  def get(self,request,id):
    resale = get_object_or_404(models.Resale,pk=id)
    resale.delete()
    messages.info(request,'Resale deleted!')
    return redirect(reverse("store:resales"))
  
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

class SalesOrder(LoginRequiredMixin,View):
  template_name='store/sales-order.html'
  def get(self,request,id):
    context=sales_context
    order = get_object_or_404(models.Order,pk=id)
    context['order']=order
    return render(request,self.template_name,context)

class WithdrawRequest(LoginRequiredMixin,View):
  template_name='store/withdraw.html'
  def get(self,request,id):
    context=sales_context
    wallet = get_object_or_404(models.Wallet,pk=id)
    context['form'] = forms.WithdrawRequest(wallet=wallet)
    return render(request,self.template_name,context)
  
  def post(self,request,id):
    context=sales_context
    wallet = get_object_or_404(models.Wallet,pk=id)
    form=forms.WithdrawRequest(wallet=wallet,data=request.POST)
    if form.is_valid():
      form.save()
      messages.info(request,'Withdraw request successfully submitted!')
      return redirect(reverse('store:sales'))
    return render(request,self.template_name,context)

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
      form.cart()
      if request.POST['submit_type'] == 'buy':
        return redirect(reverse('store:checkout-payment'))
      elif request.POST['submit_type'] == 'cart':
        messages.success(request,'Added to cart!')
      else:
        form.add_error(field=None,error='Invalid request')

    context['listing']=listing
    context['form']=form

    return render(request, self.template_name, context)

# cart
cart_context={}
@method_decorator(never_cache,name='dispatch')
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
    order = request.user.orders.filter(draft=True).first()
    if order:
      context['order']=order
      if order.sales.all().count() > 0:
        context['transaction_id']=timezone.now().timestamp()
        context['cart_total']=self.cartTotal(order.sales.all())
        context['cart_currency']=self.cartCurrency(order.sales.all())

    return render(request,self.template_name,context)

class DeleteCartItem(LoginRequiredMixin,View):
  def get(self,request,id):
    context=cart_context
    item = models.Sale.objects.get(pk=id)
    item.delete()
    return redirect(reverse('store:cart'))

class CheckoutPayment(LoginRequiredMixin,View):
  template_name='store/checkout-payment.html'
  
  def cartCurrency(self,items)->str:
    return items[0].purchase.currency.code
  
  def cartTotal(self,items)->float:
    cart_total = 0.0
    for item in items:
      cart_total += item.quantity * item.sale_price
    return cart_total
  def get(self,request):
    context=cart_context
    order = request.user.orders.filter(draft=True).first()
    if order:
      context['order']=order
      if order.sales.all().count() > 0:
        context['transaction_id']=timezone.now().timestamp()
        context['cart_total']=self.cartTotal(order.sales.all())
        context['cart_currency']=self.cartCurrency(order.sales.all())
    return render(request,self.template_name,context)

class Checkout(LoginRequiredMixin,View):
  def get(self,request,order):
    context=cart_context
    
    form = forms.CheckoutForm(data=request.GET,order_id=order)
    if form.is_valid():
      form.save()
      return redirect(reverse('store:customer-order',kwargs={'id':order}))
    else:
      messages.error(request,form.errors.as_text())
    
    return redirect(reverse('store:cart'))

class CheckoutCOD(LoginRequiredMixin,View):
  def get(self,request,order):
    context=cart_context
    order = get_object_or_404(models.Order,pk=order)
    for item in order.sales.all():
      item.cart = False
      item.save()
        
    order.draft = False
    order.save()
    
    steadfastCreateOrder(order)
    return redirect(reverse('store:customer-order',kwargs={'id':order.id}))

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

# customer
class CustomerOrders(LoginRequiredMixin,View):
  template_name='store/profile/orders.html'
  def get(self,request):
    context={}
    return render(request,self.template_name,context)

class SingleCustomerOrder(LoginRequiredMixin,View):
  template_name='store/profile/single-order.html'
  def get(self,request,id):
    order = request.user.orders.get(pk=id)
    context={
      'order':order,
      'steadfast_delivery':SteadFastDelivery.objects.filter(invoice=str(order.id)).first()
    }
    return render(request,self.template_name,context)

# Staff orders
staff_orders_context={
  'sidebar_menu_staff_orders_class':'active'
}
class StaffOrders(LoginRequiredMixin,View):
  template_name='store/staff/orders.html'
  def get(self,request):
    context=staff_orders_context
    orders = models.Order.objects.filter(draft=False)
    context['orders']=orders
    return render(request,self.template_name,context)

class StaffApproveOrder(LoginRequiredMixin,View):
  template_name='store/staff/approve-order.html'
  def get(self,request,id):
    context=staff_orders_context
    order=get_object_or_404(models.Order,pk=id)
    form=forms.ApproveOrderForm(order=order,data={
      'transaction_id':timezone.now().timestamp(),
      'amount':order.total_cost_number()
    })
    context['form']=form
    return render(request,self.template_name,context)
  def post(self,request,id):
    context=staff_orders_context
    order=get_object_or_404(models.Order,pk=id)
    form=forms.ApproveOrderForm(order=order,data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Order successfully approved!')
      return redirect(reverse('store:staff-orders'))
    context['form']=form
    return render(request,self.template_name,context)

class StaffOrder(LoginRequiredMixin,View):
  template_name='store/staff/staff-order.html'
  def get(self,request,id):
    context=staff_orders_context
    order = get_object_or_404(models.Order,pk=id)
    context['order']=order
    return render(request,self.template_name,context)