from langchain_core.tools import tool, BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field

from helpers import BaseFileTool, FileValidationError


class ListResultFilesTool(BaseFileTool, BaseTool):
    """Tool that lists experiment results."""

    class ArgsSchema(BaseModel):
        pass

    name = "list_results_files"
    args_schema = ArgsSchema
    description = 'Lists the files in the results directory with their descriptions. The output is one file per line formatted "path: description".'

    def _run(self, run_manager=None) -> str:
        result = []
        for file in self.root_folder.glob("**/*.xxpa"):
            path = str(file.relative_to(self.root_folder))
            path = path[:-5]  # remove ".xxpa"

            with file.open() as f:
                description = f.readline().strip()

            result.append(f"{path}: {description}\n")

        return "".join(result)


# TODO (optional): force the LLM to read the description before reading file
class FileDescriptionTool(BaseFileTool, BaseTool):
    """Tool that reads a description of a file."""

    class ArgsSchema(BaseModel):
        file_path: str = Field(description="Path to the file")

    name = "get_file_description"
    args_schema = ArgsSchema
    description = "Returns the description of the file. You should read the description of a file before reading the file itself."

    def _run(self, file_path: str, run_manager=None) -> str:
        description_path = file_path + ".xxpa"
        try:
            read_path = self.get_validated_relative_path(description_path)
            return read_path.read_text()

        except FileValidationError:
            return f"Error: Access denied to: {file_path}. Permission granted exclusively to the current working directory"
        except FileNotFoundError:
            return f"Error: file '{file_path}' does not exist in experiment results"
        except Exception as e:
            return "Error: " + str(e)


class CSVFileReadTool(BaseFileTool, BaseTool):
    """Tool that reads a file."""

    class ArgsSchema(BaseModel):
        file_path: str = Field(description="Path to the CSV file")

    name = "read_csv_file"
    args_schema = ArgsSchema
    # description = "Read the first and last 5 rows of a CSV file"
    description = "Read the CSV file"

    def _run(self, file_path: str, run_manager=None) -> str:
        try:
            read_path = self.get_validated_relative_path(file_path)
            with read_path.open("r", encoding="utf-8") as file:
                content = file.readlines()
            # return "".join(content[:6] + ["...\n"] + content[-5:])
            return "".join(content[:20])  # prevent reading too much  TODO: how to handle this?

        except FileValidationError:
            return f"Error: Access denied to: {file_path}. Permission granted exclusively to the current working directory"
        except FileNotFoundError:
            return f"Error: file '{file_path}' does not exist in experiment results"
        except Exception as e:
            return "Error: " + str(e)
