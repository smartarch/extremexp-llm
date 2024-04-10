from pathlib import Path
from typing import Type, Any, Optional

from langchain_core.messages import SystemMessage, BaseMessage
from langchain_core.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field

from helpers import MEMORY_KEY, AGENT_SCRATCHPAD


def get_prompt_template(main_workflow_name, main_workflow_package, with_memory=True, with_main=True):
    # based on https://smith.langchain.com/hub/hwchase17/openai-tools-agent and modified
    messages = [
        SystemMessage(content="""\
Your goal is to help the user with analyzing results of an experiment and suggest improvements to the experiment itself.

The experiment is defined by a workflow, which is an activity diagram consisting of several tasks with a data flow among them. Each of the tasks can be composed of a subworkflow and you can use tools to obtain the specification of the subworkflow.

The workflow is specified using a DSL:
arrows "->" represent control flow
arrows with question mark “?->” represent conditional control flow
dashed arrows "-->" represent data flow

A workflow can be derived from another workflow, which is denoted by the "from" keyword. When working with a derived workflow, always obtain the specification of the base workflow as it is necessary to fully understand the derived workflow.

Think in steps and use the available tools. Use the tools if you need specification of a workflow or a task, list the results collected during the experiment, etc. If the information cannot be obtained using the tools, ask the user. Always gather all the necessary information before submitting your final answer.
"""),
    ]

    if with_main:
        messages.append(HumanMessagePromptTemplate.from_template(f"Experiment workflow: '{main_workflow_name}' from package '{main_workflow_package}'\n"))

    if with_memory:
        messages.append(MessagesPlaceholder(variable_name=MEMORY_KEY))
    
    messages += [
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name=AGENT_SCRATCHPAD),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)
    return prompt

class DSLWorkflowSpecificationTool(BaseTool):

    class ArgsSchema(BaseModel):
        package_name: str = Field(description="Name of the package.")
        workflow_name: str = Field(description="Name of the workflow in the given package.")

    name: str = "workflow_specification"
    args_schema: Type[BaseModel] = ArgsSchema
    description = "Get the specification of the workflow (or subworkflow). Note that the workflow specification can contain references to subworkflows and parent workflows. To fully understand the whole workflow, it might be necessary to also obtain the specification of the subworkflows and parent workflows."

    specification_folder: Optional[Path]

    def __init__(self, specification_folder, **kwargs: Any):
        super().__init__(**kwargs)
        self.specification_folder = Path(specification_folder)

    def _run(self, package_name: str, workflow_name: str, run_manager=None) -> str:
        packages = [package.name for package in self.specification_folder.glob("*") if package.is_dir()]
        if package_name not in packages:
            return f"Error: package '{package_name}' not found. Available packages: {packages}"

        package_path = self.specification_folder / package_name
        workflow_path = package_path / f"{workflow_name}.xxp"
        if not workflow_path.exists():
            available_workflows = [workflow.stem for workflow in package_path.glob("*.xxp")]
            return f"Error: workflow '{workflow_name}' not found in package '{package_name}'. Available workflows: {available_workflows}"

        return workflow_path.read_text()


def list_workflows(specification_folder):
    packages = [package.name for package in specification_folder.glob("*") if package.is_dir()]
    workflows = [f"{package}.{workflow.stem}" for package in packages for workflow in package.glob("*.xxp")]
    return workflows
