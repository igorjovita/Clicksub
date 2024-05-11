import mysql.connector
import streamlit as st


class DataBaseMysql:
    def __init__(self, ):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        mydb = mysql.connector.connect(
            host='vkh7buea61avxg07.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
            user='zmfyc4dcy6w1ole8',
            passwd='yvdnjfingsqqk6q0',
            db='zaitpacb8oi8ppgt',
            autocommit=True)
        self.__connection = mydb
        self.__cursor = self.__connection.cursor(buffered=True)
        return self.__cursor

    def disconnect(self):
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def execute_query(self, query, params=None):
        try:

            cursor = self.connect()
            cursor.execute(query, params)

            if query.strip().startswith('SELECT') or query.strip().startswith('WITH'):
                result = cursor.fetchall()
                st.write(result)
                return result

            elif query.strip().startswith('INSERT INTO'):
                id_lastrow = cursor.lastrowid

                return id_lastrow

            else:
                return None
        except mysql.connector.Error as e:
            st.error(f"Error executing query: {e}")
            raise
        finally:
            self.disconnect()
