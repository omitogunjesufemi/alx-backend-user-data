#!/usr/bin/env python3
"""
A module for creating a function that returns a log message
obfuscated
"""
from typing import List
import re


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
