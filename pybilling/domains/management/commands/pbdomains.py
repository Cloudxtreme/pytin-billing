from django.core.management.base import BaseCommand


class Command(BaseCommand):
    registered_handlers = {}

    def add_arguments(self, parser):
        # subparsers = parser.add_subparsers(title="Assets manager",
        #                                    help="Commands help",
        #                                    dest='manager_name',
        #                                    parser_class=ArgumentParser)
        #
        # # switch
        # switch_cmd_parser = subparsers.add_parser('switch', help='Show what is linked to switch.')
        # switch_cmd_parser.add_argument('switch-id', help="Resource ID of the switch.")
        # switch_cmd_parser.add_argument('-p', '--port', nargs='*', help="Specify switch ports to list connections.")
        # self._register_handler('switch', self._handle_switch)
        #
        # # unit
        # unit_cmd_parser = subparsers.add_parser('unit', help='Manage Rack units.')
        # unit_cmd_parser.add_argument('ip-or-id', nargs='*', help="IDs or IPs of the unit device to view.")
        # unit_cmd_parser.add_argument('-r', '--update-parent-rack', action='store_true',
        #                              help="Auto update unit device parent Rack based on Switch port connections.")
        # unit_cmd_parser.add_argument('--set-position', type=int, metavar='POS',
        #                              help="Set the unit device position in the parent Rack.")
        # unit_cmd_parser.add_argument('--set-size', type=int, metavar='SIZE',
        #                              help="Set the unit device size in Units.")
        # unit_cmd_parser.add_argument('--set-on-rails', metavar='RAILS',
        #                              help="Set unit device is on rails or not.")
        # self._register_handler('unit', self._handle_rack_unit)
        #
        # # rack
        # rack_cmd_parser = subparsers.add_parser('rack', help='Get rack info.')
        # rack_cmd_parser.add_argument('id', nargs='*', help="IDs of the racks to query info.")
        # rack_cmd_parser.add_argument('-l', '--layout', action='store_true', help="Show racks layout.")
        # rack_cmd_parser.add_argument('--set-size', type=int,
        #                              help="Set the Rack size in Units.")
        # self._register_handler('rack', self._handle_rack)
        pass
