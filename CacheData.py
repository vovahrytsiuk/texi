import threading
from flask_restful import reqparse
from SingletonDB import SingletonMeta, DB
import datetime
from Builder import OwnRequestsBuilder, Service2Builder, Service1Builder, Director
import multiprocessing as mp
from psycopg2.extras import execute_values


class CacheTable(metaclass=SingletonMeta):
    def __init__(self):
        self.own_cache = []
        self.service1_cache = []
        self.service2_cache = []
        self.director = Director()

    @staticmethod
    def time_to_update():
        dt = datetime.datetime.now()
        tomorrow = dt + datetime.timedelta(days=1)
        return (datetime.datetime.combine(tomorrow, datetime.time.min) - dt).seconds

    def own_requests(self, queue):
        builder = OwnRequestsBuilder()
        self.director.builder = builder
        self.director.build_all_requests()
        own = builder.requests
        print(len(own.requests))
        queue.put(own.requests)

    def service1_requests(self, queue):
        builder = Service1Builder()
        self.director.builder = builder
        self.director.build_all_requests()
        service1requests = builder.requests
        print(len(service1requests.requests))
        queue.put(service1requests.requests)

    def service2_requests(self, queue):
        builder = Service2Builder()
        self.director.builder = builder
        self.director.build_all_requests()
        service2requests = builder.requests
        print(len(service2requests.requests))
        queue.put(service2requests.requests)

    def update_cache(self):
        queue1 = mp.Queue()
        p1 = mp.Process(target=self.own_requests, args=(queue1,))

        queue2 = mp.Queue()
        p2 = mp.Process(target=self.service1_requests, args=(queue2,))

        queue3 = mp.Queue()
        p3 = mp.Process(target=self.service2_requests, args=(queue3,))

        p1.start()
        p2.start()
        p3.start()

        self.own_cache = queue1.get()
        self.service1_cache = queue2.get()
        self.service2_cache = queue3.get()

        with DB().conn.cursor() as cursor:
            cursor.execute('truncate "cache"')
            requests = self.own_cache + self.service1_cache + self.service2_cache
            execute_values(cursor,
                           '''INSERT INTO "cache" 
                           ("requestID", "clientID", "driverID", "operatorID", "fromAddress", "toAddress", "time", 
                           "paymentType", "clientFullName", "phoneNumber",  "driverFullName", "isAvailable",
                            "operatorFullName", "password") VALUES %s''',
                           [(args["requests_id"], args["client_id"], args["driver_id"], args["operator_id"],
                             str(args["from_address"]), str(args["to_address"]), str(args["time"]),
                             str(args["payment_type"]), str(args["client_name"]), args["phone_number"],
                             str(args["driver_name"]), str(args["is_available"]), str(args["operator_name"]),
                             str(args["password"])) for args in requests])

        DB().commit()
        p1.join()
        p2.join()
        p3.join()
        timer = threading.Timer(self.time_to_update(), self.update_cache)
        timer.start()

