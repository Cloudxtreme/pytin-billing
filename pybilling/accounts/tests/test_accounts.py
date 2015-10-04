# coding=utf-8
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.test import TestCase

from accounts.models import UserAccount, PersonalDataPerson, PersonalData, PersonalDataEntrepreneur, PersonalDataCompany


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
        self.assertEqual(user.language, 'RU')

    def test_create_user_contact(self):
        user, created = UserAccount.objects.get_or_create(name='Dmitry')

        email1 = user.update_contact('main', 'email', 'dmitry@shyliaev.com', validator=validate_email)
        self.assertEqual('main', email1.name)
        self.assertEqual('email', email1.type)
        self.assertEqual('dmitry@shyliaev.com', email1.address)

        email2 = user.update_contact(' home ', '  email', '  dmitry@shyliaev1.com ', validator=validate_email)
        self.assertEqual('home', email2.name)
        self.assertEqual('email', email2.type)
        self.assertEqual('dmitry@shyliaev1.com', email2.address)

        try:
            user.update_contact('main', 'email', 'dmitryshyliaev.com', validator=validate_email)
        except ValidationError, ex:
            self.assertEqual(1, len(ex.messages))
            self.assertEqual('Enter a valid email address.', ex.messages[0])

    def test_manage_personal_company_lat_bug(self):
        """
        companyname_lat is not being filled
        """

        user, created = UserAccount.objects.get_or_create(name='Dmitry')

        # normal transliteration
        company_data_1_data = dict(
            postal_index=610001, postal_address='Address Postal 1',
            phone='+7 495 6680903',
            email='lkdfds@ldkjfs.com',

            company_name='ООО "Баксэт"',
            inn='4345115602',
            ogrn='1234567890123',
            kpp='123456789',

            postal_person='Дмитрий Шиляев',
            company_address='2347864 Какой-то адрес компании на планете'
        )
        personal_data_1 = user.add_personal_data(PersonalDataCompany, **company_data_1_data)

        self.assertEqual('OOO "Bakset"', personal_data_1.extended.company_name_lat)

    def test_manage_personal_strict_bug(self):
        """
        pytils.translit.translify() with strict=True (default) raises error while working. Fixed.
        """

        user, created = UserAccount.objects.get_or_create(name='Dmitry')

        # normal transliteration
        personal_data_1_data = dict(
            fio="Зби́гнев Кази́меж Бжези́нс",
            birth='1983-09-05',
            postal_index=610001, postal_address='Address Postal 1',
            phone='+7 495 6680903',
            passport='8734 238764234 239874',
            email='lkdfds@ldkjfs.com'
        )
        personal_data_1 = user.add_personal_data(PersonalDataPerson, **personal_data_1_data)

        self.assertEqual('Zbígnev Kazímezh Bzhezíns', personal_data_1.extended.fio_lat)

    def test_manage_personal_data(self):
        user, created = UserAccount.objects.get_or_create(name='Dmitry')

        # add personal data of different types: PersonalDataPerson, PersonalDataPerson, PersonalDataEntrepreneur
        personal_data_1_data = dict(
            fio="Клиент Имя 1",
            birth='1983-09-05',
            postal_index=610001, postal_address='Address Postal 1',
            phone='+7 495 6680903',
            passport='8734 238764234 239874',
            email='lkdfds@ldkjfs.com'
        )
        personal_data_1 = user.add_personal_data(PersonalDataPerson, **personal_data_1_data)

        personal_data_2_data = dict(
            fio="Клиент Имя 2",
            birth='1983-09-25',
            postal_index=610001, postal_address='Address Postal 2',
            phone='+7 495 66809032',
            passport='8734 238764234 2398742',
            email='lkdfds@ldkjfs1.com'
        )
        personal_data_2 = user.add_personal_data(PersonalDataPerson, **personal_data_2_data)

        personal_data_3_data = dict(
            fio="Клиент Имя 3",
            inn_code=398472897492874,
            birth='1983-09-03',
            postal_index=610003, postal_address='Address Postal 3',
            phone='+7 495 6680903',
            passport='8734 238764234 239874',
            email='lkdfds@ldkjfs3.com',
        )
        personal_data_3 = user.add_personal_data(PersonalDataEntrepreneur, **personal_data_3_data)

        self.assertEqual(3, len(PersonalData.objects.all()))
        self.assertEqual(2, len(PersonalDataPerson.objects.all()))
        self.assertEqual(1, len(PersonalDataEntrepreneur.objects.all()))

        # update second personal data PersonalDataPerson
        personal_data_2.fio = 'Клиент Имя 2 ed'
        personal_data_2.save()

        personal_data_2.refresh_from_db()
        self.assertEqual('Клиент Имя 2 ed', personal_data_2.fio)

        # SEARCHING. Two types of search.
        # get list of extended personal data
        pers_data_list = PersonalDataPerson.objects.filter(common_data__account=user, phone='+7 495 6680903')
        self.assertEqual(1, len(pers_data_list))

        # search for personal data by extended fields, but you MUST specify 'type' property.
        try:
            PersonalData.objects.filter(fio="some fio")
            self.fail("Waiting for ValidationError")
        except ValidationError, ex:
            self.assertEqual(1, len(ex.error_dict))
            self.assertTrue('type' in ex.error_dict)

        personal_data_objects = PersonalData.objects.filter(phone='+7 495 6680903',
                                                            type=PersonalDataPerson.__name__)
        self.assertEqual(1, len(personal_data_objects))

        # Delete first PersonalDataPerson. To delete all models, need to delete via common_data.
        # To delete only related extra data, run just personal_data_1.delete()
        personal_data_1.common_data.delete()

        self.assertEqual(2, len(PersonalData.objects.all()))
        self.assertEqual(1, len(PersonalDataPerson.objects.all()))
        self.assertEqual(1, len(PersonalDataEntrepreneur.objects.all()))

    def test_validate_personal_data(self):
        user, created = UserAccount.objects.get_or_create(name='Dmitry')

        personal_data_3_data = dict(
            fio="Клиент Имя 3",
            birth='1983-09-03',
            postal_index=610003, postal_address='Address Postal 3',
            phone='+7 4951 6680903',
            passport='8734 238764234 239874',
            email='lkdfdsldkjfs3.com',
        )

        try:
            user.add_personal_data(PersonalDataEntrepreneur, **personal_data_3_data)
            self.fail("Waiting for ValidationError")
        except ValidationError, ex:
            self.assertEqual(3, len(ex.error_dict))
            self.assertTrue('inn_code' in ex.error_dict)
            self.assertTrue('email' in ex.error_dict)
            self.assertTrue('phone' in ex.error_dict)
