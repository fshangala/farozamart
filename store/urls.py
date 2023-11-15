from django.urls import path
from store import views

app_name='store'
urlpatterns = [
  path('become-seller/',views.BecomeSeller.as_view(),name='become-seller'),
  
  path('dashboard/inventory/',views.Inventory.as_view(),name='inventory'),
  path('dashboard/new-inventory/',views.NewInventory.as_view(),name='new-inventory'),
  path('dashboard/inventory/<id>/edit/',views.EditInventory.as_view(),name='edit-inventory'),
  path('dashboard/inventory/<id>/delete/',views.DeleteInventory.as_view(),name='delete-inventory'),
  
  path('dashboard/purchases/',views.Purchases.as_view(),name='purchases'),
  path('dashboard/purchases/new/',views.NewPurchase.as_view(),name='new-purchase'),
  path('dashboard/purchases/<id>/edit/',views.EditPurchase.as_view(),name='edit-purchase'),
  path('dashboard/purchases/<id>/delete/',views.DeletePurchase.as_view(),name='delete-purchase'),
  
  path('dashboard/sales/',views.Inventory.as_view(),name='sales'),
]
