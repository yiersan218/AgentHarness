"""A single-node LangGraph agent."""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph

from agent_harness.config import Settings

SYSTEM_PROMPT = "You are a helpful AI assistant. Answer clearly and concisely."


def create_model(settings: Settings) -> ChatOpenAI:
    """Create an OpenAI-compatible chat model."""

    model_options: dict[str, object] = {
        "model": settings.model_name,
        "api_key": settings.api_key,
    }
    if settings.base_url:
        model_options["base_url"] = settings.base_url
    return ChatOpenAI(**model_options)


def build_agent(model: BaseChatModel):
    """Compile the smallest useful LangGraph conversation graph."""

    def call_model(state: MessagesState) -> dict[str, list]:
        response = model.invoke([SystemMessage(content=SYSTEM_PROMPT), *state["messages"]])
        return {"messages": [response]}

    graph = StateGraph(MessagesState)
    graph.add_node("model", call_model)
    graph.add_edge(START, "model")
    graph.add_edge("model", END)
    return graph.compile()
