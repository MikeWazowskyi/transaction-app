import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class TransactionViewSetTest(TestCase):
    def setUp(self) -> None:
        self.users_data = (
            dict(
                email='email0@default.com',
                first_name='FirstName0',
                last_name='LastName0',
                password='DefaultPass0',
                tax_id_number='000000000000',
                account=100.00
            ),
            dict(
                email='email1@default.com',
                first_name='FirstName1',
                last_name='LastName1',
                password='DefaultPass1',
                tax_id_number='000000000001'
            ),
            dict(
                email='email2@default.com',
                first_name='FirstName2',
                last_name='LastName2',
                password='DefaultPass2',
                tax_id_number='000000000002'
            ),
        )

        self.users = User.objects.bulk_create(
            [User(**user_data) for user_data in self.users_data]
        )
        self.amount = self.users[0].account / 2
        self.remainder = self.users[0].account - self.amount
        self.sender = self.users[0]
        self.receivers = [user.tax_id_number for user in self.users[1:]]
        self.client = APIClient()

    def test_get_transaction_endpoint_response_ok(self):
        response = self.client.get('/api/transaction/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transaction_endpoint_return_users_amount(self):
        response = self.client.get('/api/transaction/')
        self.assertEqual(len(response.data.get('results')), 3)

    def test_get_transaction_endpoint_return_limited_users_amount(self):
        limited_response = self.client.get('/api/transaction/?limit=1')
        self.assertEqual(len(limited_response.data.get('results')), 1)
        limited_response = self.client.get(
            '/api/transaction/?limit=1&page=2')
        self.assertEqual(len(limited_response.data.get('results')), 1)

    def test_update_transaction_endpoint_response_ok(self):
        valid_data = json.dumps(
            {'receivers': self.receivers, 'amount': self.amount})
        response = self.client.patch(f'/api/transaction/{self.sender.id}/',
                                     valid_data,
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_transaction_endpoint_make_transaction(self):
        valid_data = json.dumps(
            {'receivers': self.receivers, 'amount': self.amount})
        self.client.patch(f'/api/transaction/{self.sender.id}/',
                          valid_data,
                          content_type='application/json')
        self.sender.refresh_from_db()
        self.assertEqual(self.sender.account,
                         self.remainder)
        for receiver in self.receivers:
            self.assertEqual(
                User.objects.get(tax_id_number=receiver).account,
                round(self.amount / len(self.receivers), 2))

    def test_update_transaction_endpoint_return_error_on_invalid_receivers(
            self):
        empty_receivers_data = json.dumps(
            {'receivers': [], 'amount': self.amount}
        )
        response = self.client.patch(f'/api/transaction/{self.sender.id}/',
                                     empty_receivers_data,
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        sender_in_receivers_data = json.dumps(
            {'receivers': self.receivers.append(self.sender.account),
             'amount': self.amount}
        )
        response = self.client.patch(f'/api/transaction/{self.sender.id}/',
                                     sender_in_receivers_data,
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_transaction_endpoint_return_error_invalid_amount(
            self):
        too_big_amount_data = json.dumps(
            {'receivers': self.receivers,
             'amount': self.users[0].account * 2}
        )
        response = self.client.patch(
            f'/api/transaction/{self.sender.id}/',
            too_big_amount_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        zero_amount_data = json.dumps(
            {'receivers': self.receivers,
             'amount': -20.00}
        )
        response = self.client.patch(
            f'/api/transaction/{self.sender.id}/',
            zero_amount_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
