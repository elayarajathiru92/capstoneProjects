import mysql.connector
from pymongo import MongoClient
from googleapiclient.discovery import build
import sqlalchemy

# local MySQL connection details
# replace your credentials here
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
my_sql_cursor = mydb.cursor(buffered=True)

# replace your credentials here
database_username = ''
database_password = ''
database_ip       = ''
database_name     = ''
sql_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))

#MongoDB Atlas config details and connections
# replace your credentials here
client = MongoClient("")
mongo_db = client.youtube_data
collections=mongo_db.channels


# Youtube API connections details
api_key = "" # replace your api key credentials here
youtube = build('youtube','v3',developerKey=api_key)
