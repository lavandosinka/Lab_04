import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Tuple
import os

class Database:
    def __init__(self):
        self.connection = None
        self.create_database()
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='5930',
                database='shipping_company'
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def create_database(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='5930'  # Using the password here as well
            )
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS shipping_company")
            connection.commit()
            print("Database created successfully")
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error creating database: {e}")

    def create_tables(self):
        if not self.connection:
            return

        create_tariffs_table = """
        CREATE TABLE IF NOT EXISTS tariffs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            base_price DECIMAL(10, 2) NOT NULL,
            discount DECIMAL(5, 2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_tariffs_table)
            self.connection.commit()
            print("Tariffs table created successfully")
        except Error as e:
            print(f"Error creating table: {e}")

    def add_tariff(self, name: str, base_price: float) -> bool:
        if not self.connection:
            return False

        query = "INSERT INTO tariffs (name, base_price) VALUES (%s, %s)"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (name, base_price))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error adding tariff: {e}")
            return False

    def set_tariff_discount(self, name: str, discount: float) -> bool:
        if not self.connection:
            return False

        query = "UPDATE tariffs SET discount = %s WHERE name = %s"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (discount, name))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error setting discount: {e}")
            return False

    def get_all_tariffs(self) -> List[Tuple]:
        if not self.connection:
            return []

        query = "SELECT name, base_price, discount FROM tariffs ORDER BY base_price ASC"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error getting tariffs: {e}")
            return []

    def get_min_price_tariff(self) -> Optional[Tuple]:
        if not self.connection:
            return None

        query = """
        SELECT name, base_price, discount, 
               base_price * (1 - discount/100) as final_price 
        FROM tariffs 
        ORDER BY final_price ASC 
        LIMIT 1
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return result if result else None
        except Error as e:
            print(f"Error finding min price tariff: {e}")
            return None

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
