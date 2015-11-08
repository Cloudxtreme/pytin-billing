# coding=utf-8
from __future__ import unicode_literals
import random

from django.test import TestCase

from domains.registrars.core import DomainRegistrarConfig
from domains.registrars.rucenter.connector import RucenterRegistrar, RucenterRequest, REQUEST, CONTRACT_TYPE, \
    RucenterContract


class UserAccountTest(TestCase):
    def _get_test_registrar(self):
        registrar_config = DomainRegistrarConfig('rucenter')

        return registrar_config.get_connector()

    def test_contract_create_koir_encoding_bug(self):
        """
        Запрос в RU-CENTER отправляется в формате KOI-R. При кодировании некоторых символов может
        возникать ошибка. Используем request_body.encode('KOI8-R', errors='ignore').
        :return:
        """
        rucenter = self._get_test_registrar()

        # create Company
        payload = {
            'contract-type': CONTRACT_TYPE.COMPANY,
            'country': 'RU',
            'e-mail': 'dfdjkh@gmail.com',
            'currency-id': 'RUR',
            'password': 'mWRFW4CTwu9vfiW',
            'phone': '+7 3287 23746782364',
            # проблема бала змечана на знаке №
            'p-addr': '328746 ываырвпаы а №1 ывоапыорвп аы воарпы ваоыпва',
            'code': '4345115602',
            'address-r': '312365 khfsdkfh sdk sdkfh ылвоарыолва',
            'kpp': '123456789',
            'org': 'Company name',
            'org-r': 'Название компании',
        }

        # проблемы возникнуть не должно
        rucenter.create_contract(payload)

    def test_create_personal_filter_out_bug(self):
        """
        Ошибка в поле person. Разрешено использование букв русского, латинского алфавита, пробелов, дефисов и апострофов.
        error value: Pupkin Igor' Aleksandrovich
        BUG: https://github.com/servancho/pytin-billing/issues/7
        """
        rucenter = self._get_test_registrar()

        contract1 = rucenter.create_contract({
            'contract-type': CONTRACT_TYPE.PERSON,
            'country': 'RU',
            'currency-id': 'RUR',
            'e-mail': 'dfdjkh@gmail.com',
            'password': 'mWRFW4CTwu9vfiW',
            'phone': '+7 3287 23746782364',
            'p-addr': '328746 ываырвпаы а ывоапыорвп аы воарпы ваоыпва ',
            'passport': 'passport паспорт dsfsdf',
            'birth-date': '05.09.1989',
            'person': "Pupkin Igor Aleksandrovich",
            'person-r': 'Hello World Mine',
        })

    def test_domain_handlers(self):
        rucenter = self._get_test_registrar()

        contract = RucenterContract(rucenter, {})

        data = contract.handle_rf({
            'domain': 'какой-то-домен.рф'
        })

        self.assertEqual('xn-----6kcsfufbwlecc6c.xn--p1ai', data['domain'])

    def test_register_domain_ns_with_ip(self):
        rucenter = self._get_test_registrar()

        # create Person
        contract1 = rucenter.create_contract({
            'contract-type': CONTRACT_TYPE.PERSON,
            'country': 'RU',
            'currency-id': 'RUR',
            'e-mail': 'dfdjkh@gmail.com',
            'password': 'mWRFW4CTwu9vfiW',
            'phone': '+7 3287 23746782364',
            'p-addr': '328746 ываырвпаы а ывоапыорвп аы воарпы ваоыпва ',
            'passport': 'passport паспорт dsfsdf',
            'birth-date': '05.09.1989',
            'person': 'Vassiliy Pupkin',
            'person-r': 'Hello World Mine',
        })
        self.assertTrue(contract1.number.endswith('/NIC-D'))

        domain_name = "test-domain-%s.ru" % random.randint(1, 1000)

        order = contract1.domain_register(domain_name,
                                          nserver='ns1.justhost.ru 46.17.40.100\nns2.justhost.ru 46.17.41.100')

        self.assertTrue('order_id' in order.order_data)

    def test_register_domain_and_orders_list(self):
        rucenter = self._get_test_registrar()

        # create Person
        contract1 = rucenter.create_contract({
            'contract-type': CONTRACT_TYPE.PERSON,
            'country': 'RU',
            'currency-id': 'RUR',
            'e-mail': 'dfdjkh@gmail.com',
            'password': 'mWRFW4CTwu9vfiW',
            'phone': '+7 3287 23746782364',
            'p-addr': '328746 ываырвпаы а ывоапыорвп аы воарпы ваоыпва ',
            'passport': 'passport паспорт dsfsdf',
            'birth-date': '05.09.1989',
            'person': 'Vassiliy Pupkin',
            'person-r': 'Hello World Mine',
        })
        self.assertTrue(contract1.number.endswith('/NIC-D'))

        domain_name = "test-domain-%s.ru" % random.randint(1, 1000)

        order = contract1.domain_register(domain_name)

        self.assertTrue('order_id' in order.order_data)

        # find orders
        orders = list(contract1.find_orders({'order_id': order.order_id}))
        self.assertEqual(1, len(orders))
        self.assertEqual('waiting', orders[0].state)

        # find all orders
        orders = list(contract1.find_orders({}))
        self.assertTrue(len(orders) >= 1)

    def test_contract_delete(self):
        rucenter = self._get_test_registrar()

        # create Person
        contract1 = rucenter.create_contract({
            'contract-type': CONTRACT_TYPE.PERSON,
            'country': 'RU',
            'currency-id': 'RUR',
            'e-mail': 'dfdjkh@gmail.com',
            'password': 'mWRFW4CTwu9vfiW',
            'phone': '+7 3287 23746782364',
            'p-addr': '328746 ываырвпаы а ывоапыорвп аы воарпы ваоыпва ',
            'passport': 'passport паспорт dsfsdf',
            'birth-date': '05.09.1989',
            'person': 'Vassiliy Pupkin',
            'person-r': 'Hello World Mine',
        })
        self.assertTrue(contract1.number.endswith('/NIC-D'))

        query = {
            'contract-num': contract1.number
        }
        contracts = list(rucenter.find_contracts(query))
        self.assertEqual(1, len(contracts))

        # delete contract
        contract1.delete()

        contracts = list(rucenter.find_contracts(query))
        self.assertEqual(0, len(contracts))

    def test_contract_create_errors(self):
        rucenter = self._get_test_registrar()

        # create Company
        payload = {
            'contract-type': CONTRACT_TYPE.COMPANY,
            'country': 'RU',
            'e-mail': 'dfdjkh@gmail.com',
            'currency-id': 'RUR',
            'password': 'mWRFW4CTwu9vfiW',
            'phone': '+7 3287 23746782364',
            'p-addr': '328746 ываырвпаы а ывоапыорвп аы воарпы ваоыпва',
            'code': '4345115602_',
            'address-r': '312365 khfsdkfh sdk sdkfh ылвоарыолва',
            'kpp': '123456789_',
            'org': 'Company name',
            'org-r': 'Название компании',
        }

        try:
            rucenter.create_contract(payload)
            self.fail("Exception expected")
        except Exception, ex:
            self.assertEqual('API ERROR 402: Поле kpp должно состоять из 9 цифр; '
                             'Ошибка в поле code. Некорректный ИНН',
                             ex.message)

    def test_contract_create(self):
        rucenter = self._get_test_registrar()

        # create Person
        contract1 = rucenter.create_contract({
            'contract-type': CONTRACT_TYPE.PERSON,
            'country': 'RU',
            'currency-id': 'RUR',
            'e-mail': 'dfdjkh@gmail.com',
            'password': 'mWRFW4CTwu9vfiW',
            'phone': '+7 3287 23746782364',
            'p-addr': '328746 ываырвпаы а ывоапыорвп аы воарпы ваоыпва ',
            'passport': 'passport паспорт dsfsdf',
            'birth-date': '05.09.1989',
            'person': 'Vassiliy Pupkin',
            'person-r': 'Hello World Mine',
        })

        self.assertTrue(contract1.number.endswith('/NIC-D'))

        # create Entrepreneur
        contract2 = rucenter.create_contract({
            'contract-type': CONTRACT_TYPE.PERSON,
            'birth-date': '05.09.1989',
            'country': 'RU',
            'code': '384762786428',
            'currency-id': 'RUR',
            'e-mail': 'dfdjkh@gmail.com',
            'p-addr': '328746 ываырвпаы а ывоапыорвп аы воарпы ваоыпва ',
            'passport': 'passport паспорт dsfsdf',
            'password': 'mWRFW4CTwu9vfiW',
            'person': 'Vassiliy Pupkin',
            'person-r': 'Hello World Mine',
            'phone': '+7 3287 23746782364',
        })
        self.assertTrue(contract2.number.endswith('/NIC-D'))
        self.assertNotEquals(contract1.number, contract2.number)

        # create Company
        contract3 = rucenter.create_contract({
            'contract-type': CONTRACT_TYPE.COMPANY,
            'country': 'RU',
            'e-mail': 'dfdjkh@gmail.com',
            'currency-id': 'RUR',
            'password': 'mWRFW4CTwu9vfiW',
            'phone': '+7 3287 23746782364',
            'p-addr': '328746 ываырвпаы а ывоапыорвп аы воарпы ваоыпва',
            'code': '4345115602',
            'address-r': '312365 khfsdkfh sdk sdkfh ылвоарыолва',
            'kpp': '123456789',
            'org': 'Company name',
            'org-r': 'Название компании',
        })
        self.assertTrue(contract3.number.endswith('/NIC-D'))
        self.assertNotEquals(contract2.number, contract3.number)

    def test_contract_search(self):
        rucenter = self._get_test_registrar()

        query = {
            'contract-num': '288198/NIC-D'
        }
        contracts = list(rucenter.find_contracts(query))

        self.assertEqual(1, len(contracts))
        self.assertEqual('288198/NIC-D', contracts[0].number)

    def test_registrar_balance(self):
        rucenter = self._get_test_registrar()

        balance = rucenter.get_balance()

        self.assertTrue(balance != 0)

    def test_error_handling(self):
        request = RucenterRequest(request_type=REQUEST.ACCOUNT,  # skip request field
                                  operation='dslkfjsldkfj',
                                  login='370/NIC-REG/adm', password='dogovor', lang='ru')

        self.assertRaisesMessage(Exception, 'API ERROR 401: Authorization failed', request.send,
                                 RucenterRegistrar.RUCENTER_GATEWAY)
