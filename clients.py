from SingletonDB import DB
import psycopg2


class Clients:
    def __init__(self):
        self.conn = DB().conn

    @staticmethod
    def to_json(clients_list):
        clients = []
        for client in clients_list:
            c = {
                "client_id": client[0],
                "client_name": str(client[1]),
                "phone_number": client[2]
            }
            clients.append(c)
        return clients

    def select_data(self, args) -> list:
        query = '''
                select "clientID", "clientFullName", "phoneNumber" 
                from "clients" 
                '''
        if args["client_id"] is not None:
            query += ''' where "clientID" = {}'''.format(args["client_id"])
        clients = []
        print(query)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            clients = cursor.fetchall()
        print(clients)
        return clients

    def insert_data(self, args):
        id = 0
        query = '''
        insert into "clients" ("clientFullName", "phoneNumber")
        values ('{}', {})
        returning "clientID"
        '''.format(args["client_name"], args["phone_number"])
        print(query)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            id = cursor.fetchone()[0]
        self.conn.commit()

        return self.to_json(self.select_data({"client_id": id}))

    def update_data(self, args) -> int:
        key_mapper = {
            "client_id": "clientID",
            "client_name": "clientFullName",
            "phone_number": "phoneNumber"
        }
        query = '''update "clients" set'''
        for key, value in args.items():
            if value is not None and key != "client_id":
                if type(value) == int:
                    query += '"' + key_mapper[key] + '"' + '=' + str(value) + ","
                elif type(value) == str:
                    query += '"' + key_mapper[key] + '"' + '=' + "'" + str(value) + "',"
        query = query[0: -1]
        query += '''where "clientID" = {}'''.format(args["client_id"])
        with self.conn.cursor() as cursor:
            cursor.execute(query)
        self.conn.commit()
        return args["client_id"]

    def delete_data(self, args):
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''delete from "clients"
                where "clientID" = {}
                '''.format(args["client_id"])
            )
        self.conn.commit()
