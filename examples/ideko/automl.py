import csv
from itertools import chain
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import train_test_split, ParameterGrid
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from joblib import dump
import random

random.seed(42)

# workflow AutoML

def W_automl():
    input_data_path = get_environ_path("NEW_DATA_FILE")

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
    params_iterator = chain(iter(ParameterGrid({
        "algorithm": ["neural_network"],
        "hidden_layer_sizes": [1, 2, 5, 10],
    # })), iter(ParameterGrid({
    #     "algorithm": ["decision_tree"],
    #     "max_leaf_nodes": [1, 2, 5],
    })))

    results_path = get_environ_path("RESULTS_FOLDER") / 'ml_models.csv'
    with open(results_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["MLModelHyperparameters", "Accuracy", "Precision", "Recall", "F1", "NumOfParams"])

        while True:
            hyperparameters = T_hyperparameter_proposal(params_iterator)
            if hyperparameters is None:  # stop condition
                break

            ml_model_metrics = T_ml_model_validation(hyperparameters, training_data)

            writer.writerow([stringify_hyperparameters(hyperparameters), *ml_model_metrics])

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
    if hyperparameters["algorithm"] == "neural_network":
        model_hyperparameters = hyperparameters.copy()
        del model_hyperparameters["algorithm"]
        ml_model = MLPClassifier(**model_hyperparameters, max_iter=1000, random_state=42)
    elif hyperparameters["algorithm"] == "decision_tree":
        model_hyperparameters = hyperparameters.copy()
        del model_hyperparameters["algorithm"]
        ml_model = DecisionTreeClassifier(**model_hyperparameters, random_state=42)

    train_X, train_Y = training_features
    ml_model.fit(train_X, train_Y)

    model_name = stringify_hyperparameters(hyperparameters)
    
    # save the training losses (for each epoch)
    if isinstance(ml_model, MLPClassifier):
        training_results_path = get_environ_path("RESULTS_FOLDER") / 'ml_models' / f"{model_name}_training.csv"
        with open(training_results_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Epoch", "Loss"])
            for epoch, loss in enumerate(ml_model.loss_curve_):
                writer.writerow([epoch, loss])

    # save the model
    ml_model_path = get_environ_path("RESULTS_FOLDER") / 'ml_models' / f"{model_name}.joblib"
    dump(ml_model, ml_model_path)

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

# Helpers

def get_environ_path(key):
    return Path(__file__).parent / os.environ[key]

def stringify_hyperparameters(hyperparameters):
    return ",".join([f"{key}={value}" for key, value in hyperparameters.items()])

# Main

if __name__ == '__main__':
    load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.
    os.makedirs(get_environ_path("RESULTS_FOLDER") / 'ml_models', exist_ok=True)
    W_automl()
