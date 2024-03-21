"""
A LLM-based Agent, all tools are faked and require a human to respond.
"""

import sys
from pathlib import Path

from colorama import Style
from dotenv import find_dotenv, load_dotenv
from langchain.tools import tool
from langchain_community.callbacks import get_openai_callback
import yaml

from helpers import LOGGER_FOLDER, MAIN_WORKFLOW, MAIN_WORKFLOW_PACKAGE, MODEL, SPECIFICATION_FOLDER, SPECIFICATION_TYPE, Logger, multiline_input, print_color, print_token_usage, print_prompt_template, \
    print_available_tools, print_input_message, print_result, RESULTS_FOLDER, SpecificationType
from agent import create_agent, create_llm
from results_tools import ListResultFilesTool, FileDescriptionTool, CSVFileReadTool
import xxp_dsl_tools
import yaml_tools
import xxp_dsl_tools_assembled

load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.

PROJECT_DIR = Path(__file__).parent.parent  # root of the repository

# Load configuration file

config_file_path = input("Configuration file path: ")
config = yaml.load((PROJECT_DIR / config_file_path).open(), Loader=yaml.Loader)

# Create Logger

sys.stdout = Logger(PROJECT_DIR / config.get(LOGGER_FOLDER, "xxp_agent_logs"))

print("Configuration file path:", config_file_path)
print("Configuration:", config)

# Create LLM

llm = create_llm(model=config.get(MODEL, "gpt-3.5-turbo"))
tools = []

# Tools

# TODO: update
@tool
def workflow_data_schema(schema_file_name: str) -> str:
    """Read the schema of data referenced in workflow specification."""
    return multiline_input()

# tools.append(workflow_data_schema)

# result files tools

if RESULTS_FOLDER in config:
    tools += [
        ListResultFilesTool(config[RESULTS_FOLDER]),
        FileDescriptionTool(config[RESULTS_FOLDER]),
        CSVFileReadTool(config[RESULTS_FOLDER])
    ]

# Main

print_color("This script uses multiline input. Press Ctrl+D (Linux) or Ctrl+Z (Windows) on an empty line to end input message.", Style.DIM)

if config[SPECIFICATION_TYPE] == SpecificationType.XXP:
    prompt = xxp_dsl_tools.get_prompt_template(config[MAIN_WORKFLOW], config[MAIN_WORKFLOW_PACKAGE])
    tools.append(xxp_dsl_tools.DSLWorkflowSpecificationTool(PROJECT_DIR / config[SPECIFICATION_FOLDER]))
elif config[SPECIFICATION_TYPE] == SpecificationType.YAML:
    prompt = yaml_tools.get_prompt_template(config[MAIN_WORKFLOW])
    tools.append(yaml_tools.YAMLWorkflowSpecificationTool(PROJECT_DIR / config[SPECIFICATION_FOLDER]))
elif config[SPECIFICATION_TYPE] == SpecificationType.XXP_ASSEMBLED:
    prompt = xxp_dsl_tools_assembled.get_prompt_template(config[MAIN_WORKFLOW])
    tools.append(xxp_dsl_tools_assembled.DSLAssembledWorkflowSpecificationTool(PROJECT_DIR / config[SPECIFICATION_FOLDER]))

agent, message_history = create_agent(llm, tools, prompt)

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
