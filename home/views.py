from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class Home(View):
  template_name='base.html'
  def get(self,request):
    context={}
    return render(request,self.template_name,context)