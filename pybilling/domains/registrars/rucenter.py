# coding=utf-8
from __future__ import unicode_literals

import re

from django.utils import timezone
from django.utils.http import urlencode
import requests
from django.utils.translation import ugettext_lazy as _

from domains.registrars.core import Registrar, Contract
from pybilling.settings import logger


def serialize_fields(fields):
    """
    Serializes fields, according to RU-CENTER API rules
    :param fields:
    :return:
    """
    serialized = ''
    for key in fields:
        serialized += "%s:%s\n" % (key, fields[key])

    return serialized


def deserialize_fields(text):
    """
    Deserializes fields, according to RU-CENTER API rules
    :return:
    """
    fields = {}
    for record in text.split('\n'):
        record = record.strip()
        if record == '':
            continue

        logger.debug("Unpack record '%s'" % record)

        key_value = record.split(':', 1)
        if len(key_value) != 2:
            raise ValueError(_("Wrong field record '%s'" % record))

        (key, value) = key_value
        fields[key.strip()] = value.strip()

    return fields


class REQUEST:
    ACCOUNT = 'account'
    CONTRACT = 'contract'
    ORDER = 'order'
    SERVICE_OBJECT = 'service-object'
    SERVICE = 'service'
    CONTACT = 'contact'
    SERVER = 'server'


class OPERATION:
    SEARCH = 'search'
    GET = 'get'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    SWAP = 'swap'


class ACTION:
    NEW = 'new'
    UPDATE = 'update'
    PROLONG = 'prolong'
    PICKUP = 'pickup'


class ProtocolHeader(object):
    def __init__(self, **fields):
        self.fields = fields

    def serialize(self):
        return serialize_fields(self.fields)

    @staticmethod
    def deserialize(text):
        assert text

        fields = deserialize_fields(text)

        return ProtocolHeader(**fields)


class ProtocolSection(object):
    def __init__(self, name, **fields):
        assert name

        self.name = name
        self.fields = fields

    def serialize(self):
        serialized = '[%s]\n' % self.name
        serialized += serialize_fields(self.fields)

        return serialized

    @staticmethod
    def deserialize(text):
        assert text

        mt = re.match(r'\[(.+)\]', text)
        if mt:
            name = mt.group(1)
            fields = deserialize_fields(text[mt.regs[0][1]:])

            return ProtocolSection(name, **fields)

        raise Exception(_("Malformed response section."))


class RucenterResponse(object):
    def __init__(self, header, *sections):
        assert header

        self.header = header
        self.sections = sections

        self._state = 200
        self._error = ''

        if 'State' in self.header.fields:
            mt = re.match(r'(\d+)\s+(.+)', self.header.fields['State'])
            if mt:
                self._state = mt.group(1)
                self._error = mt.group(2)

    @staticmethod
    def from_text(response_text):
        assert response_text

        # split into blocks: header and sections
        blocks = response_text.split('\n\n')

        # parse header
        header = ProtocolHeader.deserialize(blocks[0])

        # parse sections
        sections = []
        for section_text_block in blocks[1:]:
            section_text_block = section_text_block.strip()
            if section_text_block == '':
                continue

            sections.append(ProtocolSection.deserialize(section_text_block))

        return RucenterResponse(header, *sections)

    @property
    def state(self):
        return int(self._state)

    @property
    def error(self):
        return self._error

    def get_section(self, name):
        for section in self.sections:
            if section.name == name:
                return section

        raise Exception(_("Missing section %s" % name))


class RucenterRequest(object):
    """
    Request object.
    """

    def __init__(self, request_type, operation, login, password, lang='ru'):
        assert request_type
        assert operation

        self.sections = []
        self.headers = {
            'request': request_type,
            'operation': operation,

            'login': login,
            'password': password,
            'lang': lang,

            # YYYYMMDDHHMMSS.PROC_NUM@partner-web-site
            'request_id': timezone.now().strftime('%Y%m%d%H%M%S.pybilling@justhost.ru')
        }

    def add_header(self, key, value):
        assert key

        self.headers[key] = value

    def send(self, url):
        """
        Send request to url and get Response
        """
        assert url

        request_body = ''

        # serialize headers
        header = ProtocolHeader(**self.headers)
        request_body += header.serialize()
        request_body += "\n"

        # serialize sections
        for section in self.sections:
            request_body += section.serialize()
            request_body += "\n"

        # send request
        headers = {
            "http-equiv": "Content-type",
            "content": "application/x-www-form-urlencoded",
            "charset": "utf8"
        }
        data = urlencode({
            'SimpleRequest': request_body
        })

        request = requests.post(url, data, headers=headers)
        if request.status_code >= 500 or request.status_code == 405:
            raise Exception(_("HTTP error %s. Service unavailable." % request.status_code))

        response = RucenterResponse.from_text(request.text)
        if response.state >= 400:
            raise Exception(_("Code %s: %s" % (response.state, response.error)))

        return response


class RucenterContract(Contract):
    @property
    def number(self):
        return self.fields['contract-num']

    def find_orders(self):
        super(RucenterContract, self).find_orders()

    def find_services(self):
        super(RucenterContract, self).find_services()

    def create_order(self):
        super(RucenterContract, self).create_order()


class RucenterRegistrar(Registrar):
    """
    Details:
    https://www.nic.ru/manager/docs/partners/protocol/requests/account_get.shtml

    Response:
    present_payments:7110.00 RUR
    payments:7364.69 RUR
    services:191.57 RUR
    credit:192867.00 RUR
    blocked_services:199965.00 RUR
    blocked_prolong:28230.00 RUR
    usd_rate:
    present_services:0.00 RUR
    blockable:75.12 RUR
    balance:-192791.88 RUR
    nds:18
    blocked_new:171735.00 RUR
    rate_date:14.09.2007
    """

    RUCENTER_GATEWAY = 'https://www.nic.ru/dns/dealer'

    def __init__(self, login, password, lang='ru'):
        assert login
        assert password

        self.login = login
        self.password = password
        self.lang = lang

    def create_contract(self, **kwargs):
        pass

    def find_contracts(self, **query):
        """
        Search for the clients contracts.
        Details: https://www.nic.ru/manager/docs/partners/protocol/requests/contract_search.shtml

        Query can contain:
            contracts-limit:10
            contracts-first:1
            contract-num:3470/NIC-D
            e-mail:ivan@sidorov.ru
            domain:test.ru
            org:Sony
            org-r:Сони
            code:7709203571
            person:Sidorov
            person-r:Иван
            passport:232322
            is-resident:YES
            identity:identified

        :param query: fields from Query
        :return: contracts
        """
        request = RucenterRequest(request_type=REQUEST.CONTRACT,
                                  operation=OPERATION.SEARCH,
                                  login=self.login,
                                  password=self.password,
                                  lang=self.lang)

        request.sections.append(ProtocolSection('contract', **query))

        while True:
            response = request.send(self.RUCENTER_GATEWAY)

            paging_data = response.get_section('contracts-list')
            item_first = int(paging_data.fields['contracts-first'])
            item_limit = int(paging_data.fields['contracts-limit'])
            item_total = int(paging_data.fields['contracts-found'])

            for section in response.sections[1:]:
                yield RucenterContract(self, **section.fields)

            if (item_first + item_limit) >= item_total:
                break

            # update paging
            query['contracts-first'] = item_first + item_limit + 1
            request.sections[0] = ProtocolSection('contract', **query)

    def get_balance_info(self):
        request = RucenterRequest(request_type=REQUEST.ACCOUNT,
                                  operation=OPERATION.GET,
                                  login=self.login,
                                  password=self.password,
                                  lang=self.lang)

        response = request.send(self.RUCENTER_GATEWAY)

        acc_section = response.get_section('account')

        return acc_section.fields
