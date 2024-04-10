from pathlib import Path
import yaml

from helpers import MAIN_WORKFLOW, MAIN_WORKFLOW_PACKAGE, SPECIFICATION_FOLDER, SPECIFICATION_TYPE, SpecificationType
import xxp_dsl_tools
import yaml_tools
import xxp_dsl_tools_assembled


def load_config(config_file_path: Path):
    return yaml.load(config_file_path.open(), Loader=yaml.Loader)


def get_prompt_template(config, **kwargs):
    if config[SPECIFICATION_TYPE] == SpecificationType.XXP:
        return xxp_dsl_tools.get_prompt_template(config[MAIN_WORKFLOW], config[MAIN_WORKFLOW_PACKAGE], **kwargs)
    elif config[SPECIFICATION_TYPE] == SpecificationType.YAML:
        return yaml_tools.get_prompt_template(config[MAIN_WORKFLOW], **kwargs)
    elif config[SPECIFICATION_TYPE] == SpecificationType.XXP_ASSEMBLED:
        return xxp_dsl_tools_assembled.get_prompt_template(config[MAIN_WORKFLOW], **kwargs)
    raise ValueError("Unsupported specification type: " + config[SPECIFICATION_TYPE])

def get_specification_tools(config, project_dir: Path):
    if config[SPECIFICATION_TYPE] == SpecificationType.XXP:
        return xxp_dsl_tools.DSLWorkflowSpecificationTool(project_dir / config[SPECIFICATION_FOLDER])
    elif config[SPECIFICATION_TYPE] == SpecificationType.YAML:
        return yaml_tools.YAMLWorkflowSpecificationTool(project_dir / config[SPECIFICATION_FOLDER])
    elif config[SPECIFICATION_TYPE] == SpecificationType.XXP_ASSEMBLED:
        return xxp_dsl_tools_assembled.DSLAssembledWorkflowSpecificationTool(project_dir / config[SPECIFICATION_FOLDER])
    raise ValueError("Unsupported specification type: " + config[SPECIFICATION_TYPE])
