"""The memory store: four choices from Mika's design, each pinned here."""

from __future__ import annotations

from phoneagent.core.memory import (
    FULL_MAX_TOKENS,
    MemoryItem,
    MemoryStore,
    build,
    estimate_tokens,
    extract,
    is_sensitive,
)


def _store(tmp_path, items=None):
    return MemoryStore(str(tmp_path / "memory.json"), items or [])


# -- 1. the sensitive filter has two sides ---------------------------------


def test_credentials_are_never_stored():
    for text in ("MyPaymentPasswordis 123456", "Verify码 8848", "cvv 123", "pin 4321"):
        assert is_sensitive(text), text


def test_facts_a_phone_assistant_needs_are_allowed():
    for text in ("[CH]", "[CH] 3 月 5 日", "Phone号 138xxxx", "[CH]"):
        assert not is_sensitive(text), text


def test_store_refuses_a_credential(tmp_path):
    store = _store(tmp_path)
    assert store.add("fact", "PaymentPasswordis 123456") is None
    assert store.items == []


# -- 2. a procedure waits for approval -------------------------------------


def test_a_procedure_is_pending_until_approved(tmp_path):
    store = _store(tmp_path)
    item = store.add("procedure", "[CH]", quote="[CH]")
    assert item is not None and item.status == "pending"
    assert store.active() == []          # never injected yet
    assert build(store.items, "[CH]").message == ""

    assert store.approve(item.id)
    assert store.active()
    assert "[CH]" in build(store.items, "[CH]").message


def test_a_fact_is_active_immediately(tmp_path):
    store = _store(tmp_path)
    item = store.add("fact", "[CH]")
    assert item.status == "active"


# -- 3. the quote is kept ---------------------------------------------------


def test_the_quote_is_kept_for_provenance(tmp_path):
    store = _store(tmp_path)
    item = store.add("preference", "Order[CH]", quote="[CH]")
    assert item.quote == "[CH]"


# -- 4. fixed prefix beats retrieval until the budget runs out -------------


def test_everything_is_injected_when_it_fits(tmp_path):
    store = _store(tmp_path)
    for index in range(5):
        store.add("fact", f"[CH]{index}：第{index}[CH]")
    block = build(store.items, "[CH]")
    # retrieval would have dropped these (nothing overlaps the task)
    assert block.used_ids and len(block.used_ids) == 5


def test_a_huge_store_falls_back_to_retrieval():
    items = [MemoryItem(id=f"i{n}", kind="fact", content="[CH]" * 40) for n in range(60)]
    items.append(MemoryItem(id="hit", kind="fact", content="[CH]Bluetooth[CH]", keywords=["Bluetooth"]))
    block = build(items, "OpenBluetooth", mode="auto")
    assert "hit" in block.used_ids
    assert len(block.used_ids) < len(items)


def test_retrieval_drops_what_the_task_does_not_mention():
    items = [MemoryItem(id="a", kind="fact", content="[CH]", keywords=["[CH]", "[CH]"]),
             MemoryItem(id="b", kind="fact", content="[CH]Bluetooth[CH]", keywords=["Bluetooth"])]
    block = build(items, "OpenBluetooth", mode="relevant")
    assert "b" in block.used_ids and "a" not in block.used_ids


def test_token_estimate_counts_cjk_and_words():
    assert estimate_tokens("OpenBluetooth") >= 3
    assert estimate_tokens("open the bluetooth settings") >= 4


def test_full_injection_respects_its_own_ceiling():
    items = [MemoryItem(id=f"i{n}", kind="fact", content="字" * 200) for n in range(40)]
    block = build(items, "[CH]", mode="full")
    assert estimate_tokens(block.message) > FULL_MAX_TOKENS  # full mode does not trim


# -- usage tracking ---------------------------------------------------------


def test_mark_used_records_the_count(tmp_path):
    store = _store(tmp_path)
    item = store.add("fact", "[CH]")
    store.mark_used([item.id])
    assert store.items[0].use_count == 1
    assert store.items[0].last_used_at > 0


# -- extraction -------------------------------------------------------------


class _LLM:
    def __init__(self, payload):
        self.payload = payload

    def text(self, system, user, temperature=0.0):
        return self.payload


def test_extraction_parses_candidates():
    llm = _LLM('{"memories": [{"kind": "preference", "content": "Order[CH]", '
               '"quote": "[CH]"}]}')
    out = extract(llm, "[CH]Charging器", "[CH]")
    assert out == [{"kind": "preference", "content": "Order[CH]", "quote": "[CH]"}]


def test_extraction_survives_garbage():
    assert extract(_LLM("not json"), "[CH]", "[CH]") == []
    assert extract(_LLM('{"memories": []}'), "[CH]", "[CH]") == []
    assert extract(None, "[CH]", "[CH]") == []


# -- agent integration ------------------------------------------------------


def test_the_block_is_a_fixed_prefix_ahead_of_the_task(tmp_path):
    from phoneagent.core.agent import AgentConfig, PhoneAgent
    from phoneagent.core.llm import Choice, ToolCall
    from phoneagent.devices.mock import MockDevice

    class Device(MockDevice):
        def dump_ui(self):
            return '<hierarchy><node text="Settings" bounds="[0,0][200,120]"/></hierarchy>'

    class LLM:
        def __init__(self):
            self.prompts = []

        def choose(self, system, user, image_png=None, tools=None, temperature=0.0):
            self.prompts.append(user)
            return Choice(call=ToolCall(name="finish", arguments={"message": "已Done"}))

    store = _store(tmp_path)
    store.add("fact", "[CH]")
    llm = LLM()
    agent = PhoneAgent(Device(), [], llm, config=AgentConfig(verify_with_vlm=False),
                       sleep=lambda _s: None, memory=store)
    agent.run("OpenBluetooth")

    prompt = llm.prompts[0]
    assert prompt.index("[CH]") < prompt.index("Task: OpenBluetooth")
    # and the item is marked as used
    assert store.items[0].use_count == 1


def test_remember_reports_what_was_stored(tmp_path):
    from phoneagent.server import remember

    class LLM:
        def text(self, system, user, temperature=0.0):
            return ('{"memories": ['
                    '{"kind": "fact", "content": "[CH]", "quote": "[CH]"},'
                    '{"kind": "procedure", "content": "[CH]Order", "quote": ""},'
                    '{"kind": "fact", "content": "PaymentPasswordis 123456", "quote": ""}]}')

    store = _store(tmp_path)
    steps = remember(LLM(), store, "[CH]", "已Order")

    kinds = [(step.action, step.detail) for step in steps]
    assert ("remembered", "[CH]") in kinds
    assert ("pending", "[CH]Order") in kinds       # a procedure waits
    assert any(step.action == "refused" for step in steps)  # credential refused
    assert all("123456" not in item.content for item in store.items)


def test_maps_built_for_another_screen_are_skipped(tmp_path):
    import yaml
    from phoneagent.ondevice import _usable_maps

    good = tmp_path / "good.yaml"
    good.write_text(yaml.safe_dump({"app": "Settings", "screen_w": 1280, "screen_h": 2772}))
    other = tmp_path / "other.yaml"
    other.write_text(yaml.safe_dump({"app": "Settings", "screen_w": 1080, "screen_h": 2400}))
    legacy = tmp_path / "legacy.yaml"
    legacy.write_text(yaml.safe_dump({"app": "Settings"}))

    class Device:
        width, height = 1280, 2772

    kept, skipped = _usable_maps([str(good), str(other), str(legacy)], Device())

    assert kept == [str(good), str(legacy)]      # no size recorded: keep it
    assert skipped and skipped[0][0] == str(other)
    assert "built for 1080x2400" in skipped[0][1]
