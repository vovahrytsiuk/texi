from __future__ import annotations
from Builder import *
from flask_restful import Resource, Api, reqparse
import time


class Facade:
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.director = Director()

    def get_requests(self):
        builder = OwnRequestsBuilder()
        self.director.builder = builder
        self.director.build_all_requests()
        return builder.requests.requests

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

