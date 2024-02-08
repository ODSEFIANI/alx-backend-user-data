#!/usr/bin/env python3
"""A module for filtering logs.
"""
import logging
import os
import re
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] user_data INFO %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Blur and obscure sensitive data in log messages."""
    pattern = r'(?:(?<=^)|(?<={0}))({1}=)[^;]*'.format(
        separator, '|'.join(fields))
    return re.sub(pattern, r'\1' + redaction, message)


def get_logger() -> logging.Logger:
    """Return a logger named 'user_data'."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a connector to the database."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database_name = os.getenv("PERSONAL_DATA_DB_NAME", "")

    db = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database_name
    )

    return db


def main():
    """Retrieve al"""
    logger = get_logger()

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger.info("Filtered fields:\n%s", '\n'.join(PII_FIELDS))

    for row in cursor:
        log_message = "; ".join(f"{field}={row[i]}" for i,
                                field in enumerate(PII_FIELDS))
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
