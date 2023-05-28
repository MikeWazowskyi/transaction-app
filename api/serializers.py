import re

from django.db.models import F
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .exceptions import InvalidTransaction

User = get_user_model()


class TransactionSerializers(serializers.Serializer):
    """Transaction serializer class"""
    receivers = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        write_only=True
    )
    amount = serializers.FloatField(write_only=True)

    def update(self, instance, validated_data):
        amount_per_reviver = round(
            (validated_data['amount'] /
             len(validated_data['receivers'])), 2
        )  # Calculate amount per receiver
        instance.account = F('account') - validated_data['amount']
        instance.save()
        User.objects.filter(
            tax_id_number__in=validated_data['receivers']).update(
            account=F('account') + amount_per_reviver)
        return instance

    def validate_amount(self, amount):
        pattern = re.compile(r'^\d+(\.\d{1,2})?$')
        if amount <= 0:
            raise InvalidTransaction('Amount must be greater then 0')
        if not re.match(pattern, str(amount)):
            raise InvalidTransaction('Invalid amount format, must be 0.00')
        sender = self.instance
        if sender.account < amount:
            raise InvalidTransaction('Not enough amount on account')
        return amount

    def validate_receivers(self, receivers_data):
        sender = self.instance
        receivers = User.objects.filter(
            tax_id_number__in=receivers_data)
        if receivers.count() != len(receivers_data):
            raise InvalidTransaction('Invalid tax id number')
        if sender in receivers:
            raise InvalidTransaction('Sender in receivers')
        return receivers_data


class UserSerializer(serializers.ModelSerializer):
    """User model serializer class"""

    class Meta:
        model = User
        fields = ('id', 'full_name')
