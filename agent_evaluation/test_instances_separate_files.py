from test_instance_templates import SetQuestion, YesNoQuestion, instance_generator


def test_instances(update_specification_tool_path):
    test_instances_structure = {
        "List of tasks": [
            update_specification_tool_path("artificial_workflow"),
            SetQuestion("List all tasks in workflow 'package2.MainWorkflow'. Do not list tasks nested inside other tasks.", {"Task1", "Task2", "Task3", "Task4"}),
            SetQuestion("List all tasks in workflow 'package2.MainWorkflow' that have a subworkflow. Do not list tasks nested inside other tasks.", {"Task1", "Task4"}),
            update_specification_tool_path("automl_wrong_implementation"),
            SetQuestion("List all tasks in workflow 'automl.HyperparameterOptimization'. Do not list tasks nested inside other tasks.", {"HyperparameterProposal", "MLModelValidation", "BestHyperparameterSelection"}),
            SetQuestion("List all tasks in workflow 'automl_ideko.MLTrainingAndEvaluation' that have a parameter (set via the 'param' keyword). Do not list tasks nested inside other tasks.", {"ModelEvaluation"}),
            SetQuestion("List all tasks in workflow 'automl_ideko.MLTrainingAndEvaluation' that have a subworkflow. Do not list tasks nested inside other tasks.", set()),
        ],
        "Task links in flow": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("In workflow 'package2.SubWorkflow', does 'Task9' follow directly after 'Task10' in the control flow?", True),
            YesNoQuestion("In workflow 'package2.SubWorkflow', does 'Task10' follow directly after 'Task9' in the control flow?", False),
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("In workflow 'automl.MLTrainingAndEvaluation', does 'ModelTraining' follow directly after 'ModelEvaluation' in the control flow?", False),
            YesNoQuestion("In workflow 'automl.MLTrainingAndEvaluation2', does 'ModelTraining' follow directly after 'ModelEvaluation' in the control flow?", True),  # semantically incorrect order
        ],
        "Next tasks in flow": [
            update_specification_tool_path("artificial_workflow"),
            SetQuestion("In workflow 'package2.MainWorkflow', which tasks come directly after 'Task2' in the control flow?", {"Task1", "Task3"}),  # parallel
            SetQuestion("In workflow 'package1.Workflow3', which tasks come directly after 'Task7' in the control flow?", {"Task9", "Task8"}),  # conditional
            SetQuestion("In workflow 'package2.MainWorkflow', which tasks come directly after 'Task3' in the control flow?", {"Task4"}),
            SetQuestion("In workflow 'package2.SubWorkflow', which tasks come directly after 'Task9' in the control flow?", {"Task11"}),
        ],
        "Flow cycle": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("In workflow 'package1.Workflow2', is there a cycle in the control flow?", True),
            YesNoQuestion("In workflow 'package2.MainWorkflow', is there a cycle in the control flow?", False),
            YesNoQuestion("In workflow 'package1.Workflow3', is there a cycle in the control flow?", False),  # conditional flow
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("In workflow 'automl.HyperparameterOptimization', is there a cycle in the control flow?", True),  # conditional cycle
        ],
    }

    test_instances_behavior = {
        "Mutually exclusive conditional flow": [
            update_specification_tool_path("artificial_workflow"),
            YesNoQuestion("In workflow 'package1.Workflow3', are conditional links in control flow from 'Task7' mutually exclusive?", False),
            update_specification_tool_path("automl_wrong_implementation"),
            YesNoQuestion("In workflow 'automl.HyperparameterOptimization', are conditional links in control flow from 'HyperparameterProposal' mutually exclusive?", True),  # "otherwise"
        ]
    }

    yield from instance_generator("structure", test_instances_structure)
    yield from instance_generator("behavior", test_instances_behavior)
