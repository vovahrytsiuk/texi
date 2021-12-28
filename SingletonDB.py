import psycopg2
import time
import datetime
from flask_restful import reqparse


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
        self.commit()

    def delete_request(self, args):
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''delete from "requests"
                where "requestsID" = {}
                '''.format(args["request_id"])
            )
        self.commit()

    def update_request(self, args):
        key_mapper = {
            "request_id": "requestsID",
            "client_id": "clientID",
            "operator_id": "operatorID",
            "driver_id": "driverID",
            "from_address": "fromAddress",
            "to_address": "toAddress",
            "payment_type": "paymentType",
        }
        query = '''update "requests" set'''
        for key, value in args.items():
            if value is not None and key != "request_id":
                if type(value) == int:
                    query += '"' + key_mapper[key] + '"' + '=' + str(value) + ","
                elif type(value) == str:
                    query += '"' + key_mapper[key] + '"' + '=' + "'" + str(value) + "',"
        query = query[0: -1]
        query += '''where "requestsID" = {}'''.format(args["request_id"])
        with self.conn.cursor() as cursor:
            cursor.execute(query)
        self.commit()

    def select_requests(self):
        parser = reqparse.RequestParser()
        parser.add_argument("client_id", type=int),
        parser.add_argument("request_id", type=int),
        parser.add_argument("driver_id", type=int),
        parser.add_argument("operator_id", type=int),
        parser.add_argument("payment_type", type=str),
        parser.add_argument("before_date", type=self.to_date),
        parser.add_argument("after_date", type=self.to_date)
        args = parser.parse_args()
        query = '''
        select "requestsID", "clientID", "driverID", 
        "operatorID", "fromAddress", "toAddress", "time", 
        "paymentType", "clientFullName", "phoneNumber", "driverFullName", 
        "isAvailable", "operatorFullName", "password"
        from "cache"
        '''
        options = []
        if args["request_id"] is not None:
            options.append('''
            "requestsID" = '{}'
            '''.format(args["request_id"]))
        if args["client_id"] is not None:
            options.append('''
            "clientID" = '{}'
            '''.format(args["client_id"]))
        if args["driver_id"] is not None:
            options.append('''
            "driverID" = '{}'
            '''.format(args["driver_id"]))
        if args["operator_id"] is not None:
            options.append('''
            "operatorID" = '{}'
            '''.format(args["operator_id"]))
        if args["payment_type"] is not None:
            options.append('''
            "paymentType" = '{}'
            '''.format(args["payment_type"]))
        if args["before_date"] is not None:
            options.append('''
            "time" < '{}'
            '''.format(args["before_date"]))
        if args["after_date"] is not None:
            options.append('''
            "time" > '{}'
            '''.format(args["after_date"]))
        if options is not []:
            query += " where "
        for i in range(len(options)):
            query += options[i]
            if i != len(options) - 1:
                query += " and "
        requests_data = []
        with DB().conn.cursor() as cursor:
            cursor.execute(query)
            requests_data = cursor.fetchall()
        return requests_data
