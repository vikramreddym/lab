import requests

url = "http://localhost:9696/predict"
client = {'session_id': 317526,
 'user_id': 16554,
 'product': 'H',
 'campaign_id': 359520,
 'webpage_id': 13787,
 'product_category_1': 4,
 'user_group_id': 3.0,
 'gender': 'Male',
 'age_level': 3.0,
 'user_depth': 1.0,
 'city_development_index': 4.0,
 'var_1': 0,
 'hour': 10}

response = requests.post(url, json=client)
result = response.json()
print(result)