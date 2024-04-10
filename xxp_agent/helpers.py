import enum
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from colorama import Style, Fore
from langchain_core.pydantic_v1 import BaseModel


class Logger:
    """Prints the stdout simultaneously to the terminal and a file."""
    def __init__(self, logs_dir: Path):
        self.stdout = sys.stdout
        os.makedirs(logs_dir, exist_ok=True)
        self.file_name = f'{logs_dir}/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.ansi'
        self.file = open(self.file_name, "w")

    def write(self, message):
        self.stdout.write(message)
        self.file.write(message)

    def flush(self):
        pass  # do nothing


def multiline_input() -> str:
    result = ""
    while True:
        try:
            line = input()
            result += line + "\n"
        except EOFError:
            break
    return result


def print_color(message, color):
    print(color)
    print(message)
    print(Style.RESET_ALL)


def print_token_usage(token_counter):
    return  # this does not work as expected when the LLM is streaming (which it does when run inside agent)
    print()
    print_color(token_counter, Style.DIM)


def print_prompt_template(prompt):
    print("Prompt template:")
    print_color("\n".join(
        repr(message) for message in prompt.messages
    ), Fore.MAGENTA)


def print_available_tools(tools):
    print("Tools:")
    print_color("\n".join(
        f"{tool.name}: {tool.description}" for tool in tools
    ), Fore.MAGENTA)


def print_input_message(message):
    print("User input:")
    print_color(message, Fore.MAGENTA)


def print_result(message):
    print("Agent reply:")
    print_color(message, Fore.CYAN)


def fake_tool(input: str) -> str:
    response = multiline_input()
    return response


class BaseFileTool(BaseModel):
    """Sets root directory for listing files. Based on BaseFileToolMixin (https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/tools/file_management/utils.py#L30C7-L30C24)."""

    root_folder: Path = None

    def __init__(self, root_folder, **kwargs: Any):
        super().__init__(**kwargs)
        self.root_folder = Path(root_folder)

    def get_validated_relative_path(self, path: str) -> Path:
        """Resolve a relative path, raising an error if it is not within the root directory or it doesn't exist."""
        root = self.root_folder.resolve()
        full_path = (root / path).resolve()

        if not full_path.is_relative_to(root):
            raise FileValidationError()
        if not full_path.exists():
            raise FileNotFoundError()
        return full_path


class FileValidationError(ValueError):
    """Error for paths outside the root directory."""


MEMORY_KEY = "chat_history"
AGENT_SCRATCHPAD = "agent_scratchpad"
RESULTS_FOLDER = "results_folder"
SPECIFICATION_TYPE = "specification_type"
SPECIFICATION_FOLDER = "specification_folder"
LOGGER_FOLDER = "logger_folder"
MODEL = "model"
MAIN_WORKFLOW = "main_workflow_name"
MAIN_WORKFLOW_PACKAGE = "main_workflow_package"

class SpecificationType(str, enum.Enum):
    XXP = "xxp"
    XXP_ASSEMBLED = "xxp_assembled"
    YAML = "yaml"
