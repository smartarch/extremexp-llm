import csv
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import train_test_split, ParameterGrid
from sklearn.neural_network import MLPClassifier
import random

random.seed(42)

# workflow AutoML

def W_automl():
    input_data_path = Path(__file__).parent / os.environ["NEW_DATA_FILE"]

    retrieved_data = T_data_retrieval(input_data_path)
    training_data, test_data = T_train_test_split(retrieved_data)
    T_hyperparameter_optimization(training_data)

def T_data_retrieval(input_data_path):
    dataframe = pd.read_csv(input_data_path)
    
    # add labels
    dataframe['label'] = 0
    # correct data
    dataframe.loc[343:, 'label'] = 1

    retrieved_data = dataframe
    return retrieved_data

def T_train_test_split(retrieved_data, test_size=0.2):
    training_data, test_data = train_test_split(retrieved_data, test_size=test_size)
    return training_data, test_data

def T_hyperparameter_optimization(training_data):
    W_hyperparameter_optimization(training_data)
    # best hyperparameter selection (and following tasks) is not implemented, it should be aided by the LLM


# workflow HyperparameterOptimization

def W_hyperparameter_optimization(training_data):
    params_iterator = iter(ParameterGrid({
        "hidden_layer_sizes": [1, 2, 5, 10],
    }))

    results_path = Path(__file__).parent / 'ml_models.csv'
    with open(results_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["MLModelHyperparameters", "Accuracy", "Precision", "Recall", "F1", "NumOfParams"])

        while True:
            hyperparameters = T_hyperparameter_proposal(params_iterator)
            if hyperparameters is None:  # stop condition
                break

            ml_model_metrics = T_ml_model_validation(hyperparameters, training_data)

            writer.writerow([hyperparameters, *ml_model_metrics])

    # best hyperparameter selection (and following tasks) is not implemented, it should be aided by the LLM

def T_hyperparameter_proposal(params_iterator):
    try:
        hyperparameters = next(params_iterator)
        return hyperparameters
    except StopIteration:
        return None

def T_ml_model_validation(hypeparameters, training_data):
    ml_model_metrics = W_train_test_split_validation(hypeparameters, training_data)
    return ml_model_metrics


# workflow TrainTestSplitValidation

# T_train_test_split is the same as in AutoML workflow

def W_train_test_split_validation(hypeparameters, input_data):
    training_data, validation_data = T_train_test_split(input_data)
    ml_model_metrics = T_ml_training_and_evaluation(hypeparameters, training_data, validation_data)
    return ml_model_metrics

def T_ml_training_and_evaluation(hypeparameters, training_data, validation_data):
    ml_model_metrics = W_ml_training_and_evaluation(hypeparameters, training_data, validation_data)
    return ml_model_metrics


# workflow MLTrainingAndEvaluation

def W_ml_training_and_evaluation(hypeparameters, training_data, test_data):
    training_features, test_features = T_feature_extraction(hypeparameters, training_data, test_data)
    ml_model = T_model_training(hypeparameters, training_features)
    ml_model_metrics = T_model_evaluation(ml_model, test_features)
    return ml_model_metrics

def T_feature_extraction(hypeparameters, training_data, test_data):
    train_X = training_data.drop("label", axis=1)
    # train_X = training_data[["positive_std","negative_std"]]
    train_Y = training_data["label"]

    test_X = test_data.drop("label", axis=1)
    # test_X = test_data[["positive_std","negative_std"]]
    test_Y = test_data["label"]

    training_features = train_X, train_Y
    test_features = test_X, test_Y
    return training_features, test_features

def T_model_training(hyperparameters, training_features):
    ml_model = MLPClassifier(**hyperparameters, max_iter=1000, random_state=42)

    train_X, train_Y = training_features
    ml_model.fit(train_X, train_Y)

    return ml_model

def T_model_evaluation(ml_model, test_features):
    test_X, test_Y = test_features
    predicted_Y = ml_model.predict(test_X)

    accuracy = accuracy_score(test_Y, predicted_Y)
    precision = precision_score(test_Y, predicted_Y)
    recall = recall_score(test_Y, predicted_Y)
    f1 = f1_score(test_Y, predicted_Y)
    num_of_params = sum(np.prod(coef.shape) for coef in ml_model.coefs_ + ml_model.intercepts_)

    ml_model_metrics = [accuracy, precision, recall, f1, num_of_params]
    return ml_model_metrics


# Main

if __name__ == '__main__':
    load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.
    W_automl()
