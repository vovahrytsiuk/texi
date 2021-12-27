from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from flask_restful import  reqparse
import datetime


def to_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()


class BaseSpecification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate: Any) -> bool:
        raise NotImplementedError()

    def __call__(self, candidate: Any) -> bool:
        return self.is_satisfied_by(candidate)

    def __and__(self, other: "BaseSpecification") -> "AndSpecification":
        return AndSpecification(self, other)

    def __or__(self, other: "BaseSpecification") -> "OrSpecification":
        return OrSpecification(self, other)


@dataclass(frozen=True)
class AndSpecification(BaseSpecification):
    first: BaseSpecification
    second: BaseSpecification

    def is_satisfied_by(self, candidate: Any) -> bool:
        return self.first.is_satisfied_by(candidate) and self.second.is_satisfied_by(candidate)


@dataclass(frozen=True)
class OrSpecification(BaseSpecification):
    first: BaseSpecification
    second: BaseSpecification

    def is_satisfied_by(self, candidate: Any) -> bool:
        return self.first.is_satisfied_by(candidate) or self.second.is_satisfied_by(candidate)


class RequestIDFilter(BaseSpecification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        parser = reqparse.RequestParser()
        parser.add_argument("request_id", type=int)
        args = parser.parse_args()
        if args["request_id"] is not None:
            return candidate["requests_id"] == args["request_id"]
        return True


class ClientIDFilter(BaseSpecification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        parser = reqparse.RequestParser()
        parser.add_argument("client_id", type=int)
        args = parser.parse_args()
        if args["client_id"] is not None:
            return candidate["client_id"] == args["client_id"]
        return True


class DriverIDFilter(BaseSpecification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        parser = reqparse.RequestParser()
        parser.add_argument("driver_id", type=int)
        args = parser.parse_args()
        if args["driver_id"] is not None:
            return candidate["driver_id"] == args["driver_id"]
        return True


class OperatorIDFilter(BaseSpecification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        parser = reqparse.RequestParser()
        parser.add_argument("operator_id", type=int)
        args = parser.parse_args()
        if args["operator_id"] is not None:
            return candidate["operator_id"] == args["operator_id"]
        return True


class PaymentTypeFilter(BaseSpecification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        parser = reqparse.RequestParser()
        parser.add_argument("payment_type", type=str)
        args = parser.parse_args()
        if args["payment_type"] is not None:
            return candidate["payment_type"] == args["payment_type"]
        return True


class BeforeTimeFilter(BaseSpecification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        parser = reqparse.RequestParser()
        parser.add_argument("before_date", type=to_date)
        args = parser.parse_args()
        if args["before_date"] is not None:
            return to_date(candidate["time"]) < args["before_date"]
        return True


class AfterDateFilter(BaseSpecification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        parser = reqparse.RequestParser()
        parser.add_argument("after_date", type=to_date)
        args = parser.parse_args()
        if args["after_date"] is not None:
            return to_date(candidate["time"]) > args["after_date"]
        return True
