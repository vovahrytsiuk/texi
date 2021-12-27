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
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


class Post(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "POST":
            # self.facade.insert()
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
            # self.facade.delete()
            return "OK"
        else:
            return super().handle(request)
