from django.urls import path
from dropshipping import views

app_name='dropshipping'
urlpatterns = [
    path('steadfast-configuration/',views.SteadfastConfiguration.as_view(),name="steadfast-configuration"),
]
