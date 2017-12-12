import os
from csv import Dialect, QUOTE_MINIMAL
from typing import List, Dict

from ive_trains.reader.CsvReader import readFile
from ive_trains.reader.TrainDataParser import parseDailyTrainData


class TrainDataDialect(Dialect):
    """Describe the usual properties of Excel-generated CSV files."""
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL


def processDrivingDynamics(path: str) -> Dict[str, Dict[str, Dict]]:
    firstData: Dict[str, Dict[str, Dict]] = None
    filesInFolder = os.listdir(path)
    print(filesInFolder)
    noOfDatFiles: int = 0
    for file in filesInFolder:
        if file.endswith(".dat"):
            noOfDatFiles += 1
            print("Parsing file " + file)

            file = readFile(os.path.join(path, file), TrainDataDialect())
            data: Dict[str, Dict[str, Dict]] = parseDailyTrainData(file)

            if firstData is None:
                firstData = data

            if data is not firstData:
                appendMissingData(firstData, data)

            for trainId in data:
                trackDict: Dict[str, Dict] = data[trainId]
                for track in trackDict:
                    if data is not firstData:
                        firstData[trainId][track]["time"] += data[trainId][track]["time"]
                        firstData[trainId][track]["energy"] += data[trainId][track]["energy"]

                    if "noEntries" not in firstData[trainId][track].keys():
                        firstData[trainId][track]["noEntries"] = 0
                    firstData[trainId][track]["noEntries"] += 1

    if firstData is not None:
        for trainId in firstData:
            trackDict: Dict[str, Dict] = firstData[trainId]
            for track in trackDict:
                firstData[trainId][track]["time"] /= firstData[trainId][track]["noEntries"]
                firstData[trainId][track]["energy"] /= firstData[trainId][track]["noEntries"]

    return firstData


def appendMissingData(firstData: Dict[str, Dict[str, Dict]], data) -> None:
    for trainId in data:

        if trainId not in firstData.keys():
            firstData[trainId] = {}

        trackDict: Dict[Dict[str, float]] = data[trainId]

        for track in trackDict:
            if track not in firstData[trainId].keys():
                firstData[trainId][track] = {"energy": 0, "time": 0}


def checkEquality(firstData, data) -> bool:
    if len(firstData) != len(data):
        throwNotSameNumberOfTrainIdsError()

    for key in firstData:
        firstDataList: List[Dict[str, object]] = firstData[key]
        dataEntry: List[Dict[str, object]] = None

        try:
            dataEntry = data[key]
        except KeyError:
            throwNoTrainIdError(key)

        if len(firstDataList) != len(dataEntry):
            throwNotSameNumberOfTracksError(key)

        for i in range(0, len(firstDataList)):
            firstDataTrack: str = firstDataList[i]["track"]
            dataTrack: str = ""

            try:
                dataTrack = dataEntry[i]["track"]
            except KeyError:
                throwNoTrackError(firstDataTrack, key)

            if firstDataTrack != dataTrack:
                print(firstDataTrack)
                print(dataTrack)
                throwTrackNotEqualError(firstDataTrack, key)

    return True


def throwNotSameNumberOfTrainIdsError():
    message = "Train data does not contain same number of train id entries"
    raise TrainDataNotEqualException(message)


def throwNoTrainIdError(key):
    message = "Train data does not contain entry for train with id: " + str(key)
    raise TrainDataNotEqualException(message)


def throwNotSameNumberOfTracksError(key):
    message = "Train data does not contain same number of track entries for train with id: " + str(key)
    raise TrainDataNotEqualException(message)


def throwNoTrackError(firstDataTrack, key):
    message = "Train data for train with id " + \
              str(key) + " does not contain entry for track: " + firstDataTrack
    raise TrainDataNotEqualException(message)


def throwTrackNotEqualError(firstDataTrack, key):
    message = "Train data for train with id " + \
              str(key) + " does not contain entry for track: " + firstDataTrack
    raise TrainDataNotEqualException(message)


class TrainDataNotEqualException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


