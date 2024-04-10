from test_instance_templates import SetQuestion, YesNoQuestion, instance_generator


def test_instances(update_specification_tool_path):
    test_instances_structure = {
        "List of tasks": [
            update_specification_tool_path("artificial_workflow"),
            SetQuestion("List all tasks in workflow 'MainWorkflow'.", {"Task1", "Task2", "Task3", "Task4"}),
            SetQuestion("List all tasks in workflow 'MainWorkflow' that have a subworkflow.", {"Task1", "Task4"}),
            update_specification_tool_path("automl_wrong_implementation"),
            SetQuestion("List all tasks in workflow 'HyperparameterOptimization'.", {"HyperparameterProposal", "MLModelValidation", "BestHyperparameterSelection"}),
            SetQuestion("List all tasks in workflow 'MLTrainingAndEvaluation' that have a parameter (set via the 'param' keyword).", {"ModelEvaluation"}),
            SetQuestion("List all tasks in workflow 'MLTrainingAndEvaluation' that have a subworkflow.", set()),
        ],
        "Task links in flow": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("In workflow 'SubWorkflow', does 'Task9' follow directly after 'Task10' in the control flow?", True),
            YesNoQuestion("In workflow 'SubWorkflow', does 'Task10' follow directly after 'Task9' in the control flow?", False),
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("In workflow 'MLTrainingAndEvaluation', does 'ModelTraining' follow directly after 'ModelEvaluation' in the control flow?", False),
            YesNoQuestion("In workflow 'MLTrainingAndEvaluation2', does 'ModelTraining' follow directly after 'ModelEvaluation' in the control flow?", True),  # semantically incorrect order
        ],
        "Next tasks in flow": [
            update_specification_tool_path("artificial_workflow"),
            SetQuestion("In workflow 'MainWorkflow', which tasks come directly after 'Task2' in the control flow?", {"Task1", "Task3"}),  # parallel
            SetQuestion("In workflow 'Workflow3', which tasks come directly after 'Task7' in the control flow?", {"Task9", "Task8"}),  # conditional
            SetQuestion("In workflow 'MainWorkflow', which tasks come directly after 'Task3' in the control flow?", {"Task4"}),
            SetQuestion("In workflow 'SubWorkflow', which tasks come directly after 'Task9' in the control flow?", {"Task11"}),
        ],
        "Flow cycle": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("In workflow 'Workflow2', is there a cycle in the control flow?", True),
            YesNoQuestion("In workflow 'MainWorkflow', is there a cycle in the control flow?", False),
            YesNoQuestion("In workflow 'Workflow3', is there a cycle in the control flow?", False),  # conditional flow
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("In workflow 'HyperparameterOptimization', is there a cycle in the control flow?", True),  # conditional cycle
        ],
    }

    test_instances_behavior = {
        "Mutually exclusive conditional flow": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("In workflow 'Workflow3', are conditional links in control flow from 'Task7' mutually exclusive?", False),
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("In workflow 'HyperparameterOptimization', are conditional links in control flow from 'HyperparameterProposal' mutually exclusive?", True),  # "otherwise"
        ]
    }

    yield from instance_generator("structure", test_instances_structure)
    yield from instance_generator("behavior", test_instances_behavior)
