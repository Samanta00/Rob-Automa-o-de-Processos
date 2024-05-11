# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")


class TcePipeline:
    def process_item(self, item, spider):
        return item


class savingToMysqlPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                database=os.getenv("MYSQL_DB"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD")
            )
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def process_item(self, item, spider):
        self.create_connection()
        return item