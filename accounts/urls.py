from django.urls import path
from accounts import views

app_name='accounts'
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/',views.Logout.as_view(), name='logout'),
    path('register', views.Register.as_view(), name='register'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit-profile'),
    path('profile/update-picture/', views.UpdateProfilePicture.as_view(), name='update-picture'),
    path('become-seller/',views.BecomeSeller.as_view(), name='become-seller'),
    path('become-reseller/',views.BecomeReseller.as_view(), name='become-reseller'),
    
    path('profile/verify-user-email/',views.VerifyUserEmail.as_view(),name='verify-user-email'),
]