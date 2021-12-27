from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional
from Facade import *


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None
    facade: Facade = Facade()

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


class Post(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "POST":
            self.facade.post_request()
            return "OK"
        else:
            return super().handle(request)


class Get(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "GET":
            return {"requests": self.facade.get_requests()}
        else:
            return super().handle(request)


class Delete(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "DELETE":
            self.facade.delete_request()
            return "OK"
        else:
            return super().handle(request)
