from __future__ import unicode_literals

from rest_framework.test import APITestCase

from accounts.models import UserAccount


class AccountsAPITests(APITestCase):
    def setUp(self):
        super(AccountsAPITests, self).setUp()

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
            'account': user.id
        }
        response = self.client.put('/v1/contacts/%s/' % response.data['id'], payload, format='json')

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

        response = self.client.put('/v1/accounts/%s/' % response.data['id'], payload, format='json')

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
