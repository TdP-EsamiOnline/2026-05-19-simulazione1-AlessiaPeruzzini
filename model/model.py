from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getAllGenere(self):
        return DAO.getAllGenere()