from pathlib import Path
import sys

sys.path.append(str((Path(__file__).parent / ".." / "xxp_agent" ).resolve()))  # dirty trick to allow importing python files from the 'xxp_agent' folder

from colorama import Style
from dotenv import find_dotenv, load_dotenv

from helpers import LOGGER_FOLDER, MODEL, Logger, print_color, print_prompt_template, \
    print_available_tools, print_input_message, print_result
from agent import create_agent, create_llm
from config import get_prompt_template, get_specification_tools, load_config

from test_instance_templates import SetQuestion, YesNoQuestion

load_dotenv(find_dotenv(), override=True)  # take environment variables from .env.

PROJECT_DIR = Path(__file__).parent.parent  # root of the repository

# Load configuration file

# config_file_path = input("Configuration file path: ")
config_file_path = "examples/artificial_workflow/2_config.yaml"
config = load_config(PROJECT_DIR / config_file_path)

# Create Logger

sys.stdout = Logger(PROJECT_DIR / "questions_generator_logs")

print("Configuration file path:", config_file_path)
print("Configuration:", config)

# Create LLM

llm = create_llm(model=config.get(MODEL, "gpt-3.5-turbo"))

# Tools

tools = []
tools.append(get_specification_tools(config, PROJECT_DIR))

# Test instances

test_instances = [
    YesNoQuestion("In workflow 'SubWorkflow', does 'Task9' follow directly after 'Task10' in the control flow?", True),
    YesNoQuestion("In workflow 'SubWorkflow', does 'Task10' follow directly after 'Task9' in the control flow?", False),
    SetQuestion("List all tasks in workflow 'MainWorkflow'.", {"Task1", "Task2", "Task3", "Task4"}),
    SetQuestion("List all tasks in workflow 'MainWorkflow' that have a subworkflow.", {"Task1", "Task4"}),
]

# Main

print_color("This script uses multiline input. Press Ctrl+D (Linux) or Ctrl+Z (Windows) on an empty line to end input message.", Style.DIM)

prompt = get_prompt_template(config, with_memory=False)
agent = create_agent(llm, tools, prompt)

print_prompt_template(prompt)
print_available_tools(tools)

print("\nStart of test.\n")

results = []

# Chat loop
for test_instance in test_instances:
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

    results.append(metric)


print("\nEnd of test.\n")

print("Total test instances:", len(test_instances))
print(f"Final result: {sum(results) / len(results):.3f}")
