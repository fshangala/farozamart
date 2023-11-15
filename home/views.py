from django.shortcuts import render
from django.views.generic import View
from store.models import Sale

# Create your views here.
home_context={
  'nav_home_class':'active'
}
class Home(View):
  template_name='home/home.html'
  def get(self,request):
    context=home_context
    latest_sales = Sale.objects.all()[:8]
    context['latest_sales'] = latest_sales
    return render(request,self.template_name,context)