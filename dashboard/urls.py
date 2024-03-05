from django.urls import path, include
from dashboard import views

app_name="dashboard"
urlpatterns = [
  path('',views.Dashboard.as_view(),name="dashboard"),
  path('settings/',views.GeneralSettings.as_view(),name='general-settings'),
  path('mailing-settings/',views.Mailing.as_view(),name='mailing-settings'),
]
