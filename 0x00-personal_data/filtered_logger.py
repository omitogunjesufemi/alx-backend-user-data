#!/usr/bin/env python3
"""
A module for creating a function that returns a log message
obfuscated
"""
from typing import List
import re
import os
import logging
import mysql.connector


PII_FIELDS = ("email", "phone", "ssn", "password", "ip")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        """Initialization"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    A function that returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(rf"{field}=(?P<password>[^{separator}]+)",
                         f"{field}={redaction}", message)
    return message


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database """
    connector = None
    user = os.environ.get("PERSONAL_DATA_DB_USERNAME")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD")
    host = os.environ.get("PERSONAL_DATA_DB_HOST")
    database = os.environ.get("PERSONAL_DATA_DB_NAME")

    connector = mysql.connector.connect(host=host,
                                        database=database,
                                        user=user,
                                        password=password)

    return connector
