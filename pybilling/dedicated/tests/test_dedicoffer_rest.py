# coding=utf-8
from __future__ import unicode_literals

from rest_framework.test import APITestCase

from dedicated.models import DedicatedServerOffer


class DedicOfferAPITests(APITestCase):
    def setUp(self):
        DedicatedServerOffer.objects.all().delete()

        super(DedicOfferAPITests, self).setUp()

    def test_manage_offer(self):
        payload = {
            'platform': '1U Asus RS120-X5-PI2',
            'cpu_name': 'Intel Pentium D 820 2.8GHz',
            'cpu_count': 1,
            'ram_gb': 3,
            'hdd_gb': 250,
            'hdd_count': 2,
            'price': 5000,
            'visible': True,
            'comment': ''
        }
        response = self.client.post('/v1/dedic_offer/', payload, format='json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response.data['id'])

        del response.data['id']
        self.assertEqual(payload, response.data)

        # get offers from database
        response = self.client.get('/v1/dedic_offer/', format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data['count'])
        self.assertEqual('1U Asus RS120-X5-PI2', response.data['results'][0]['platform'])
        self.assertEqual(5000, response.data['results'][0]['price'])
