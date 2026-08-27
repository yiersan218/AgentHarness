"""Command-line interface for the minimal agent."""

from __future__ import annotations

from langchain_core.messages import BaseMessage, HumanMessage

from agent_harness.agent import build_agent, create_model
from agent_harness.config import Settings

EXIT_COMMANDS = {"exit", "quit"}


def chat() -> None:
    """Run a process-local conversation loop."""

    settings = Settings.from_env()
    agent = build_agent(create_model(settings))
    history: list[BaseMessage] = []

    print("AgentHarness is ready. Type exit or quit to stop.")
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return

        if not user_input:
            continue
        if user_input.lower() in EXIT_COMMANDS:
            print("Bye!")
            return

        history.append(HumanMessage(content=user_input))
        result = agent.invoke({"messages": history})
        history = list(result["messages"])
        print(f"Agent: {history[-1].content}")


def main() -> None:
    try:
        chat()
    except ValueError as error:
        raise SystemExit(f"Configuration error: {error}") from error
