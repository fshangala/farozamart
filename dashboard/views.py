from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
class Dashboard(LoginRequiredMixin,UserPassesTestMixin,View):
  template_name='dashboard/dashboard.html'
  
  def test_func(self):
    return self.request.user.profile.is_seller or self.request.user.is_staff
  
  def get(self, request):
    context={
      'sidebar_menu_dashboard_class':'active'
    }
    return render(request,self.template_name,context)