from __future__ import unicode_literals

from argparse import ArgumentParser
import argparse

from django.core.management.base import BaseCommand

from accounts.models import PersonalData
from domains.models import RegistrarContract, RegistrarDomain
from domains.registrars.core import DomainRegistrarConfig


class Command(BaseCommand):
    registered_handlers = {}

    def add_arguments(self, parser):
        # Global arguments
        subparsers = parser.add_subparsers(title="Management commands.",
                                           help="Commands help",
                                           dest='manager_name',
                                           parser_class=ArgumentParser)

        # contract
        contract_cmd_parser = subparsers.add_parser('contract', help='Contract management commands.')
        contract_cmd_parser.add_argument('--list', '-l', help="List available contracts for the account number.")
        contract_cmd_parser.add_argument('--create', '-c', help="Create contract based on personal data.")
        contract_cmd_parser.add_argument('--delete_by_num', help="Delete contract from registrar, by number.")
        self._register_handler('contract', self._handle_contract)

        domain_cmd_parser = subparsers.add_parser('domain', help='Domain management commands.')
        domain_cmd_parser.add_argument('--list', '-l', help="List domains for the account number.")
        domain_cmd_parser.add_argument('--contract-id', '-c',
                                       help="Register domains specified in --domain by contract ID.")
        domain_cmd_parser.add_argument('--domain', '-d', help="Register domains by contract ID.",
                                       nargs=argparse.ONE_OR_MORE)
        self._register_handler('domain', self._handle_domain)

    def _handle_domain(self, *args, **options):
        registrar_name = 'rucenter'

        registrar_config = DomainRegistrarConfig(registrar_name)
        reg_connector = registrar_config.get_connector()

        if options['list']:
            user_id = int(options['list'])

            for personal_data in PersonalData.objects.filter(account=user_id):
                for local_contract in RegistrarContract.objects.filter(personal_data=personal_data):
                    print "%s (%s)" % (local_contract.number, local_contract.registrar)

                    for domain in RegistrarDomain.objects.filter(contract=local_contract):
                        print "%s (%s)" % (domain.domain, domain.created_at)

        elif options['contract_id']:
            contracts = list(reg_connector.find_contracts({'contract-num': options['contract_id']}))

            if len(contracts) > 0:
                contract = contracts[0]
                for domain_name in options['domain']:
                    contract.domain_register(domain_name, nserver='ns1.justhost.ru\nns2.justhost.ru')

    def _handle_contract(self, *args, **options):
        """
        Handle operations with contracts.
        :param args:
        :param options:
        :return:
        """
        registrar_name = 'rucenter'

        registrar_config = DomainRegistrarConfig(registrar_name)
        reg_connector = registrar_config.get_connector()

        if options['list']:
            user_id = int(options['list'])

            for personal_data in PersonalData.objects.filter(account=user_id):
                print "%s - %s - %s - %s" % (
                    personal_data.id, personal_data.type, personal_data.default, personal_data.verified)

                print '    ', unicode(personal_data.extended)

        elif options['export']:
            personal_data_id = int(options['export'])
            personal_data = PersonalData.objects.get(pk=personal_data_id)

            known_contracts = RegistrarContract.objects.filter(personal_data=personal_data)
            if len(known_contracts) <= 0:
                personal_data_serializer = registrar_config.get_serializer(personal_data.type)
                contract = reg_connector.create_contract(personal_data_serializer.serialize(personal_data))

                # track created contracts
                contract, created = RegistrarContract.objects.update_or_create(
                    registrar=registrar_name,
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

        elif options['delete_by_num']:
            contract_number = options['delete_by_num']

            RegistrarContract.objects.filter(number=contract_number).delete()

            for contract in reg_connector.find_contracts({'contract-num': contract_number}):
                print "Remove contract %s from %s" % (contract_number, registrar_name)
                contract.delete()

    def _register_handler(self, command_name, handler):
        assert command_name, "command_name must be defined."
        assert handler, "handler must be defined."

        self.registered_handlers[command_name] = handler

    def handle(self, *args, **options):
        if 'subcommand_name' in options:
            subcommand = "%s.%s" % (options['manager_name'], options['subcommand_name'])
        else:
            subcommand = options['manager_name']

        try:
            self.registered_handlers[subcommand](*args, **options)
        except Exception, ex:
            print "Error: %s" % ex.message
