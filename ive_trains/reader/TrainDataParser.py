from typing import List, Dict

import re

TRAIN = 0
TIME = 4
ENERGY = 14
STATION = 16


def parseDailyTrainData(data: List[List[str]]) -> Dict[str, Dict[str, Dict]]:
    if not checkHeader(data[0]):
        return {}
    data.pop(0)
    return parseRawFileDataWithoutHeader(data)


def checkHeader(header: List[str]) -> bool:
    neededHeader: List[str] = ['Zug', 'Zeit', 'Position [km]', 'Fahrmodus', 'Fahrzeit [s]', 'Weg [m]', 'vStart [km/h]',
                               'vZiel [km/h]', 'Neigung', 'Beschleunigung [m/s²]', 'Kraft [kN]', 'Masse [kg]',
                               'Arbeit [kWh]', 'Leistung [kW]', 'gesamte positive mech. Arbeit [kWh]',
                               'gesamte negative mech. Arbeit [kWh]', 'Station', 'Halt/außerplanm. Halt/Durchfahrt',
                               'Zielsignal', 'Halt/Durchfahrt', 'Weiche/Kreuzung',
                               'Weiche/Kreuzung mit Zugspitze/Zugende befahren', 'Oberleitungsschaltgruppe',
                               'Speiseleitung', 'Unterwerk', 'vMax [km/h]', '']

    if not len(header) == len(neededHeader):
        return False

    for i in range(0, len(neededHeader)):
        if neededHeader[i] != header[i]:
            return False

    return True


def parseRawFileDataWithoutHeader(data) -> Dict[str, Dict[str, Dict]]:
    lastStation: str = ""
    timeSum: float = 0
    startEnergy: float = 0
    currentTrain: str = ""
    dailyTrainData: Dict[str, Dict[str, Dict]] = {}
    for row in data:
        rowDict: Dict = parseRawDataRow(row)

        if not rowDict["station"] and not lastStation:
            continue

        if not currentTrain or currentTrain != rowDict["trainId"]:
            currentTrain = rowDict["trainId"]
            startEnergy = 0

        if rowDict["station"]:
            if rowDict["station"] != lastStation:
                writeTrainData(dailyTrainData, (rowDict["energy"] - startEnergy), lastStation, rowDict["station"], timeSum, rowDict["trainId"])
                startEnergy = rowDict["energy"]
                lastStation = rowDict["station"]
                timeSum: float = 0

        timeSum += rowDict["time"]

    return dailyTrainData


def parseRawDataRow(row) -> Dict[str, object]:
    trainId: str = row[TRAIN]
    time: float = float(row[TIME])
    energy: float = float(row[ENERGY])
    station: str = row[STATION]
    return {"energy": energy, "station": station, "time": time, "trainId": trainId}


def writeTrainData(dailyTrainData: Dict[str, Dict[str, Dict]], energy: float, lastStation: str, station: str, timeSum: float, trainId: str) -> None:
    if lastStation:
        track = re.sub(' +', ' ', lastStation.strip() + "-" + station.strip())
        if energy < 0:
            print(trainId + " " + track + " " + str(energy))
        trainData: Dict = {"time": timeSum, "energy": energy}
        if trainId not in dailyTrainData.keys():
            dailyTrainData[trainId] = {}
        if track in dailyTrainData[trainId].keys():
            print(track + " is already in " + trainId)
        dailyTrainData[trainId][track] = trainData
