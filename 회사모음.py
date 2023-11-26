import gspread
from pandas import DataFrame

json_file_path = "furnitures-recruit-automation-5da954d2f389.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1ygo_XrS4p6bD5nD6ozG20NLz3NmVRn9u5JlM7rNuatY/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)

update_sheet = doc.worksheet("회사 모음")
worksheet_11_1 = doc.worksheet("11월 1주차")

cpn_name = worksheet_11_1.col_values(6)
cpn_people = worksheet_11_1.col_values(8)
cpn_add = worksheet_11_1.col_values(9)
cpn_url = worksheet_11_1.col_values(11)


#11월 2주차 부터 채용공고를 올리는 사무소마다 중복되지 않으면 추가하기

df = DataFrame({'회사 명':cpn_name, '직원 수':cpn_people, '위치':cpn_add, '홈페이지':cpn_url})
update_sheet.update([df.columns.values.tolist()] + df.values.tolist())