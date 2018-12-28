import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from contextlib import suppress

wb = load_workbook('Grades.xlsx')
ws = wb['FCIH 2017-2018']

for i in range(1, 2448):
    r = requests.get("http://app2.helwan.edu.eg/NatHSB/StdDataview.asp?StdCode=" + str(i))
    soup = BeautifulSoup(r.content, 'html.parser')
    std = soup.form.select('div > b')
    data = soup.select('div > b > font')
    with suppress(IndexError):
        print([std[0].text, std[1].text, std[4].text, data[0].text, data[7].text, data[14].text, data[1].text, data[8].text, data[15].text, data[2].text, data[9].text, data[16].text, data[3].text, data[10].text, data[17].text, data[4].text, data[11].text, data[18].text, data[5].text, data[12].text, data[19].text, data[6].text, data[13].text, data[20].text])

wb.save('Grades.xlsx')
print("DONE !!!")