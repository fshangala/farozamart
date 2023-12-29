from rest_framework.routers import DefaultRouter
from store.api import views as apiviews

router = DefaultRouter()
router.register(r'store/listing',apiviews.ListingViewSet,basename='store')
router.register(r'store/cart',viewset=apiviews.CartViewSet,basename='cart')