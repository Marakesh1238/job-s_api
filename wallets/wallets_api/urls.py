from django.urls import path

urlpatterns = [
    path('api/v1/wallets/<uuid:wallet_uuid>/operation',
         ),
    path('api/v1/wallets/<uuid:wallet_uuid>',
         ),
]
