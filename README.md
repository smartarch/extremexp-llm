# extremexp-llm

## Quickstart

1. (Optional): create virtual environment: `python3 -m venv .venv` and activate it: `source env/bin/activate`
2. install requirements: `pip install -r requirements.txt`

To use OpenAI (paid API):

* create API key: <https://platform.openai.com/api-keys>
* rename `.env.example` to `.env` and save the API key there

### Not used anymore

To use Ollama (local free models):

* `curl -fsSL https://ollama.com/install.sh | sh`
* Fetch a model: `ollama pull llama2` (3.8GB)

## [`agent_with_fake_tools.py`](agent_with_fake_tools.py)

Simple chat with an LLM-based agent. The tools are not implemented, they are instead redirected to the human input. The input is multiline, Press Ctrl+D (Linux) or Ctrl+Z (Windows) on an empty line to end it. To close the chat, end the script (Ctrl+C).

Logs of the conversation are stored in [`agent_with_fake_tools_logs`](agent_with_fake_tools_logs/) (not stored in git). The logs contain ANSI formatting characters for colors, to read them properly, either `cat` them or use a [VS Code extension](https://marketplace.visualstudio.com/items?itemName=iliazeus.vscode-ansi).

## IDEKO AutoML example

Partial implementation of AutoML workflow. The goal is to try several ML models. The results of this workdlow can then be consulted with the LLM agent to choose the best model.

1. navigate to [`example/ideko`](examples/ideko/): `cd examples/ideko`
2. install requirements: `pip install -r requirements.txt`
3. rename `.env.example` to `.env` and set the `IDEKO_DATA_FOLDER` (obtain the data from [GitLab](https://colab-repo.intracom-telecom.com/colab-projects/extremexp/uc-data/uc5-ideko/failure-prediction-in-manufacture/))
4. run [`extract_ideko_data.py`](examples/ideko/extract_ideko_data.py) to extract the data from ZIP files and also extract only a subset of features from the data (this is to simplify and speedup the AutoML, in a real ExtremeXP experiment, this extraction might be part of the experiment workflow)
