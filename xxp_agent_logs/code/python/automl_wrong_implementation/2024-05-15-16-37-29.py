import subprocess

# Function for executing subprocesses
def run_subprocess(command):
    result = print(command)
    # if result.returncode != 0:
    #     raise Exception(f"Error executing {command}: {result.stderr}")
    # print(result.stdout)

# Task: DataRetrieval
def data_retrieval():
    # Running the data retrieval script
    run_subprocess("python ideko_data_retreival.py")

# Task: TrainTestSplit
def train_test_split():
    # Running the train-test split script
    run_subprocess("python random_train_test_split.py")

# Subworkflow: MLTrainingAndEvaluation
def ml_training_and_evaluation():
    # Task: FeatureExtraction
    run_subprocess("python ideko_feature_extraction.py")
    
    # Task: ModelTraining
    run_subprocess("python regression_training.py")
    
    # Task: ModelEvaluation
    run_subprocess("python regression_evaluation.py")

# Subworkflow: MLModelValidation
def ml_model_validation():
    ml_training_and_evaluation()

# Subworkflow: HyperparameterOptimization
def hyperparameter_optimization():
    # Task: HyperparameterProposal
    run_subprocess("python grid_search.py")
    
    # Task: MLModelValidation
    ml_model_validation()
    
    # Task: BestHyperparameterSelection
    run_subprocess("python user_hyperparameter_selection.py")

# Main workflow: FailurePredictionInManufacture
def failure_prediction_in_manufacture():
    data_retrieval()
    train_test_split()
    hyperparameter_optimization()
    ml_training_and_evaluation()

# Execute the main workflow
if __name__ == "__main__":
    failure_prediction_in_manufacture()
