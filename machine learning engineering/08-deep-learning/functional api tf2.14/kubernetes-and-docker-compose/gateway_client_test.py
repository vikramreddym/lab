import requests

# url = "http://localhost:8080/predict"
url = "http://a0bcb5c025def4f1c849a2825558edfc-174606405.us-east-2.elb.amazonaws.com:8080/predict"
data = {"image_url": "https://bit.ly/mlbookcamp-pants"}
result = requests.post(url, json=data).json()
print(result)
