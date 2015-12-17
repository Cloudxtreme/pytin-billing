# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from accounts.models import PersonalData
from domains.registrars.core import DomainRegistrarConfig, Contract
from pybilling.settings import logger


class RegistrarContract(models.Model):
    personal_data = models.OneToOneField(PersonalData, primary_key=True)
    created_at = models.DateTimeField(db_index=True, default=timezone.now, null=False)
    registrar = models.CharField(db_index=True, max_length=35)
    number = models.CharField(db_index=True, max_length=15)

    def __unicode__(self):
        return "%s (%s)" % (self.number, self.registrar)

    @staticmethod
    def get_matched_personal_data(registrar_contract, account_id):
        """
        Find the match between existing personal data and existing registrar contract, using email.
        :param registrar_contract: Native registrar contract.
        :param account_id: Account used to find the matched personal data.
        :return: Matched PersonalData object
        """
        assert registrar_contract
        assert account_id > 0
        assert isinstance(registrar_contract, Contract)

        found_personal_data = None
        for pd in PersonalData.objects.filter(account__exact=account_id):
            if hasattr(pd.extended, 'email') and pd.extended.email == registrar_contract.email:
                found_personal_data = pd
                break

        if not found_personal_data:
            raise Exception("Personal data not found for the email %s" % registrar_contract.email)

        return found_personal_data

    @staticmethod
    def get_linked_personal_data(account_id, registrar):
        """
        Trying to find the personal data already linked to the native contract at the registrar. If there is no
        linked contracts, then returns first personal data that is found.
        :param account_id: Account used to find the matched personal data.
        :return: Matched PersonalData object
        """
        assert account_id > 0
        assert registrar

        linked_contracts = RegistrarContract.objects.filter(personal_data__account__exact=account_id,
                                                            registrar=registrar)
        if len(linked_contracts) <= 0:
            if not PersonalData.objects.filter(account__exact=account_id).exists():
                raise Exception("User %s have no personal data." % account_id)

            return PersonalData.objects.filter(account__exact=account_id)[0]

        return linked_contracts[0].personal_data

    @staticmethod
    def link_contract(registrar_contract, personal_data):
        """
        Link remote registrar contract to the local personal data.
        :param registrar_contract: Contract at the registrar
        :param personal_data: User personal data.
        :return: RegistrarContract object.
        """
        assert registrar_contract
        assert personal_data
        assert isinstance(registrar_contract, Contract)

        if not RegistrarContract.objects.filter(number=registrar_contract.number,
                                                registrar=registrar_contract.registrar.NAME).exists():
            logger.info("Linking contract %s to personal data %s." % (registrar_contract, personal_data.id))
            RegistrarContract.objects.update_or_create(
                    registrar=registrar_contract.registrar.NAME,
                    number=registrar_contract.number,
                    defaults=dict(
                            personal_data=personal_data
                    )
            )

        return RegistrarContract.objects.filter(number=registrar_contract.number,
                                                registrar=registrar_contract.registrar.NAME)[0]

    @staticmethod
    def get_or_create_contract(personal_data, registrar):
        """
        Get existing or create new contract in the registrar system. If there is no known contracts,
        then it will be created from the personal data.
        :param personal_data: Personal data.
        :param registrar: Name of the registrar.
        :return: RegistrarContract object.
        """
        assert personal_data
        assert registrar

        logger.info("Getting contract for user %s from registrar %s." % (personal_data.account.id, registrar))

        registrar_config = DomainRegistrarConfig(registrar)
        reg_connector = registrar_config.get_connector()
        serializer_factory = registrar_config.get_serializer_factory()

        created = False
        linked_contracts = RegistrarContract.objects.filter(personal_data=personal_data)
        if len(linked_contracts) <= 0:
            logger.info("Linked contracts not found. Trying to find at registrar.")

            existing_contracts = list(reg_connector.find_contracts({'e-mail': personal_data.email}))
            if len(existing_contracts) <= 0:
                logger.info("Exporting contract...")
                personal_data_serializer = serializer_factory.get_serializer_by_data_type(personal_data.type)
                registrar_contract = reg_connector.create_contract(personal_data_serializer.serialize(personal_data))
                logger.info("Exported as %s. Trying to link local." % registrar_contract)
                created = True
            else:
                registrar_contract = existing_contracts[0]
                logger.info("Used existing contract %s. Trying to link local." % registrar_contract)

            RegistrarContract.link_contract(registrar_contract, personal_data)

            return registrar_contract, created

        return linked_contracts[0].get_native(), created

    def get_native(self):
        """
        Returns linked native contract from the registrar.
        :return:
        """
        registrar_config = DomainRegistrarConfig(self.registrar)
        reg_connector = registrar_config.get_connector()

        existing_contracts = list(reg_connector.find_contracts({'contract-num': self.number}))
        if len(existing_contracts) <= 0:
            return None

        return existing_contracts[0]
