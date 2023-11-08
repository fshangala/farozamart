from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class Dashboard(View):
  template_name='dashboard/base.html'
  def get(self, request):
    context={}
    return render(request,self.template_name,context)