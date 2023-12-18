from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from accounts.api import serializers
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class TokenUser(ViewSet):
  def list(self,request,*args,**kwargs):
    userSerializer = serializers.UserSerializer(instance=request.user)
    return Response(userSerializer.data)