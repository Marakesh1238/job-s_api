from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Wallet
from .serializers import OperationSerializer


class WalletOperationView(APIView):

    @transaction.atomic
    def post(self, request, wallet_uuid):
        # Блокируем запись до конца транзакции
        wallet = get_object_or_404(
            Wallet.objects.select_for_update(),
            id=wallet_uuid
        )

        serializer = OperationSerializer(data=request.data, wallet=wallet)

        if serializer.is_valid():
            data = serializer.validated_data

            if data['operation_type'] == 'DEPOSIT':
                wallet.balance += data['amount']
            else:
                wallet.balance -= data['amount']

            wallet.save(update_fields=['balance'])

            return Response({
                'status': 'success',
                'new_balance': wallet.balance
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletBalanceView(APIView):

    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, id=wallet_uuid)
        return Response({'balance': wallet.balance})
