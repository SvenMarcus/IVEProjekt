import csv
from typing import List


def readFile(filePath: str, dialect=None) -> List[List[str]]:
    with open(filePath, newline='', encoding='ISO-8859-1') as csvfile:
        lst = []

        if dialect is None:
            dialect = csv.excel

        reader = csv.reader(csvfile, dialect)

        for row in reader:
            lst.append(row)

        return lst
