from test_instance_templates import OpenQuestion


q = OpenQuestion("", '**Mismatch in Task Objectives**: The "FailurePredictionInManufacture" workflow is described as being for "predicting machine failures (binary classification)". However, the subworkflow "MLTrainingAndEvaluation" derived from the "automl_xyz" package is described for "training and evaluation of the regression ML model". Regression models are not typically used for binary classification tasks. This discrepancy suggests that the task might not be achieving its intended purpose of binary classification.')

print("Correct answer + 2 other:")
print(q.check_answer('''Final answer:
1. **Mismatch in Model Type Description**:
    - The parent workflow "FailurePredictionInManufacture" describes the prediction task as "binary classification". However, the subworkflow "MLTrainingAndEvaluation" is specified for "training and evaluation of the regression ML model". This inconsistency could lead to confusion and errors in model evaluation and application.
    - **Related Task**: MLTrainingAndEvaluation

2. **Inappropriate Evaluation Metrics**:
    - Within the "MLTrainingAndEvaluation" subworkflow, the "ModelEvaluation" task uses metrics like "accuracy", "precision", "recall", "f1", which are classification metrics, not suitable for regression tasks as described in the workflow. This inconsistency indicates either an error in the choice of metrics or a misdescription of the model type.
    - **Related Task**: ModelEvaluation

3. **Hyperparameter Optimization Loop Condition Ambiguity**:
    - In the "HyperparameterOptimization" subworkflow, there is a loop between "HyperparameterProposal" and "MLModelValidation" based on "otherwise" condition and a transition to "BestHyperparameterSelection" based on "stop condition". The criteria for these conditions are not explicitly defined, which could lead to ambiguity in when to stop the optimization process.
    - **Related Task**: HyperparameterOptimization
'''))

print("Only correct answer:")
print(q.check_answer('''Final answer:
1. **Mismatch in Model Type Description**:
    - The parent workflow "FailurePredictionInManufacture" describes the prediction task as "binary classification". However, the subworkflow "MLTrainingAndEvaluation" is specified for "training and evaluation of the regression ML model". This inconsistency could lead to confusion and errors in model evaluation and application.
    - **Related Task**: MLTrainingAndEvaluation
'''))

print("Not correct, but similar:")
print(q.check_answer('''Final answer:
2. **Inappropriate Evaluation Metrics**:
    - Within the "MLTrainingAndEvaluation" subworkflow, the "ModelEvaluation" task uses metrics like "accuracy", "precision", "recall", "f1", which are classification metrics, not suitable for regression tasks as described in the workflow. This inconsistency indicates either an error in the choice of metrics or a misdescription of the model type.
    - **Related Task**: ModelEvaluation
'''))

print("Not correct:")
print(q.check_answer('''Final answer:
3. **Hyperparameter Optimization Loop Condition Ambiguity**:
    - In the "HyperparameterOptimization" subworkflow, there is a loop between "HyperparameterProposal" and "MLModelValidation" based on "otherwise" condition and a transition to "BestHyperparameterSelection" based on "stop condition". The criteria for these conditions are not explicitly defined, which could lead to ambiguity in when to stop the optimization process.
    - **Related Task**: HyperparameterOptimization
'''))