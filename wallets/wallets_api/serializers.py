from rest_framework import serializers


class OperationSerializer(serializers.Serializer):
    OPERATION_CHOICES = ['DEPOSIT', 'WITHDRAW']

    operation_type = serializers.ChoiceField(choices=OPERATION_CHOICES)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)

    def __init__(self, *args, **kwargs):
        self.wallet = kwargs.pop('wallet', None)
        super().__init__(*args, **kwargs)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value

    def validate(self, attrs):
        if (
            attrs['operation_type'] == 'WITHDRAW'
            and self.wallet.balance < attrs['amount']
        ):
            raise serializers.ValidationError("Insufficient funds")
        return attrs
