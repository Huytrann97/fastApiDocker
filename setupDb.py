import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "Asdasd123@",
    database = "testdatabase"
)

mycursor = db.cursor()

# mycursor.execute("CREATE DATABASE testdatabase")  # create database



