from SingletonDB import DB
import psycopg2


class Drivers:
    def __init__(self):
        self.conn = DB().conn

    @staticmethod
    def to_json(drivers_list):
        drivers = []
        for driver in drivers_list:
            c = {
                "driver_id": driver[0],
                "driver_name": str(driver[1]),
                "is_available": driver[2]
            }
            drivers.append(c)
        return drivers

    def select_data(self, args) -> list:
        query = '''
                select "driverID", "driverFullName", "isAvailable" 
                from "drivers" 
                '''
        if args["driver_id"] is not None:
            query += ''' where "driverID" = {}'''.format(args["driver_id"])
        drivers = []
        print(query)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            drivers = cursor.fetchall()
        print(drivers)
        return drivers

    def insert_data(self, args):
        id = 0
        query = '''
        insert into "drivers" ("driverFullName", "isAvailable")
        values ('{}', {})
        returning "driverID"
        '''.format(args["driver_name"], args["is_available"])
        print(query)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            id = cursor.fetchone()[0]
        self.conn.commit()

        return self.to_json(self.select_data({"driver_id": id}))
