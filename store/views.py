from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import View
from store import forms
from store import models
from store import functions
from store import signals
from dropshipping.functions import steadfastCreateOrder
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from dropshipping.models import SteadFastDelivery
from django.utils import timezone

# Create your views here.
class BecomeSeller(LoginRequiredMixin,UserPassesTestMixin,View):
  template_name='store/become-seller.html'
  
  def get_login_url(self):
    return reverse('accounts:register')
  
  def test_func(self):
    return not (self.request.user.profile.is_seller and self.request.method == 'GET')
  
  def get(self,request):
    form = forms.BecomeSellerRequestForm(user=request.user)
    context={
      'form':form
    }
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.BecomeSellerRequestForm(user=request.user,data=request.POST)
    if form.is_valid():
      form.save()
      messages.info(request,'Request successfull. Seller status under review.')
      return redirect(reverse('store:become-seller'))
    context={
      'form':form
    }
    return render(request,self.template_name,context)

class BecomeReseller(LoginRequiredMixin,View):
  template_name='store/become-reseller.html'
  
  def get_login_url(self):
    return reverse('accounts:register')
  
  def get(self,request):
    context={}
    form = forms.BecomeResellerRequestForm(user=request.user)
    context['form']=form
    if request.user.profile.is_reseller:
      return redirect(reverse('dashboard:dashboard'))
    return render(request,self.template_name,context)
  def post(self,request):
    form = forms.BecomeResellerRequestForm(user=request.user,data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Request successfull. Reseller status under review.')
      return redirect(reverse('store:become-reseller'))
      
    context={
      'form':form
    }
    return render(request,self.template_name,context)

class BecomeResellerSuccess(LoginRequiredMixin,View):
  template_name='store/become-reseller-success.html'
  def get(self,request):
    return render(request,self.template_name,{})

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
    form = forms.InventoryForm(user=request.user,instance=inventory,data=request.POST,files=request.FILES)
    
    if form.is_valid():
      form.save()
      messages.success(request,'Inventory successfully updated!')
      return redirect(reverse("store:inventory"))
    
    context=inventory_context
    context['form']=form
    return render(request,self.template_name,context)

class InventoryImages(LoginRequiredMixin,View):
  template_name='store/inventory-images.html'
  def get(self,request,id):
    context=inventory_context
    inventory=models.Inventory.objects.get(pk=id)
    form=forms.InventoryImagesForm(inventory=inventory)
    context['inventory']=inventory
    context['form']=form
    return render(request,self.template_name,context)
  def post(self,request,id):
    context=inventory_context
    inventory=models.Inventory.objects.get(pk=id)
    form=forms.InventoryImagesForm(inventory=inventory,data=request.POST,files=request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request,'Image successfully added!')
      return redirect(reverse('store:inventory-images',kwargs={'id':id}))
    context['inventory']=inventory
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
    form = forms.InventoryForm(user=request.user,data=request.POST,files=request.FILES)
    
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

# dashboard categories
categories_context = {
  'sidebar_menu_categories_class':'active'
}
class Categories(LoginRequiredMixin,View):
  template_name='store/categories.html'
  def get(self,request):
    context=categories_context
    context['categories']=models.Category.objects.all()
    return render(request,self.template_name,context)

class EditCategory(LoginRequiredMixin,View):
  template_name='store/edit_category.html'
  
  def get(self,request,id):
    category = models.Category.objects.get(pk=id)
    form = forms.CategoryForm(user=request.user,instance=category)
    
    context=categories_context
    context['form']=form
    return render(request,self.template_name,context)
  
  def post(self,request,id):
    category = models.Category.objects.get(pk=id)
    form = forms.CategoryForm(user=request.user,instance=category,data=request.POST)
    
    if form.is_valid():
      form.save()
      messages.success(request,'Category successfully updated!')
      return redirect(reverse("store:categories"))
    
    context=categories_context
    context['form']=form
    return render(request,self.template_name,context)

class NewCategory(LoginRequiredMixin,View):
  template_name='store/new_category.html'
  
  def get(self,request):
    form = forms.CategoryForm(user=request.user)
    
    context=categories_context
    context['form']=form
    return render(request,self.template_name,context)
  
  def post(self,request):
    form = forms.CategoryForm(user=request.user,data=request.POST)
    
    if form.is_valid():
      form.save()
      return redirect(reverse("store:categories"))
    
    context=categories_context
    context['form']=form
    return render(request,self.template_name,context)

class DeleteCategory(LoginRequiredMixin,View):
  def get(self,request,id):
    category = models.Category.objects.get(pk=id)
    category.delete()
    return redirect(reverse("store:categories"))

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
    inventory_id = request.GET.get('inventory_id')
    if inventory_id:
      try:
        inventory = models.Inventory.objects.get(pk=inventory_id)
        form = forms.PurchaseForm(user=request.user,inventory=inventory)
      except Exception as e:
        messages.error(request,str(e))
    
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
resales_context = {
  'sidebar_menu_resales_class':'active'
}
class Resales(LoginRequiredMixin,View):
  template_name='store/resales.html'
  def get(self,request):
    context=resales_context
    resales = functions.getUserResalePurchases(request.user)
    context['resales']=resales
    return render(request,self.template_name,context)

# dashboard resale purchases
resale_purchases_context = {
  'sidebar_menu_resale_purchases_class':'active'
}
class ResalePurchases(LoginRequiredMixin,View):
  template_name='store/resale-purchases.html'
  def get(self,request):
    context=resale_purchases_context
    purchases=models.Purchase.objects.filter(resale_price__gt=0.0,stock__gt=0)
    context['purchases']=purchases
    return render(request,self.template_name,context)

class ResalePurchase(LoginRequiredMixin,View):
  template_name='store/resale-purchase.html'
  def get(self,request,id):
    context=resale_purchases_context
    resale_purchase=models.Purchase.objects.get(pk=id)
    context['resale_purchase']=resale_purchase
    context['form']=forms.AddToResaleCartForm(user=request.user,listing=resale_purchase)
    return render(request,self.template_name,context)
  
  def post(self,request,id):
    context=resale_purchases_context
    listing=models.Purchase.objects.get(pk=id)
    form=forms.AddToResaleCartForm(user=request.user,listing=listing,data=request.POST)
    if form.is_valid():
      form.cart()
      messages.success(request,'Added to cart!')
      return redirect(reverse('store:resale-purchase',kwargs={'id':listing.id}))

    context['listing']=listing
    context['form']=form

    return render(request, self.template_name, context)

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

# dashboard reseller cart
reseller_cart_context = {}
class ResellerCart(LoginRequiredMixin,View):
  template_name='store/reseller-cart.html'
  
  def cartCurrency(self,items)->str:
    return items[0].purchase.currency.code
  
  def cartTotal(self,items)->float:
    cart_total = 0.0
    for item in items:
      cart_total += item.quantity * item.sale_price
    return cart_total
  
  def get(self,request):
    context=reseller_cart_context
    try:
      order = request.user.orders.get(draft=True)
    except Exception as e:
      pass
    else:
      context['order']=order
      if order.sales.all().count() > 0:
        context['transaction_id']=timezone.now().timestamp()
        context['cart_total']=self.cartTotal(order.sales.all())
        context['cart_currency']=self.cartCurrency(order.sales.all())

    return render(request,self.template_name,context)

class ResellerCODCheckout(LoginRequiredMixin,View):
  template_name='store/reseller-cod-checkout.html'
  
  def cartCurrency(self,items)->str:
    return items[0].purchase.currency.code
  
  def cartTotal(self,items)->float:
    cart_total = 0.0
    for item in items:
      cart_total += item.quantity * item.sale_price
    return cart_total
  
  def get(self,request):
    context=reseller_cart_context
    order = request.user.orders.get(draft=True)
    if order:
      context['order']=order
      if order.sales.all().count() > 0:
        context['transaction_id']=timezone.now().timestamp()
        context['cart_total']=self.cartTotal(order.sales.all())
        context['cart_currency']=self.cartCurrency(order.sales.all())
        context['form']=forms.ResellerCODCheckout(reseller=request.user,order=order)
    return render(request,self.template_name,context)
  
  def post(self,request):
    context=reseller_cart_context
    order = request.user.orders.get(draft=True)
    if order:
      form=forms.ResellerCODCheckout(reseller=request.user,order=order,data=request.POST)
      if form.is_valid():
        form.save()
        messages.info(request,'Order submitted!')
        return redirect(reverse('store:resales'))
      
      context['cart_total']=self.cartTotal(order.sales.all())
      context['cart_currency']=self.cartCurrency(order.sales.all())
      context['order']=order
      context['form']=form
    return render(request,self.template_name,context)
  
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

    listings = models.Purchase.objects.filter(stock__gt=0)
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
    order = request.user.orders.get(draft=True)
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
        context['cod_checkout_form']=forms.CODCheckoutForm(user=request.user,order=order)
        context['cod_checkout_form_action']=reverse('store:checkout-cod',kwargs={'order':order.id})
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
    order = functions.CODPayment(order)
    return redirect(reverse('store:customer-order',kwargs={'id':order.id}))
  def post(self,request,order):
    order = models.Order.objects.get(pk=order)
    form = forms.CODCheckoutForm(user=request.user,order=order,data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Your order has been received. you will be notified by mail when your order is processed!')
      return redirect(reverse('store:customer-order',kwargs={'id':order.id}))
    messages.error(request,form.errors.as_text())
    return redirect(reverse('store:checkout-payment'))

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

class StaffCancelOrder(LoginRequiredMixin,View):
  def get(self,request,id):
    context=staff_orders_context
    order=get_object_or_404(models.Order,pk=id)
    order.delete()
    messages.success(request,'Order successfully canceled!')
    signals.order_canceled.send(models.Order,order=order)
    return redirect(reverse('store:staff-orders'))
    

class StaffOrder(LoginRequiredMixin,View):
  template_name='store/staff/staff-order.html'
  def get(self,request,id):
    context=staff_orders_context
    order = get_object_or_404(models.Order,pk=id)
    context['order']=order
    return render(request,self.template_name,context)
  
# Staff orders
staff_withdraws_context={
  'sidebar_menu_staff_withdraws_class':'active'
}
class StaffWithdraws(LoginRequiredMixin,View):
  template_name='store/staff/withdraws.html'
  def get(self,request):
    context=staff_withdraws_context
    context['withdraws']=models.Withdraw.objects.all()
    return render(request,self.template_name,context)

class StaffApproveWithdraw(LoginRequiredMixin,View):
  def get(self,request,pk):
    withdraw = models.Withdraw.objects.get(pk=pk)
    withdraw.approved = True
    withdraw.save()
    signals.withdraw_request_approved.send(models.Withdraw,withdraw=withdraw)
    messages.success(request,'Withdraw request approved')
    return redirect(reverse('store:staff-withdraws'))

#Staff sellers
staff_sellers_context={
  'sidebar_menu_staff_sellers_class':'active'
}
class StaffSellers(LoginRequiredMixin,View):
  template_name='store/staff/sellers.html'
  def get(self,request):
    context=staff_sellers_context
    sellers = User.objects.filter(profile__is_seller=True)
    seller_requests = models.Becomeseller.objects.all()
    context['sellers']=sellers
    context['seller_requests']=seller_requests
    return render(request,self.template_name,context)

class StaffSellerRequest(LoginRequiredMixin,View):
  template_name='store/staff/general-profile.html'
  def get(self,request,pk):
    context=staff_sellers_context
    seller = User.objects.get(pk=pk)
    context['obj'] = seller
    return render(request,self.template_name,context)

class StaffGeneralProfile(LoginRequiredMixin,View):
  template_name='store/staff/general-profile.html'
  def get(self,request,user_id):
    context=staff_sellers_context
    seller = User.objects.get(pk=user_id)
    context['obj'] = seller
    return render(request,self.template_name,context)

class StaffApproveSeller(LoginRequiredMixin,View):
  def get(self,request,pk):
    sellerRequest = models.Becomeseller.objects.get(pk=pk)
    form = forms.BecomeSellerForm(user=sellerRequest.user,data={
      'name':sellerRequest.name,
      'description':sellerRequest.description,
      'address':sellerRequest.address,
      'email':sellerRequest.email,
      'phone':sellerRequest.phone,
      'whatsapp':sellerRequest.whatsapp,
      'facebook_url':sellerRequest.facebook_url,
      'trade_licence':sellerRequest.trade_licence
    })
    if form.is_valid():
      form.save()
      sellerRequest.delete()
      messages.success(request,'Seller successfully approved!')
    else:
      messages.error(request,form.errors.as_text)
    
    return redirect(reverse('store:staff-sellers'))

class StaffDeclineSellerRequest(LoginRequiredMixin,View):
  def get(self,request,pk):
    sellerRequest = models.Becomeseller.objects.get(pk=pk)
    signals.become_seller_request_declined.send(models.Becomeseller,becomeseller=sellerRequest)
    sellerRequest.delete()
    messages.info(request, 'Request declined successfully!')
    return redirect(reverse('store:staff-sellers'))

#Staff resellers
staff_resellers_context={
  'sidebar_menu_staff_resellers_class':'active'
}
class StaffResellers(LoginRequiredMixin,View):
  template_name='store/staff/resellers.html'
  def get(self,request):
    context=staff_resellers_context
    resellers = User.objects.filter(profile__is_reseller=True)
    reseller_requests = models.Becomereseller.objects.all()
    context['resellers']=resellers
    context['reseller_requests']=reseller_requests
    return render(request,self.template_name,context)

class StaffApproveReseller(LoginRequiredMixin,View):
  def get(self,request,pk):
    resellerRequest = models.Becomereseller.objects.get(pk=pk)
    form = forms.BecomeResellerForm(user=resellerRequest.user,data={
      'address':resellerRequest.address,
      'email':resellerRequest.email,
      'phone':resellerRequest.phone,
      'whatsapp':resellerRequest.whatsapp,
      'facebook_url':resellerRequest.facebook_url
    })
    if form.is_valid():
      form.save()
      resellerRequest.delete()
      messages.success(request,'Reseller successfully approved!')
    else:
      messages.error(request,form.errors.as_text)
    
    return redirect(reverse('store:staff-resellers'))

class StaffDeclineResellerRequest(LoginRequiredMixin,View):
  def get(self,request,pk):
    resellerRequest = models.Becomereseller.objects.get(pk=pk)
    signals.become_reseller_request_declined.send(models.Becomereseller,becomereseller=resellerRequest)
    resellerRequest.delete()
    messages.info(request, 'Request declined successfully!')
    return redirect(reverse('store:staff-resellers'))

#Staff users
staff_users_context={
  'sidebar_menu_users_class':'active'
}
class StaffUsers(LoginRequiredMixin,View):
  template_name='store/staff/users.html'
  def get(self,request):
    context=staff_resellers_context
    users = User.objects.all()
    context['users']=users
    return render(request,self.template_name,context)

class StaffBlocOrUnblockUser(LoginRequiredMixin,View):
  def get(self,request,user_id):
    user = User.objects.get(pk=user_id)
    if user.is_active:
      user.is_active = False
      user.save()
      messages.success(request,'User blocked!')
    else:
      user.is_active = True
      user.save()
      messages.success(request,'User unblocked!')
    return redirect(reverse('store:staff-users'))
