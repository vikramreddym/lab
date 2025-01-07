import requests

url = "http://localhost:9696/predict"
data = {"image_url": "https://bit.ly/mlbookcamp-pants"}
result = requests.post(url, json=data).json()
print(result)
