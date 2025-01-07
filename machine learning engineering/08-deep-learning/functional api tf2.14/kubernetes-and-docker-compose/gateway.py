import os

import grpc
import numpy as np
from flask import Flask, jsonify, request
from keras_image_helper import create_preprocessor
from proto import np_to_protobuf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

CLASS_NAMES = [
    "dress",
    "hat",
    "longsleeve",
    "outwear",
    "pants",
    "shirt",
    "shoes",
    "shorts",
    "skirt",
    "t-shirt",
]

URL = "http://bit.ly/mlbookcamp-pants"
INPUT_SIZE = 299
HOST = os.getenv("TF_SERVING_HOST", "localhost:8500")
channel = grpc.insecure_channel(HOST)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)


def prepare_request(X):
    pb_request = predict_pb2.PredictRequest()
    pb_request.model_spec.name = "clothing-model"
    pb_request.model_spec.signature_name = "serving_default"
    pb_request.inputs["input_2"].CopyFrom(np_to_protobuf(X))
    return pb_request


def prepare_response(pb_response):
    predictions = pb_response.outputs["dense_1"].float_val
    scores = {c: round(float(p), 2) for c, p in zip(CLASS_NAMES, predictions)}
    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    return {"predicted_class": predicted_class, "scores": scores}


def predict(url):
    preprocessor = create_preprocessor("xception", target_size=(INPUT_SIZE, INPUT_SIZE))
    X = preprocessor.from_url(url)
    pb_request = prepare_request(X)

    pb_response = stub.Predict(pb_request, timeout=20.0)
    response = prepare_response(pb_response)
    return response


app = Flask("gateway")


@app.route("/predict", methods=["POST"])
def predict_url():
    data = request.get_json()
    url = data["image_url"]
    result = predict(url)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
