# coding=utf-8
from __future__ import unicode_literals

import hashlib
import random

from domains.registrars.core import PersonalDataSerializer
from domains.registrars.rucenter.connector import CONTRACT_TYPE


def make_password():
    return hashlib.md5(unicode(random.randint(1, 1000000))).hexdigest()[0:29]


class RuCenterSerializersFactory(object):
    @staticmethod
    def get_serializer_by_data_type(personal_data_type):
        assert personal_data_type

        serializers_map = {
            'PersonalDataPerson': RuCenterPersonSerializer(),
            'PersonalDataEntrepreneur': RuCenterEntrepreneurSerializer(),
            'PersonalDataCompany': RuCenterCompanySerializer(),
            'PersonalDataForeignPerson': RuCenterForeignPersonSerializer(),
            'PersonalDataForeignEntrepreneur': RuCenterForeignEntrepreneurSerializer(),
            'PersonalDataForeignCompany': RuCenterForeignCompanySerializer(),
        }

        return serializers_map[personal_data_type]

    @staticmethod
    def get_serializer_by_contract(rucenter_contract):
        """
        Get the specific serializer for the registrar contract.
        :param rucenter_contract: Contract from the registrar.
        :return: Appropriate serializer class.
        """
        assert rucenter_contract

        rucenter_contract.load_details()

        if rucenter_contract.contract_type == CONTRACT_TYPE.PERSON:
            entrepreneur = 'code' in rucenter_contract.fields

            if rucenter_contract.is_resident:
                return RuCenterEntrepreneurSerializer() if entrepreneur else RuCenterPersonSerializer()
            else:
                return RuCenterForeignEntrepreneurSerializer() if entrepreneur else RuCenterEntrepreneurSerializer()
        else:
            if rucenter_contract.is_resident:
                return RuCenterCompanySerializer()
            else:
                return RuCenterForeignCompanySerializer()


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
            'birth-date': personal_data_instance.extended.birth.strftime('%d.%m.%Y'),
            'person': personal_data_instance.extended.fio_lat[:100],
            'person-r': personal_data_instance.extended.fio[:100],
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
            'birth-date': personal_data_instance.extended.birth.strftime('%d.%m.%Y'),
            'person': personal_data_instance.extended.fio_lat[:100],
            'person-r': personal_data_instance.extended.fio[:100],
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
            'org': personal_data_instance.extended.company_name_lat[:100],
            'org-r': personal_data_instance.extended.company_name[:100],
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
            'birth-date': personal_data_instance.extended.birth.strftime('%d.%m.%Y'),
            'person': personal_data_instance.extended.fio_lat[:100],
            'person-r': personal_data_instance.extended.fio_lat[:100],
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
            'birth-date': personal_data_instance.extended.birth.strftime('%d.%m.%Y'),
            'person': personal_data_instance.extended.fio_lat[:100],
            'person-r': personal_data_instance.extended.fio_lat[:100],
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
            'org': personal_data_instance.extended.company_name_lat[:100],
            'org-r': personal_data_instance.extended.company_name_lat[:100],
        }
