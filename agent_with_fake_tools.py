"""
A LLM-based Agent, all tools are faked and require a human to respond.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Type

from colorama import Fore, Style
from dotenv import find_dotenv, load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import StructuredTool, tool
from langchain_community.callbacks import get_openai_callback
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.tools.file_management.utils import INVALID_PATH_TEMPLATE, BaseFileToolMixin, FileValidationError
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.


AUTOML_RESULTS_FOLDER = Path(__file__).parent / "examples" / "predictive_maintenance" / "results"


########## Helpers ##########

class Logger:
    """Prints the stdout simultaneously to the terminal and a file."""
    def __init__(self):
        self.stdout = sys.stdout
        self.file = open(f'agent_with_fake_tools_logs/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.ansi', "w")
   
    def write(self, message):
        self.stdout.write(message)
        self.file.write(message)

    def flush(self):
        pass  # do nothing

sys.stdout = Logger()

def multiline_input() -> str:
    result = ""
    while True:
        try:
            line = input()
            result += line + "\n"
        except EOFError:
            break
    return result

def print_token_usage(token_counter):
    return  # this does not work as expected when the LLM is streaming (which it does when run inside agent)
    print()
    print(Style.DIM)
    print(token_counter)
    print(Style.RESET_ALL)

def print_prompt_template(prompt):
    print("Prompt template:")
    print(Fore.MAGENTA)
    for message in prompt.messages:
        print(repr(message))
    print(Style.RESET_ALL)

def print_available_tools(tools):
    print("Tools:")
    print(Fore.MAGENTA)
    for tool in tools:
        print(tool.name, tool.description, sep=": ")
    print(Style.RESET_ALL)

def print_main_workflow(message):
    print(Fore.MAGENTA)
    print(message)
    print(Style.RESET_ALL)

def print_input_message(message):
    print("User input:")
    print(Fore.MAGENTA)
    print(message)
    print(Style.RESET_ALL)

def print_result(message):
    print("Agent reply:")
    print(Fore.CYAN)
    print(message)
    print(Style.RESET_ALL)


########## Prompt ##########

MEMORY_KEY = "chat_history"

# based on https://smith.langchain.com/hub/hwchase17/openai-tools-agent and modified
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="""Your goal is to help the user with analyzing results of an experiment and suggest improvements to the experiment itself.

The experiment workflow is an activity diagram consisting of several tasks with a data flow among them. Each of the tasks can be composed of a sub-workflow and you can use tools to obtain the description of the sub-workflow.

The workflow is described using a DSL:
arrows "->" represent control flow
arrows with question mark “?->” represent conditional control flow
dashed arrows "-->" represent data flow

The workflow can be derived from another workflow, which is denoted by the “from” keyword. Use the tools to obtain the description of the original workflow.

You can use the tools and ask the user if you need additional information about a task, results collected during the experiment, etc. Be specific with your questions and include all the necessary information to answer them.
"""),
    HumanMessagePromptTemplate.from_template("Description of {main_workflow_name}:\n{main_workflow}\nEnd of description."),
    MessagesPlaceholder(variable_name=MEMORY_KEY),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


########## LLM ##########

llm = ChatOpenAI(model="gpt-3.5-turbo")


########## Tools ##########

# Define the fake tools
# (later, for real tools, it will be more comfortable to use the @tool decorator, see https://python.langchain.com/docs/modules/agents/tools/custom_tools)
def fake_tool(input: str) -> str:
    response = multiline_input()
    return response

# fake tools names and descriptions
TOOLS = {
    # "workflow_tasks": "Get the description of the workflow tasks.",
    # "results_schema": "Get the names of the columns of the table with results.",
}
tools = [
    StructuredTool.from_function(
        func=fake_tool, name=name, description=description,
    ) for name, description in TOOLS.items()
]

# workflow description tool

@tool
def workflow_description(workflow_name: str) -> str:
    """Get the description of the workflow with the given name."""
    return fake_tool(workflow_name)

tools += [workflow_description]

# result files tools

@tool
def list_results_directory() -> str:
    """Lists the files in the results directory."""
    return "\n".join(
        str(file.relative_to(AUTOML_RESULTS_FOLDER))
        for file in AUTOML_RESULTS_FOLDER.glob("**/*.csv")
    ) + "\n"

tools += [list_results_directory]


class CSVFileReadTool(BaseFileToolMixin, BaseTool):
    """Tool that reads a file. Based on https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/tools/file_management/read.py"""

    class CSVFileReadToolInput(BaseModel):
        file_path: str = Field(..., description="Path to the CSV file")

    name: str = "read_csv_file"
    args_schema: Type[BaseModel] = CSVFileReadToolInput
    description: str = "Read the first and last 5 rows of a CSV file"

    def _run(self, file_path: str, run_manager=None) -> str:
        try:
            read_path = self.get_relative_path(file_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(arg_name="file_path", value=file_path)
        if not read_path.exists():
            return f"Error: no such file or directory: {file_path}"
        try:
            with read_path.open("r", encoding="utf-8") as file:
                content = file.readlines()
            return "".join(content[:6] + ["...\n"] + content[-5:])
        except Exception as e:
            return "Error: " + str(e)
        
read_csv_file_tool = CSVFileReadTool()
read_csv_file_tool.root_dir = str(AUTOML_RESULTS_FOLDER)
tools += [read_csv_file_tool]


########## Agent ##########

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)  # TODO: max_iterations are for debugging, we can increase it or change to max_execution_time later

message_history = ChatMessageHistory()
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key=MEMORY_KEY,
)


########## Main ##########
print(f"{Style.DIM}This script uses multiline input. Press Ctrl+D (Linux) or Ctrl+Z (Windows) on an empty line to end input message.{Style.RESET_ALL}\n")

print_prompt_template(prompt)
print_available_tools(tools)

print("\nEnter main workflow name:")
main_workflow_name = input()
print_main_workflow(main_workflow_name)

print("\nEnter main workflow DSL:")
main_workflow = multiline_input()
print_main_workflow(main_workflow)

print("\nStart of chat.\n")

# Chat loop
while True:
    message = multiline_input()
    if message == "":
        break

    with get_openai_callback() as token_counter:
        print_input_message(message)

        result = agent_with_chat_history.invoke(
            {"input": message, "main_workflow_name": main_workflow_name, "main_workflow": main_workflow},
            # This is needed because in most real world scenarios, a session id is needed
            # It isn't really used here because we are using a simple in memory ChatMessageHistory
            config={"configurable": {"session_id": "<foo>"}},
        )

        print_result(result['output'])

        print_token_usage(token_counter)
