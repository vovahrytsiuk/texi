from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from SingletonDB import DB
from clients import Clients
from Drivers import Drivers
from Operators import Operators

from Specification import *
import requests


class Builder(ABC):
    @property
    @abstractmethod
    def requests(self) -> None:
        pass

    @abstractmethod
    def get_from_source(self) -> None:
        pass

    @abstractmethod
    def filter_requests(self) -> None:
        pass

    @abstractmethod
    def to_json(self) -> None:
        pass


class OwnRequestsBuilder(Builder):
    def __init__(self) -> None:
        self._requests = OwnRequests()

    def reset(self) -> None:
        self._requests = OwnRequests()

    @property
    def requests(self) -> OwnRequests:
        requests = self._requests
        self.reset()
        return requests

    def get_from_source(self) -> None:
        self._requests.set_requests(DB().get_data())

    def filter_requests(self) -> None:
        self._requests.filter_requests()

    def to_json(self) -> None:
        formatted_requests = []
        for row in self.requests.requests:
            req = {"requests_id": row[0], "client_id": row[1], "driver_id": row[2], "operator_id": row[3],
                   "from_address": row[4], "to_address": row[5], "time": str(row[6]),
                   "payment_type": row[7], "client_name": row[8], "phone_number": row[9], "driver_name": row[10],
                   "is_available": str(row[11]), "operator_name": row[12], "password": row[13]}
            formatted_requests.append(req)
        self._requests.set_requests(formatted_requests)


class ClientsBuilder(Builder):
    def __init__(self):
        self.clients = []

    def reset(self) -> None:
        self.clients = []

    @property
    def requests(self):
        print(self.clients)
        requests = self.clients
        self.reset()
        return requests

    def get_from_source(self, args) -> None:
        client = Clients()
        self.clients = client.select_data(args)
        print(self.clients)

    def filter_requests(self) -> None:
        pass

    def to_json(self) -> None:
        clients = []
        for client in self.clients:
            c = {
                "client_id": client[0],
                "client_name": str(client[1]),
                "phone_number": client[2]
            }
            clients.append(c)
        self.clients = clients
        print(self.clients)


class DriversBuilder(Builder):
    def __init__(self):
        self.drivers = []

    def reset(self) -> None:
        self.drivers = []

    @property
    def requests(self):
        requests = self.drivers
        self.reset()
        return requests

    def get_from_source(self, args) -> None:
        driver = Drivers()
        self.drivers = driver.select_data(args)

    def filter_requests(self) -> None:
        pass

    def to_json(self) -> None:
        drivers = []
        for driver in self.drivers:
            c = {
                "driver_id": driver[0],
                "driver_name": str(driver[1]),
                "is_available": driver[2]
            }
            drivers.append(c)
        self.drivers = drivers


class OperatorsBuilder(Builder):
    def __init__(self):
        self.operators = []

    def reset(self) -> None:
        self.operators = []

    @property
    def requests(self):
        requests = self.operators
        self.reset()
        return requests

    def get_from_source(self, args) -> None:
        operator = Operators()
        self.operators = operator.select_data(args)

    def filter_requests(self) -> None:
        pass

    def to_json(self) -> None:
        operators = []
        for op in self.operators:
            c = {
                "operator_id": op[0],
                "operator_name": str(op[1]),
                "password": op[2]
            }
            operators.append(c)
        self.operators = operators


class FromCacheBuilder(Builder):
    def __init__(self) -> None:
        self._requests = OwnRequests()

    def reset(self) -> None:
        self._requests = OwnRequests()

    @property
    def requests(self) -> OwnRequests:
        requests = self._requests
        self.reset()
        return requests

    def get_from_source(self, args=None) -> None:
        self._requests.set_requests(DB().select_requests(args))

    def filter_requests(self) -> None:
        pass

    def to_json(self) -> None:
        result = []
        for req in self._requests.requests:
            a = {"request_id": req[0], "client_id": req[1], "driver_id": req[2], "operator_id": req[3],
                 "from_address": str(req[4]),
                 "to_address": str(req[5]), "payment_type": str(req[6]), "client_name": str(req[8]),
                 "driver_name": str(req[7]), "operator_name": str(req[9])}
            result.append(a)
        self._requests.requests = result


class Service1Builder(Builder):
    def __init__(self) -> None:
        self._requests = OwnRequests()

    def reset(self) -> None:
        self._requests = OwnRequests()

    @property
    def requests(self) -> OwnRequests:
        requests = self._requests
        self.reset()
        return requests

    def get_from_source(self) -> None:
        self._requests.set_requests(requests.get('http://127.0.0.1:5001/search/').json())

    def filter_requests(self) -> None:
        pass

    def to_json(self) -> None:
        pass


class Service2Builder(Builder):
    def __init__(self) -> None:
        self._requests = OwnRequests()

    def reset(self) -> None:
        self._requests = OwnRequests()

    @property
    def requests(self) -> OwnRequests:
        requests = self._requests
        self.reset()
        return requests

    def get_from_source(self) -> None:
        self._requests.set_requests(requests.get('http://127.0.0.1:5002/short_search/').json())
        request_details = []
        for req in self._requests.requests:
            request_details.append(requests.get('http://127.0.0.1:5002/details/{}'.format(req["requests_id"])).json())
        self._requests.set_requests(request_details)

    def filter_requests(self) -> None:
        self._requests.filter_requests()

    def to_json(self) -> None:
        pass


class OwnRequests:
    def __init__(self) -> None:
        self.requests = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def merge(self, other_requests: OwnRequests):
        self.requests += other_requests.requests

    def delete_request(self, id):
        del self.requests[id]

    def set_requests(self, new_requests):
        self.requests = new_requests

    def filter_requests(self):
        specification = RequestIDFilter() & ClientIDFilter() & DriverIDFilter() & \
                        OperatorIDFilter() & PaymentTypeFilter() & \
                        BeforeTimeFilter() & AfterDateFilter()
        filtered_requests = []
        for request in self.requests:
            if specification.is_satisfied_by(request):
                filtered_requests.append(request)
        self.requests = filtered_requests


class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def build_all_requests(self, args) -> None:
        self.builder.get_from_source(args)
        self.builder.to_json()