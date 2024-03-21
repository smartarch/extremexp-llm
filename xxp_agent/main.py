"""
A LLM-based Agent, all tools are faked and require a human to respond.
"""

import sys
from pathlib import Path

from colorama import Style
from dotenv import find_dotenv, load_dotenv
from langchain.tools import tool
from langchain_community.callbacks import get_openai_callback

from helpers import Logger, multiline_input, print_color, print_token_usage, print_prompt_template, \
    print_available_tools, print_input_message, print_result
from agent import create_agent, create_llm
from results_tools import ListResultFilesTool, FileDescriptionTool, CSVFileReadTool
import xxp_dsl_tools
import yaml_tools
import xxp_dsl_tools_assembled

load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.

PROJECT_DIR = Path(__file__).parent.parent  # root of the repository

AUTOML_RESULTS_FOLDER = PROJECT_DIR / "examples" / "predictive_maintenance" / "results"
YAML = False  # TODO: better management of configurations


sys.stdout = Logger(PROJECT_DIR / "xxp_agent_logs" / "automl_wrong_implementation")

llm = create_llm(model="gpt-3.5-turbo")  # model="gpt-4-0125-preview"
tools = []

# Tools


# TODO: update
@tool
def workflow_data_schema(schema_file_name: str) -> str:
    """Read the schema of data referenced in workflow specification."""
    return multiline_input()


# tools.append(workflow_data_schema)

# result files tools

# tools += [ListResultFilesTool(AUTOML_RESULTS_FOLDER), FileDescriptionTool(AUTOML_RESULTS_FOLDER), CSVFileReadTool(AUTOML_RESULTS_FOLDER)]

# Main

print_color("This script uses multiline input. Press Ctrl+D (Linux) or Ctrl+Z (Windows) on an empty line to end input message.", Style.DIM)

main_workflow_name = "FailurePredictionInManufacture"


# DSL
# prompt = xxp_dsl_tools.get_prompt_template(main_workflow_name, "automl_ideko")
# # tools.append(xxp_dsl_tools.DSLWorkflowSpecificationTool(PROJECT_DIR / "examples/automl_wrong_implementation/1_separate_files"))
# tools.append(xxp_dsl_tools.DSLWorkflowSpecificationTool(PROJECT_DIR / "examples/automl_wrong_implementation/4_separate_files_descriptions"))
# # YAML
# prompt = yaml_tools.get_prompt_template(main_workflow_name)
# tools.append(yaml_tools.YAMLWorkflowSpecificationTool(PROJECT_DIR / "examples/automl_wrong_implementation/2_yaml_descriptions"))
# DSL assembled
prompt = xxp_dsl_tools_assembled.get_prompt_template(main_workflow_name)
# tools.append(xxp_dsl_tools_assembled.DSLAssembledWorkflowSpecificationTool(PROJECT_DIR / "examples/automl_wrong_implementation/3_assembled"))
tools.append(xxp_dsl_tools_assembled.DSLAssembledWorkflowSpecificationTool(PROJECT_DIR / "examples/automl_wrong_implementation/5_assembled_descriptions"))

agent = create_agent(llm, tools, prompt)

print_prompt_template(prompt)
print_available_tools(tools)

print("\nStart of chat.\n")

# Chat loop
while True:
    message = multiline_input()
    if message == "":
        break

    with get_openai_callback() as token_counter:
        print_input_message(message)

        result = agent.invoke(
            {"input": message},
            # This is needed because in most real world scenarios, a session id is needed
            # It isn't really used here because we are using a simple in memory ChatMessageHistory
            config={"configurable": {"session_id": "<foo>"}},
        )

        print_result(result['output'])

        print_token_usage(token_counter)
