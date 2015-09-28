# coding=utf-8
from __future__ import unicode_literals

from rest_framework.test import APITestCase

from accounts.models import UserAccount, PersonalDataPerson, PersonalDataEntrepreneur, PersonalData


class AccountsAPITests(APITestCase):
    def setUp(self):
        PersonalData.objects.all().delete()

        super(AccountsAPITests, self).setUp()

    def test_create_account_defined_id(self):
        payload = {
            'name': 'Dmitry',
            'pk': 150
        }
        response = self.client.post('/v1/accounts/', payload, format='json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(150, response.data['id'])

    def test_personal_data_filter(self):
        user, created = UserAccount.objects.get_or_create(
            name='User testing',
            balance=100,
            bonus_balance=50
        )

        personal_data_types = [PersonalDataPerson, PersonalDataEntrepreneur]

        for idx in xrange(1, 30):
            data = dict(
                fio="Клиент %s" % idx,
                inn_code=12345600 + idx,
                birth='1983-09-%s' % idx,
                postal_index=610000 + idx, postal_address='Address Postal %s' % idx,
                phone='+7 495 6680800%s' % idx,
                passport='8734 238764234 %s' % idx,
                email='lkdfds@ldkjfs%s.com' % idx,
            )
            user.add_personal_data(personal_data_types[idx % 2], **data)

        self.assertEqual(29, len(PersonalData.objects.all()))

        # test filters, all
        response = self.client.get('/v1/pdata/', {}, format='json')
        self.assertEqual(29, response.data['count'])

        response = self.client.get('/v1/pdata/',
                                   {'fio__startswith': 'Клиент 2', 'type': PersonalDataPerson.__name__}, format='json')
        self.assertEqual(6, response.data['count'])

    def test_personal_data_bug_extra(self):
        """
        There was a bug, when there is no extra data, serializer raises exception.
        """
        user, created = UserAccount.objects.get_or_create(
            name='User testing',
            balance=100,
            bonus_balance=50
        )

        personal_data_1_data = dict(
            fio="Клиент Имя 1",
            birth='1983-09-05',
            postal_index=610001, postal_address='Address Postal 1',
            phone='+7 495 6680903',
            passport='8734 238764234 239874',
            email='lkdfds@ldkjfs.com'
        )
        personal_data_1 = user.add_personal_data(PersonalDataPerson, **personal_data_1_data)

        # normal account retrieval
        response = self.client.get('/v1/accounts/%s/' % user.id, format='json')
        self.assertEqual(13, len(response.data['personal_data'][0].keys()))

        if personal_data_1.extended:
            personal_data_1.extended.delete()

        # normal account retrieval, with empty personal data
        response = self.client.get('/v1/accounts/%s/' % user.id, format='json')
        self.assertEqual(5, len(response.data['personal_data'][0].keys()))

    def test_personal_data_manage(self):
        user, created = UserAccount.objects.get_or_create(
            name='User testing',
            balance=100,
            bonus_balance=50
        )

        # create personal data
        payload = dict(
            fio="Zbignev Bj Жезинский",
            birth='1983-09-05',
            postal_index=610001, postal_address='Address Postal',
            phone='+7 495 6680903',
            passport='8734 238764234 239874',
            email='lkdfds@ldkjfs.com',
            account=user.id,
            type=PersonalDataPerson.__name__
        )

        response = self.client.post('/v1/pdata/', payload, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual('610001', response.data['postal_index'])
        self.assertEqual('Zbignev Bj Zhezinskij', response.data['fio_lat'])
        self.assertEqual('Zbignev Bj Жезинский', response.data['fio'])
        self.assertEqual('PersonalDataPerson', response.data['type'])
        self.assertEqual('+7 495 6680903', response.data['phone'])

        self.assertEqual(1, len(PersonalDataPerson.objects.all()))
        self.assertEqual(0, len(PersonalDataEntrepreneur.objects.all()))

        # update personal data
        payload = dict(
            fio="Вассисуалий Петров",
            birth='1983-11-05',
            postal_index=610501, postal_address='Address Postal 2',
            phone='+7 495 66809035',
            passport='8734 238764234 2398746',
            email='lkdfds@ldkjfs1.com',
            account=user.id,
            type=PersonalDataPerson.__name__
        )
        response = self.client.put('/v1/pdata/%s/' % response.data['id'], payload, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('610501', response.data['postal_index'])
        self.assertEqual('Zbignev Bj Zhezinskij', response.data['fio_lat'])
        self.assertEqual('Вассисуалий Петров', response.data['fio'])
        self.assertEqual('PersonalDataPerson', response.data['type'])
        self.assertEqual('+7 495 66809035', response.data['phone'])

        self.assertEqual(1, len(PersonalDataPerson.objects.all()))
        self.assertEqual(0, len(PersonalDataEntrepreneur.objects.all()))

        # change personal data type and some fields
        payload = dict(
            fio="Вассисуалий Петров",
            birth='1983-11-05',
            postal_index=610501, postal_address='Address Postal 2',
            phone='+7 495 66809035',
            passport='8734 238764234 2398746',
            email='lkdfds@ldkjfs1.com',
            account=user.id,
            inn_code='324876237846238746',
            type=PersonalDataEntrepreneur.__name__
        )
        response = self.client.put('/v1/pdata/%s/' % response.data['id'], payload, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('610501', response.data['postal_index'])
        self.assertEqual('Vassisualij Petrov', response.data['fio_lat'])
        self.assertEqual('Вассисуалий Петров', response.data['fio'])
        self.assertEqual('+7 495 66809035', response.data['phone'])
        self.assertEqual('324876237846238746', response.data['inn_code'])
        self.assertEqual('PersonalDataEntrepreneur', response.data['type'])

        self.assertEqual(0, len(PersonalDataPerson.objects.all()))
        self.assertEqual(1, len(PersonalDataEntrepreneur.objects.all()))

        # delete personal data
        response = self.client.delete('/v1/pdata/%s/' % response.data['id'], format='json')
        self.assertEqual(204, response.status_code)

        self.assertEqual(0, len(PersonalDataPerson.objects.all()))
        self.assertEqual(0, len(PersonalDataEntrepreneur.objects.all()))

    def test_get_account_with_personal_data(self):
        user, created = UserAccount.objects.get_or_create(
            name='User testing',
            balance=100,
            bonus_balance=50
        )

        user.add_personal_data(PersonalDataPerson,
                               fio="Zbignev Bj Жезинский",
                               birth='1983-09-05',
                               postal_index=610001, postal_address='Address Postal',
                               phone='+7 495 6680903',
                               passport='8734 238764234 239874',
                               email='lkdfds@ldkjfs.com'
                               )

        response = self.client.get('/v1/accounts/%s/' % user.id, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data['personal_data']))
        self.assertEqual('610001', response.data['personal_data'][0]['postal_index'])
        self.assertEqual('Zbignev Bj Zhezinskij', response.data['personal_data'][0]['fio_lat'])
        self.assertEqual('Zbignev Bj Жезинский', response.data['personal_data'][0]['fio'])
        self.assertEqual('PersonalDataPerson', response.data['personal_data'][0]['type'])
        self.assertEqual('+7 495 6680903', response.data['personal_data'][0]['phone'])

    def test_account_with_contacts_crud(self):
        user, created = UserAccount.objects.get_or_create(
            name='User testing',
            balance=100,
            bonus_balance=50
        )

        # CREATE
        payload = {
            'name': 'home',
            'address': 'dmitry@shyliaev.com',
            'type': 'email',
            'account': user.id
        }
        response = self.client.post('/v1/contacts/', payload, format='json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response.data['id'])
        self.assertEqual('home', response.data['name'])
        self.assertEqual('email', response.data['type'])
        self.assertEqual('dmitry@shyliaev.com', response.data['address'])
        self.assertEqual(user.id, response.data['account'])

        # UPDATE
        payload = {
            'name': 'work',
            'address': 'bxtgroup@gmail.com',
            'type': 'email',
        }
        response = self.client.patch('/v1/contacts/%s/' % response.data['id'], payload, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data['id'])
        self.assertEqual('work', response.data['name'])
        self.assertEqual('email', response.data['type'])
        self.assertEqual('bxtgroup@gmail.com', response.data['address'])
        self.assertEqual(user.id, response.data['account'])

        # DETAILS
        response = self.client.get('/v1/contacts/%s/' % response.data['id'], format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data['id'])
        self.assertEqual('work', response.data['name'])
        self.assertEqual('email', response.data['type'])
        self.assertEqual('bxtgroup@gmail.com', response.data['address'])
        self.assertEqual(user.id, response.data['account'])

        # DELETE
        response = self.client.delete('/v1/contacts/%s/' % response.data['id'], format='json')

        self.assertEqual(204, response.status_code)

    def test_account_contacts_filter(self):
        user, created = UserAccount.objects.get_or_create(
            name='User testing'
        )

        for idx in xrange(1, 100):
            user.update_contact(name='home %s' % idx,
                                type='phone',
                                address='+7 495 %s' % (idx * 2))

        # all set
        response = self.client.get('/v1/contacts/', {}, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(99, response.data['count'])
        self.assertEqual(50, len(response.data['results']))  # page size
        self.assertTrue('next' in response.data)

        # filtered
        response = self.client.get('/v1/contacts/', {'address__startswith': '+7 495 2'}, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(6, response.data['count'])
        self.assertEqual(6, len(response.data['results']))  # page size
        self.assertTrue('next' in response.data)

    def test_account_filter(self):
        for idx in xrange(1, 100):
            UserAccount.objects.get_or_create(
                name='User %s' % idx,
                balance=idx * 100,
                bonus_balance=idx * 50
            )

        # all set
        response = self.client.get('/v1/accounts/', {}, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(99, response.data['count'])
        self.assertEqual(50, len(response.data['results']))  # page size
        self.assertTrue('next' in response.data)

        # filtered
        response = self.client.get('/v1/accounts/', {'balance__gt': 5000}, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(49, response.data['count'])
        self.assertEqual(49, len(response.data['results']))  # page size
        self.assertTrue('next' in response.data)

    def test_account_crud(self):
        # CREATE
        payload = {
            'name': 'Dmitry',
        }
        response = self.client.post('/v1/accounts/', payload, format='json')

        self.assertEqual(201, response.status_code)

        self.assertEqual(1, response.data['id'])
        self.assertEqual('Dmitry', response.data['name'])
        self.assertEqual(0, response.data['balance'])
        self.assertEqual(0, response.data['bonus_balance'])
        self.assertEqual('ru', response.data['language'])

        # UPDATE
        payload = {
            'name': 'Dmitry Shilyaev',
            'language': 'en',
            'balance': 100,
            'bonus_balance': 200
        }

        response = self.client.patch('/v1/accounts/%s/' % response.data['id'], payload, format='json')

        self.assertEqual(200, response.status_code)

        self.assertEqual(1, response.data['id'])
        self.assertEqual('Dmitry Shilyaev', response.data['name'])
        self.assertEqual(0, response.data['balance'])  # not modified
        self.assertEqual(0, response.data['bonus_balance'])  # not modified
        self.assertEqual('en', response.data['language'])

        # DETAILS
        response = self.client.get('/v1/accounts/%s/' % response.data['id'], format='json')

        self.assertEqual(200, response.status_code)

        self.assertEqual(1, response.data['id'])
        self.assertEqual('Dmitry Shilyaev', response.data['name'])
        self.assertEqual(0, response.data['balance'])
        self.assertEqual(0, response.data['bonus_balance'])
        self.assertEqual('en', response.data['language'])

        # DELETE
        response = self.client.delete('/v1/accounts/%s/' % response.data['id'], format='json')

        self.assertEqual(204, response.status_code)  # empty response on delete
