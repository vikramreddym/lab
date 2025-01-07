
# CTR Prediction: Click-Through Rate Prediction Project

This project predicts whether a user will click on an advertisement using demographic, session, and product data. It combines data preprocessing, modeling, and a Dockerized deployment.
The dataset is taken from here: https://www.kaggle.com/datasets/arashnic/ctr-in-advertisement/data

## Features
- **Data Preprocessing:** Handles missing values, time-based feature extraction, and encoding.
- **Model Training:** Evaluates Logistic Regression, Decision Trees, Random Forest, and XGBoost.
- **Hyperparameter Tuning:** Optimizes DecisionTree for the best F1 score.
- **Model Deployment:** Includes Dockerized service and a Python prediction client.


## Pre-requisites
- Python 3.12 
- Docker Desktop

## Usage

### Option 1 (Docker)

#### a. Build the Docker Image
```bash
docker build -t adpred .
```

#### b. Run the Docker Container
```bash
docker run -d -p 9696:9696 adpred
```

#### c. Use the Client
Run the client to send prediction requests to the service:
```bash
python predict_client.py
```
---
### Option 2 (Local execution)

#### a. Install pipenv if not already installed:
```bash
pip install pipenv
```

#### b. Install dependencies using Pipfile and Pipfile.lock:
```bash
pipenv install --dev
```

#### c. Activate the virtual environment:
```bash
pipenv shell
```

#### d. Run the service locally:
```bash
python service.py
```

#### e.	Test the Prediction Locally:
```bash
python predict_client.py 
```
---
### Re-Training
### 1. Train the Model
Update the data if necessary. Use `ad-click-prediction.py` to train the DecisionTree Classifier model with the best hyperparameters:
```bash
python ad-click-prediction.py
```
This script saves the model and preprocessors as:
- `model.bin`

### 2. Test the Model
Use `test-predict.py` to load the saved models and make prediction for the single data point in the script:
```bash
python test-predict.py
```
---
To run the notebook or to run re-training script, setup virtual env using steps from option 2 above and execute it.
## Documentation
For detailed explanations of the project structure and methodology, check the [Documentation](Documentation/documentation.pdf).