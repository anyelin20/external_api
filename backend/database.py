import pymysql

def conectar_db():
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="123Queso",
        database="weather_app",
        cursorclass=pymysql.cursors.DictCursor
    )
