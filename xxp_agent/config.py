from pathlib import Path
import yaml

from helpers import MAIN_WORKFLOW, MAIN_WORKFLOW_PACKAGE, PROMPT_KWARGS, SPECIFICATION_FOLDER, SPECIFICATION_TYPE, SpecificationType
import xxp_dsl_tools
import yaml_tools
import xxp_dsl_tools_assembled


def load_config(config_file_path: Path):
    return yaml.load(config_file_path.open(), Loader=yaml.Loader)


def get_prompt_template(config, **kwargs):
    if config[SPECIFICATION_TYPE] == SpecificationType.XXP:
        if kwargs["all_xxp"]:
            del kwargs["all_xxp"]
            return xxp_dsl_tools.get_prompt_template_all_xxp(config[MAIN_WORKFLOW], config[MAIN_WORKFLOW_PACKAGE], **config.get(PROMPT_KWARGS, {}), **kwargs)
        return xxp_dsl_tools.get_prompt_template(config[MAIN_WORKFLOW], config[MAIN_WORKFLOW_PACKAGE], **config.get(PROMPT_KWARGS, {}), **kwargs)
    elif config[SPECIFICATION_TYPE] == SpecificationType.YAML:
        return yaml_tools.get_prompt_template(config[MAIN_WORKFLOW], **config.get(PROMPT_KWARGS, {}), **kwargs)
    elif config[SPECIFICATION_TYPE] == SpecificationType.XXP_ASSEMBLED:
        if kwargs["all_xxp"]:
            del kwargs["all_xxp"]
            return xxp_dsl_tools_assembled.get_prompt_template_all_xxp(config[MAIN_WORKFLOW], **config.get(PROMPT_KWARGS, {}), **kwargs)
        return xxp_dsl_tools_assembled.get_prompt_template(config[MAIN_WORKFLOW], **config.get(PROMPT_KWARGS, {}), **kwargs)
    raise ValueError("Unsupported specification type: " + config[SPECIFICATION_TYPE])

def get_specification_tools(config, project_dir: Path):
    if config[SPECIFICATION_TYPE] == SpecificationType.XXP:
        return xxp_dsl_tools.DSLWorkflowSpecificationTool(project_dir / config[SPECIFICATION_FOLDER])
    elif config[SPECIFICATION_TYPE] == SpecificationType.YAML:
        return yaml_tools.YAMLWorkflowSpecificationTool(project_dir / config[SPECIFICATION_FOLDER])
    elif config[SPECIFICATION_TYPE] == SpecificationType.XXP_ASSEMBLED:
        return xxp_dsl_tools_assembled.DSLAssembledWorkflowSpecificationTool(project_dir / config[SPECIFICATION_FOLDER])
    raise ValueError("Unsupported specification type: " + config[SPECIFICATION_TYPE])
