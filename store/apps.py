from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    
    def ready(self):
        from store import signals     
        # order
        signals.order_submitted.connect(signals.catch_order_submitted)
        signals.order_processed.connect(signals.catch_order_processed)
        
        # withdraw
        signals.withdraw_request_submitted.connect(signals.catch_withdraw_request_submitted)
        signals.withdraw_request_approved.connect(signals.catch_withdraw_request_approved)
        
        # seller
        signals.become_seller_request_approved.connect(signals.catch_become_seller_request_approved)
        signals.become_seller_request_declined.connect(signals.catch_become_seller_request_declined)
        
        # reseller
        signals.become_reseller_request_approved.connect(signals.catch_become_reseller_request_approved)
        signals.become_reseller_request_declined.connect(signals.catch_become_reseller_request_declined)
        
        # staff
        signals.order_canceled.connect(signals.catch_order_canceled)
