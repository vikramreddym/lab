import keras
import tensorflow as tf
from keras import layers
from keras.applications.xception import Xception
from keras.utils import register_keras_serializable


@register_keras_serializable(package="Custom")
class CustomModel(keras.Model):
    def __init__(
        self,
        input_size,
        num_classes,
        size_inner=100,
        droprate=0.5,
        metadata=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.input_size = input_size
        self.num_classes = num_classes
        self.size_inner = size_inner
        self.droprate = droprate
        self.metadata = metadata  # Metadata for saving class names and input size

        # Base Model (Xception)
        self.base_model = Xception(
            weights="imagenet",
            include_top=False,
            input_shape=(input_size, input_size, 3),
        )
        self.base_model.trainable = False

        # Layers for the custom model
        self.global_pool = layers.GlobalAveragePooling2D()
        self.inner_dense = layers.Dense(size_inner, activation="relu")
        self.dropout = layers.Dropout(droprate)
        self.output_layer = layers.Dense(num_classes)

    def call(self, inputs, training=False):
        x = self.base_model(inputs, training=False)
        x = self.global_pool(x)
        x = self.inner_dense(x)
        x = self.dropout(x, training=training)
        return self.output_layer(x)

    def get_config(self):
        # Include metadata in the configuration
        config = super().get_config()
        config.update(
            {
                "input_size": self.input_size,
                "num_classes": self.num_classes,
                "size_inner": self.size_inner,
                "droprate": self.droprate,
                "metadata": self.metadata,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        metadata = config.pop("metadata", None)
        return cls(metadata=metadata, **config)

    def _get_save_spec(self, dynamic_batch=False):
        """
        Returns the input specification for saving the model.
        """
        batch_size = None if dynamic_batch else 1
        input_spec = tf.TensorSpec(
            shape=(batch_size, self.input_size, self.input_size, 3), dtype=tf.float32
        )
        return [input_spec]
