from test_instance_templates import OpenQuestion, SetQuestion, YesNoQuestion, instance_generator


def test_instances(update_specification_tool_path):
    test_instances_structure = {
        "List of tasks": [
            update_specification_tool_path("artificial_workflow"),
            SetQuestion("List all tasks directly in workflow 'MainWorkflow'. Do not list tasks nested inside other tasks.", {"Task1", "Task2", "Task3", "Task4"}),
            SetQuestion("List all tasks directly in workflow 'MainWorkflow' that have nested subtasks. Do not list tasks nested inside other tasks.", {"Task1", "Task4"}),
            update_specification_tool_path("automl_wrong_implementation"),
            SetQuestion("Work with workflow 'FailurePredictionInManufacture'. List all subtasks directly in task 'HyperparameterOptimization'. Do not list tasks nested inside other tasks.", {"HyperparameterProposal", "MLModelValidation", "BestHyperparameterSelection"}),
            SetQuestion("Work with workflow 'FailurePredictionInManufacture'. List all subtasks directly in task 'MLTrainingAndEvaluation' that have a parameter (set via the 'param' keyword). Do not list tasks nested inside other tasks.", {"ModelEvaluation"}),
            SetQuestion("Work with workflow 'FailurePredictionInManufacture'. List all subtasks directly in task 'MLTrainingAndEvaluation' that have nested subtasks. Do not list tasks nested inside other tasks.", set()),
        ],
        "Links in flow": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("Work with workflow 'MainWorkflow'. In task 'Task4', is there a control flow link from 'Task10' to 'Task9'?", True),
            YesNoQuestion("Work with workflow 'MainWorkflow'. In task 'Task4', is there a control flow link from 'Task9' to 'Task10'?", False),
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("Work with workflow 'FailurePredictionInManufacture'. In task 'MLTrainingAndEvaluation', is there a control flow link from 'ModelEvaluation' to 'ModelTraining'?", False),
            YesNoQuestion("Work with workflow 'FailurePredictionInManufacture2'. In task 'MLTrainingAndEvaluation', is there a control flow link from 'ModelEvaluation' to 'ModelTraining'?", True),  # semantically incorrect order
        ],
        "Task after task": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("Work with workflow 'MainWorkflow'. In task 'Task4', does 'Task9' follow directly after 'Task10' in the control flow?", True),
            YesNoQuestion("Work with workflow 'MainWorkflow'. In task 'Task4', does 'Task10' follow directly after 'Task9' in the control flow?", False),
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("Work with workflow 'FailurePredictionInManufacture'. In task 'MLTrainingAndEvaluation', does 'ModelTraining' follow directly after 'ModelEvaluation' in the control flow?", False),
            YesNoQuestion("Work with workflow 'FailurePredictionInManufacture2'. In task 'MLTrainingAndEvaluation', does 'ModelTraining' follow directly after 'ModelEvaluation' in the control flow?", True),  # semantically incorrect order
        ],
        "Next tasks in flow": [
            update_specification_tool_path("artificial_workflow"),
            SetQuestion("In workflow 'MainWorkflow', which tasks come directly after 'Task2' in the control flow?", {"Task1", "Task3"}),  # parallel
            SetQuestion("In workflow 'MainWorkflow', which tasks come directly after 'Task7' in the control flow?", {"Task9", "Task8"}),  # conditional
            SetQuestion("In workflow 'MainWorkflow', which tasks come directly after 'Task3' in the control flow?", {"Task4"}),
            SetQuestion("In workflow 'MainWorkflow', which tasks come directly after 'Task9' in the control flow?", {"Task11"}),
        ],
        "Flow cycle": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("In task 'Task1' from workflow 'MainWorkflow', is there a cycle in the control flow?", True),
            YesNoQuestion("In workflow 'MainWorkflow', is there a cycle in the control flow directly in the workflow (not inside any of the subtasks)?", False),
            YesNoQuestion("In task 'Task6' from workflow 'MainWorkflow', is there a cycle in the control flow?", False),  # conditional flow
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("In task 'HyperparameterOptimization' from workflow 'FailurePredictionInManufacture', is there a cycle in the control flow?", True),  # conditional cycle
        ],
    }

    test_instances_behavior = {
        "Mutually exclusive conditional flow": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("In workflow 'MainWorkflow', are conditional links in control flow from 'Task7' mutually exclusive?", False),
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("In workflow 'FailurePredictionInManufacture', are conditional links in control flow from 'HyperparameterProposal' mutually exclusive?", True),  # "otherwise"
        ]
    }

    test_instances_semantics = {
        "Inconsistent task name and description": [
            update_specification_tool_path("automl_wrong_implementation"),
            OpenQuestion(
                "Identify potential errors in the descriptions of tasks in workflow 'FailurePredictionInManufacture'. Write one error per line.",
                "The description of task 'DataRetrieval' does not correspond with its name. The task should retrieve the input data, while the description says that it saves the results of the experiment and produces plots."),
        ],
        "Inconsistent descriptions": [
            update_specification_tool_path("automl_wrong_implementation"),
            OpenQuestion(
                "Identify potential errors in the description of workflow 'FailurePredictionInManufacture' and its tasks (including all nested subtasks). Write one error per line.",
                "The description of the 'MLTrainingAndEvaluation' task does not correspond with the description of the 'FailurePredictionInManufacture' workflow. The tasks state that they train a regression ML model while the workflow is intended for binary classification."),
        ],
    }

    yield from instance_generator("structure", test_instances_structure)
    yield from instance_generator("behavior", test_instances_behavior)
    yield from instance_generator("semantics", test_instances_semantics)
