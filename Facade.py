from __future__ import annotations
from Builder import *
from flask_restful import Resource, Api, reqparse


class Facade:
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.director = Director()

    def get_requests(self):
        builder = OwnRequestsBuilder()
        self.director.builder = builder
        self.director.build_all_requests()
        return builder.requests.requests
