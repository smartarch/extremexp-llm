import subprocess

# Function to run a command using subprocess
def run_command(command):
    result = print(command)
    # if result.returncode != 0:
    #     # print(f"Error running command: {command}")
    #     # print(result.stderr)
    # else:
    #     # print(result.stdout)

# Function to execute the MLTrainingAndEvaluation subworkflow
def execute_ml_training_and_evaluation(training_data, test_data, hyperparameters):
    # FeatureExtraction task
    # print("Running FeatureExtraction task in MLTrainingAndEvaluation...")
    run_command("python ideko_feature_extraction.py")

    # ModelTraining task
    # print("Running ModelTraining task in MLTrainingAndEvaluation...")
    run_command("python regression_training.py")

    # ModelEvaluation task
    # print("Running ModelEvaluation task in MLTrainingAndEvaluation...")
    run_command("python regression_evaluation.py")

# Function to execute the MLModelValidation subworkflow
def execute_ml_model_validation(input_data, hyperparameters):
    # TrainTestSplit task
    # print("Running TrainTestSplit task in MLModelValidation...")
    run_command("python random_train_test_split.py")

    # MLTrainingAndEvaluation subworkflow
    # print("Running MLTrainingAndEvaluation subworkflow in MLModelValidation...")
    execute_ml_training_and_evaluation(training_data="TrainingData", test_data="ValidationData", hyperparameters=hyperparameters)

# Function to execute the HyperparameterOptimization subworkflow
def execute_hyperparameter_optimization(training_data):
    # HyperparameterProposal task
    # print("Running HyperparameterProposal task in HyperparameterOptimization...")
    run_command("python grid_search.py")

    # MLModelValidation subworkflow
    # print("Running MLModelValidation subworkflow in HyperparameterOptimization...")
    execute_ml_model_validation(input_data="InputData", hyperparameters="Hyperparameters")

    # BestHyperparameterSelection task
    # print("Running BestHyperparameterSelection task in HyperparameterOptimization...")
    run_command("python user_hyperparameter_selection.py")

# Main workflow execution
def main():
    # DataRetrieval task
    # print("Running DataRetrieval task...")
    run_command("python ideko_data_retreival.py")

    # TrainTestSplit task
    # print("Running TrainTestSplit task...")
    run_command("python random_train_test_split.py")

    # HyperparameterOptimization subworkflow
    # print("Running HyperparameterOptimization subworkflow...")
    execute_hyperparameter_optimization(training_data="TrainingData")

    # MLTrainingAndEvaluation subworkflow
    # print("Running MLTrainingAndEvaluation subworkflow...")
    execute_ml_training_and_evaluation(training_data="TrainingData", test_data="TestData", hyperparameters="BestHyperparameters")

if __name__ == "__main__":
    main()
