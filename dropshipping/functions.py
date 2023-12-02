from django.conf import settings
import requests
from dashboard.function import getOptions
from store.models import Order
from dropshipping import models

def steadfastCreateOrder(order:Order):
  option=getOptions()
  
  if option.get('steadfast_api_key') and option.get('steadfast_api_secrete'):
    header={
      'Api-Key':option.get('steadfast_api_key'),
      'Api-Secrete':option.get('steadfast_api_secrete'),
      'Content-Type':'application/json'
    }
    data={
      'invoice':order.id,
      'recipient_name':order.user.profile.full_name(),
      'recipient_phone':order.user.profile.phone,
      'recipient_address':order.user.profile.address,
      'cod_amount':0
    }
    response = requests.post(settings.STEADFAST_BASEURL+'/create-order',data=data,header=header)
    if response.status_code == 200:
      resulte = response.json()
      models.SteadFastDelivery.objects.create(
        consignment_id=resulte['consignment_id'],
        invoice=resulte['invoice'],
        tracking_code=resulte['tracking_code'],
        created_at=resulte['created_at'],
        updated_at=resulte['updated_at']
      )
      