from django.conf import settings
import requests
from dashboard.function import getOptions
from store.models import Order
from dropshipping import models
from django.utils import timezone

def steadfastCreateOrder(order:Order):
  option=getOptions()
  
  if option.get('steadfast_status') == 'ACTIVATED':
    if option.get('steadfast_api_key') == 'test' and option.get('steadfast_api_secrete') == 'test':
      resulte={
        "status": 200,
        "message": "Consignment has been created successfully.",
        "consignment": {
          "consignment_id": 1424107,
          'invoice':str(order.id),
          "tracking_code": str(timezone.datetime.now().timestamp()),
          'recipient_name':order.user.profile.full_name(),
          'recipient_phone':order.user.profile.phone,
          'recipient_address':order.user.profile.address,
          "cod_amount": 0,
          "status": "in_review",
          "note": "Deliver within 3PM",
          "created_at": str(timezone.datetime.now()),
          "updated_at": str(timezone.datetime.now())
        }
      }
      resulte = resulte['consignment']
      models.SteadFastDelivery.objects.create(
        consignment_id=resulte['consignment_id'],
        invoice=resulte['invoice'],
        tracking_code=resulte['tracking_code'],
        status=resulte['status'],
        created_at=resulte['created_at'],
        updated_at=resulte['updated_at']
      )
    else:
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
        resulte = response.json()['consignment']
        models.SteadFastDelivery.objects.create(
          consignment_id=resulte['consignment_id'],
          invoice=resulte['invoice'],
          tracking_code=resulte['tracking_code'],
          status=resulte['status'],
          created_at=resulte['created_at'],
          updated_at=resulte['updated_at']
        )
      