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
