from pathlib import Path
import sys

sys.path.append(str((Path(__file__).parent / ".." / "xxp_agent" ).resolve()))  # dirty trick to allow importing python files from the 'xxp_agent' folder

from colorama import Style
from dotenv import find_dotenv, load_dotenv
import pandas as pd

from helpers import LOGGER_FOLDER, MODEL, SPECIFICATION_FOLDER, Logger, print_color, print_prompt_template, \
    print_available_tools, print_input_message, print_result
from agent import create_agent, create_llm
from config import get_prompt_template, get_specification_tools, load_config

from test_instance_templates import SetQuestion, TestInstance, YesNoQuestion

load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.

PROJECT_DIR = Path(__file__).parent.parent  # root of the repository

# Load configuration file

# config_file_path = input("Configuration file path: ")
variant = "2_config.yaml"
config_file_path = f"examples/artificial_workflow/{variant}"
config = load_config(PROJECT_DIR / config_file_path)

# Create Logger

sys.stdout = Logger(PROJECT_DIR / "agent_evaluation_logs")

print("Configuration file path:", config_file_path)
print("Configuration:", config)

# Create LLM

llm = create_llm(model=config.get(MODEL, "gpt-3.5-turbo"))

# Tools

tools = []
specification_tool = get_specification_tools(config, PROJECT_DIR)
tools.append(specification_tool)

# FIXME: this is a hacky way to change the configuration folder, but it works for now
def update_specification_tool_path(folder_name):
    def update_specification_folder():
        new_config_path = f"examples/{folder_name}/{variant}"
        new_config = load_config(PROJECT_DIR / new_config_path)
        new_specification_folder = PROJECT_DIR / new_config[SPECIFICATION_FOLDER]
        specification_tool.specification_folder = new_specification_folder
        print(f"Configuration: 'specification_folder' updated to {new_config[SPECIFICATION_FOLDER]}")
    return update_specification_folder


# Test instances

test_instances_structure = {
    "List of tasks": [
        update_specification_tool_path("artificial_workflow"),
        SetQuestion("List all tasks in workflow 'MainWorkflow'.", {"Task1", "Task2", "Task3", "Task4"}),
        SetQuestion("List all tasks in workflow 'MainWorkflow' that have a subworkflow.", {"Task1", "Task4"}),
        update_specification_tool_path("automl_wrong_implementation"),
        SetQuestion("List all tasks in workflow 'HyperparameterOptimization'.", {"HyperparameterProposal", "MLModelValidation", "BestHyperparameterSelection"}),
        SetQuestion("List all tasks in workflow 'MLTrainingAndEvaluation' that have a parameter (set via the 'param' keyword).", {"ModelEvaluation"}),
        SetQuestion("List all tasks in workflow 'MLTrainingAndEvaluation' that have a subworkflow.", set()),  # TODO: deal with empty set as an answer
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

def test_instances():
    for pattern, test_instances in test_instances_structure.items():
        for test_instance in test_instances:
            yield "structure", pattern, test_instance

# Main

print_color("This script uses multiline input. Press Ctrl+D (Linux) or Ctrl+Z (Windows) on an empty line to end input message.", Style.DIM)

prompt = get_prompt_template(config, with_memory=False)
agent = create_agent(llm, tools, prompt)

print_prompt_template(prompt)
print_available_tools(tools)

print("\nStart of test.\n")

results = pd.DataFrame(columns=["category", "pattern", "score"])

# Chat loop
for category, pattern, test_instance in test_instances():
    if isinstance(test_instance, TestInstance):

        question = test_instance.question()
        print_input_message(question)

        response = agent.invoke(
            {"input": question},
            # This is needed because in most real world scenarios, a session id is needed
            # It isn't really used here because we are using a simple in memory ChatMessageHistory
            config={"configurable": {"session_id": "<foo>"}},
        )

        answer = response['output']
        print_result(answer)

        metric = test_instance.check_answer(answer)
        print(f"Answer correctness: {metric:.3f}\n")

        results.loc[len(results.index)] = [category, pattern, metric]

    elif callable(test_instance):  # helper function
        test_instance()
    else:
        raise ValueError(f"Unsupported test instance type: {test_instance}")


print("\nEnd of test.\n")

print("Total test instances:", len(results.index))

results_path = sys.stdout.file_name.replace(".ansi", ".csv")  # FIXME: this is ugly and depends on the implementation of Logger
results.to_csv(results_path, index=False)

pattern_results = results.groupby(by="pattern").agg({"category": pd.Series.mode, "score": "mean"})
pattern_results['count'] = results.groupby(by="pattern").size()
pattern_results.to_csv(results_path.replace(".csv", "_patterns.csv"), index=True)

category_results = results.groupby(by="category").agg({"score": "mean"})
category_results['count'] = results.groupby(by="category").size()
category_results.to_csv(results_path.replace(".csv", "_categories.csv"), index=True)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(pattern_results)
    print()
    print(category_results)
