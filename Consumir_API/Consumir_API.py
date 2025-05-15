import requests

url="http://localhost:3000/api/peaton/"

response=requests.get(url)

if response.status_code==200:
    print(response.json())
else:
    print(response.json())

url="http://localhost:3000/api/peaton/add"

data={'temperatura':27,'temperatura':27,'temperatura':27}
response=requests.post(url, json=data)

if response.status_code==200:
    print(response.json())
else:
    print(response.json())