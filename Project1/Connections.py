import mysql.connector
from pymongo import MongoClient
from googleapiclient.discovery import build
import sqlalchemy

# local MySQL connection details
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="viswa"
)
my_sql_cursor = mydb.cursor(buffered=True)

database_username = 'root'
database_password = ''
database_ip       = 'localhost'
database_name     = 'viswa'
sql_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))

#MongoDB Atlas config details and connections
client = MongoClient("mongodb+srv://elayarajathiru:1234@cluster0.tklibaz.mongodb.net/?retryWrites=true&w=majority")
mongo_db = client.youtube_data
collections=mongo_db.channels


# Youtube API connections details
api_key = "AIzaSyC0DiVDCzkqhscbbeGCIyzhgKBshXliPv4"
youtube = build('youtube','v3',developerKey=api_key)