# coding=utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from domains.models import RegistrarContract, RegistrarOrder
from domains.registrars.core import DomainRegistrarConfig
from pybilling.settings import logger


class DomainOrderSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    domain = serializers.CharField(max_length=200)
    registrar = serializers.CharField(max_length=25)

    def prolong_domain(self, domain, registrar, native_contract, account_id):
        """
        Prolongate domain using known registrar contract.
        :param domain: Domain to prolong.
        :param registrar: Name of the registrar.
        :param native_contract: Used native registrar contract.
        :return: Prolong order.
        """
        assert domain
        assert registrar
        assert native_contract
        assert account_id > 0

        prolong_years = 1

        personal_data = RegistrarContract.get_matched_personal_data(native_contract, account_id)
        registrar_contract = RegistrarContract.link_native_contract(native_contract, personal_data)

        order = native_contract.domain_prolong(prolong_years, domain)
        logger.info("Order created: %s. Domain %s prolongation for %s." % (order, domain, native_contract.number))

        RegistrarOrder.objects.create(id=order.fields['order_id'],
                                      contract=registrar_contract,
                                      domain=domain,
                                      is_prolong=True,
                                      prolong_period=prolong_years)

        return native_contract, order

    def register_domain(self, domain, registrar, account_id, dns_list):
        """
        Register the new domain to account.
        :param dns_list:
        :param domain: Domain to register.
        :param registrar: Name of the registrar.
        :param account_id: ID of the domain owner.
        :return: Registration order.
        """
        assert domain
        assert registrar
        assert account_id > 0

        personal_data = RegistrarContract.get_linked_personal_data(account_id, registrar)
        registrar_contract, created = RegistrarContract.get_or_create_contract(personal_data, registrar)

        order = registrar_contract.get_native().domain_register(domain, nserver='\n'.join(dns_list))
        logger.info("Order created: %s. Domain %s registration for %s." % (order, domain, registrar_contract.number))

        RegistrarOrder.objects.create(id=order.fields['order_id'],
                                      contract=registrar_contract,
                                      domain=domain,
                                      is_prolong=False)

        return registrar_contract, order

    def save(self, **kwargs):
        domain = self.validated_data['domain']
        account_id = self.validated_data['account_id']
        registrar = self.validated_data['registrar']
        dns = self.validated_data.get('dns', '')

        logger.info('Begin registrar session: %s, %s, %s (%s)' % (domain, account_id, registrar, dns))

        native_contract = RegistrarContract.find_native_by_domain(domain, registrar)
        if native_contract:
            contract, order = self.prolong_domain(domain, registrar, native_contract, account_id)
        else:
            contract, order = self.register_domain(domain, registrar, account_id, dns.split(','))

        # request balance
        registrar_config = DomainRegistrarConfig(registrar)
        reg_connector = registrar_config.get_connector()
        registrar_balance = reg_connector.get_balance()

        return {
            'id': order.fields['order_id'],
            'domain': domain,
            'balance': registrar_balance,
            'contract': contract.number
        }
