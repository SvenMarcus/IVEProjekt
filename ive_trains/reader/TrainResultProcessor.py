from typing import List, Dict

from os import path, os

from ive_trains.reader.CsvReader import readFile
from ive_trains.reader.TrainDataProcessor import processDrivingDynamics
from ive_trains.reader.TrainListProcessor import processTrainList, TrainListDialect


def processTrainResults(folder) -> None:
    trainTypeDict: Dict[str, List[int]] = processTrainList(path.join(folder, "Zugliste.csv"))
    allTrainData: Dict[str, Dict[str, Dict]] = processDrivingDynamics(folder)
    trainTypeTrackDict: Dict[str, List[List[str]]] = {}

    for trainType in trainTypeDict:
        trainTypeFileName = trainType + ".csv"
        if trainTypeFileName in os.listdir(folder):
            trackFile = readFile(trainTypeFileName, TrainListDialect())
            trainTypeTrackDict[trainType] = trackFile

    for trainId in allTrainData:
        actualTrainType = None
        for trainType in trainTypeTrackDict:
            if trainId in trainTypeTrackDict[trainType]:
                actualTrainType = trainType

        if actualTrainType is not None:
            for track in allTrainData[trainId]:
                splitTrack = track.split("-")
                # trackEntry = getTrackWith()

indexLookup: Dict[List[str], int] = {}


def getTrackWith(trackData, start: str, end: str) -> List[str]:
    track = [start, end]
    if track in indexLookup.keys():
        return trackData[indexLookup[track]]

    for i in range(0, len(trackData)):
        track = trackData[i]
        if len(track) < 3:
            continue

        if track[0] == start and track[2] == end:
            indexLookup[[start, end]] = i
            return track
    return []
