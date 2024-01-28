from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    
    def ready(self):
        from store import signals     
        signals.order_submitted.connect(signals.catch_order_submitted)
        signals.order_processed.connect(signals.catch_order_processed)
        signals.withdraw_request_submitted.connect(signals.catch_withdraw_request_submitted)
