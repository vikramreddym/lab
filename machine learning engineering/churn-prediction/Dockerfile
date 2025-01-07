FROM python:3.12.7-slim

RUN pip install pipenv

WORKDIR /app
COPY ["Pipfile", "Pipfile.lock",  "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "./"]
COPY ["models/churn-model.bin", "./models/"]
EXPOSE 9696

ENTRYPOINT ["waitress-serve", "--host=0.0.0.0", "--port=9696", "predict:app"]