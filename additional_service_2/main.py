import random

from flask import Flask
from flask_restful import Resource, Api, reqparse
from Specification import *
import psycopg2
import time
import datetime


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DB(metaclass=SingletonMeta):
    def __init__(self):
        self.conn = psycopg2.connect(dbname='taxi2', user='service2', password='11111111', host='localhost')

    def commit(self):
        self.conn.commit()

    def get_data(self):
        data = []
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''select   "requestsID", requests."clientID", requests."driverID", 
                            requests."operatorID", "fromAddress", "toAddress", "time", 
                            "paymentType", "clientFullName", "phoneNumber", "driverFullName", 
                            "isAvailable", "operatorFullName", "password" 
                    from "requests" 
                            join "clients" on ("requests"."clientID" = "clients"."clientID") 
                            join "drivers" on ("requests"."driverID" = "drivers"."driverID") 
                            join "operators" on ("operators"."operatorID" = "requests"."operatorID")''')
            data = cursor.fetchall()
        return data

    def get_data_by_id(self, id: int):
        data = []
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''select   "requestsID", requests."clientID", requests."driverID", 
                            requests."operatorID", "fromAddress", "toAddress", "time", 
                            "paymentType", "clientFullName", "phoneNumber", "driverFullName", 
                            "isAvailable", "operatorFullName", "password" 
                    from "requests" 
                            join "clients" on ("requests"."clientID" = "clients"."clientID") 
                            join "drivers" on ("requests"."driverID" = "drivers"."driverID") 
                            join "operators" on ("operators"."operatorID" = "requests"."operatorID")
                    where "requestsID" = {}'''.format(id))
            data = cursor.fetchall()
        return data


class ShortRequests(Resource):
    def get(self):
        requests = DB().get_data()
        formatted_requests = []
        for row in requests:
            req = {"requests_id": row[0], "client_id": row[1], "driver_id": row[2], "operator_id": row[3],
                   "from_address": row[4], "to_address": row[5], "time": str(row[6]),
                   "payment_type": row[7], "client_name": row[8], "phone_number": row[9], "driver_name": row[10],
                   "is_available": str(row[11]), "operator_name": row[12], "password": row[13]}
            formatted_requests.append(req)
        formatted_requests

        return formatted_requests


class RequestDetail(Resource):
    def get(self, id: int):
        requests = DB().get_data_by_id(id)
        formatted_requests = []
        for row in requests:
            req = {"requests_id": row[0], "client_id": row[1], "driver_id": row[2], "operator_id": row[3]}
            formatted_requests.append(req)
        requests = formatted_requests

        return requests


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(ShortRequests, '/short_search/')
    api.add_resource(RequestDetail, '/details/<int:id>')

    app.run(port=5002, debug=True)
