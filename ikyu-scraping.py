# -*- coding: utf-8 -*-
from datetime import datetime
import openpyxl as px
from openpyxl.styles import PatternFill
import requests
from bs4 import BeautifulSoup
 
url = 'https://www.ikyu.com/hokuriku/220000/?hoi=2&gotoFlag=0';
 
r    = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')


def Pagecrawling(soup, item_list):
  ryokans = soup.find_all('div', class_='acc_list_each')
 
  for ryokan in ryokans:
    names  = ryokan.find_all('h2', class_='acmName')
    basyos = ryokan.find_all('div', class_='acmArea')
 
    for (name, basyo) in zip(names, basyos):
      nameEx  = name.get_text()
      basyoEx = basyo.get_text().strip()
 
      item_list.append([nameEx, basyoEx])

  return item_list
 
def Write_excel(item_list):
  wb = px.Workbook()
  ws = wb.active
 
  fill = PatternFill(patternType='solid', fgColor='e0e0e0', bgColor='e0e0e0')
 
  headers = ['名前', '地域']
  for i, header in enumerate(headers):
    ws.cell(row=1, column=1+i, value=headers[i])
    ws.cell(row=1, column=1+i).fill = fill
 
    for y, row in enumerate(item_list):
      for x, cell in enumerate(row):
        ws.cell(row= y+2, column= x+1, value=item_list[y][x])

    now = datetime.now()
    data = now.strftime('%Y-%m-%d')
 
    filename = 'Ikyu' + data + '.xlsx'
    wb.save(filename)

item_list = []
item_list = Pagecrawling(soup, item_list)
Write_excel(item_list)