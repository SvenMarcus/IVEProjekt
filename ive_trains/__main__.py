from typing import Dict

import re

from ive_trains.reader.CsvReader import readFile
from ive_trains.reader.TrainDataProcessor import processDrivingDynamics
from ive_trains.reader.TrainListProcessor import TrainListDialect, processTrainList


def filterFolder(folder: Dict):
    tracksToPop = []
    for train in folder:
        for track in folder[train]:
            if not folder[train][track]["noEntries"] > 1:
                tracksToPop.append([train, track])

    for entry in tracksToPop:
        folder[entry[0]].pop(entry[1])


if __name__ == "__main__":
    # folder = processFolder("/Users/svenmarcus/Documents/Institut/IVE/neu")
    # print(folder)
    # file = readFile("./Zugliste.csv", TrainListDialect())

    # listEntry = file[0]
    # detailString: str = listEntry[0]
    # trainId: int = int(listEntry[1])
    #
    # print(detailString.split('\\'))
    #
    # listEntry = file[36]
    # detailString: str = listEntry[0]
    # print(detailString.split('\\'))

    print(processTrainList("./Zugliste.csv"))



