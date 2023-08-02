from django.db.models import F

from api.exceptions import InvalidTransaction


def perform_transactions(sender, receivers, validated_data):
    amount = validated_data['amount']
    if sender.account < amount:
        raise InvalidTransaction('Not enough amount on account')
    amount_per_reviver = round(
        (amount / len(validated_data['receivers'])), 2
    )
    sender.account = F('account') - amount
    sender.save()
    receivers.update(account=F('account') + amount_per_reviver)
    return sender, receivers
