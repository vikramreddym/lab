import pickle

from flask import Flask, jsonify, request

with open("model1.bin", "rb") as f_in:
    model = pickle.load(f_in)

with open("dv.bin", "rb") as f_in:
    dv = pickle.load(f_in)

client = {"job": "management", "duration": 400, "poutcome": "success"}
X = dv.transform([client])

print(model.predict_proba(X)[0, 1])
