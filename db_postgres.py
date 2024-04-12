import psycopg2
from psycopg2 import Error
import datetime
import csv

class Database:
    def __init__(self, db_params: dict = None):
        if db_params is None:
            db_params = {
                "host": "localhost",
                "database": "my_database",
                "user": "postgres",
                "password": "7292",
                "port": "5432"
            }

        try:
            self.connection = psycopg2.connect(**db_params)
            self.cursor = self.connection.cursor()
            self.create_tables()
        except Error as e:
            print(f"Error while connecting to PostgreSQL: {e}")

    def create_tables(self):
        try:
            create_users_table_query = """CREATE TABLE IF NOT EXISTS users (
                                            user_id BIGINT PRIMARY KEY,
                                            username TEXT,
                                            real_name TEXT,
                                            open_order BIGINT,
                                            product INTEGER,
                                            address TEXT,
                                            phone_number TEXT,
                                            open_date DATE
                                            
                                        )"""
            create_products_table_query = """CREATE TABLE IF NOT EXISTS products (
                                                id SERIAL PRIMARY KEY,
                                                name TEXT,
                                                price TEXT,
                                                about TEXT, 
                                                photo_path TEXT
                                            )"""

            create_completed_tasks_query = """CREATE TABLE IF NOT EXISTS orders (
                                                            user_id BIGINT,
                                                            username TEXT,
                                                            real_name TEXT,
                                                            open_order BIGINT,
                                                            product INTEGER,
                                                            address TEXT,
                                                            phone_number TEXT,
                                                            open_date DATE,
                                                            closed_date DATE,
                                                            post_code TEXT,
                                                            id SERIAL PRIMARY KEY
                                                        )"""
            self.cursor.execute(create_users_table_query)
            self.cursor.execute(create_products_table_query)
            self.cursor.execute(create_completed_tasks_query)
            self.connection.commit()
        except Error as e:
            print(f"Error while creating tables: {e}")

    def add_user(self, user_id: int, username: str):
        try:
            insert_query = "INSERT INTO users (user_id, username) VALUES (%s, %s)"
            self.cursor.execute(insert_query, (user_id, username))
            self.connection.commit()
            print(f"User added with ID = {user_id} | Username = {username}")
        except Error as e:
            print(f"Error while adding user: {e}")

    def add_product(self, name: str, about: str, price: str,  photo_path: str):
        try:
            insert_query = "INSERT INTO products (name, about, price, photo_path) VALUES (%s, %s, %s, %s) RETURNING id"
            self.cursor.execute(insert_query, (name, about, price + '₽', photo_path))
            data = self.cursor.fetchone()
            self.connection.commit()
            print("Product added successfully.")
            return data

        except Error as e:
            print(f"Error while adding product: {e}")

    # Остальные методы здесь...

    def get_info(self, user_id):
        try:
            select_query = "SELECT * FROM users WHERE user_id = %s"
            self.cursor.execute(select_query, (user_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error while fetching user info: {e}")

    def get_info_product(self, name):
        try:
            select_query = "SELECT * FROM products WHERE name = %s"
            self.cursor.execute(select_query, (name,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error while fetching product info: {e}")

    def get_info_product_id(self, product_id):
        try:
            select_query = "SELECT * FROM products WHERE id = %s"
            self.cursor.execute(select_query, (product_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error while fetching product info: {e}")


    def get_users(self):
        try:
            select_query = "SELECT * FROM users WHERE sell_date IS NOT NULL"
            self.cursor.execute(select_query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error while fetching users: {e}")

    def cancel_order(self, user_id):
        try:
            update_query = "UPDATE users SET open_date = NULL, phone_number = NULL, address = NULL, product = NULL, open_order = NULL WHERE user_id = %s"
            self.cursor.execute(update_query, (user_id,))
            self.connection.commit()
            print("Order cancelled successfully.")
        except Error as e:
            print(f"Error while cancelling order: {e}")

    def get_products(self):
        try:
            select_query = "SELECT * FROM products"
            self.cursor.execute(select_query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error while fetching products: {e}")

    def set_data(self, buy_date, sell_date, about, user_id):
        try:
            update_query = "UPDATE users SET buy_date = %s, sell_date = %s, about = %s WHERE user_id = %s"
            self.cursor.execute(update_query, (buy_date, sell_date, about, user_id))
            self.connection.commit()
        except Error as e:
            print(f"Error while updating user data: {e}")

    def set_data_username(self, buy_date, sell_date, about, username):
        try:
            update_query = "UPDATE users SET buy_date = %s, sell_date = %s, about = %s WHERE username = %s"
            self.cursor.execute(update_query, (buy_date, sell_date, about, username))
            self.connection.commit()
        except Error as e:
            print(f"Error while updating user data by username: {e}")

    def get_date(self, user_id):
        try:
            select_query = "SELECT sell_date FROM users WHERE user_id = %s"
            self.cursor.execute(select_query, (user_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error while fetching sell date: {e}")

    def delete_item(self, name):
        try:
            delete_query = "DELETE FROM products WHERE name = %s"
            self.cursor.execute(delete_query, (name,))
            self.connection.commit()
        except Error as e:
            print(f"Error while deleting product: {e}")

    def clear_date_username(self, about, username):
        try:
            update_query = "UPDATE users SET buy_date = NULL, sell_date = NULL, about = %s WHERE username = %s"
            self.cursor.execute(update_query, (about, username))
            self.connection.commit()
        except Error as e:
            print(f"Error while clearing user data by username: {e}")

    def order(self, real_name, user_id, product,address,phone_number):
        try:
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            update_query = "UPDATE users SET real_name = %s, open_order = %s, product = %s, address = %s, phone_number = %s, open_date = %s WHERE user_id = %s"
            self.cursor.execute(update_query, (real_name, user_id, product,address,phone_number,formatted_datetime,user_id))
            self.connection.commit()
        except Error as e:
            print(f"Error while placing order: {e}")

    def check_order(self, user_id):
        try:
            select_query = "SELECT * FROM users WHERE user_id = %s"
            self.cursor.execute(select_query, (user_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error while checking order: {e}")


    def move_data_to_orders(self, user_id_to_move):
        try:
            # Выборка данных из таблицы users по заданному user_id
            select_query = "SELECT user_id, username, open_order, product, address, phone_number, open_date FROM users WHERE user_id = %s"
            self.cursor.execute(select_query, (user_id_to_move,))
            data_to_move = self.cursor.fetchone()

            # Проверка, найдена ли строка с заданным user_id
            if data_to_move:
                date = datetime.date.today()
                tmp = []
                for data in data_to_move:
                    tmp.append(data)
                tmp.append(date)
                # Вставка данных в таблицу orders
                insert_query = "INSERT INTO orders (user_id, username, open_order, product, address, phone_number, open_date, closed_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                self.cursor.execute(insert_query, tmp)

                # Удаление перенесенной строки из таблицы users
                delete_query = "UPDATE users SET open_order = NULL, product = NULL, address = NULL, phone_number = NULL, open_date = NULL WHERE user_id = %s"
                self.cursor.execute(delete_query, (user_id_to_move,))

                # Коммит транзакции
                self.connection.commit()
                print(f"Data for user_id {user_id_to_move} moved to 'orders' table successfully.")
            else:
                print(f"No data found for user_id {user_id_to_move} in 'users' table.")
        except Error as e:
            print(f"Error while moving data to 'orders' table: {e}")





    def export_orders(self):
        try:
            # Выполнение SQL-запроса для выбора содержимого таблицы orders
            select_query = "SELECT * FROM orders"
            self.cursor.execute(select_query)
            orders_data = self.cursor.fetchall()

            # Запись данных в CSV файл
            with open('orders_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                # Записываем заголовки
                csv_writer.writerow([i[0] for i in self.cursor.description])
                # Записываем данные
                csv_writer.writerows(orders_data)

            print("Data exported to orders_export.csv successfully.")

        except Error as e:
            print(f"Error while connecting to PostgreSQL: {e}")

    def get_post_code(self, user_id):
        try:
            select_query = "SELECT post_code FROM orders WHERE user_id = %s"
            self.cursor.execute(select_query, (user_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error while fetching post code: {e}")

    def set_post_code(self, user_id, id, post_code):
        try:
            update_query = "UPDATE orders SET post_code = %s WHERE user_id = %s AND id = %s"
            self.cursor.execute(update_query, (post_code, user_id, id))
            self.connection.commit()
            print("Post code updated successfully.")
        except Error as e:
            print(f"Error while setting post code: {e}")

    def get_product_by_user_id(self, user_id):
        try:
            select_query = "SELECT product FROM orders WHERE user_id = %s"
            self.cursor.execute(select_query, (user_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error while fetching product by user_id: {e}")

    def get_last_row_by_user_id(self, user_id):
        try:
            select_query = """
                  SELECT id
                  FROM orders
                  WHERE user_id = %s
                  AND id = (SELECT MAX(id) FROM orders WHERE user_id = %s)
              """
            self.cursor.execute(select_query, (user_id, user_id))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error while fetching last row by user_id: {e}")

# Пример использования:
db_params = {
    "host": "localhost",
    "database": "TgShop",
    "user": "postgres",
    "password": "7292",
    "port": "5432"
}
db = Database(db_params)
# db.add_user(1, "user1")
print(db.get_last_row_by_user_id(6158117041))
# db.add_product("product1", "About product 1", "10")


