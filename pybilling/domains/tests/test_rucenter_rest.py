# coding=utf-8
from __future__ import unicode_literals

import random

from rest_framework.test import APITestCase

from accounts.models import PersonalData, UserAccount, PersonalDataEntrepreneur
from domains.models import RegistrarContract
from domains.registrars.core import DomainRegistrarConfig
from domains.registrars.rucenter.connector import RucenterRegistrar


class RegistrarAPITests(APITestCase):
    """
    Testing the domain registration and prolong API.
    Tests are organized depends on personal data is exported or not.
        linked_yes: there is a known registrar contract exists (no need to export and link)
        linked_no: there is NO known registrar contract exists (need to export and link)
        exported_no: there is NO contract based on personal data at the registrar (need to export).
        exported_yes: there is a contract at the registrar (maybe created manually earlier).
    """

    def setUp(self):
        PersonalData.objects.all().delete()
        UserAccount.objects.all().delete()

        self.registrar_name = RucenterRegistrar.NAME

        self.user, created = UserAccount.objects.get_or_create(
                name='User testing',
                balance=100,
                bonus_balance=50
        )

        super(RegistrarAPITests, self).setUp()

    def test_domain_register_linked_yes_exported_yes(self):
        """
        Using known contract linked to the personal data.
        """
        personal_data_ok_data = dict(
                fio="Клиент Имя 3",
                birth='1983-09-03',
                postal_index=610003, postal_address='Address Postal 3',
                phone='+7 495 6680903',
                passport='8734 238764234 239874',
                email='dfdjkh%s@gmail.com' % random.randint(1, 1000),
                inn_code=384762786428
        )
        pd = self.user.add_personal_data(PersonalDataEntrepreneur, **personal_data_ok_data)
        self.assertEqual(1, len(PersonalData.objects.all()))
        self.assertEqual(0, len(RegistrarContract.objects.all()))

        # export personal data to the registrar
        registrar_config = DomainRegistrarConfig(self.registrar_name)
        reg_connector = registrar_config.get_connector()
        serializer_factory = registrar_config.get_serializer_factory()

        personal_data_serializer = serializer_factory.get_serializer_by_data_type(pd.type)
        existing_contract = reg_connector.create_contract(personal_data_serializer.serialize(pd))

        # link contract
        RegistrarContract.objects.update_or_create(
                registrar=self.registrar_name,
                number=existing_contract.number,
                defaults=dict(
                        personal_data=pd
                )
        )

        # register the domain
        payload = {
            'domain': 'dfjslkfjsdlkfj-%s.ru' % random.randint(1, 1000),
            'registrar': self.registrar_name,
            'account_id': self.user.id
        }

        response = self.client.post('/v1/domain_orders/', payload, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(RegistrarContract.objects.all()))

        linked_contract = RegistrarContract.objects.get(personal_data=pd)
        self.assertEqual(linked_contract.number, response.data['contract'])
        self.assertEqual(existing_contract.number, response.data['contract'])

    def test_domain_register_linked_no_exported_yes(self):
        """
        Must find the match with local personal data and contract at the registrar, link them.
        """
        personal_data_ok_data = dict(
                fio="Клиент Имя 3",
                birth='1983-09-03',
                postal_index=610003, postal_address='Address Postal 3',
                phone='+7 495 6680903',
                passport='8734 238764234 239874',
                email='dfdjkh%s@gmail.com' % random.randint(1, 1000),
                inn_code=384762786428
        )
        pd = self.user.add_personal_data(PersonalDataEntrepreneur, **personal_data_ok_data)
        self.assertEqual(1, len(PersonalData.objects.all()))
        self.assertEqual(0, len(RegistrarContract.objects.all()))

        # export personal data to the registrar
        registrar_config = DomainRegistrarConfig(self.registrar_name)
        reg_connector = registrar_config.get_connector()
        serializer_factory = registrar_config.get_serializer_factory()

        personal_data_serializer = serializer_factory.get_serializer_by_data_type(pd.type)
        existing_contract = reg_connector.create_contract(personal_data_serializer.serialize(pd))

        # register the domain
        payload = {
            'domain': 'dfjslkfjsdlkfj-%s.ru' % random.randint(1, 1000),
            'registrar': self.registrar_name,
            'account_id': self.user.id
        }

        response = self.client.post('/v1/domain_orders/', payload, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(RegistrarContract.objects.all()))

        linked_contract = RegistrarContract.objects.get(personal_data=pd)
        self.assertEqual(linked_contract.number, response.data['contract'])
        self.assertEqual(existing_contract.number, response.data['contract'])

    def test_domain_register_linked_no_exported_no(self):
        """
        Must create and link registrar contract based on personal data.
        """
        personal_data_ok_data = dict(
                fio="Клиент Имя 3",
                birth='1983-09-03',
                postal_index=610003, postal_address='Address Postal 3',
                phone='+7 495 6680903',
                passport='8734 238764234 239874',
                email='dfdjkh%s@gmail.com' % random.randint(1, 1000),
                inn_code=384762786428
        )
        pd = self.user.add_personal_data(PersonalDataEntrepreneur, **personal_data_ok_data)
        self.assertEqual(1, len(PersonalData.objects.all()))
        self.assertEqual(0, len(RegistrarContract.objects.all()))

        payload = {
            'domain': 'dfjslkfjsdlkfj-%s.ru' % random.randint(1, 1000),
            'registrar': self.registrar_name,
            'account_id': self.user.id
        }

        response = self.client.post('/v1/domain_orders/', payload, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(RegistrarContract.objects.all()))

        linked_contract = RegistrarContract.objects.get(personal_data=pd)
        self.assertEqual(linked_contract.number, response.data['contract'])

    def test_domain_register_error_no_personal_data(self):
        payload = {
            'domain': 'dfjslkfjsdlkfj.ru',
            'registrar': self.registrar_name,
            'account_id': self.user.id
        }

        response = self.client.post('/v1/domain_orders/', payload, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual('User %s have no personal data.' % self.user.id, response.data)

    def test_domain_prolong_linked_yes_exported_yes(self):
        pass

    def test_domain_prolong_linked_no_exported_yes(self):
        pass
