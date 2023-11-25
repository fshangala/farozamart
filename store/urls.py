from django.urls import path
from store import views

app_name='store'
urlpatterns = [
  path('shop/',views.Shop.as_view(),name='shop'),
  path('shop/listing/<id>/',views.Listing.as_view(),name='listing'),
  path('shop/cart/',views.Cart.as_view(),name='cart'),
  path('shop/cart/<id>/delete',views.DeleteCartItem.as_view(),name='delete-cart-item'),

  path('become-seller/',views.BecomeSeller.as_view(),name='become-seller'),
  
  path('dashboard/inventory/',views.Inventory.as_view(),name='inventory'),
  path('dashboard/new-inventory/',views.NewInventory.as_view(),name='new-inventory'),
  path('dashboard/inventory/<id>/edit/',views.EditInventory.as_view(),name='edit-inventory'),
  path('dashboard/inventory/<id>/delete/',views.DeleteInventory.as_view(),name='delete-inventory'),
  
  path('dashboard/purchases/',views.Purchases.as_view(),name='purchases'),
  path('dashboard/purchases/new/',views.NewPurchase.as_view(),name='new-purchase'),
  path('dashboard/purchases/<id>/edit/',views.EditPurchase.as_view(),name='edit-purchase'),
  path('dashboard/purchases/<id>/delete/',views.DeletePurchase.as_view(),name='delete-purchase'),
  
  path('dashboard/sales/',views.Sales.as_view(),name='sales'),
  path('dashboard/sales/new/',views.NewSale.as_view(),name='new-sale'),
  path('dashboard/sales/<id>/edit/',views.EditSale.as_view(),name='edit-sale'),
  path('dashboard/sales/<id>/delete/',views.DeleteSale.as_view(),name='delete-sale'),
]
