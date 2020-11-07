import requests

url = 'www.baidu.com'
headers = {}
reponse = requests.get(url, headers=headers)
html = repsonse.text
print(html)

