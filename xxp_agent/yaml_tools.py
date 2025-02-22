from pathlib import Path
from typing import Type, Any, Optional

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field

from helpers import MEMORY_KEY, AGENT_SCRATCHPAD


def get_prompt_template(main_workflow_name):
    # based on https://smith.langchain.com/hub/hwchase17/openai-tools-agent and modified
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""\
Your goal is to help the user with analyzing results of an experiment and suggest improvements to the experiment itself.

The experiment is defined by a workflow, which is an activity diagram consisting of several tasks with a data flow among them. Each of the tasks can be composed of a subworkflow so to fully understand the whole workflow, it is necessary to also read the specification of the subworkflows (use the available tools to obtain it).

Think in steps and use the available tools. Use the tools if you need a description of a workflow (or subworkflow), list the results collected during the experiment, etc. If the information cannot be obtained using the tools, ask the user. Always gather all the necessary information before submitting your final answer.
"""),
        HumanMessagePromptTemplate.from_template(f"Experiment workflow: '{main_workflow_name}'\n"),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name=AGENT_SCRATCHPAD),
    ])
    return prompt


class YAMLWorkflowSpecificationTool(BaseTool):

    class ArgsSchema(BaseModel):
        workflow_name: str = Field(description="Name of the workflow.")

    name: str = "workflow_specification"
    args_schema: Type[BaseModel] = ArgsSchema
    description = "Get the specification of the workflow (or subworkflow) in YAML. Note that the workflow specification can contain references to subworkflows. To fully understand the whole workflow, it might be necessary to also obtain the specification of the subworkflows."

    specification_folder: Optional[Path]

    def __init__(self, specification_folder, **kwargs: Any):
        super().__init__(**kwargs)
        self.specification_folder = Path(specification_folder)

    def _run(self, workflow_name: str, run_manager=None) -> str:
        workflow_path = self.specification_folder / f"{workflow_name}.yaml"
        if not workflow_path.exists():
            available_workflows = [workflow.stem for workflow in self.specification_folder.glob("*.yaml")]
            return f"Error: workflow '{workflow_name}' not found. Available workflows: {available_workflows}"

        return workflow_path.read_text()


def list_workflows(specification_folder):
    workflows = [workflow.stem for workflow in specification_folder.glob("*.yaml")]
    return workflows
