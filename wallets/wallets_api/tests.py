from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Wallet
from decimal import Decimal


class WalletTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.wallet = Wallet.objects.create(balance=1000)

    def test_deposit(self):
        url = reverse('wallets_api:wallet-operation',
                      kwargs={'wallet_uuid': self.wallet.id})
        response = self.client.post(url, {
            'operation_type': 'DEPOSIT',
            'amount': 500
        })
        self.assertEqual(response.status_code, 200)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1500)

    def test_withdraw(self):
        url = reverse('wallets_api:wallet-operation',
                      kwargs={'wallet_uuid': self.wallet.id})
        response = self.client.post(url, {
            'operation_type': 'WITHDRAW',
            'amount': 300
        })
        self.assertEqual(response.status_code, 200)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 700)

    def test_insufficient_funds(self):
        url = reverse('wallets_api:wallet-operation',
                      kwargs={'wallet_uuid': self.wallet.id})
        response = self.client.post(url, {
            'operation_type': 'WITHDRAW',
            'amount': 1500
        })
        self.assertEqual(response.status_code, 400)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1000)

    def test_get_balance(self):
        url = reverse('wallets_api:wallet-balance',
                      kwargs={'wallet_uuid': self.wallet.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['balance'], Decimal('1000.00'))

    def test_invalid_operation_type(self):
        url = reverse('wallets_api:wallet-operation',
                      kwargs={'wallet_uuid': self.wallet.id})
        response = self.client.post(url, {
            'operation_type': 'INVALID',
            'amount': 100
        })
        self.assertEqual(response.status_code, 400)

    def test_negative_amount(self):
        url = reverse('wallets_api:wallet-operation',
                      kwargs={'wallet_uuid': self.wallet.id})
        response = self.client.post(url, {
            'operation_type': 'DEPOSIT',
            'amount': -100
        })
        self.assertEqual(response.status_code, 400)
