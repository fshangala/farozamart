from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from store import models
from store.api import serializers

class ListingViewSet(ViewSet):
  permission_classes=[]
  def list(self,request,*args,**kwargs):
    listing = models.Purchase.objects.all()
    listingSerializer = serializers.PurchaseSerializer(listing, many=True)
    return Response(listingSerializer.data)