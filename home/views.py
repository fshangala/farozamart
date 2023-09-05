from django.shortcuts import render
from django.views.generic import View
from store.models import Purchase

# Create your views here.
home_context={
  'nav_home_class':'active'
}
class Home(View):
  template_name='home/home.html'
  def get(self,request):
    context=home_context
    latest_listings = Purchase.objects.all()[:8]
    context['latest_listings'] = latest_listings
    return render(request,self.template_name,context)