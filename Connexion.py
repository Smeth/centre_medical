from PySide2.QtSql import QSqlTableModel, QSqlDatabase, QSqlError, QSqlQuery, QSqlQueryModel


class DataConnexion:  # ma classe de connexion à la base de donnée
    def __init__(self):
        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("./DB/davina_db.sqlite")  # indiquez juste un chemin d'accès
        if con.open():
            print("Connexion etablie")
        else:
            print(con.lastError().text())


'''
con = DataConnexion()
query = QSqlQuery()
query.exec("SELECT * FROM patient")
cpt = 0
while query.next():
    print("valeur = ",query.value(cpt))
    cpt = cpt +1

print ("terminer")
'''