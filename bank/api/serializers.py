from rest_framework import serializers

from bank.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'account', 'amount', 'description',
                  'trans_date', 'trans_type')
