from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from SingletonDB import DB
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
        self._requests.set_requests(DB().select_requests())

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
        self._requests.filter_requests()

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

    def build_all_requests(self) -> None:
        self.builder.get_from_source()
        self.builder.to_json()
        self.builder.filter_requests()
