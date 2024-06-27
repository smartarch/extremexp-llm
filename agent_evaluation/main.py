from pathlib import Path
import sys
import time

sys.path.append(str((Path(__file__).parent / ".." / "xxp_agent" ).resolve()))  # dirty trick to allow importing python files from the 'xxp_agent' folder

from colorama import Style, Fore
from dotenv import find_dotenv, load_dotenv
import pandas as pd

from helpers import LOGGER_FOLDER, MODEL, SPECIFICATION_FOLDER, Logger, print_color, print_prompt_template, \
    print_available_tools, print_input_message, print_result
from agent import create_agent, create_llm
from config import get_prompt_template, get_specification_tools, load_config

from test_instance_templates import TestInstance

load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.

PROJECT_DIR = Path(__file__).parent.parent  # root of the repository

# Load configuration file

if len(sys.argv) == 2:
    variant = int(sys.argv[1])
else:
    # variant = 1  # separate files (inheritance)
    variant = 2  # assembled
    # variant = 3  # expanded
config_file_suffix = "_config.yaml"

config_file_path = f"examples/artificial_workflow/{variant}{config_file_suffix}"
config = load_config(PROJECT_DIR / config_file_path)

# Create Logger

sys.stdout = Logger(PROJECT_DIR / "agent_evaluation_logs" / "gpt_4o" / str(variant))

print("Configuration file path:", config_file_path)
print("Configuration:", config)

# Create LLM

llm = create_llm(model=config.get(MODEL, "gpt-4-0125-preview"))

# Tools

# TODO: Try feeding all the specifications to the LLM in the prompt (glob all the .xxp files). With current pricing, it should be reasonable. 

tools = []
specification_tool = get_specification_tools(config, PROJECT_DIR)
tools.append(specification_tool)

# FIXME: this is a hacky way to change the configuration folder, but it works for now
def update_specification_tool_path(folder_name):
    def update_specification_folder():
        if folder_name == "automl_wrong_implementation":
            config_file = str(variant + 3) + config_file_suffix  # FIXME: variants with descriptions are +3
        else:
            config_file = str(variant) + config_file_suffix
        new_config_path = f"examples/{folder_name}/{config_file}"
        new_config = load_config(PROJECT_DIR / new_config_path)
        new_specification_folder = PROJECT_DIR / new_config[SPECIFICATION_FOLDER]
        specification_tool.specification_folder = new_specification_folder
        print(f"Configuration: 'specification_folder' updated to {new_config[SPECIFICATION_FOLDER]}")
    return update_specification_folder


# Test instances

if variant == 1:
    from test_instances_separate_files import test_instances
elif variant == 2:
    from test_instances_assembled import test_instances
else:  # 3_config.yaml
    from test_instances_expanded import test_instances

# Main

print_color("This script uses multiline input. Press Ctrl+D (Linux) or Ctrl+Z (Windows) on an empty line to end input message.", Style.DIM)

prompt = get_prompt_template(config, with_memory=False, with_main=False)
agent = create_agent(llm, tools, prompt)

print_prompt_template(prompt)
print_available_tools(tools)

print("\nStart of test.\n")

results = pd.DataFrame(columns=["category", "pattern", "score"])

# Chat loop
start_time = time.time()
for category, pattern, test_instance in test_instances(update_specification_tool_path):
    if isinstance(test_instance, TestInstance):

        question = test_instance.question()

        print_color(f"Pattern: {pattern}", Fore.YELLOW)

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
end_time = time.time()

print("Total test instances:", len(results.index))
print(f"Test duration: {end_time - start_time:.2f} s, per instance: {(end_time - start_time) / len(results.index):.2f} s")

results_path = sys.stdout.file_name.replace(".ansi", ".csv")  # FIXME: this is ugly and depends on the implementation of Logger
results.to_csv(results_path, index=False)

pattern_results = results.groupby(by="pattern", sort=False).agg({"category": pd.Series.mode, "score": "mean"})
pattern_results['count'] = results.groupby(by="pattern", sort=False).size()
pattern_results.to_csv(results_path.replace(".csv", ".patterns.csv"), index=True)

category_results = results.groupby(by="category", sort=False).agg({"score": "mean"})
category_results['count'] = results.groupby(by="category", sort=False).size()
category_results.to_csv(results_path.replace(".csv", ".categories.csv"), index=True)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(pattern_results)
    print()
    print(category_results)
