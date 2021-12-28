# from flask import Flask, render_template, request
# from flask_restful import Resource, Api, reqparse
# from Handler import *
# from SingletonDB import DB
#
# if __name__ == "__main__":
#     app = Flask(__name__)
#     api = Api(app)
#
#     @app.route("/get_requests/", methods=['GET', 'POST', 'DELETE', 'PUT'])
#     def get_requests():
#         post = Post()
#         get = Get()
#         delete = Delete()
#         put = Put()
#         post.set_next(get).set_next(delete).set_next(put)
#         return post.handle(request.method)
#
#     app.run(debug=False)
#     DB().conn.close()
#
# from __future__ import annotations
# from abc import ABC, abstractmethod
# from typing import Any
# from SingletonDB import DB
# from Specification import *
# import requests
#
#
# class Builder(ABC):
#     @property
#     @abstractmethod
#     def requests(self) -> None:
#         pass
#
#     @abstractmethod
#     def get_from_source(self) -> None:
#         pass
#
#     @abstractmethod
#     def filter_requests(self) -> None:
#         pass
#
#     @abstractmethod
#     def to_json(self) -> None:
#         pass
#
#
# class OwnRequestsBuilder(Builder):
#     def __init__(self) -> None:
#         self._requests = OwnRequests()
#
#     def reset(self) -> None:
#         self._requests = OwnRequests()
#
#     @property
#     def requests(self) -> OwnRequests:
#         requests = self._requests
#         self.reset()
#         return requests
#
#     def get_from_source(self) -> None:
#         self._requests.set_requests(DB().get_data())
#
#     def filter_requests(self) -> None:
#         self._requests.filter_requests()
#
#     def to_json(self) -> None:
#         formatted_requests = []
#         for row in self.requests.requests:
#             req = {"requests_id": row[0], "client_id": row[1], "driver_id": row[2], "operator_id": row[3],
#                    "from_address": row[4], "to_address": row[5], "time": str(row[6]),
#                    "payment_type": row[7], "client_name": row[8], "phone_number": row[9], "driver_name": row[10],
#                    "is_available": str(row[11]), "operator_name": row[12], "password": row[13]}
#             formatted_requests.append(req)
#         self._requests.set_requests(formatted_requests)
#
#
# class Service1Builder(Builder):
#     def __init__(self) -> None:
#         self._requests = OwnRequests()
#
#     def reset(self) -> None:
#         self._requests = OwnRequests()
#
#     @property
#     def requests(self) -> OwnRequests:
#         requests = self._requests
#         self.reset()
#         return requests
#
#     def get_from_source(self) -> None:
#         self._requests.set_requests(requests.get('http://127.0.0.1:5001/search/').json())
#
#     def filter_requests(self) -> None:
#         self._requests.filter_requests()
#
#     def to_json(self) -> None:
#         pass
#
#
# class Service2Builder(Builder):
#     def __init__(self) -> None:
#         self._requests = OwnRequests()
#
#     def reset(self) -> None:
#         self._requests = OwnRequests()
#
#     @property
#     def requests(self) -> OwnRequests:
#         requests = self._requests
#         self.reset()
#         return requests
#
#     def get_from_source(self) -> None:
#         self._requests.set_requests(requests.get('http://127.0.0.1:5002/short_search/').json())
#         request_details = []
#         for req in self._requests.requests:
#             request_details.append(requests.get('http://127.0.0.1:5002/details/{}'.format(req["requests_id"])).json())
#
#     def filter_requests(self) -> None:
#         self._requests.filter_requests()
#
#     def to_json(self) -> None:
#         pass
#
#
# class OwnRequests:
#     def __init__(self) -> None:
#         self.requests = []
#
#     def add(self, part: Any) -> None:
#         self.parts.append(part)
#
#     def merge(self, other_requests: OwnRequests):
#         self.requests += other_requests.requests
#
#     def delete_request(self, id):
#         del self.requests[id]
#
#     def set_requests(self, new_requests):
#         self.requests = new_requests
#
#     def filter_requests(self):
#         specification = RequestIDFilter() & ClientIDFilter() & DriverIDFilter() & \
#                         OperatorIDFilter() & PaymentTypeFilter() & \
#                         BeforeTimeFilter() & AfterDateFilter()
#         filtered_requests = []
#         for request in self.requests:
#             if specification.is_satisfied_by(request):
#                 filtered_requests.append(request)
#         self.requests = filtered_requests
#
#
# class Director:
#     def __init__(self) -> None:
#         self._builder = None
#
#     @property
#     def builder(self) -> Builder:
#         return self._builder
#
#     @builder.setter
#     def builder(self, builder: Builder) -> None:
#         self._builder = builder
#
#     def build_all_requests(self) -> None:
#         self.builder.get_from_source()
#         self.builder.to_json()
#         self.builder.filter_requests()
#
# from __future__ import annotations
# from Builder import *
# from flask_restful import Resource, Api, reqparse
# import time
#
#
# class Facade:
#     def __init__(self) -> None:
#         self.parser = reqparse.RequestParser()
#         self.director = Director()
#
#     def get_requests(self):
#         builder = OwnRequestsBuilder()
#         self.director.builder = builder
#         self.director.build_all_requests()
#         own = builder.requests
#
#         builder = Service1Builder()
#         self.director.builder = builder
#         self.director.build_all_requests()
#         add1 = builder.requests
#
#         builder = Service2Builder()
#         self.director.builder = builder
#         self.director.build_all_requests()
#         add2 = builder.requests
#
#         own.merge(add1)
#         own.merge(add2)
#         return own.requests
#
#     def post_request(self):
#         self.parser.add_argument("client_id", type=int)
#         self.parser.add_argument("operator_id", type=int)
#         self.parser.add_argument("driver_id", type=int)
#         self.parser.add_argument("from_address", type=str)
#         self.parser.add_argument("to_address", type=str)
#         self.parser.add_argument("payment_type", type=str)
#
#         args = self.parser.parse_args()
#         DB().insert_request(args)
#
#     def delete_request(self):
#         self.parser.add_argument("request_id", type=int)
#         args = self.parser.parse_args()
#         DB().delete_request(args)
#
#     def update_request(self):
#         self.parser.add_argument("request_id", type=int)
#         self.parser.add_argument("client_id", type=int)
#         self.parser.add_argument("operator_id", type=int)
#         self.parser.add_argument("driver_id", type=int)
#         self.parser.add_argument("from_address", type=str)
#         self.parser.add_argument("to_address", type=str)
#         self.parser.add_argument("payment_type", type=str)
#
#         args = self.parser.parse_args()
#         DB().update_request(args)
#
# from __future__ import annotations
# from abc import ABC, abstractmethod
# from typing import Any, Optional
# from Facade import *
#
#
# class Handler(ABC):
#     @abstractmethod
#     def set_next(self, handler: Handler) -> Handler:
#         pass
#
#     @abstractmethod
#     def handle(self, request) -> Optional[str]:
#         pass
#
#
# class AbstractHandler(Handler):
#     _next_handler: Handler = None
#     facade: Facade = Facade()
#
#     def set_next(self, handler: Handler) -> Handler:
#         self._next_handler = handler
#         return handler
#
#     @abstractmethod
#     def handle(self, request: Any) -> str:
#         if self._next_handler:
#             return self._next_handler.handle(request)
#
#         return None
#
#
# class Post(AbstractHandler):
#     def handle(self, request: Any) -> str:
#         if request == "POST":
#             self.facade.post_request()
#             return "OK"
#         else:
#             return super().handle(request)
#
#
# class Get(AbstractHandler):
#     def handle(self, request: Any) -> str:
#         if request == "GET":
#             return {"requests": self.facade.get_requests()}
#         else:
#             return super().handle(request)
#
#
# class Delete(AbstractHandler):
#     def handle(self, request: Any) -> str:
#         if request == "DELETE":
#             self.facade.delete_request()
#             return "OK"
#         else:
#             return super().handle(request)
#
#
# class Put(AbstractHandler):
#     def handle(self, request: Any) -> str:
#         if request == "PUT":
#             self.facade.update_request()
#             return "OK"
#         else:
#             return super().handle(request)
#
# import psycopg2
# import time
# import datetime
#
#
# class SingletonMeta(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             instance = super().__call__(*args, **kwargs)
#             cls._instances[cls] = instance
#         return cls._instances[cls]
#
#
# class DB(metaclass=SingletonMeta):
#     def __init__(self):
#         self.conn = psycopg2.connect(dbname='taxi', user='systemUser', password='jw8s0F4', host='localhost')
#
#     def commit(self):
#         self.conn.commit()
#
#     def get_data(self):
#         data = []
#         with self.conn.cursor() as cursor:
#             cursor.execute(
#                 '''select   "requestsID", requests."clientID", requests."driverID",
#                             requests."operatorID", "fromAddress", "toAddress", "time",
#                             "paymentType", "clientFullName", "phoneNumber", "driverFullName",
#                             "isAvailable", "operatorFullName", "password"
#                     from "requests"
#                             join "clients" on ("requests"."clientID" = "clients"."clientID")
#                             join "drivers" on ("requests"."driverID" = "drivers"."driverID")
#                             join "operators" on ("operators"."operatorID" = "requests"."operatorID")''')
#             data = cursor.fetchall()
#         return data
#
#     def insert_request(self, args):
#         with self.conn.cursor() as cursor:
#             cursor.execute(
#                 '''insert into "requests"
#                 ("clientID", "operatorID", "driverID", "fromAddress", "toAddress", "time", "paymentType")
#                 values ({},     {},         {},         '{}',           '{}',       '{}',     '{}')'''.format(
#                     args["client_id"],
#                     args["operator_id"],
#                     args["driver_id"],
#                     args["from_address"],
#                     args["to_address"],
#                     datetime.datetime.now().date(),
#                     args["payment_type"]
#                 )
#             )
#         self.commit()
#
#     def delete_request(self, args):
#         with self.conn.cursor() as cursor:
#             cursor.execute(
#                 '''delete from "requests"
#                 where "requestsID" = {}
#                 '''.format(args["request_id"])
#             )
#         self.commit()
#
#     def update_request(self, args):
#         key_mapper = {
#             "request_id": "requestsID",
#             "client_id": "clientID",
#             "operator_id": "operatorID",
#             "driver_id": "driverID",
#             "from_address": "fromAddress",
#             "to_address": "toAddress",
#             "payment_type": "paymentType",
#         }
#         query = '''update "requests" set'''
#         for key, value in args.items():
#             if value is not None and key != "request_id":
#                 if type(value) == int:
#                     query += '"' + key_mapper[key] + '"' + '=' + str(value) + ","
#                 elif type(value) == str:
#                     query += '"' + key_mapper[key] + '"' + '=' + "'" + str(value) + "',"
#         query = query[0: -1]
#         query += '''where "requestsID" = {}'''.format(args["request_id"])
#         with self.conn.cursor() as cursor:
#             cursor.execute(query)
#         self.commit()
#
#
# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# from typing import Any
# from flask_restful import reqparse
# import datetime
#
#
# def to_date(date_string):
#     return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
#
#
# class BaseSpecification(ABC):
#     @abstractmethod
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         raise NotImplementedError()
#
#     def __call__(self, candidate: Any) -> bool:
#         return self.is_satisfied_by(candidate)
#
#     def __and__(self, other: BaseSpecification):
#         return AndSpecification(self, other)
#
#     def __or__(self, other: BaseSpecification):
#         return OrSpecification(self, other)
#
#
# @dataclass(frozen=True)
# class AndSpecification(BaseSpecification):
#
#
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         return self.first.is_satisfied_by(candidate) and self.second.is_satisfied_by(candidate)
#
#
# @dataclass(frozen=True)
# class OrSpecification(BaseSpecification):
#
#
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         return self.first.is_satisfied_by(candidate) or self.second.is_satisfied_by(candidate)
#
#
# class RequestIDFilter(BaseSpecification):
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         parser = reqparse.RequestParser()
#         parser.add_argument("request_id", type=int)
#         args = parser.parse_args()
#         if args["request_id"] is not None:
#             return candidate["requests_id"] == args["request_id"]
#         return True
#
#
# class ClientIDFilter(BaseSpecification):
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         parser = reqparse.RequestParser()
#         parser.add_argument("client_id", type=int)
#         args = parser.parse_args()
#         if args["client_id"] is not None:
#             return candidate["client_id"] == args["client_id"]
#         return True
#
#
# class DriverIDFilter(BaseSpecification):
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         parser = reqparse.RequestParser()
#         parser.add_argument("driver_id", type=int)
#         args = parser.parse_args()
#         if args["driver_id"] is not None:
#             return candidate["driver_id"] == args["driver_id"]
#         return True
#
#
# class OperatorIDFilter(BaseSpecification):
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         parser = reqparse.RequestParser()
#         parser.add_argument("operator_id", type=int)
#         args = parser.parse_args()
#         if args["operator_id"] is not None:
#             return candidate["operator_id"] == args["operator_id"]
#         return True
#
#
# class PaymentTypeFilter(BaseSpecification):
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         parser = reqparse.RequestParser()
#         parser.add_argument("payment_type", type=str)
#         args = parser.parse_args()
#         if args["payment_type"] is not None:
#             return candidate["payment_type"] == args["payment_type"]
#         return True
#
#
# class BeforeTimeFilter(BaseSpecification):
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         parser = reqparse.RequestParser()
#         parser.add_argument("before_date", type=to_date)
#         args = parser.parse_args()
#         if args["before_date"] is not None:
#             return to_date(candidate["time"]) < args["before_date"]
#         return True
#
#
# class AfterDateFilter(BaseSpecification):
#     def is_satisfied_by(self, candidate: Any) -> bool:
#         parser = reqparse.RequestParser()
#         parser.add_argument("after_date", type=to_date)
#         args = parser.parse_args()
#         if args["after_date"] is not None:
#             return to_date(candidate["time"]) > args["after_date"]
#         return True
