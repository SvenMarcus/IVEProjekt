import re
import os
from typing import List, Dict

from os import path

from ive_trains.reader.CsvReader import readFile
from ive_trains.reader.TrainDataProcessor import processDrivingDynamics
from ive_trains.reader.TrainListProcessor import processTrainList, TrainListDialect
from ive_trains.writer.CsvWriter import writeFile

ENERGY_STRING = "Summe gesamte positive mech. Arbeit aller Züge des Zugtyps [KWh]"
TIME_STRING = "Summe Fahrzeit aller Züge des Zugtyps [h]"

indexLookup: Dict[str, int] = {}


def processTrainResults(folder) -> None:
    trainTypeDict: Dict[str, List[int]] = processTrainList(path.join(folder, "Zugliste.csv"))
    allTrainData: Dict[str, Dict[str, Dict]] = processDrivingDynamics(folder)
    trainTypeTrackDict: Dict[str, List[List[str]]] = {}

    for trainType in trainTypeDict:
        trainTypeFileName = trainType + ".csv"
        if trainTypeFileName in os.listdir(folder):
            parseTrackFile(trainType, path.join(folder, trainType + ".csv"), trainTypeTrackDict)

    for trainId in allTrainData:
        actualTrainType = None
        for trainType in trainTypeTrackDict:
            if int(trainId) in trainTypeDict[trainType]:
                actualTrainType = trainType

        if actualTrainType is not None:
            for track in allTrainData[trainId]:
                splitTrack = track.split("-")
                start = splitTrack[0]
                end = splitTrack[1]
                trackEntry = getTrackWith(trainTypeTrackDict[actualTrainType], start, end)

                if len(trackEntry) != 0:
                    header = trainTypeTrackDict[actualTrainType][0]
                    while len(trackEntry) != len(header):
                        trackEntry.append("0")

                    trackEntry[len(trackEntry) - 2] = str(
                        float(trackEntry[len(trackEntry) - 2]) + allTrainData[trainId][track]["energy"])
                    trackEntry[len(trackEntry) - 1] = str(
                        float(trackEntry[len(trackEntry) - 1]) + allTrainData[trainId][track]["time"])

    for trainType in trainTypeTrackDict:
        trainTypeFileName = trainType + ".csv"
        print("Writing file " + trainTypeFileName)
        writeFile(path.join(folder, trainTypeFileName), trainTypeTrackDict[trainType], '|')


def parseTrackFile(trainType, trainTypeFileName, trainTypeTrackDict) -> None:
    trackFile = readFile(trainTypeFileName, TrainListDialect())
    header = trackFile[0]
    secondLast = header[len(header) - 2]
    last = header[len(header) - 1]
    if secondLast != ENERGY_STRING:
        header.append(ENERGY_STRING)
    if last != TIME_STRING:
        header.append(TIME_STRING)
    trainTypeTrackDict[trainType] = trackFile


def getTrackWith(trackData, start: str, end: str) -> List[str]:
    trackString = start + "_" + end
    if trackString in indexLookup.keys():
        return trackData[indexLookup[trackString]]

    for i in range(0, len(trackData)):
        track = trackData[i]
        if len(track) < 3:
            continue

        if track[0] == start and track[2] == end:
            indexLookup[trackString] = i
            return track
    return []
