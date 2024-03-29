from django.dispatch import Signal
from store import models
from django.core.mail import send_mail
from dashboard.function import getOptions, admin_send_mail
from dropshipping.functions import steadfastCreateOrder, steadfastCreateOrderManual, redxCreateParcel
from dropshipping.models import SteadFastDelivery

withdraw_request_submitted = Signal()
def catch_withdraw_request_submitted(sender,withdraw:models.Withdraw,**kwargs):
    options = getOptions()
    if withdraw.wallet_type == 'STORE':
      wallet=models.StoreWallet.objects.get(pk=withdraw.transaction_id)
      email=wallet.store.user.email
    elif withdraw.wallet_type == 'USER':
      wallet=models.UserWallet.objects.get(pk=withdraw.transaction_id)
      email=wallet.user.email
    else:
      wallet=None
      
    admin_send_mail(
        f"{options['name']} - Withdraw requested",
        f"A withdraw of {withdraw.amount} has been requested, Please review in the dashboard",
        [options['site_mail']]
    )
    if wallet:
        admin_send_mail(
            f"{options['name']} - Withdraw requested",
            f"A withdraw of {withdraw.amount} has been requested, you will be notified when it is proceseed!",
            [email]
        )

withdraw_request_approved = Signal()
def catch_withdraw_request_approved(sender,withdraw:models.Withdraw,**kwargs):
    options = getOptions()
    if withdraw.wallet_type == 'STORE':
      wallet=models.StoreWallet.objects.get(pk=withdraw.transaction_id)
      email=wallet.store.user.email
    elif withdraw.wallet_type == 'USER':
      wallet=models.UserWallet.objects.get(pk=withdraw.transaction_id)
      email=wallet.user.email
    else:
      wallet=None
    
    if wallet:
        admin_send_mail(
            f"{options['name']} - Withdraw approved",
            f"A withdraw of {withdraw.amount} has been approved.",
            [email]
        )

become_seller_request_approved = Signal()
def catch_become_seller_request_approved(sender,becomeseller:models.Becomeseller,**kwargs):
    options = getOptions()
    admin_send_mail(
        f"{options['name']} - Become seller request approved",
        f"Congratulations, your request to become a seller at {options['name']} has been approved. Please login and visit the dashboard to begin selling.",
        [becomeseller.user.email]
    )

become_seller_request_declined = Signal()
def catch_become_seller_request_declined(sender,becomeseller:models.Becomeseller,**kwargs):
    options = getOptions()
    admin_send_mail(
        f"{options['name']} - Become seller request declined",
        f"We are sorry to inform you that your request to become a seller at {options['name']} has been declined.",
        [becomeseller.user.email]
    )

become_reseller_request_approved = Signal()
def catch_become_reseller_request_approved(sender,becomereseller:models.Becomereseller,**kwargs):
    options = getOptions()
    admin_send_mail(
        f"{options['name']} - Become reseller request approved",
        f"Congratulations, your request to become a reseller at {options['name']} has been approved. Please login and visit the dashboard to begin reselling.",
        [becomereseller.user.email]
    )

become_reseller_request_declined = Signal()
def catch_become_reseller_request_declined(sender,becomereseller:models.Becomereseller,**kwargs):
    options = getOptions()
    admin_send_mail(
        f"{options['name']} - Become reseller request declined",
        options['site_mail'],
        [becomereseller.user.email]
    )

order_submitted = Signal()
def catch_order_submitted(sender,order:models.Order,**kwargs):
    options = getOptions()
    admin_send_mail(
        f"{options['name']} - Order received",
        f"Your order with ID:{order.id} has been received, you will be notified by mail, when your order has been processed! Our sales team will contact you on {order.customer_phone} concerning delivery.",
        [order.user.email]
    )
    admin_send_mail(
        f"{options['name']} - Order received",
        f"Order with ID:{order.id} has been received, Please login to the dashboard to comfirm this order.",
        [options['site_mail']]
    )

order_processed = Signal()
def catch_order_processed(sender,order:models.Order,**kwargs):
    options = getOptions()
    
    for sale in order.sales.all():
        sale.sale()
        
    admin_send_mail(
        f"{options['name']} - Order processed",
        f"Your order with ID:{order.id} has been processed, Thanks for shopping with {options['name']}.",
        [order.user.email]
    )

order_canceled=Signal()
def catch_order_canceled(sender,order:models.Order,**kwargs):
    options = getOptions()
    admin_send_mail(
        f"{options['name']} - Order canceled",
        f"We are sorry to inform you that your order canceled by admin.",
        [order.user.email]
    )

order_comfirmed=Signal()
def catch_order_comfirmed(sender,order:models.Order,**kwargs):
    steadfastCreateOrder(order=order)
    #success,response_text=redxCreateParcel(order=order)
    
    options = getOptions()
    delivery=SteadFastDelivery.objects.filter(invoice=order.id).first()
    if delivery:
        message=f"Your order with ID {order.id} and Tracking ID {delivery.tracking_code} has been comfirmed and will be delivered to you, you can log in to your profile and check the progess."
    else:
        message =  f"Your order with ID {order.id} has been comfirmed and will be delivered to you, you can log in to your profile and check the progess."
        
    admin_send_mail(
        f"{options['name']} - Order comfirmed",
        message,
        [order.user.email]
    )

order_declined=Signal()
def catch_order_declined(sender,order:models.Order,**kwargs):
    options = getOptions()
    admin_send_mail(
        f"{options['name']} - Order declined",
        f"We are sorry to inform you that your order with ID {order.id} was declined.",
        [order.user.email]
    )

order_submitted_for_delivery=Signal()
def catch_order_submitted_for_delivery(sender,order:models.Order,**kwargs):
    options = getOptions()
    delivery=SteadFastDelivery.objects.filter(invoice=order.id).first()
    message=f"Your order with ID {order.id} and tracking ID {delivery.tracking_code} has been submitted for delivery, you will receive it soon." if delivery else f"Your order with ID {order.id} has been submitted for delivery, you will receive it soon."
    admin_send_mail(
        f"{options['name']} - Order submitted for delivery",
        message,
        [order.user.email]
    )