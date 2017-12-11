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


# Example entry:
# ['\\PNV-D\\N34 Glauburg-Stockheim - Frankfurt (Main) Hbf\\rÃ¼ck\\RB Diesel 1703435', ... ]

def processTrainList(file: str) -> Dict[str, List[int]]:
    trainList: List[List[str]] = readFile(file, TrainListDialect())
    typeDict: Dict[str, List[int]] = {}

    for listEntry in trainList:
        if len(listEntry) < 2:
            continue

        trainId = tryIntConversion(listEntry[1])
        if trainId == -1:
            continue

        detailStrings: List[str] = listEntry[0].split('\\')
        trainType: str = detailStrings[1]
        print(trainType)

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
