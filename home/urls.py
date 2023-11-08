from django.urls import path
from home import views as homeViews

app_name="home"
urlpatterns = [
    path('', homeViews.Home.as_view(), name='home'),
]
