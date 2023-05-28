from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class CustomUserManagerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_user = User.objects.create_user(
            email='email@default.com',
            first_name='FirstName',
            last_name='LastName',
            password='DefaultPass',
            tax_id_number='000000000000'
        )

    def test_create_user(self):
        self.assertEqual(self.valid_user.email, 'email@default.com')
        self.assertEqual(self.valid_user.first_name, 'FirstName')
        self.assertEqual(self.valid_user.last_name, 'LastName')
        self.assertEqual(self.valid_user.tax_id_number, '000000000000')
        self.assertEqual(self.valid_user.account, 0.0)
        self.assertTrue(self.valid_user.is_active)
        self.assertFalse(self.valid_user.is_staff)

    def test_create_negative_account(self):
        invalid_account_user = User(
            email='email2@default.com',
            first_name='FirstName1',
            last_name='LastName1',
            password='DefaultPass1',
            tax_id_number='000000000001',
            account=-10.0,
        )

        with self.assertRaises(Exception):
            invalid_account_user.full_clean()

    def test_email_field_unique(self):
        invalid_email_user = User(
            email='email@default.com',
            first_name='FirstName1',
            last_name='LastName1',
            password='DefaultPass1',
            tax_id_number='000000000001'
        )
        with self.assertRaises(Exception):
            invalid_email_user.full_clean()

    def test_tax_id_number_field_unique(self):
        invalid_email_user = User(
            email='email1@default.com',
            first_name='FirstName1',
            last_name='LastName1',
            password='DefaultPass1',
            tax_id_number='000000000000'
        )
        with self.assertRaises(Exception):
            invalid_email_user.full_clean()

    def test_tax_id_number_has_appropriate_length(self):
        long_tax_id_number_user = User(
            email='email1@default.com',
            first_name='FirstName1',
            last_name='LastName1',
            password='DefaultPass1',
            tax_id_number='0000000000000'
        )
        short_tax_id_number_user = User(
            email='email1@default.com',
            first_name='FirstName1',
            last_name='LastName1',
            password='DefaultPass1',
            tax_id_number='00000000000'
        )
        invalid_tax_id_number_user = User(
            email='email1@default.com',
            first_name='FirstName1',
            last_name='LastName1',
            password='DefaultPass1',
            tax_id_number='00000000000O'
        )
        with self.assertRaises(Exception):
            long_tax_id_number_user.full_clean()
        with self.assertRaises(Exception):
            short_tax_id_number_user.full_clean()
        with self.assertRaises(Exception):
            invalid_tax_id_number_user.full_clean()

    def test_required_fields(self):
        user = User(email='test@example.com')
        with self.assertRaises(Exception) as context:
            user.full_clean()
        self.assertIn('first_name', context.exception.error_dict)
        self.assertIn('last_name', context.exception.error_dict)
        self.assertIn('tax_id_number', context.exception.error_dict)
        self.assertIn('password', context.exception.error_dict)

    def test_get_full_name(self):
        user = User.objects.get(email='email@default.com')
        full_name = user.full_name
        self.assertEqual(full_name, 'FirstName LastName')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.valid_user.delete()
