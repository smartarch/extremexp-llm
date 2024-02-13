# extremexp-llm

## Quickstart

1. (Optional): create virtual environment: `python3 -m venv .venv` and activate it: `source env/bin/activate`
2. install requirements: `pip install -r requirements.txt`

To use Ollama (local free models):

* `curl -fsSL https://ollama.com/install.sh | sh`
* Fetch a model: `ollama pull llama2` (3.8GB)

To use OpenAI (paid API):

* create API key: <https://platform.openai.com/api-keys>
* rename `.env.example` to `.env` and save the API key there
