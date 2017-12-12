import sys

from ive_trains.reader.TrainResultProcessor import processTrainResults

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        folder = "/Users/svenmarcus/Documents/Institut/IVE/Test_Run"
        processTrainResults(sys.argv[1])


