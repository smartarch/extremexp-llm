from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from helpers import MEMORY_KEY


def create_llm(model="gpt-3.5-turbo"):
    print("LLM model:", model, "\n")
    llm = ChatOpenAI(model=model)
    return llm


def create_agent(llm, tools, prompt):
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10, return_intermediate_steps=True)  # TODO: max_iterations are for debugging, we can increase it or change to max_execution_time later

    message_history = ChatMessageHistory()

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        # This is needed because in most real world scenarios, a session id is needed
        # It isn't really used here because we are using a simple in memory ChatMessageHistory
        lambda session_id: message_history,
        input_messages_key="input",
        history_messages_key=MEMORY_KEY,
    )

    return agent_with_chat_history
