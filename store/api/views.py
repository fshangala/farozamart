from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from store import models, functions
from store.api import serializers
from django.shortcuts import get_object_or_404

class ListingViewSet(ViewSet):
  def list(self,request,*args,**kwargs):
    listing = models.Purchase.objects.all()
    listingSerializer = serializers.PurchaseSerializer(listing, many=True)
    return Response(listingSerializer.data)
  
  def retrieve(self,request,pk,*args,**kwargs):
    listing = models.Purchase.objects.get(pk=pk)
    listingSerializer = serializers.PurchaseSerializer(listing)
    return Response(listingSerializer.data)
  
  @action(detail=True,methods=['post'])
  def add_to_cart(self,request,pk):
    listing = models.Purchase.objects.get(pk=pk)
    serializer = serializers.AddToCartSerializer(user=request.user,listing=listing,data=request.POST)
    if serializer.is_valid():
      serializer.save()
      sales = models.Sale.objects.filter(user=request.user,cart=True,approved=False)
      saleSerializer = serializers.SalesSerializer(sales,many=True)
      return Response(saleSerializer.data)
    return Response(serializer.error_messages,status=500)

class CartViewSet(ViewSet):
  @action(detail=False,methods=['get'])
  def get_cart(self,request,*args,**kwargs):
    order = request.user.orders.get(draft=True)
    orderSerializer = serializers.OrderSerializer(order)
    return Response(orderSerializer.data)
  
  @action(detail=True,methods=['get'])
  def cod_checkout(self,request,pk,*args,**kwargs):
    order = functions.CODPayment(pk=pk)
    orderSerializer = serializers.OrderSerializer(order)
    return Response(orderSerializer.data)
    