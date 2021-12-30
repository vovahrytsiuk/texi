from SingletonDB import DB
import psycopg2


class Operators:
    def __init__(self):
        self.conn = DB().conn

    @staticmethod
    def to_json(operators_list):
        operators = []
        for operator in operators_list:
            c = {
                "operator_id": operator[0],
                "operator_name": str(operator[1]),
                "password": str(operator[2])
            }
            operators.append(c)
        return operators

    def select_data(self, args) -> list:
        query = '''
                select "operatorID", "operatorFullName", "password" 
                from "operators" 
                '''
        if args["operator_id"] is not None:
            query += ''' where "operatorID" = {}'''.format(args["operator_id"])
        operators = []
        print(query)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            operators = cursor.fetchall()

        print(operators)
        return operators

    def insert_data(self, args):
        id = 0
        query = '''
        insert into "operators" ("operatorFullName", "password")
        values ('{}', '{}')
        returning "operatorID"
        '''.format(args["operator_name"], args["password"])
        print(query)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            id = cursor.fetchone()[0]
        self.conn.commit()

        return self.to_json(self.select_data({"operator_id": id}))