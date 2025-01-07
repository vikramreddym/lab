# # load the model
import pickle

from flask import Flask, jsonify, request

model_file = "model.bin"
with open(model_file, 'rb') as f_in:
    dv, std_scaler, model = pickle.load(f_in)

app = Flask("ad-prediction")


@app.route("/predict", methods=["POST"])
def predict():
    client = request.get_json()

    X = dv.transform([client])
    X = std_scaler.transform(X)
    y_pred = model.predict_proba(X)[0, 1]
    click = y_pred >= 0.5

    result = {"click_probability": float(y_pred), "click": bool(click)}
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)