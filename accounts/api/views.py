from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from accounts.api import serializers
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import action
from accounts.forms import RegistrationForm

class TokenUser(ViewSet):
  def list(self,request,*args,**kwargs):
    userSerializer = serializers.UserSerializer(instance=request.user)
    return Response(userSerializer.data)

class RegisterUser(ViewSet):
  authentication_classes=[]
  permission_classes=[]
  @action(detail=False,methods=['post'])
  def register(self,request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
      form.save()
      return Response(data={'registered':True})
    
    return Response(data=form.errors)