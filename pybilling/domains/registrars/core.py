# coding=utf-8
from __future__ import unicode_literals
from pybilling import settings
from pybilling.lib import loader


class Registrar(object):
    def create_contract(self, data):
        pass

    def find_contracts(self, query):
        pass

    def get_balance(self):
        pass


class Contract(object):
    def __init__(self, registrar, fields):
        assert registrar

        self.registrar = registrar
        self.fields = fields

    def delete(self):
        pass

    def domain_register(self, domain_name, **data):
        pass

    def domain_prolong(self, domain_name, **data):
        pass

    def find_orders(self, query):
        pass

    def find_services(self, query):
        pass


class Contact(object):
    def __init__(self, contract, fields):
        assert contract
        assert fields

        self.contract = contract
        self.fields = fields

    def update(self, data):
        pass

    def delete(self):
        pass

    def find_contacts(self, query):
        pass


class Order(object):
    def __init__(self, contract, fields):
        assert contract
        assert fields

        self.fields = fields

        self._contract = contract

    def __unicode__(self):
        return unicode(self.order_id)

    def find_services(self, query):
        pass

    def cancel(self):
        pass

    @property
    def order_id(self):
        pass

    @property
    def contract(self):
        return self._contract

    @property
    def state(self):
        pass

    @property
    def order_data(self):
        return self.fields


class Service(object):
    def __init__(self, contract, fields):
        assert contract
        assert fields

        self.fields = fields

        self._contract = contract

    @property
    def contract(self):
        return self._contract

    @property
    def type(self):
        pass

    @property
    def state(self):
        pass

    @property
    def service_data(self):
        return self.fields


class DomainRegistrarConfig(object):
    def __init__(self, config_name):
        assert config_name

        self.config = settings.DOMAIN_REGISTRARS[config_name]

    def get_connector(self, **kwargs):
        connector_class = loader.get_class(self.config['connector'])

        auth_options = self.config['auth']
        auth_options.update(kwargs)

        return connector_class(**auth_options)


class PersonalDataSerializer(object):
    def serialize(self, personal_data_instance):
        assert personal_data_instance

        raise Exception('Not implemented')
