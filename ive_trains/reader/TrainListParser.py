from csv import Dialect, QUOTE_MINIMAL

from ive_trains.reader.CsvReader import readFile


class TrainListDialect(Dialect):
    """Describe the usual properties of Excel-generated CSV files."""
    delimiter = '|'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL


def processTrainList(file: str):
    trainList = readFile(file)