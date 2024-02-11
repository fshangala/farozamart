from django.conf import settings
import requests
from dashboard.function import getOptions
from store.models import Order
from dropshipping import models
from django.utils import timezone
import json

def steadfastCreateOrderManual(order:Order,recipient_name:str,recipient_phone:str,recipient_address:str):
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
          'recipient_name':order.customer_name,
          'recipient_phone':order.customer_phone,
          'recipient_address':order.customer_address,
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
          'recipient_name':order.customer_name,
          'recipient_phone':order.customer_phone,
          'recipient_address':order.customer_address,
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
      return True,'Test delivery created. This will not appear in steadfast dashboard.'
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
      response = requests.post('https://portal.steadfast.com.bd/api/v1/create-order',data=data,headers=header)
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
        return True,'Order successfully submitted for delivery!'
      else:
        return False,f"status_code:{response.status_code}; response_text:{response.text}"
  else:
    return False,'Steadfast is deactivated, order not submitted for delivery!'

def redxCreateParcel(order:Order):
  headers={
    'API-ACCESS-TOKEN': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4NDgxMDQiLCJpYXQiOjE3MDY1OTg3MDIsImlzcyI6IllDTWJHdGM4eWpnRTRJQ1dWQm9nSWVJZUM4V0dDNUFRIiwic2hvcF9pZCI6ODQ4MTA0LCJ1c2VyX2lkIjoyNTYzMTkzfQ.MfWXh7ebg9HVrji8VkXgAfWfOcOG30NGBU52vdTqSdw',
    'Content-Type': 'application/json',
  }
  payload={
    "customer_name": order.customer_name,
    "customer_phone": order.customer_phone,
    "delivery_area": order.delivery_area,
    "delivery_area_id": 1,
    "customer_address": order.customer_address,
    "merchant_invoice_id": str(order.id),
    "cash_collection_amount": order.total_cost_number(),
    "parcel_weight": 500,
    "instruction": "",
    "value": 100,
    "is_closed_box": False,
    "parcel_details_json": []
  }
  response=requests.post('https://sandbox.redx.com.bd/v1.0.0-beta/parcel',data=json.dumps(payload),headers=headers)
  if response.status_code == 201:
    tracking_id = response.json()['tracking_id']
    order.tracking_id=tracking_id
    return True,f'Order successfully submitted for delivery! {response.text}'
  else:
    return False,f"status_code:{response.status_code}; response_text:{response.text}"
  