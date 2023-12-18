"""
URL configuration for farozamart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from store.api.routes import router as storeRouter
from accounts.api.routes import router as accountsRouter

router = DefaultRouter()
router.registry.extend(storeRouter.registry)
router.registry.extend(accountsRouter.registry)

urlpatterns = [
    path('favicon.ico',RedirectView.as_view(url=staticfiles_storage.url('favicon.png'))),
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('accounts/',include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('store/', include('store.urls')),
    path('dropshipping/',include('dropshipping.urls')),
    path('paymentgateway/',include('paymentgateway.urls')),
    path('api/v1/',include(router.urls)),
    path('api/auth/login/',views.obtain_auth_token)
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
