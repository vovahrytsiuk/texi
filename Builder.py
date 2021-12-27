from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from SingletonDB import DB


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


class OwnRequestsBuilder(Builder):
    def __init__(self) -> None:
        self.reset()

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
        pass


class OwnRequests:
    def __init__(self) -> None:
        self.requests = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def merge(self, other_requests):
        self.requests += other_requests.requests

    def delete_request(self, id):
        del self.requests[id]

    def set_requests(self, new_requests):
        self.requests = new_requests

    def delete(self, id):
        pass
        # put here call to db to delete requests with id = id


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

    def build_filtered_requests(self) -> None:
        self.builder.get_from_source()
        self.builder.filter_requests()
