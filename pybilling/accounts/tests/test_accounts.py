# coding=utf-8
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.test import TestCase

from accounts.models import UserAccount, PersonalDataPerson


class UserAccountTest(TestCase):
    def test_create_account(self):
        user, created = UserAccount.objects.get_or_create(name='Dmitry')
        user.refresh_from_db()

        self.assertTrue(created)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, 'Dmitry')
        self.assertEqual(user.balance, 0)
        self.assertEqual(user.bonus_balance, 0)
        self.assertEqual(user.bonus_balance, 0)
        self.assertEqual(user.language, 'ru')

    def test_create_user_contact(self):
        user, created = UserAccount.objects.get_or_create(name='Dmitry')

        email1 = user.update_contact('main', 'email', 'dmitry@shyliaev.com', validator=validate_email)
        self.assertEqual('main', email1.name)
        self.assertEqual('email', email1.type)
        self.assertEqual('dmitry@shyliaev.com', email1.address)

        email2 = user.update_contact(' main ', '  email', '  dmitry@shyliaev.com ', validator=validate_email)
        self.assertEqual('main', email2.name)
        self.assertEqual('email', email2.type)
        self.assertEqual('dmitry@shyliaev.com', email2.address)

        try:
            user.update_contact('main', 'email', 'dmitryshyliaev.com', validator=validate_email)
        except ValidationError, ex:
            self.assertEqual(1, len(ex.messages))
            self.assertEqual('Enter a valid email address.', ex.messages[0])

    def test_set_personal_data(self):
        user, created = UserAccount.objects.get_or_create(name='Dmitry')

        pers_data1 = user.update_personal_data(PersonalDataPerson,
                                               fio="Дмитрий Шиляев",
                                               birth='1983-09-05',
                                               postal_index=610001, postal_address='Address Postal',
                                               phone='+7 495 6680903',
                                               passport='8734 238764234 239874',
                                               email='lkdfds@ldkjfs.com'
                                               )

        self.assertEqual('Dmitrij Shilyaev', pers_data1.fio_lat)

        # access to common_data from extended data
        self.assertEqual('PersonalDataPerson', pers_data1.common_data.type)
        self.assertEqual(False, pers_data1.common_data.default)
        self.assertEqual(False, pers_data1.common_data.verified)

        # access to extended data from common data
        self.assertEqual('Dmitrij Shilyaev', pers_data1.common_data.personaldataperson.fio_lat)

        try:
            pers_data2 = user.update_personal_data(PersonalDataPerson,
                                                   fio="Збигнев Бжезински",
                                                   birth='1983-09-05',
                                                   postal_index=610001, postal_address='Address Postal',
                                                   phone='+7 4951 6680903',
                                                   passport='8734 238764234 239874',
                                                   email='lkdfdsldkjfs.com'
                                                   )
        except ValidationError, ex:
            self.assertEqual(2, len(ex.error_dict))
            self.assertTrue('email' in ex.error_dict)
            self.assertTrue('phone' in ex.error_dict)


        # adding extra data
        pers_data3 = user.update_personal_data(PersonalDataPerson,
                                               fio="Збигнев Бжезински",
                                               birth='1983-09-05',
                                               postal_index=610001, postal_address='Address Postal',
                                               phone='+7 495 6680903',
                                               passport='8734 238764234 239874',
                                               email='lkdfds@ldkjfs.com'
                                               )

        pers_data_list = PersonalDataPerson.objects.filter(common_data__account=user)
        self.assertEqual(1, len(pers_data_list))
