import requests

url = "http://localhost:8080/2015-03-31/functions/function/invocations"
data = {"image_url": "https://bit.ly/mlbookcamp-pants"}

result = requests.post(url, json=data).json()
print(result)
