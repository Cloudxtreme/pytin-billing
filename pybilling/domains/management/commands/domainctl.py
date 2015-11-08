# coding=utf-8
from __future__ import unicode_literals

from argparse import ArgumentParser
import argparse
import sys

from django.core.management.base import BaseCommand

from django.utils.translation import ugettext_lazy as _

from accounts.models import PersonalData
from domains.models import RegistrarContract
from domains.registrars.core import DomainRegistrarConfig
from pybilling.settings import logger


class Command(BaseCommand):
    registered_handlers = {}
    known_registrars = DomainRegistrarConfig.known_registrars

    def add_arguments(self, parser):
        # Global arguments
        parser.add_argument('registrar', choices=self.known_registrars,
                            help="Specify registrar name to work with.")

        parser.add_argument('--user-id', '-u', help="Define user ID to work with.")
        parser.add_argument('--contract', '-n', help="Define contract number to work with, depends on registrar.")
        parser.add_argument('--profile-id', '-p', help="Define personal data (profile) ID.")

        # define subparsers
        subparsers = parser.add_subparsers(title="Management commands.",
                                           help="Commands help",
                                           dest='manager_name',
                                           parser_class=ArgumentParser)

        # contract
        contract_cmd_parser = subparsers.add_parser('contract', help='Contract management commands.')

        contract_cmd_parser.add_argument('--list', '-l', help="List available contracts for the user.",
                                         action='store_true')
        contract_cmd_parser.add_argument('--export', '-e', help="Create contract based on profile ID.",
                                         action='store_true')
        contract_cmd_parser.add_argument('--delete',
                                         help="Delete contract from registrar by its number or by profile id.",
                                         action='store_true')
        contract_cmd_parser.add_argument('--link', help="Link registrar contract to the profile.",
                                         action='store_true')
        contract_cmd_parser.add_argument('--unlink', help="Unlink registrar contract from the profile.",
                                         action='store_true')
        self._register_handler('contract', self._handle_contract)

        # domain
        domain_cmd_parser = subparsers.add_parser('domain', help='Domain management commands.')
        domain_cmd_parser.add_argument('--nameserver', '--ns', help="Comma separated list of nameservers.",
                                       default='ns1.justhost.ru,ns2.justhost.ru'.encode('utf-8'))
        domain_cmd_parser.add_argument('--domain', '-d', help="Register domains by contract ID.",
                                       nargs=argparse.ONE_OR_MORE)

        domain_cmd_parser.add_argument('--register', help="Register specified domains.",
                                       action='store_true')
        domain_cmd_parser.add_argument('--update', help="Update data of specified domains.",
                                       action='store_true')
        domain_cmd_parser.add_argument('--search', help="Search specified domains.",
                                       action='store_true')
        domain_cmd_parser.add_argument('--prolong',
                                       help="Prolongate specified domains. Specify the number of years.")
        self._register_handler('domain', self._handle_domain)

        # order
        order_cmd_parser = subparsers.add_parser('order', help='Control orders.')
        order_cmd_parser.add_argument('--state', '-s',
                                      help="Specify state of orders to get. Related to registrar.")

        order_cmd_parser.add_argument('--list', '-l', help="List all available orders.",
                                      action='store_true')
        self._register_handler('order', self._handle_order)

        # service
        service_cmd_parser = subparsers.add_parser('service', help='Control services.')
        service_cmd_parser.add_argument('--list', '-l', help="List all available services.",
                                        action='store_true')
        self._register_handler('service', self._handle_service)

    def _parse_globals(self, **options):
        self.registrar_name = options['registrar']
        self.user_id = int(options['user_id']) if options['user_id'] else None
        self.contract = options['contract']
        self.profile_id = int(options['profile_id']) if options['profile_id'] else None

        if self.profile_id and not self.contract:
            logger.info("Searching for the profile %s" % self.profile_id)
            local_contracts = RegistrarContract.objects.filter(personal_data=self.profile_id)
            if len(local_contracts) > 0:
                self.contract = local_contracts[0].number
            else:
                logger.error(_("There is no linked contracts to profile %s" % self.profile_id))
        elif not self.profile_id and self.contract:
            local_contracts = RegistrarContract.objects.filter(registrar=self.registrar_name, number=self.contract)
            if len(local_contracts) > 0:
                self.profile_id = local_contracts[0].personal_data.id

        logger.info("Registered globals:")
        logger.info("registrar_name = %s" % self.registrar_name)
        logger.info("user_id = %s" % self.user_id)
        logger.info("contract = %s" % self.contract)
        logger.info("profile_id = %s" % self.profile_id)

    def _decode_options_to_unicode(self, **options):
        """
        Строки из консоли приходят в кодировке sys.stdin.encoding, их нужно преобразовать в unicode
        для дальнейшего использования.
        """
        for option_name in options:
            if isinstance(options[option_name], str):
                options[option_name] = options[option_name].decode(sys.stdin.encoding)
            elif isinstance(options[option_name], list):
                new_values = []
                for option_value in options[option_name]:
                    if isinstance(option_value, str):
                        new_values.append(option_value.decode(sys.stdin.encoding))
                    else:
                        new_values.append(option_value)

                options[option_name] = new_values

        return options

    def _handle_contract(self, *args, **options):
        """
        Handle operations with contracts.
        :param args:
        :param options:
        :return:
        """
        registrar_config = DomainRegistrarConfig(self.registrar_name)
        reg_connector = registrar_config.get_connector()
        serializer_factory = registrar_config.get_serializer_factory()

        if options['unlink']:
            assert self.contract, _("Specify existing contract.")

            linked_contracts = RegistrarContract.objects.filter(registrar=self.registrar_name, number=self.contract)
            for linked_contract in linked_contracts:
                linked_contract.delete()
                logger.info("    unlinked %s" % linked_contract)

        elif options['link']:
            assert self.contract, _("Specify existing contract.")

            linked_contracts = RegistrarContract.objects.filter(registrar=self.registrar_name, number=self.contract)
            if len(linked_contracts) > 0:
                logger.info("Contract %s already linked to profile %s." % (self.contract, linked_contracts[0].id))
            else:
                personal_data = PersonalData.objects.get(pk=self.profile_id)

                RegistrarContract.objects.update_or_create(
                    registrar=self.registrar_name,
                    number=self.contract,
                    defaults=dict(
                        personal_data=personal_data
                    )
                )

                logger.info("Contract %s linked to profile id %s of account %s" % (self.contract,
                                                                                   personal_data.id,
                                                                                   personal_data.account.id))
        elif options['list']:
            assert self.user_id, _("Specify user id.")

            for personal_data in PersonalData.objects.filter(account=self.user_id):
                logger.info("%s - %s - %s - %s" % (
                    personal_data.id,
                    personal_data.type,
                    'default' if personal_data.default else '',
                    'verified' if personal_data.verified else 'not verified'))

                logger.info(personal_data.extended)

                print_none = True
                for local_contract in RegistrarContract.objects.filter(personal_data=personal_data):
                    logger.info("    %s (%s)" % (local_contract.number, local_contract.registrar))
                    print_none = False

                if print_none:
                    logger.info(_("    there is no linked registrar contracts."))

        elif options['export']:
            assert self.profile_id, _("Specify profile or contract.")

            personal_data = PersonalData.objects.get(pk=self.profile_id)

            known_contracts = RegistrarContract.objects.filter(personal_data=personal_data)
            if len(known_contracts) <= 0:
                personal_data_serializer = serializer_factory.get_serializer_by_data_type(personal_data.type)

                contract = reg_connector.create_contract(personal_data_serializer.serialize(personal_data))

                # track created contracts
                contract, created = RegistrarContract.objects.update_or_create(
                    registrar=self.registrar_name,
                    number=contract.number,
                    defaults=dict(
                        personal_data=personal_data
                    )
                )

                if created:
                    logger.info("Created contract: %s" % contract.number)
                else:
                    logger.info("Updated contract: %s" % contract.number)
            else:
                for known_contract in known_contracts:
                    logger.info("Existing contract: %s" % known_contract.number)

        elif options['delete']:
            assert self.contract, _("Specify profile or existing linked contract.")

            try:
                for contract in reg_connector.find_contracts({'contract-num': self.contract}):
                    logger.info("Remove contract %s from %s" % (self.contract, self.registrar_name))
                    contract.delete()

                local_contracts_count = RegistrarContract.objects.filter(number=self.contract).count()
                if local_contracts_count > 0:
                    RegistrarContract.objects.filter(number=self.contract).delete()
                    logger.info("Local contracts removed: %s" % local_contracts_count)
            except Exception, ex:
                raise ex

    def _handle_service(self, *args, **options):
        """
        Handle operations with orders.
        :param args:
        :param options:
        :return:
        """
        registrar_config = DomainRegistrarConfig(self.registrar_name)
        reg_connector = registrar_config.get_connector()

        if options['list']:
            assert self.contract, _("Specify profile or existing linked contract.")

            contracts = list(reg_connector.find_contracts({'contract-num': self.contract}))
            if len(contracts) > 0:
                contract = contracts[0]

                for service in contract.find_services({}):
                    logger.info(service.service_data['service-id'], ' - ', service.service_data['domain'])

    def _handle_order(self, *args, **options):
        """
        Handle operations with orders.
        :param args:
        :param options:
        :return:
        """
        registrar_config = DomainRegistrarConfig(self.registrar_name)
        reg_connector = registrar_config.get_connector()

        if options['list']:
            assert self.contract, _("Specify profile or existing linked contract.")

            contracts = list(reg_connector.find_contracts({'contract-num': self.contract}))
            if len(contracts) > 0:
                contract = contracts[0]

                query = {}
                if 'state' in options:
                    query['state'] = options['state']

                for order in contract.find_orders(query):
                    logger.info(order.order_data['order_id'], ' - ', order.order_data['order_items'])

    def _handle_domain(self, *args, **options):
        """
        Handle operations with domains.
        :param args:
        :param options:
        :return:
        """
        registrar_config = DomainRegistrarConfig(self.registrar_name)
        reg_connector = registrar_config.get_connector()

        if options['search']:
            assert options['domain'], _("Specify domains to search (wildcards are supported).")

            for domain_name in options['domain']:
                logger.info("Searching for %s" % domain_name)

                contracts = list(reg_connector.find_contracts({'domain': domain_name}))
                if len(contracts) <= 0:
                    logger.warning(_("Domain %s is not found in %s." % (domain_name, self.registrar_name)))
                else:
                    for contract in contracts:
                        logger.info("    %s" % contract.number)

        elif options['prolong']:
            assert self.contract, _("Specify profile or existing linked contract.")
            assert options['prolong'], _("Specify the prolongation period.")

            prolong_years = int(options['prolong'])

            contracts = list(reg_connector.find_contracts({'contract-num': self.contract}))

            if len(contracts) > 0:
                contract = contracts[0]

                for domain_name in options['domain']:
                    order = contract.domain_prolong(prolong_years, domain_name)
                    logger.info("Order created: %s" % order)

        elif options['register']:
            assert self.contract, _("Specify profile or existing linked contract.")

            contracts = list(reg_connector.find_contracts({'contract-num': self.contract}))

            if len(contracts) > 0:
                contract = contracts[0]
                name_servers = options['nameserver'].split(',')

                for domain_name in options['domain']:
                    order = contract.domain_register(domain_name, nserver='\n'.join(name_servers))
                    logger.info(
                        "Order created: %s. Domain %s registration on %s." % (order, domain_name, self.contract))
            else:
                logger.info("There is no such contract %s in %s" % (self.contract, self.registrar_name))

        elif options['update']:
            assert self.contract, _("Specify profile or existing linked contract.")

            contracts = list(reg_connector.find_contracts({'contract-num': self.contract}))

            if len(contracts) > 0:
                contract = contracts[0]
                name_servers = options['nameserver'].split(',')

                for domain_name in options['domain']:
                    order = contract.domain_update(domain_name, nserver='\n'.join(name_servers))
                    logger.info("Order created: %s. Domain %s update in %s." % (order, domain_name, self.contract))
            else:
                logger.info("There is no such contract %s in %s" % (self.contract, self.registrar_name))

    def _register_handler(self, command_name, handler):
        assert command_name, "command_name must be defined."
        assert handler, "handler must be defined."

        self.registered_handlers[command_name] = handler

    def handle(self, *args, **options):
        subcommand = options['manager_name']

        decoded_options = self._decode_options_to_unicode(**options)

        self._parse_globals(**decoded_options)

        # try:
        self.registered_handlers[subcommand](*args, **decoded_options)
        # except Exception, ex:
        #     print "Error: %s" % ex
