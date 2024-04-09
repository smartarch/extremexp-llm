# Understanding workflow architectures by LLMs

This is a replication package for the "Understanding workflow architectures by LLMs" paper submitted to ECSA 2024.

---

Full list of evaluation patterns: [`patterns.md](patterns.md)

## Quickstart

1. (Optional): create virtual environment: `python3 -m venv .venv` and activate it: `source env/bin/activate`
2. install requirements: `pip install -r requirements.txt`

To use OpenAI (paid API):

* create API key: <https://platform.openai.com/api-keys>
* rename `.env.example` to `.env` and save the API key there

## LLM Evaluation

The [`agent_evaluation`](agent_evaluation/) folder contains sample test instances for evaluating a LLM-based Agent. The instances are manually created based on the [*test instance patterns*](patterns.md). The evaluation can be run via the [`main.py`](xxp_agent/main.py) file.

## XXP Agent Chat

The [`xxp_agent`](xxp_agent/) folder contains code for running a LLM-based agent that chats with the user. Based on the configuration (see examples in the [`examples`](examples/) folder) the available tools are selected (so the agent can read workflow specifications, ...). To start the agent, run the [`main.py`](xxp_agent/main.py) file.
