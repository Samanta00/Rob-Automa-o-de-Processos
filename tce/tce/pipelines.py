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
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_PORT= os.getenv("MYSQL_PORT")


print("MYSQL_HOST:", MYSQL_HOST)
print("MYSQL_DB:", MYSQL_DB)
print("MYSQL_PASSWORD:", MYSQL_PASSWORD)


class TcePipeline:
    def process_item(self, item, spider):
        return item

class savingToMysqlPipeline(object):
    def __init__(self):
        self.connection = None
        self.create_connection()
        if self.connection:
            self.create_table() 

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                database=MYSQL_DB,
                username='root',
                password=MYSQL_PASSWORD
            )
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute("USE registros_tce ")  
                cursor.close()
        except Error as e:
            print("Error while connecting to MySQL", e)

    def create_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS armazenamento_registros_tce (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    doc VARCHAR(255),
                    Nprocesso VARCHAR(255),
                    dataAtuacao VARCHAR(255),
                    partes TEXT,
                    materia TEXT,
                    url TEXT,
                    ementa TEXT
                )
            """)
            self.connection.commit()
            print("Table 'armazenamento_registros_tce' created successfully")
        except Error as e:
            print("Error while creating table:", e)
            self.connection = None

    def process_item(self, item, spider):
        try:
            cursor = self.connection.cursor()
            partes_str = ", ".join(item['partes'])

            cursor.execute("""
                INSERT INTO armazenamento_registros_tce (doc, Nprocesso, dataAtuacao, partes, materia, url, ementa)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (item['doc'], item['Nprocesso'], item['dataAtuacao'], partes_str, item['materia'], item['url'], item['ementa']))
            self.connection.commit()
            print("Record inserted successfully")
        except Error as e:
            print("Error while inserting record:", e)
        return item

    def close_spider(self, spider):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
