FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11

RUN pip install keras-image-helper
RUN pip install numpy==1.26.4
RUN pip install https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.14.0-cp311-cp311-linux_x86_64.whl

COPY clothing-model.tflite .
COPY lambda_function.py .

CMD [ "lambda_function.lambda_handler" ]