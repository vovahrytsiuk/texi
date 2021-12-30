from __future__ import annotations

from typing import Dict, Any

from Builder import Director, OwnRequestsBuilder, Service1Builder, Service2Builder, FromCacheBuilder, ClientsBuilder, DriversBuilder, OperatorsBuilder
from flask_restful import Resource, Api, reqparse
import time
from SingletonDB import DB
from CacheData import CacheTable
from Drivers import Drivers
from clients import Clients
from Operators import Operators


class Facade:
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.director = Director()
        self.driver = Drivers()
        self.client = Clients()
        self.operator = Operators()

    def get_requests(self):
        builder = FromCacheBuilder()
        self.director.builder = builder
        self.director.build_all_requests()
        own = builder.requests
        return own.requests

    def requests_resolver(self, obj, info, client_id=None, request_id=None, driver_id=None, operator_id=None,
                          payment_type=None, from_address=None, to_address=None):
        args = {
           "client_id": client_id,
           "request_id": request_id,
           "driver_id": driver_id,
           "operator_id": operator_id,
           "payment_type": payment_type,
           "from_address": from_address,
           "to_address": to_address
        }
        builder = FromCacheBuilder()
        self.director.builder = builder
        self.director.build_all_requests(args)
        cache = builder.requests
        return {"success": True, "requests": cache.requests}

    def clients_resolver(self, obj, info, client_id=None):
        args = {
            "client_id": client_id
        }
        builder = ClientsBuilder()
        self.director.builder = builder
        self.director.build_all_requests(args)
        clients = builder.requests
        return {"success": True, "clients": clients}

    def driver_resolver(self, obj, info, driver_id=None):
        args = {
            "driver_id": driver_id
        }
        builder = DriversBuilder()
        self.director.builder = builder
        self.director.build_all_requests(args)
        drivers = builder.requests
        return {"success": True, "drivers": drivers}

    def operator_resolver(self, obj, info, operator_id=None):
        args = {
            "operator_id": operator_id
        }
        builder = OperatorsBuilder()
        self.director.builder = builder
        self.director.build_all_requests(args)
        operators = builder.requests
        return {"success": True, "operators": operators}

    def create_driver_resolver(self, obj, info, driver_name, is_available):
        args = {
            "driver_name": driver_name,
            "is_available": is_available
        }
        return {"success": True, "drivers": self.driver.insert_data(args)}

    def create_client_resolver(self, obj, info, client_name, phone_number):
        args = {
            "client_name": client_name,
            "phone_number": phone_number
        }
        return {"success": True, "clients": self.client.insert_data(args)}

    def create_operator_resolver(self, obj, info, operator_name, password):
        args = {
            "operator_name": operator_name,
            "password": password
        }
        op = self.operator.insert_data(args)
        print(op)
        return {"success": True, "operators": op}

    def create_request_resolver(self, obj, info, client_id, driver_id, operator_id, from_address, to_address, payment_type):
        args = {
            "client_id": client_id,
            "driver_id": driver_id,
            "operator_id": operator_id,
            "from_address": from_address,
            "to_address": to_address,
            "payment_type": to_address
        }
        id = DB().insert_request(args)
        return self.requests_resolver(obj, info, request_id=id)

    def update_client_resolver(self, obj, info, client_id, client_name=None, phone_number=None):
        args = {
            "client_id": client_id,
            "client_name": client_name,
            "phone_number": phone_number
        }
        id = self.client.update_data(args)
        print(id)
        return self.clients_resolver(obj, info, id)

    def update_driver_resolver(self, obj, info, driver_id, driver_name=None, is_available=None):
        args = {
            "driver_id": driver_id,
            "driver_name": driver_name,
            "is_available": is_available
        }
        id = self.driver.update_data(args)
        print(id)
        return self.driver_resolver(obj, info, id)

    def update_operator_resolver(self, obj, info, operator_id, operator_name=None, password=None):
        args = {
            "operator_id": operator_id,
            "operator_name": operator_name,
            "password": password
        }
        id = self.operator.update_data(args)
        print(id)
        return self.operator_resolver(obj, info, id)

    def delete_client_resolver(self, obj, info, client_id):
        args = {
            "client_id": client_id
        }
        self.client.delete_data(args)
        return self.clients_resolver(obj, info)

    def delete_driver_resolver(self, obj, info, driver_id):
        args = {
            "driver_id": driver_id
        }
        self.driver.delete_data(args)
        return self.driver_resolver(obj, info)


    def post_request(self):
        self.parser.add_argument("client_id", type=int)
        self.parser.add_argument("operator_id", type=int)
        self.parser.add_argument("driver_id", type=int)
        self.parser.add_argument("from_address", type=str)
        self.parser.add_argument("to_address", type=str)
        self.parser.add_argument("payment_type", type=str)

        args = self.parser.parse_args()
        DB().insert_request(args)

    def delete_request(self):
        self.parser.add_argument("request_id", type=int)
        args = self.parser.parse_args()
        DB().delete_request(args)

    def update_request(self):
        self.parser.add_argument("request_id", type=int)
        self.parser.add_argument("client_id", type=int)
        self.parser.add_argument("operator_id", type=int)
        self.parser.add_argument("driver_id", type=int)
        self.parser.add_argument("from_address", type=str)
        self.parser.add_argument("to_address", type=str)
        self.parser.add_argument("payment_type", type=str)

        args = self.parser.parse_args()
        DB().update_request(args)

