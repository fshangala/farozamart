def cartCount(request):
  if not request.user.is_anonymous:
    return {
      'cart_items_count':request.user.sales.filter(cart=True).count()
    }
  
  return {}