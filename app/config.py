import os


def get_mysql_config():
    return {
        "host": os.getenv("PETSHOP_DB_HOST", "localhost"),
        "port": int(os.getenv("PETSHOP_DB_PORT", "3306")),
        "user": os.getenv("PETSHOP_DB_USER", "root"),
        "password": os.getenv("PETSHOP_DB_PASSWORD", ""),
        "database": os.getenv("PETSHOP_DB_NAME", "petshop"),
        "autocommit": True,
    }
