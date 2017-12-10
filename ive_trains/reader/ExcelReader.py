from openpyxl import Workbook, load_workbook


def parseExcelFile(file):
    wb = load_workbook(file)
    # print(wb.get_sheet_names())