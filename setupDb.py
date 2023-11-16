import mysql.connector

from dotenv import load_dotenv
load_dotenv()
import os

db = mysql.connector.connect(
    host=os.getenv("JAWSDB_HOST"),
    user =os.getenv("JAWSDB_USER"), 
    passwd = os.getenv("JAWSDB_PASSWORD"),
    database = os.getenv("JAWDB_DB_NAME")
)

mycursor = db.cursor()
# mycursor.execute("CREATE DATABASE testdatabase")  # create database, first step





