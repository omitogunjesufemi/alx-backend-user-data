#!/usr/bin/env python3
"""
A module for creating a function that returns a log message
obfuscated
"""
from typing import List
import re
import logging


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
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    A function that returns the log message obfuscated

    Arguments:
    - fields: a list of strings representing all fields to obfuscate
    - redaction: a string representing by what the field will be
      obfuscated
    - message: a string representing the log line
    - separator: a string representing by which character is separating
      all fields in the log line (message)

    The function should use a regex to replace occurrences of certain
    field values.

    filter_datum should be less than 5 lines long and use re.sub to
    perform the substitution with a single regex.
    """
    for field in fields:
        message = re.sub(rf"{field}=(?P<password>[^{separator}]+)",
                         f"{field}={redaction}", message)
    return message
