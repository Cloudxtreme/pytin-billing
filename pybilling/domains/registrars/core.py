# coding=utf-8
from __future__ import unicode_literals


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

    def create_order(self):
        pass

    def find_orders(self):
        pass

    def find_services(self):
        pass


class Order(object):
    def __init__(self, contract):
        assert contract

        self.contract = contract

    def find_services(self):
        pass

    def cancel(self):
        pass

    @property
    def status(self):
        pass


class Service(object):
    def __init__(self, order):
        assert order

        self.order = order

    @property
    def type(self):
        pass

    @property
    def state(self):
        pass

    @property
    def service_data(self):
        pass
