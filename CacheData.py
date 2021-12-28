import datetime
import threading
import multiprocessing as mp

from psycopg2.extras import execute_values
from SingletonDB import DB
from Builder import Director, OwnRequestsBuilder, Service1Builder, Service2Builder


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RequestsCache(metaclass=SingletonMeta):
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
        self.director.build_all_product()
        own = builder.product
        print(len(own.products))
        queue.put(own.products)

    def service1_requests(self, queue):
        builder = Service1Builder()
        self.director.builder = builder
        self.director.build_all_product()
        serv1 = builder.product
        print(len(serv1.products))
        queue.put(serv1.products)

    def service2_requests(self, queue):
        builder = Service2Builder()
        self.director.builder = builder
        self.director.build_all_product()
        serv2 = builder.product
        print(len(serv2.products))
        queue.put(serv2.products)

    def update_cache(self):
        queue1 = mp.Queue()
        p1 = mp.Process(target=self.own_requests, args=(queue1,))

        queue2 = mp.Queue()
        p2 = mp.Process(target=self.service1_requests, args=(queue2,))

        queue3 = mp.Queue()
        p3 = mp.Process(target=self.service2_requests, args=(queue3,))

        self.own_cache = queue1.get()
        self.service1_cache = queue2.get()
        self.service2_cache = queue3.get()

        with DB().conn.cursor() as cursor:
            cursor.execute('truncate "cache"')
            requests = self.own_cache + self.service1_cache + self.service2_cache
            for req in requests:
                cursor.execute(
                    '''
                    insert into "cache" ("requestID",
                                        "clientID",
                                        "driverID",
                                        "operatorID",
                                        "fromAddress",
                                        "toAddress",
                                        "time" ,
                                        "paymentType",
                                        "clientFullName" ,
                                        "phoneNumber",
                                        "driverFullName" ,
                                        "isAvailable" ,
                                        "operatorFullName",
                                        "password" )
                    values (
                                        {},
                                        {},
                                        {},
                                        {},
                                        {},
                                        {},
                                        {},
                                        {},
                                        {},
                                        {},
                                        {},
                                        {},
                                        {},
                                        {}
                    )
                    '''.format(req["request_id"],
                               req["client_id"],
                               req["driver_id"],
                               req["operator_id"],
                               req["from_address"],
                               req["to_address"],
                               req["time"],
                               req["payment_type"],
                               req["client_name"],
                               req["phone_number"],
                               req["drivar_name"],
                               req["is_available"],
                               req["operator_name"],
                               req["password"])
                )

        DB().commit()
        p1.join()
        p2.join()
        p3.join()
        timer = threading.Timer(self.time_to_update(), self.update)
        timer.start()
