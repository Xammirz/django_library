import requests

urlbooks = 'http://127.0.0.1:8000/library/api/v1/books/'

res = requests.get(urlbooks).text

print(res)
