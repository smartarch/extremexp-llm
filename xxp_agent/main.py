"""
A LLM-based Agent, all tools are faked and require a human to respond.
"""

import sys
from pathlib import Path

from colorama import Style
from dotenv import find_dotenv, load_dotenv
from langchain.tools import tool
from langchain_community.callbacks import get_openai_callback

from helpers import LOGGER_FOLDER, MODEL, Logger, multiline_input, print_color, print_token_usage, print_prompt_template, \
    print_available_tools, print_input_message, print_result, RESULTS_FOLDER
from agent import add_memory_to_agent, create_agent, create_llm
from results_tools import ListResultFilesTool, FileDescriptionTool, CSVFileReadTool
from config import get_prompt_template, get_specification_tools, load_config

load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.

PROJECT_DIR = Path(__file__).parent.parent  # root of the repository

# Load configuration file

config_file_path = input("Configuration file path: ")
config = load_config(PROJECT_DIR / config_file_path)

# Create Logger

sys.stdout = Logger(PROJECT_DIR / config.get(LOGGER_FOLDER, "xxp_agent_logs"))

print("Configuration file path:", config_file_path)
print("Configuration:", config)

# Create LLM

llm = create_llm(model=config.get(MODEL, "gpt-3.5-turbo"))

# Tools

tools = []

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

tools.append(get_specification_tools(config, PROJECT_DIR))

# Main

print_color("This script uses multiline input. Press Ctrl+D (Linux) or Ctrl+Z (Windows) on an empty line to end input message.", Style.DIM)

prompt = get_prompt_template(config)
agent = create_agent(llm, tools, prompt)
agent, message_history = add_memory_to_agent(agent)

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
