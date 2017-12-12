import csv


def writeFile(filePath, data, delimiter=',') -> None:
    with open(filePath, "w", encoding='ISO-8859-1') as csv_file:
        writer = csv.writer(csv_file, delimiter=delimiter)
        for line in data:
            writer.writerow(line)
