import numpy as np
from keras_image_helper import create_preprocessor
from tflite_runtime.interpreter import Interpreter

# Constants
MODEL_PATH = "clothing-model.tflite"
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
INPUT_SIZE = 299


def load_model(model_path):
    interpreter = Interpreter(model_path)
    interpreter.allocate_tensors()
    return interpreter


# Preprocess a single image
def preprocess_image(image_url, input_size=299):
    """Preprocess an image for prediction."""
    preprocessor = create_preprocessor("xception", target_size=(input_size, input_size))
    return preprocessor.from_url(image_url)


# Predict a single image
def predict_image(interpreter, image_url, input_size=299):
    """Predict the class of a single image."""
    preprocessed_img = preprocess_image(image_url, input_size=input_size)

    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]
    interpreter.set_tensor(input_index, preprocessed_img)
    interpreter.invoke()

    predictions = interpreter.get_tensor(output_index)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    scores = {c: round(float(p), 2) for c, p in zip(CLASS_NAMES, predictions[0])}
    return {"predicted_class": predicted_class, "scores": scores}


def predict(image_url):
    interpreter = load_model(MODEL_PATH)
    return predict_image(interpreter, image_url, INPUT_SIZE)


def lambda_handler(event, context):
    return predict(event["image_url"])
