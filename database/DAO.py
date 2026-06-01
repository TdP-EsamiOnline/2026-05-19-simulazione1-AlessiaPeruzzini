from database.DB_connect import DBConnect
from model.genere import Genere


class DAO():

    @staticmethod
    def getAllGenere():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
            from genre"""

        cursor.execute(query)

        for row in cursor:
            results.append(Genere(**row))

        cursor.close()
        conn.close()
        return results