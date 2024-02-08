#!/usr/bin/env python3
"""A module for filtering logs.
"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Blur and obscure sensitive data in log messages."""
    return re.sub(r'(?:(?<=^)|(?<={0}))({1}=)[^;]*'.format(
        separator, '|'.join(fields)), r'\1' + redaction, message)
