"""
A LLM-based Agent, all tools are faked and require a human to respond.
"""

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
# from langchain_community.callbacks import get_openai_callback
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.tools import StructuredTool
import sys
from datetime import datetime

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

print("This script uses multiline input. Press Ctrl+D (Linux) or Ctrl+Z (Windows) on an empty line to end it.")

def multiline_input() -> str:
    result = ""
    while True:
        try:
            line = input()
            result += line + "\n"
        except EOFError:
            break
    return result

load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.


MEMORY_KEY = "chat_history"

# based on https://smith.langchain.com/hub/hwchase17/openai-tools-agent and modified
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful assistant. You can use the provided tools to obtain additional information. If you need more information and there is no tool to do so, you can ask the user."),
    SystemMessage(content="Your goal is to help the user with analyzing results of an experiment."),
    MessagesPlaceholder(variable_name=MEMORY_KEY),
    HumanMessage(content="{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

llm = ChatOpenAI(model="gpt-3.5-turbo")


# Define the fake tools
# (later, for real tools, it will be more comfortable to use the @tool decorator, see https://python.langchain.com/docs/modules/agents/tools/custom_tools)
def fake_tool(input: str) -> str:
    response = multiline_input()
    return response

# fake tools names and descriptions
TOOLS = {
    "workflow_tasks": "Get the description of the workflow tasks.",
    "results_schema": "Get the names of the columns of the table with results.",
}
tools = [
    StructuredTool.from_function(
        func=fake_tool, name=name, description=description,
    ) for name, description in TOOLS.items()
]


# Create the agent
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


def chat():
    message = multiline_input()
    result = agent_with_chat_history.invoke(
        {"input": message},
        # This is needed because in most real world scenarios, a session id is needed
        # It isn't really used here because we are using a simple in memory ChatMessageHistory
        config={"configurable": {"session_id": "<foo>"}},
    )
    print(result['output'])


while True:
    chat()
