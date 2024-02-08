#!/usr/bin/env python3
"""A module for filtering logs.
"""
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str
                 ) -> str:
    """Blur and obscure sensitive data in log messages."""
    pattern = r'(?:(?<=^)|(?<={0}))({1}=)[^;]*'.format(
        separator, '|'.join(fields))
    return re.sub(pattern, r'\1' + redaction, message)
