from csv import Dialect, QUOTE_MINIMAL
from typing import List, Dict, Any

from ive_trains.reader.CsvReader import readFile


class TrainListDialect(Dialect):
    delimiter = '|'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL


def processTrainList(file: str) -> Dict[str, List[str]]:
    trainList: List[List[str]] = readFile(file, TrainListDialect())
    typeDict: Dict[str, List[str]] = {}

    first = True
    for listEntry in trainList:
        if first:
            first = False
            continue

        if len(listEntry) < 2:
            continue

        # trainId = tryIntConversion(listEntry[1])
        # if trainId == -1:
        #     continue

        if not listEntry[1]:
            continue

        trainId = listEntry[1]

        detailStrings: List[str] = listEntry[0].split('\\')
        trainType: str = detailStrings[1]

        if trainType not in typeDict.keys():
            typeDict[trainType] = []

        typeDict[trainType].append(trainId)

    return typeDict


def tryIntConversion(value: Any) -> int:
    try:
        intValue = int(value)
    except ValueError:
        return -1
    return intValue
