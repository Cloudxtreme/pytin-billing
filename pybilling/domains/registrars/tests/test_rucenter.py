# coding=utf-8
from __future__ import unicode_literals

from django.test import TestCase

from domains.registrars.rucenter import RucenterRegistrar, RucenterRequest, REQUEST


class UserAccountTest(TestCase):
    def test_contract_search(self):
        rucenter = RucenterRegistrar(login='370/NIC-REG/adm', password='dogovor', lang='ru')

        query = {
            'contract-num': '288198/NIC-D'
        }
        contracts = list(rucenter.find_contracts(**query))

        self.assertEqual(1, len(contracts))
        self.assertEqual('288198/NIC-D', contracts[0].number)

    def test_registrar_balance(self):
        rucenter = RucenterRegistrar(login='370/NIC-REG/adm', password='dogovor', lang='ru')

        balance_info = rucenter.get_balance_info()

        self.assertEqual(balance_info['nds'], '18')
        self.assertTrue('blocked_services' in balance_info)
        self.assertTrue('rate_date' in balance_info)

    def test_error_handling(self):
        request = RucenterRequest(request_type=REQUEST.ACCOUNT,  # skip request field
                                  operation='dslkfjsldkfj',
                                  login='370/NIC-REG/adm', password='dogovor', lang='ru')

        self.assertRaisesMessage(Exception, 'Code 401: Authorization failed', request.send,
                                 RucenterRegistrar.RUCENTER_GATEWAY)
