import numpy as np
from keras.applications.xception import preprocess_input
from keras.utils import img_to_array, load_img
from tensorflow import keras

from clothes_custom_model import CustomModel

model_path = "xception_final_15_0.874.keras"


# Preprocess a single image
def preprocess_image(image_path, input_size=299):
    """Preprocess an image for prediction."""
    img = load_img(image_path, target_size=(input_size, input_size))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Preprocessing specific to Xception
    return img_array


# Predict a single image
def predict_image(model, image_path, input_size=299):
    """Predict the class of a single image."""
    preprocessed_img = preprocess_image(image_path, input_size=input_size)
    predictions = model.predict(preprocessed_img)
    predicted_class = class_names[np.argmax(predictions[0])]
    scores = dict(zip(class_names, predictions[0]))
    return predicted_class, scores


if __name__ == "__main__":
    model = keras.models.load_model(
        model_path, custom_objects={"CustomModel": CustomModel}
    )
    input_size = model.input_size
    class_names = model.metadata["class_names"]

    test_image_path = "data/clothing-dataset-small/test/shoes/0dd87e47-ca85-4d5c-9fd1-59f5a01eb656.jpg"
    predicted_class, scores = predict_image(model, test_image_path, input_size)
    print(f"Predicted class: {predicted_class}\nscores: {scores}")
