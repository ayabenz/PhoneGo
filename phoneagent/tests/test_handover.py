"""Hand the task to the user: ask_user, and the reply coming back.

Some steps cannot be guessed -- a password, which of two identical rows, or
permission before something irreversible. The agent asks, the task waits, and
the run continues with the answer in the next prompt.
"""

from __future__ import annotations

import threading
import time

from phoneagent.core.agent import AgentConfig, PhoneAgent
from phoneagent.core.llm import Choice, ToolCall
from phoneagent.devices.mock import MockDevice


class DictDevice(MockDevice):
    def dump_ui(self):
        return '<hierarchy><node text="Settings" bounds="[0,0][200,120]"/></hierarchy>'


class AskingLLM:
    """Asks, then finishes using whatever the user said."""

    def __init__(self):
        self._queue = [
            ("ask_user", {"question": "wantOpenBluetooth[CH] WLAN？"}),
            ("finish", {"message": "[CH]Select[CH]"}),
        ]
        self.prompts: list[str] = []

    def choose(self, system, user, image_png=None, tools=None, temperature=0.0):
        self.prompts.append(user)
        name, arguments = self._queue.pop(0)
        return Choice(call=ToolCall(name=name, arguments=arguments))


def _agent(device, llm, ask):
    return PhoneAgent(device, [], llm, config=AgentConfig(verify_with_vlm=False),
                      sleep=lambda _s: None, ask=ask)


def test_the_agent_asks_and_uses_the_reply():
    asked: list[str] = []

    def ask(question):
        asked.append(question)
        return "Bluetooth"

    llm = AskingLLM()
    result = _agent(DictDevice(), llm, ask).run("Open[CH]Settings")

    assert result.ok
    assert asked == ["wantOpenBluetooth[CH] WLAN？"]
    # the reply reaches the model on the next turn
    assert "The user just said this" in llm.prompts[1]
    assert "Bluetooth" in llm.prompts[1]


def test_without_a_reply_the_turn_is_recorded_and_the_run_continues():
    llm = AskingLLM()
    agent = _agent(DictDevice(), llm, lambda _q: None)

    result = agent.run("Open[CH]Settings")

    assert result.ok                       # the model finished anyway
    assert any("no reply" in line for line in agent.history)


def test_no_ask_channel_means_the_action_fails_cleanly():
    llm = AskingLLM()
    agent = _agent(DictDevice(), llm, None)
    result = agent.run("Open[CH]Settings")
    assert result.ok
    assert any("no one to ask" in line for line in agent.history)


# ---------------------------------------------------------------------------
# server side
# ---------------------------------------------------------------------------


def test_ask_publishes_the_question_and_returns_the_answer():
    from phoneagent import server as S

    task_id = "handover1"
    S.PENDING[task_id] = {"question": "", "answer": None, "event": threading.Event()}
    got: dict = {}

    t = threading.Thread(target=lambda: got.update(reply=S._ask(task_id, "[CH]？", 5.0)))
    t.start()
    time.sleep(0.1)

    assert S.TASKS[task_id]["state"] == "waiting"
    assert S.TASKS[task_id]["question"] == "[CH]？"

    S.PENDING[task_id]["answer"] = "[CH]"
    S.PENDING[task_id]["event"].set()
    t.join(2)
    assert got["reply"] == "[CH]"
    assert S.TASKS[task_id]["state"] == "running"
    assert S.TASKS[task_id]["question"] == ""
    S.PENDING.pop(task_id, None)


def test_no_reply_times_out_into_none():
    from phoneagent import server as S

    task_id = "handover2"
    S.PENDING[task_id] = {"question": "", "answer": None, "event": threading.Event()}
    assert S._ask(task_id, "[CH]", 0.05) is None
    assert S.TASKS[task_id]["state"] == "running"
    S.PENDING.pop(task_id, None)


def test_ask_with_no_slot_returns_none():
    from phoneagent import server as S

    assert S._ask("missing", "[CH]", 0.05) is None
