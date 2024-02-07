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

withdraw_request_submitted = Signal()
def catch_withdraw_request_submitted(sender,withdraw:models.Withdraw,**kwargs):
    options = getOptions()
    send_mail(
        f"{withdraw.wallet.store.name} at {options['name']} - Withdraw requested",
        f"A withdraw from {withdraw.wallet.store.name} has been requested, Please review in the dashboard",
        options['site_mail'],
        [options['site_mail']]
    )
    send_mail(
        f"{withdraw.wallet.store.name} at {options['name']} - Withdraw requested",
        f"A withdraw from {withdraw.wallet.store.name} has been requested, you will be notified when it is proceseed!",
        options['site_mail'],
        [withdraw.wallet.store.email]
    )

withdraw_request_approved = Signal()
def catch_withdraw_request_approved(sender,withdraw:models.Withdraw,**kwargs):
    options = getOptions()
    send_mail(
        f"{withdraw.wallet.store.name} at {options['name']} - Withdraw approved",
        f"A withdraw from {withdraw.wallet.store.name} has been approved.",
        options['site_mail'],
        [withdraw.wallet.store.email]
    )

become_seller_request_approved = Signal()
def catch_become_seller_request_approved(sender,becomeseller:models.Becomeseller,**kwargs):
    options = getOptions()
    send_mail(
        f"{options['name']} - Become seller request approved",
        f"Congratulations, your request to become a seller at {options['name']} has been approved. Please login and visit the dashboard to begin selling.",
        options['site_mail'],
        [becomeseller.user.email]
    )

become_seller_request_declined = Signal()
def catch_become_seller_request_declined(sender,becomeseller:models.Becomeseller,**kwargs):
    options = getOptions()
    send_mail(
        f"{options['name']} - Become seller request declined",
        f"We are sorry to inform you that your request to become a seller at {options['name']} has been declined.",
        options['site_mail'],
        [becomeseller.user.email]
    )

become_reseller_request_approved = Signal()
def catch_become_reseller_request_approved(sender,becomereseller:models.Becomereseller,**kwargs):
    options = getOptions()
    send_mail(
        f"{options['name']} - Become reseller request approved",
        f"Congratulations, your request to become a reseller at {options['name']} has been approved. Please login and visit the dashboard to begin reselling.",
        options['site_mail'],
        [becomereseller.user.email]
    )

become_reseller_request_declined = Signal()
def catch_become_reseller_request_declined(sender,becomereseller:models.Becomereseller,**kwargs):
    options = getOptions()
    send_mail(
        f"{options['name']} - Become reseller request declined",
        f"We are sorry to inform you that your request to become a reseller at {options['name']} has been declined.",
        options['site_mail'],
        [becomereseller.user.email]
    )

order_canceled=Signal()
def catch_order_canceled(sender,order:models.Order,**kwargs):
    options = getOptions()
    send_mail(
        f"{options['name']} - Order canceled",
        f"We are sorry to inform you that your order canceled by admin.",
        options['site_mail'],
        [order.user.email]
    )