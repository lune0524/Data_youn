api_key = 'IC2pnL+590EQBSFgqvngRKjIwCftCwWFs5zRr1ako12aGYRiA0PnCxCj5e28Kv2OiLfDEqiholf5ilTFeAd7yQ=='

import requests
import json
import pandas as pd

lst_rows = []

page_no = 1
page_size = 20
my_url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
params = {
    'ServiceKey' : api_key ,
    'numOfRows' : page_size,
    'pageNo' : page_no,
    'dataType' : 'JSON',
    'dataCd' : 'ASOS',
    'dateCd' : 'DAY',
    'startDt' : '20100101',
    'endDt' : '20100601',
    'stnIds' : '108'
}

for i in range(1, 1000000):
  params['pageNo'] = i
  response = requests.get(my_url, params=params, verify=False) #verify설정 추가
  html = json.loads(response.text)

  resultCode = html['response']['header']['resultCode']
  if resultCode != '00':
    break

  items = html['response']['body']['items']['item']
  for item in items:
    lst_rows.append(pd.Series(item))

df = pd.concat(lst_rows, axis=1)
df = df.T
df.to_csv('result.csv')
print(df)