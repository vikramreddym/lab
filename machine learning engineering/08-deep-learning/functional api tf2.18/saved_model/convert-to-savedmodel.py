import tensorflow as tf
from tensorflow import keras

model_path = "xception_final_11_0.871.keras"

model = keras.models.load_model(model_path)
tf.saved_model.save(model, "clothing-model")
