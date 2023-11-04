from django.urls import path
from home import views as homeViews

urlpatterns = [
    path('', homeViews.Home.as_view()),
]
