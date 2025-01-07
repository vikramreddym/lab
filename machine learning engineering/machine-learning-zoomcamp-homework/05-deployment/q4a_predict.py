# # load the model
import pickle

from flask import Flask, jsonify, request

with open("model1.bin", "rb") as f_in:
    model = pickle.load(f_in)

with open("dv.bin", "rb") as f_in:
    dv = pickle.load(f_in)

app = Flask("subscription")


@app.route("/predict", methods=["POST"])
def predict():
    client = request.get_json()

    X = dv.transform([client])
    y_pred = model.predict_proba(X)[0, 1]
    subscribe = y_pred >= 0.5

    result = {"subscription_probability": float(y_pred), "subscribe": bool(subscribe)}
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
