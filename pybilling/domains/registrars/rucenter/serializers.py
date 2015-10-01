# coding=utf-8
from __future__ import unicode_literals
import hashlib
import random

from domains.registrars.core import PersonalDataSerializer
from domains.registrars.rucenter.connector import CONTRACT_TYPE


def make_password():
    return hashlib.md5(unicode(random.randint(1, 1000000))).hexdigest()[0:29]


class RuCenterPersonSerializer(PersonalDataSerializer):
    def serialize(self, personal_data_instance):
        assert personal_data_instance

        return {
            'contract-type': CONTRACT_TYPE.PERSON,
            'country': personal_data_instance.account.language.upper(),
            'currency-id': 'RUR',
            'password': make_password(),

            'e-mail': personal_data_instance.extended.email,
            'phone': personal_data_instance.extended.phone,

            'p-addr': "%s, %s" % (personal_data_instance.extended.postal_index,
                                  personal_data_instance.extended.postal_address),

            'passport': personal_data_instance.extended.passport,
            'birth-date': personal_data_instance.extended.birth,
            'person': personal_data_instance.extended.fio,
            'person-r': personal_data_instance.extended.fio_lat,
        }


class RuCenterEntrepreneurSerializer(PersonalDataSerializer):
    def serialize(self, personal_data_instance):
        assert personal_data_instance

        return {
            'contract-type': CONTRACT_TYPE.PERSON,
            'country': personal_data_instance.account.language.upper(),
            'currency-id': 'RUR',
            'password': make_password(),

            'e-mail': personal_data_instance.extended.email,
            'phone': personal_data_instance.extended.phone,

            'p-addr': "%s, %s" % (personal_data_instance.extended.postal_index,
                                  personal_data_instance.extended.postal_address),

            'code': personal_data_instance.extended.inn_code,
            'passport': personal_data_instance.extended.passport,
            'birth-date': personal_data_instance.extended.birth,
            'person': personal_data_instance.extended.fio,
            'person-r': personal_data_instance.extended.fio_lat,
        }


class RuCenterCompanySerializer(PersonalDataSerializer):
    def serialize(self, personal_data_instance):
        assert personal_data_instance

        return {
            'contract-type': CONTRACT_TYPE.COMPANY,
            'country': personal_data_instance.account.language.upper(),
            'currency-id': 'RUR',
            'password': make_password(),

            'e-mail': personal_data_instance.extended.email,
            'phone': personal_data_instance.extended.phone,

            'p-addr': "%s, %s, %s" % (personal_data_instance.extended.postal_person,
                                      personal_data_instance.extended.postal_index,
                                      personal_data_instance.extended.postal_address),

            'address-r': personal_data_instance.extended.company_address,

            'code': personal_data_instance.extended.inn,
            'kpp': personal_data_instance.extended.kpp,
            'org': personal_data_instance.extended.company_name_lat,
            'org-r': personal_data_instance.extended.company_name,
        }


class RuCenterForeignPersonSerializer(PersonalDataSerializer):
    def serialize(self, personal_data_instance):
        assert personal_data_instance

        return {
            'contract-type': CONTRACT_TYPE.PERSON,
            'country': personal_data_instance.account.language.upper(),
            'currency-id': 'RUR',
            'password': make_password(),

            'e-mail': personal_data_instance.extended.email,
            'phone': personal_data_instance.extended.phone,

            'p-addr': personal_data_instance.extended.postal_address,

            'passport': personal_data_instance.extended.passport,
            'birth-date': personal_data_instance.extended.birth,
            'person': personal_data_instance.extended.fio,
        }


class RuCenterForeignEntrepreneurSerializer(PersonalDataSerializer):
    def serialize(self, personal_data_instance):
        assert personal_data_instance

        return {
            'contract-type': CONTRACT_TYPE.PERSON,
            'country': personal_data_instance.account.language.upper(),
            'currency-id': 'RUR',
            'password': make_password(),

            'e-mail': personal_data_instance.extended.email,
            'phone': personal_data_instance.extended.phone,

            'p-addr': personal_data_instance.extended.postal_address,

            'code': personal_data_instance.extended.inn_code,
            'passport': personal_data_instance.extended.passport,
            'birth-date': personal_data_instance.extended.birth,
            'person': personal_data_instance.extended.fio,
        }


class RuCenterForeignCompanySerializer(PersonalDataSerializer):
    def serialize(self, personal_data_instance):
        assert personal_data_instance

        return {
            'contract-type': CONTRACT_TYPE.COMPANY,
            'country': personal_data_instance.account.language.upper(),
            'currency-id': 'RUR',
            'password': make_password(),

            'e-mail': personal_data_instance.extended.email,
            'phone': personal_data_instance.extended.phone,
            'p-addr': personal_data_instance.extended.postal_address,
            'code': personal_data_instance.extended.inn,
            'address-r': personal_data_instance.extended.company_address,
            'kpp': personal_data_instance.extended.kpp,
            'org': personal_data_instance.extended.company_name_lat,
            'org-r': personal_data_instance.extended.company_name,
        }
