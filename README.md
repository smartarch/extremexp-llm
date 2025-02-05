# Interpreting Workflow Architectures by LLMs

This is a replication package for the paper **Interpreting Workflow Architectures by LLMs** by *Michal Töpfer*, *Tomáš Bureš*, *František Plášil* and *Petr Hnětynka*.

## Test Patterns

[List of test patterns](patterns.md)

## Installation

1. (Optional): create virtual environment: `python3 -m venv .venv` and activate it: `source .venv/bin/activate`
2. install requirements: `pip install -r requirements.txt`

To use OpenAI (paid API):

* create API key: <https://platform.openai.com/api-keys>
* rename `.env.example` to `.env` and save the API key there

## LLM Evaluation

The [`agent_evaluation`](agent_evaluation/) folder contains sample test instances for evaluating a LLM-based Agent. The instances are manually created based on the [*test patterns*](patterns.md). The evaluation can be run via the [`main.py`](xxp_agent/main.py) file.

In the [`agent_evaluation/README.md`](agent_evaluation/README.md) file, the experimental results are summarized and discussed.

## XXP Agent Chat

The [`xxp_agent`](xxp_agent/) folder contains code for running a LLM-based agent that chats with the user. Based on the configuration (see examples in the [`examples`](examples/) folder) the available tools are selected (so the agent can read workflow specifications, ...). To start the agent, run the [`main.py`](xxp_agent/main.py) file.
