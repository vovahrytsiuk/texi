import psycopg2
import time
import datetime
import random
import string


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

    def generate_random_data(self):
        with self.conn.cursor() as cursor:
            for _ in range(100000):
                payment = ["cash", "py pass", "card"]
                payment_type = payment[random.randint(0, 2)]
                client = random.randint(1, 5)
                driver = random.randint(1, 5)
                operator = random.randint(1, 5)
                length = random.randint(5, 50)
                letters = string.ascii_lowercase
                from_address = ''.join(random.choice(letters) for i in range(length))
                length = random.randint(5, 50)
                to_address = ''.join(random.choice(letters) for i in range(length))
                start_date = datetime.date(1990, 1, 1)
                end_date = datetime.date(2030, 2, 1)

                time_between_dates = end_date - start_date
                days_between_dates = time_between_dates.days
                random_number_of_days = random.randrange(days_between_dates)
                random_date = start_date + datetime.timedelta(days=random_number_of_days)
                cursor.execute(
                    '''insert into "requests" 
                    ("clientID", "operatorID", "driverID", "fromAddress", "toAddress", "time", "paymentType")
                    values ({},     {},         {},         '{}',           '{}',       '{}',     '{}')'''.format(
                        client,
                        operator,
                        driver,
                        from_address,
                        to_address,
                        random_date,
                        payment_type
                    )
                )
        self.conn.commit()

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
