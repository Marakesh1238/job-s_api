from django.urls import path

from .views import WalletOperationView, WalletBalanceView


urlpatterns = [
    path(
        'api/v1/wallets/<uuid:wallet_uuid>/operation/',
        WalletOperationView.as_view(),
        name='wallet-operation'
    ),
    path(
        'api/v1/wallets/<uuid:wallet_uuid>/',
        WalletBalanceView.as_view(),
        name='wallet-balance'
    ),
]

app_name = 'wallets_api'