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
        self.conn = psycopg2.connect(dbname='taxi', user='systemUser', password='jw8s0F4', host='localhost')

    def get_data(self):
        data = []
        with self.conn.cursor() as cursor:
            cursor.execute('select "requestsID", requests."clientID", requests."driverID", requests."operatorID", "fromAddress", "toAddress", "time", "paymentType", "clientFullName", "phoneNumber", "driverFullName", "isAvailable", "operatorFullName", "password" from "requests" join "clients" on ("requests"."clientID" = "clients"."clientID") join "drivers" on ("requests"."driverID" = "drivers"."driverID") join "operators" on ("operators"."operatorID" = "requests"."operatorID")')
            data = cursor.fetchall()
        return data

    def insert_request(self, args):
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''insert into "requests" 
                ("clientID", "operatorID", "driverID", "fromAddress", "toAddress", "time", "paymentType")
                values ({},     {},         {},         '{}',           '{}',       '{}',     '{}')'''.format(
                    args["client_id"],
                    args["operator_id"],
                    args["driver_id"],
                    args["from_address"],
                    args["to_address"],
                    datetime.datetime.now().date(),
                    args["payment_type"]
                )
            )
