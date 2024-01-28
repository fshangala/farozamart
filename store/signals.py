from django.dispatch import Signal
from store import models
from django.core.mail import send_mail
from dashboard.function import getOptions

order_submitted = Signal()

def catch_order_submitted(sender,order:models.Order,**kwargs):
    options = getOptions()
    send_mail(
        f"{options['name']} - Order received",
        f"Your order with ID:{order.id} has been received, you will be notified by mail, when your order has been processed! Our sales team will contact you on {order.customer_phone} concerning delivery.",
        options['site_mail'],
        [order.user.email]
    )

order_processed = Signal()

def catch_order_processed(sender,order:models.Order,**kwargs):
    options = getOptions()
    send_mail(
        f"{options['name']} - Order processed",
        f"Your order with ID:{order.id} has been processed, Thanks for shopping with {options['name']}.",
        options['site_mail'],
        [order.user.email]
    )