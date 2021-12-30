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

    def update_data(self, args) -> int:
        key_mapper = {
            "driver_id": "driverID",
            "driver_name": "driverFullName",
            "is_available": "isAvailable"
        }
        query = '''update "drivers" set'''
        for key, value in args.items():
            if value is not None and key != "driver_id":
                if type(value) == int:
                    query += '"' + key_mapper[key] + '"' + '=' + str(value) + ","
                elif type(value) == str:
                    query += '"' + key_mapper[key] + '"' + '=' + "'" + str(value) + "',"
        query = query[0: -1]
        query += '''where "driverID" = {}'''.format(args["driver_id"])
        with self.conn.cursor() as cursor:
            cursor.execute(query)
        self.conn.commit()
        return args["driver_id"]

    def delete_data(self, args):
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''delete from "drivers"
                where "driverID" = {}
                '''.format(args["driver_id"])
            )
        self.conn.commit()
