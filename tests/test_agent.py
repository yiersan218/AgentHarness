from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import HumanMessage

from agent_harness.agent import build_agent


def test_agent_returns_model_response() -> None:
    agent = build_agent(FakeListChatModel(responses=["hello"]))

    result = agent.invoke({"messages": [HumanMessage(content="hi")]})

    assert [message.content for message in result["messages"]] == ["hi", "hello"]


def test_history_can_be_passed_into_the_next_turn() -> None:
    agent = build_agent(FakeListChatModel(responses=["first", "second"]))
    first = agent.invoke({"messages": [HumanMessage(content="one")]})

    history = [*first["messages"], HumanMessage(content="two")]
    second = agent.invoke({"messages": history})

    assert [message.content for message in second["messages"]] == [
        "one",
        "first",
        "two",
        "second",
    ]
