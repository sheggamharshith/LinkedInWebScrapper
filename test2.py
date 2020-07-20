import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("LinkedInScrapping-e0f14006296b.json", scope)

client = gspread.authorize(creds)

sheet = client.open("LinkedInData").sheet1  # Open the spreadhseet

# data = sheet.get_all_records()  # Get a list of all records

# row = sheet.row_values(3)  # Get a specific row
# col = sheet.col_values(3)  # Get a specific column
# cell = sheet.cell(1,2).value  # Get the value of a specific cell

# print(row)
# print(col)
# print(cell)
# print(data)


# numRows = sheet.row_count  # Get the number of rows in the sheet
# print(numRows)

row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python45"]
sheet.insert_row(row)

list_of_hashes = sheet.get_all_records()
print(list_of_hashes)
