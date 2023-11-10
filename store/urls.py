from django.urls import path
from store import views

app_name='store'
urlpatterns = [
  path('become-seller/',views.BecomeSeller.as_view(),name='become-seller'),
  path('inventory/',views.Inventory.as_view(),name='inventory'),
]
