from __future__ import unicode_literals

from argparse import ArgumentParser
import argparse

from django.core.management.base import BaseCommand

from accounts.models import PersonalData
from domains.models import RegistrarContract
from domains.registrars.core import DomainRegistrarConfig
from domains.registrars.rucenter.serializers import RuCenterSerializersFactory


class Command(BaseCommand):
    registered_handlers = {}
    registrar_name = 'rucenter'

    def add_arguments(self, parser):
        # Global arguments
        subparsers = parser.add_subparsers(title="Management commands.",
                                           help="Commands help",
                                           dest='manager_name',
                                           parser_class=ArgumentParser)

        # contract
        contract_cmd_parser = subparsers.add_parser('contract', help='Contract management commands.')
        contract_cmd_parser.add_argument('--account', help="Define account number to work with.")
        contract_cmd_parser.add_argument('--contract', help="Define contract number to work with.")
        contract_cmd_parser.add_argument('--data-id', help="Define personal data ID.")

        contract_cmd_parser.add_argument('--list', '-l', help="List available contracts for the account number.",
                                         action='store_true')
        contract_cmd_parser.add_argument('--export', '-e', help="Create contract based on personal data.",
                                         action='store_true')
        contract_cmd_parser.add_argument('--delete',
                                         help="Delete contract from registrar by its number or by personal data id.",
                                         action='store_true')
        contract_cmd_parser.add_argument('--link', help="Link registrar contract to the local contract.",
                                         action='store_true')
        self._register_handler('contract', self._handle_contract)

        # domain
        domain_cmd_parser = subparsers.add_parser('domain', help='Domain management commands.')
        domain_cmd_parser.add_argument('--account', help="Define account number to work with.")
        domain_cmd_parser.add_argument('--contract',
                                       help="Define contract number to work with.")
        domain_cmd_parser.add_argument('--nameserver', '-n', help="Comma separated list of nameservers.",
                                       default='ns1.justhost.ru,ns2.justhost.ru')
        domain_cmd_parser.add_argument('--domain', '-d', help="Register domains by contract ID.",
                                       nargs=argparse.ONE_OR_MORE)

        domain_cmd_parser.add_argument('--list', help="List domains for the account number.",
                                       action='store_true')
        domain_cmd_parser.add_argument('--register', help="Register domains listed in --domain.",
                                       action='store_true')
        domain_cmd_parser.add_argument('--prolong',
                                       help="Prolong domains listed in --domain. specify the number of years to prolong.")
        self._register_handler('domain', self._handle_domain)


        # order
        order_cmd_parser = subparsers.add_parser('order', help='Control orders.')
        order_cmd_parser.add_argument('--contract',
                                      help="Define contract number to work with.")
        order_cmd_parser.add_argument('--state', '-s',
                                      help="Specify state of orders to get. Related to registrar.")

        order_cmd_parser.add_argument('--list', '-l', help="List all available orders.",
                                      action='store_true')
        self._register_handler('order', self._handle_order)

        # service
        service_cmd_parser = subparsers.add_parser('service', help='Control services.')
        service_cmd_parser.add_argument('--contract',
                                        help="Define contract number to work with.")

        service_cmd_parser.add_argument('--list', '-l', help="List all available services.",
                                        action='store_true')
        self._register_handler('service', self._handle_service)

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
            contract_number = options['contract']

            contracts = list(reg_connector.find_contracts({'contract-num': contract_number}))
            if len(contracts) > 0:
                contract = contracts[0]

                for service in contract.find_services():
                    print service.service_data['service-id'], ' - ', service.service_data['domain']

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
            contract_number = options['contract']

            contracts = list(reg_connector.find_contracts({'contract-num': contract_number}))
            if len(contracts) > 0:
                contract = contracts[0]

                query = {}
                if 'state' in options:
                    query['state'] = options['state']

                for order in contract.find_orders(query):
                    print order.order_data['order_id'], ' - ', order.order_data['order_items']

    def _handle_domain(self, *args, **options):
        """
        Handle operations with domains.
        :param args:
        :param options:
        :return:
        """
        registrar_config = DomainRegistrarConfig(self.registrar_name)
        reg_connector = registrar_config.get_connector()

        if options['list']:
            account_number = int(options['account'])
            for personal_data in PersonalData.objects.filter(account=account_number):
                for local_contract in RegistrarContract.objects.filter(personal_data=personal_data):
                    print "%s (%s)" % (local_contract.number, local_contract.registrar)

        elif options['prolong']:
            contract_number = options['contract']
            prolong_years = int(options['prolong'])

            local_contract = RegistrarContract.objects.get(registrar=self.registrar_name, number=contract_number)
            contracts = list(reg_connector.find_contracts({'contract-num': contract_number}))

            if len(contracts) > 0:
                contract = contracts[0]

                for domain_name in options['domain']:
                    order = contract.domain_prolong(domain_name, prolong=prolong_years)

                    print "Order created: %s" % order

        elif options['register']:
            contract_number = options['contract']

            local_contract = RegistrarContract.objects.get(registrar=self.registrar_name, number=contract_number)

            contracts = list(reg_connector.find_contracts({'contract-num': contract_number}))

            if len(contracts) > 0:
                contract = contracts[0]
                name_servers = options['nameserver'].split(',')

                for domain_name in options['domain']:
                    order = contract.domain_register(domain_name, nserver='\n'.join(name_servers))

                    print "Order created: %s. Domain %s registration on %s." % (order, domain_name, contract_number)
            else:
                print "There is no such contract %s in %s" % (contract_number, self.registrar_name)

    def _handle_contract(self, *args, **options):
        """
        Handle operations with contracts.
        :param args:
        :param options:
        :return:
        """
        registrar_config = DomainRegistrarConfig(self.registrar_name)
        reg_connector = registrar_config.get_connector()

        if options['link']:
            contract_number = options['contract']

            if RegistrarContract.objects.filter(registrar=self.registrar_name, number=contract_number).exists():
                print "Contract %s already linked." % contract_number
                return False
            else:
                personal_data_id = int(options['data_id'])
                personal_data = PersonalData.objects.get(pk=personal_data_id)

                RegistrarContract.objects.update_or_create(
                    registrar=self.registrar_name,
                    number=contract_number,
                    defaults=dict(
                        personal_data=personal_data
                    )
                )

                print "Contract %s linked to personal data id %s of account %s" % (contract_number,
                                                                                   personal_data.id,
                                                                                   personal_data.account.id)

        elif options['list']:
            account_number = int(options['account'])

            for personal_data in PersonalData.objects.filter(account=account_number):
                print "%s - %s - %s - %s" % (
                    personal_data.id, personal_data.type, personal_data.default, personal_data.verified)

                print '    ', unicode(personal_data.extended)

        elif options['export']:
            personal_data_id = int(options['data_id'])
            personal_data = PersonalData.objects.get(pk=personal_data_id)

            known_contracts = RegistrarContract.objects.filter(personal_data=personal_data)
            if len(known_contracts) <= 0:
                personal_data_serializer = RuCenterSerializersFactory.get_serializer_by_data_type(personal_data.type)

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
                    print "Created contract: %s" % contract.number
                else:
                    print "Updated contract: %s" % contract.number
            else:
                for known_contract in known_contracts:
                    print "Existing contract: %s" % known_contract.number

        elif options['delete']:
            contract_number = None
            if options['contract']:
                contract_number = options['contract']
            else:
                personal_data_id = int(options['data_id'])
                local_contract = RegistrarContract.objects.get(personal_data=personal_data_id)
                contract_number = local_contract.number

            try:
                for contract in reg_connector.find_contracts({'contract-num': contract_number}):
                    print "Remove contract %s from %s" % (contract_number, self.registrar_name)
                    contract.delete()

                local_contracts_to_delete = RegistrarContract.objects.filter(number=contract_number).count()
                if local_contracts_to_delete > 0:
                    RegistrarContract.objects \
                        .filter(number=contract_number) \
                        .delete()
                    print "Local contracts removed: %s" % local_contracts_to_delete
            except Exception, ex:
                raise ex

    def _register_handler(self, command_name, handler):
        assert command_name, "command_name must be defined."
        assert handler, "handler must be defined."

        self.registered_handlers[command_name] = handler

    def handle(self, *args, **options):
        if 'subcommand_name' in options:
            subcommand = "%s.%s" % (options['manager_name'], options['subcommand_name'])
        else:
            subcommand = options['manager_name']

            # try:
            self.registered_handlers[subcommand](*args, **options)
            # except Exception, ex:
            #     print "Error: %s" % ex
