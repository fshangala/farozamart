from django.urls import path
from store import views

app_name='store'
urlpatterns = [
  # customer
  path('shop/',views.Shop.as_view(),name='shop'),
  path('shop/listing/<id>/',views.Listing.as_view(),name='listing'),
  path('shop/cart/',views.Cart.as_view(),name='cart'),
  path('shop/checkout/payment/',views.CheckoutPayment.as_view(),name='checkout-payment'),
  path('shop/cart/<id>/delete/',views.DeleteCartItem.as_view(),name='delete-cart-item'),
  path('shop/cart/checkout/<order>/',views.Checkout.as_view(),name='checkout'),
  path('shop/cart/checkout-cod/<order>/',views.CheckoutCOD.as_view(),name='checkout-cod'),
  
  path('profile/orders/',views.CustomerOrders.as_view(),name='customer-orders'),
  path('profile/orders/<id>/',views.SingleCustomerOrder.as_view(),name='customer-order'),

  path('become-seller/',views.BecomeSeller.as_view(),name='become-seller'),
  path('become-reseller/',views.BecomeReseller.as_view(),name='become-reseller'),
  path('become-reseller-success/',views.BecomeResellerSuccess.as_view(),name='become-reseller-success'),
  
  # staff
  path('dashboard/orders/',views.StaffOrders.as_view(),name='staff-orders'),
  path('dashboard/orders/<id>/',views.StaffOrder.as_view(),name='staff-order'),
  path('dashboard/orders/<id>/comfirm/',views.StaffComfirmOrder.as_view(),name='staff-comfirm-order'),
  path('dashboard/orders/<id>/decline/',views.StaffDeclineOrder.as_view(),name='staff-decline-order'),
  path('dashboard/orders/<id>/approve/',views.StaffApproveOrder.as_view(),name='staff-approve-order'),
  path('dashboard/orders/<id>/cancel/',views.StaffCancelOrder.as_view(),name='staff-cancel-order'),
  
  path('dashboard/withdraws/',views.StaffWithdraws.as_view(),name='staff-withdraws'),
  path('dashboard/withdraws/<pk>/approve/',views.StaffApproveWithdraw.as_view(),name='staff-approve-withdraws'),
  
  path('dashboard/sellers/',views.StaffSellers.as_view(),name='staff-sellers'),
  path('dashboard/sellers/requests/<pk>/',views.StaffSellerRequest.as_view(),name='staff-seller-request'),
  path('dashboard/sellers/<pk>/approve/',views.StaffApproveSeller.as_view(),name='staff-approve-seller'),
  path('dashboard/sellers/<pk>/decline/',views.StaffDeclineSellerRequest.as_view(),name='staff-decline-seller'),
  
  path('dashboard/resellers/',views.StaffResellers.as_view(),name='staff-resellers'),
  path('dashboard/resellers/<pk>/approve/',views.StaffApproveReseller.as_view(),name='staff-approve-reseller'),
  path('dashboard/resellers/<pk>/decline/',views.StaffDeclineResellerRequest.as_view(),name='staff-decline-reseller'),
  
  path('dashboard/currencies/',views.Currencies.as_view(),name='currencies'),
  path('dashboard/currencies/new/',views.NewCurrency.as_view(),name='new-currency'),
  path('dashboard/currencies/<id>/edit/',views.EditCurrency.as_view(),name='edit-currency'),
  path('dashboard/currencies/<id>/delete/',views.DeleteCurrency.as_view(),name='delete-currency'),
  
  path('dashboard/users/',views.StaffUsers.as_view(),name='staff-users'),
  path('dashboard/users/id/<user_id>/',views.StaffGeneralProfile.as_view(),name='staff-user'),
  path('dashboard/users/id/<user_id>/block-unblock/',views.StaffBlocOrUnblockUser.as_view(),name='staff-block-unblock-user'),
  
  # seller
  path('dashboard/inventory/',views.Inventory.as_view(),name='inventory'),
  path('dashboard/new-inventory/',views.NewInventory.as_view(),name='new-inventory'),
  path('dashboard/inventory/<id>/images/',views.InventoryImages.as_view(),name='inventory-images'),
  path('dashboard/inventory/<id>/edit/',views.EditInventory.as_view(),name='edit-inventory'),
  path('dashboard/inventory/<id>/delete/',views.DeleteInventory.as_view(),name='delete-inventory'),
  
  path('dashboard/categories/',views.Categories.as_view(),name='categories'),
  path('dashboard/categories/new/',views.NewCategory.as_view(),name='new-category'),
  path('dashboard/categories/<id>/edit/',views.EditCategory.as_view(),name='edit-category'),
  path('dashboard/categories/<id>/delete/',views.DeleteCategory.as_view(),name='delete-category'),
  
  path('dashboard/purchases/',views.Purchases.as_view(),name='purchases'),
  path('dashboard/purchases/new/',views.NewPurchase.as_view(),name='new-purchase'),
  path('dashboard/purchases/<id>/edit/',views.EditPurchase.as_view(),name='edit-purchase'),
  path('dashboard/purchases/<id>/delete/',views.DeletePurchase.as_view(),name='delete-purchase'),
  
  path('dashboard/sales/',views.Sales.as_view(),name='sales'),
  path('dashboard/sales/new/',views.NewSale.as_view(),name='new-sale'),
  path('dashboard/sales/<id>/edit/',views.EditSale.as_view(),name='edit-sale'),
  path('dashboard/sales/<id>/delete/',views.DeleteSale.as_view(),name='delete-sale'),
  path('dashboard/sales/order/<id>/',views.SalesOrder.as_view(),name='sales-order'),
  path('dashboard/sales/wallet/<id>/',views.WithdrawRequest.as_view(),name='sales-withdraw-request'),
  
  # reseller
  path('dashboard/resale/',views.Resales.as_view(),name='resales'),
  path('dashboard/resale/<id>/delete',views.DeleteResale.as_view(),name='delete-resale'),
  path('dahsboard/resale/purchases/',views.ResalePurchases.as_view(),name='resale-purchases'),
  path('dahsboard/resale/purchases/<id>/',views.ResalePurchase.as_view(),name='resale-purchase'),
  path('dahsboard/resale/purchases/<id>/resale/',views.NewResale.as_view(),name='new-resale'),
  
  path('dashboard/reseller/cart/',views.ResellerCart.as_view(),name='reseller-cart'),
  path('dashboard/reseller/cart/cod-checkout/',views.ResellerCODCheckout.as_view(),name='reseller-cod-checkout'),
]
