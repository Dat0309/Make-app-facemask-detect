from PyQt5 import QtSql

db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("data.sqlite")

if not db.open():
    print("Error")

query = QtSql.QSqlQuery()
query.exec_("create table userdata (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username VARCHAR(50) NOT NULL, pass VARCHAR(50) NOT NULL);")
query.exec_("insert into userdata (username, pass) values('dat0309', '030901');")

query.exec_("select * from userdata where id=1;")
query.first()
print(query.value("username"), query.value("pass"))