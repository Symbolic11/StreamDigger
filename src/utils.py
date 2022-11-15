import re

year_regex = re.compile(r'^[12][0-9]{3}$')

def clean(raw) -> str:
    """
    clean(raw text) -> cleaned text

    Removes whitespace and extra lines

    :param raw str: Raw text
    :returns str: Cleaned text
    """

    return (
        raw
        .strip()
        .rstrip()
    )

def is_valid_year(raw):
    return bool(year_regex.match(raw))