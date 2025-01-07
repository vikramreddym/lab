import pickle 

model_file = "model.bin"
with open(model_file, 'rb') as f_in:
    dv, std_scaler, model = pickle.load(f_in)

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

X = dv.transform([client])
X = std_scaler.transform(X)

print(model.predict(X)[0])