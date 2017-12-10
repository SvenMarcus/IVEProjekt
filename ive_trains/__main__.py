from typing import Dict

import re

from ive_trains.reader.CsvReader import readFile
from ive_trains.reader.TrainDataProcessor import processFolder
from ive_trains.reader.TrainListParser import TrainListDialect


def filterFolder(folder: Dict):
    tracksToPop = []
    for train in folder:
        for track in folder[train]:
            if not folder[train][track]["noEntries"] > 1:
                tracksToPop.append([train, track])

    for entry in tracksToPop:
        folder[entry[0]].pop(entry[1])


if __name__ == "__main__":
    folder = processFolder("/Users/svenmarcus/Documents/Institut/IVE/neu")
    print(folder)
    # print(readFile("./Zugliste.csv", TrainListDialect()))


