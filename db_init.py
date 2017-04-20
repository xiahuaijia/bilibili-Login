import mysql.connector

conn = mysql.connector.connect(host = '114.215.137.141', port=3306, user = 'test', password = '123456', database = 'test')
cursor = conn.cursor()
try:
    cursor.execute("CREATE TABLE user ("
                   "username VARCHAR (20) PRIMARY KEY NOT NULL,"
                   "password VARCHAR (100) NOT NULL,"
                   "salt0 VARCHAR(20) NOT NULL,"
                   "salt1 VARCHAR(20) NOT NULL)")

    cursor.execute("CREATE TABLE buser (b_user VARCHAR (20) PRIMARY KEY NOT NULL, "
                   "isQiandao TINYINT NOT NULL)")
except:
    cursor.execute("DROP TABLE user")
    cursor.execute("DROP TABLE buser")