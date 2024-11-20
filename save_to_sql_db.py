"""stores the extracted products data to an postgreSQL database.

through the Write_to_DB class it will connect to a the products,
variants, and images tables if they exist or create them and
stores the scraped products data in them.

Typical usage example:
    
    write_to_db = Write_to_DB("admin", "12345", "5555", "shopify")
    
    write_to_db.insert_into_table("products", products_list)
    write_to_db.insert_into_table("variants", variants_list)
    write_to_db.insert_into_table("images", images_list)
    
    write_to_db.terminate_connection()
        
"""

from sqlalchemy import create_engine, text
import json
from pprint import pprint

class Write_to_DB:
    """
    A class to handle writing data to a PostgreSQL database.

    Attributes:
        insert_statements (dict): Dictionary of SQL insert statements.
        tables_creation (list): List of SQL table creation statements.
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy engine instance.
        connection (sqlalchemy.engine.base.Connection): Active database connection.
    """
    
    insert_statements = {
        "products": """
            INSERT INTO products (
                id,
                product_publish_date,
                product_vendor,
                product_type,
                product_tags,
                product_options,
                product_page,
                product_description,
                product_title,
                images_ids
            ) VALUES (
                :id,
                :product_publish_date,
                :product_vendor,
                :product_type,
                :product_tags,
                :product_options,
                :product_page,
                :product_description,
                :product_title,
                :images_ids
            );""",
        "variants": """
            INSERT INTO variants (
                product_id,
                id,
                variant_title,
                variant_price,
                variant_compare_at_price,
                variant_sku,
                variant_created_at,
                variant_updated_at,
                variant_available
            ) VALUES (
                :product_id,
                :id,
                :variant_title,
                :variant_price,
                :variant_compare_at_price,
                :variant_sku,
                :variant_created_at,
                :variant_updated_at,
                :variant_available
            );
        """,
        "images": """
            INSERT INTO images (
                id,
                created_at,
                updated_at,
                variant_ids,
                src,
                width,
                height
            ) VALUES (
                :id,
                :created_at,
                :updated_at,
                :variant_ids,
                :src,
                :width,
                :height
            );"""
    }

    tables_creation = [
        """
        CREATE TABLE IF NOT EXISTS products (
            id BIGINT PRIMARY KEY,
            product_publish_date TIMESTAMP,
            product_vendor VARCHAR,
            product_type VARCHAR,
            product_tags JSON,
            product_options JSON,
            product_page VARCHAR,
            product_description VARCHAR,
            product_title VARCHAR,
            images_ids JSON
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS variants (
            product_id BIGINT REFERENCES products(id),
            id BIGINT PRIMARY KEY,
            variant_title VARCHAR,
            variant_price REAL,
            variant_compare_at_price REAL,
            variant_sku VARCHAR,
            variant_created_at TIMESTAMP,
            variant_updated_at TIMESTAMP,
            variant_available BOOLEAN
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS images (
            id BIGINT PRIMARY KEY,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            variant_ids JSON,
            src VARCHAR,
            width INT,
            height INT
        );
        """
    ]

    def __init__(self, user: str, password: str, port: str, db: str) -> None:
        """
        Initializes the Write_to_DB class.

        Args:
            user (str): Database username.
            password (str): Database password.
            port (str): Database port.
            db (str): Database name.
        """
        db_url = self.__get_db_url(user, password, port, db)
        self.engine = create_engine(db_url)
        self.connection = self.engine.connect()
        self.__create_tables_if_not_exists()

    def __get_db_url(self, user: str, password: str, port: str, db: str) -> str:
        """
        Constructs the database URL.

        Args:
            user (str): Database username.
            password (str): Database password.
            port (str): Database port.
            db (str): Database name.

        Returns:
            str: The database URL.
        """
        db_url = f"postgresql://{user}:{password}@localhost:{port}/{db}"
        return db_url

    def __create_tables_if_not_exists(self) -> None:
        """
        Creates tables in the database if they do not already exist.
        """
        with self.connection.begin():
            for query in self.tables_creation:
                self.connection.execute(text(query))

    def __clean_item(self, item: dict) -> dict:
        """
        Cleans an item by converting dictionaries and lists to JSON strings.

        Args:
            item (dict): The item to be cleaned.

        Returns:
            dict: The cleaned item.
        """
        for key, value in item.items():
            if type(value) in [dict, list]:
                item[key] = json.dumps(value)
        return item

    def insert_into_table(self, table_name: str, items_list: list) -> None:
        """
        Inserts a list of items into a specified table.

        Args:
            table_name (str): The name of the table.
            items_list (list): List of items to be inserted.

        Raises:
            Exception: If there is an error during insertion.
        """
        with self.connection.begin():
            for item in items_list:
                try:
                    cleaned_item = self.__clean_item(item)
                    if table_name == "images":
                        insert_statement = self.insert_statements[table_name].replace(";", "ON CONFLICT (id) DO NOTHING;")
                    else:
                        insert_statement = self.insert_statements[table_name]
                    self.connection.execute(text(insert_statement), cleaned_item)
                except Exception as e:
                    print(e)
                    with open(f"failed items/{table_name}.jsonl", "a") as f:
                        f.write(json.dumps(item) + "\n")
                    print(f'saved failed item in "failed items/{table_name}.jsonl"')

    def terminate_connection(self) -> None:
        """
        Terminates the database connection.
        """
        self.connection.commit()
        self.connection.close()
        self.engine.dispose()

