import mysql.connector
from mysql.connector import Error

from app.config import get_mysql_config


class MySQLRepository:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.config = get_mysql_config()
        self.connection = self._connect()
        self._create_table_if_not_exists()

    def _connect(self):
        try:
            return mysql.connector.connect(**self.config)
        except Error as exc:
            raise RuntimeError(f"Não foi possível conectar ao MySQL: {exc}") from exc

    def _create_table_if_not_exists(self):
        if not self.connection:
            return

        cursor = self.connection.cursor()
        if self.table_name == "clientes":
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    telefone VARCHAR(20) NOT NULL,
                    email VARCHAR(100) NOT NULL
                )
                """
            )
        elif self.table_name == "animais":
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS animais (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    especie VARCHAR(50) NOT NULL,
                    raca VARCHAR(50) NOT NULL,
                    idade INT NOT NULL,
                    dono_id INT NOT NULL
                )
                """
            )
        self.connection.commit()
        cursor.close()

    def list_all(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {self.table_name}")
        result = cursor.fetchall()
        cursor.close()
        return result

    def add(self, item: dict):
        cursor = self.connection.cursor()
        if self.table_name == "clientes":
            cursor.execute(
                "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)",
                (item["nome"], item["telefone"], item["email"]),
            )
        else:
            cursor.execute(
                "INSERT INTO animais (nome, especie, raca, idade, dono_id) VALUES (%s, %s, %s, %s, %s)",
                (item["nome"], item["especie"], item["raca"], item["idade"], item["dono_id"]),
            )
        self.connection.commit()
        item["id"] = cursor.lastrowid
        cursor.close()
        return item

    def get_by_id(self, item_id: int):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s", (item_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def update(self, item_id: int, item: dict):
        cursor = self.connection.cursor()
        if self.table_name == "clientes":
            cursor.execute(
                "UPDATE clientes SET nome = %s, telefone = %s, email = %s WHERE id = %s",
                (item["nome"], item["telefone"], item["email"], item_id),
            )
        else:
            cursor.execute(
                "UPDATE animais SET nome = %s, especie = %s, raca = %s, idade = %s, dono_id = %s WHERE id = %s",
                (item["nome"], item["especie"], item["raca"], item["idade"], item["dono_id"], item_id),
            )
        self.connection.commit()
        cursor.close()
        return self.get_by_id(item_id)

    def delete(self, item_id: int):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (item_id,))
        self.connection.commit()
        cursor.close()
        return True
