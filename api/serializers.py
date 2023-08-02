import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .exceptions import InvalidTransaction

User = get_user_model()


class TransactionSerializers(serializers.Serializer):
    """Transaction serializer class"""
    receivers = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )
    amount = serializers.FloatField()

    def update(self, instance, validated_data):
        return validated_data

    def validate_amount(self, amount):
        pattern = re.compile(r'^\d+(\.\d{1,2})?$')
        if amount <= 0:
            raise InvalidTransaction('Amount must be greater then 0')
        if not re.match(pattern, str(amount)):
            raise InvalidTransaction('Invalid amount format, must be 0.00')
        return amount

    def validate_receivers(self, receivers_data):
        receivers = User.objects.filter(
            tax_id_number__in=receivers_data)
        if receivers.count() != len(receivers_data):
            raise InvalidTransaction('Invalid tax id number')
        if self.instance in receivers:
            raise InvalidTransaction('Sender in receivers')
        return receivers_data


class UserSerializer(serializers.ModelSerializer):
    """User model serializer class"""

    class Meta:
        model = User
        fields = ('id', 'full_name')
