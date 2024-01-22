import pandas as pd

spreadsheet_file = pd.ExcelFile("/Users/lucasg17/Downloads/convertcsv.xlsx")

worksheets = spreadsheet_file.sheet_names
appended_data = []

for sheet_data_name in worksheets:
    header_name = 'nameOfIssuer'
    df = pd.read_excel(spreadsheet_file, sheet_data_name, header=0)
    print(df)
    df = df[['COID', header_name]]
    # print(df)