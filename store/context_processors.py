from store import models

def cartCount(request):
  if not request.user.is_anonymous:
    cart_items_count=0
    order=models.Order.objects.filter(status='DRAFT').first()
    if order:
      cart_items_count=order.sales.count()
    return {
      'cart_items_count':cart_items_count
    }
  
  return {}