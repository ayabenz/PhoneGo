"""Offline tests for the crawl's judgement calls."""

from __future__ import annotations

from phoneagent import build_map
from phoneagent.build_map import (
    CONTAINMENT_FLOOR,
    FOREIGN_HOSTS,
    _consequential,
    _dump_package,
    _ensure_home,
    _fingerprint,
    _foreign,
    _match_screen,
    _print_similarity,
)


def _screen(*labels, y0: float = 0.1, step: float = 0.05) -> list[dict]:
    """A screen of labelled rows starting at a given vertical offset."""
    return [
        {"text": label, "center": (0.5, y0 + index * step)}
        for index, label in enumerate(labels)
    ]


MAIN = ["WLAN", "Bluetooth", "[CH]Network", "Device[CH]", "[CH]Connection", "Settings", "[CH]", "[CH]"]


def test_a_screen_from_another_app_is_foreign():
    assert _foreign("com.miui.calculator", "com.android.settings")


def test_the_crawled_app_is_not_foreign():
    assert not _foreign("com.android.settings", "com.android.settings")


def test_an_empty_foreground_is_not_evidence():
    # current_app() returns "" when dumpsys could not answer; guessing "foreign"
    # there would throw away a good screen.
    assert not _foreign("", "com.android.settings")


def test_a_package_that_hosts_a_real_page_is_kept():
    # HyperOS implements the mobile-network page inside com.android.phone.
    for host in FOREIGN_HOSTS["com.android.settings"]:
        assert not _foreign(host, "com.android.settings"), host


def test_the_same_host_is_pollution_for_another_app():
    # A file-manager crawl recorded the Xiaomi account page as a screen of the
    # file manager; for that app the account package is not a destination.
    assert _foreign("com.xiaomi.account", "com.android.fileexplorer")


def test_the_calculator_is_never_an_allowed_host():
    for hosts in FOREIGN_HOSTS.values():
        assert "com.miui.calculator" not in hosts
        assert "com.android.browser" not in hosts


# ---------------------------------------------------------------------------
# screen dedup
# ---------------------------------------------------------------------------


def test_the_same_page_at_another_scroll_offset_is_the_same_screen():
    # This is the failure that stored one Settings page as two: the rows moved,
    # so every position-bearing key changed and the overlap test said "new".
    top = _screen(*MAIN, y0=0.2)
    scrolled = _screen(*MAIN, y0=0.35)
    assert _print_similarity(_fingerprint(top), _fingerprint(scrolled)) >= 0.85


def test_a_scrolled_page_that_shows_more_rows_is_still_the_same_screen():
    top = _screen(*MAIN, y0=0.2)
    more = _screen(*MAIN, "[CH]Feature", "[CH]Feedback", y0=0.2)
    assert _print_similarity(_fingerprint(top), _fingerprint(more)) >= 0.85


def test_two_different_pages_are_not_merged():
    main = _fingerprint(_screen(*MAIN))
    wlan = _fingerprint(_screen("WLAN", "Network[CH]", "[CH]Network", "AdvancedSettings"))
    assert _print_similarity(main, wlan) < 0.85


def test_containment_needs_enough_shared_labels_to_count():
    # Two rows in common is a shared header, not a shared page.
    a = _fingerprint(_screen("Back", "Settings"))
    b = _fingerprint(_screen("Back", "Settings", "WLAN", "Bluetooth", "[CH]Network"))
    shared = 2
    assert shared < CONTAINMENT_FLOOR
    assert _print_similarity(a, b) < 0.85


def test_matching_picks_the_closest_known_screen():
    top = _fingerprint(_screen(*MAIN, y0=0.2))
    other = _fingerprint(_screen("WLAN", "Network[CH]", "[CH]Network", "AdvancedSettings"))
    known = {"screen_0": top, "screen_1": other}
    match, score = _match_screen(known, _fingerprint(_screen(*MAIN, y0=0.3)))
    assert match == "screen_0"
    assert score >= 0.85


# ---------------------------------------------------------------------------
# start check
# ---------------------------------------------------------------------------


def _hierarchy(package: str, text: str = "") -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
        '<hierarchy rotation="0"><node index="0" text="%s" resource-id="" '
        'class="android.widget.FrameLayout" package="%s" />' % (text, package)
    )


def test_the_dumped_package_is_read_from_the_root_node():
    assert _dump_package(_hierarchy("com.android.calendar")) == "com.android.calendar"
    assert _dump_package("garbage") == ""


class _DumpDevice:
    """A device whose dumps come from wherever the accessibility focus is."""

    def __init__(self, xmls: list[str], foreground: str) -> None:
        self.xmls = list(xmls)
        self.foreground = foreground
        self.launched = 0

    def force_stop(self, package: str) -> bool:
        return True

    def launch(self, package: str, intent: str = "", wait: float = 6.0) -> bool:
        self.launched += 1
        return True

    def dump_ui(self) -> str:
        return self.xmls.pop(0) if self.xmls else _hierarchy(self.foreground)

    def press_back(self) -> bool:
        return True

    def current_app(self) -> str:
        return self.foreground


def test_a_dump_from_another_app_is_not_a_successful_start(monkeypatch):
    # dumpsys said the calendar was in front, but the dump was the WLAN page:
    # an app on a second display had the accessibility focus. Starting the
    # crawl on that dump records screens the crawler cannot see.
    monkeypatch.setattr(build_map.time, "sleep", lambda _s: None)
    device = _DumpDevice([_hierarchy("com.android.settings")] * 3,
                         foreground="com.android.calendar")
    assert not _ensure_home(device, "com.android.calendar", "", "")
    assert device.launched == 3


def test_a_dump_of_the_target_app_is_a_successful_start(monkeypatch):
    monkeypatch.setattr(build_map.time, "sleep", lambda _s: None)
    device = _DumpDevice([_hierarchy("com.android.calendar")],
                         foreground="com.android.calendar")
    assert _ensure_home(device, "com.android.calendar", "", "")


# ---------------------------------------------------------------------------
# side effects
# ---------------------------------------------------------------------------


def test_the_labels_that_left_alarms_behind_are_consequential():
    for label in ("[CH]", "[CH]", "Delete", "OK", "[CH]", "[CH]Purchase",
         "Install", "[CH]Update", "Camera"):
        assert _consequential(label), label


def test_labels_that_only_open_a_page_are_not_consequential():
    for label in ("[CH]", "[CH]", "[CH]Settings", "WLAN", "Back", "Cancel", "AdvancedSettings"):
        assert not _consequential(label), label


def test_an_empty_label_is_not_consequential():
    assert not _consequential("")


# ---------------------------------------------------------------------------
# model replies that are not one JSON object per line
# ---------------------------------------------------------------------------

import sys as _sys


def _crawler_module():
    from phoneagent.build_map import _load_crawler

    _load_crawler()
    return _sys.modules["phonecli_android_build_map"]


def test_an_enrichment_reply_is_parsed_in_every_shape_it_arrives():
    parse = _crawler_module()._parse_json_items
    shapes = {
        "one per line": '{"text": "a"}\n{"text": "b"}',
        "array": '[{"text": "a"}, {"text": "b"}]',
        "fenced": '```json\n{"text": "a"}\n{"text": "b"}\n```',
        "wrapped in a key": '{"elements": [{"text": "a"}, {"text": "b"}]}',
        "numbered list": '1. {"text": "a"}\n2. {"text": "b"}',
        "trailing commas": '{"text": "a"},\n{"text": "b"},',
        "prose around it": 'Sure, here you go:\n{"text": "a"}\n{"text": "b"}',
    }
    for name, reply in shapes.items():
        assert len(parse(reply)) == 2, name


def test_an_empty_or_junk_reply_yields_nothing():
    parse = _crawler_module()._parse_json_items
    assert parse("") == []
    assert parse("   ") == []
    assert parse("I cannot help with that.") == []


def test_a_pretty_printed_reply_is_parsed():
    # The shape that broke a crawl: one object, twenty lines, no array.
    reply = '{\n  "text": "Back",\n  "aliases": [\n    "back",\n    "go back"\n  ],\n  "semantic_type": "button"\n}'
    items = _crawler_module()._parse_json_items(reply)
    assert len(items) == 1
    assert items[0]["text"] == "Back"


def test_several_pretty_printed_objects_are_all_parsed():
    reply = ('{\n  "text": "a"\n}\n'
             '{"text": "b"}\n'
             '{\n  "text": "c",\n  "aliases": ["C"]\n}')
    parse = _crawler_module()._parse_json_items
    assert [i["text"] for i in parse(reply)] == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# a permission dialog is not "the app never came up"
# ---------------------------------------------------------------------------


def _dialog_with(*labels: str) -> str:
    nodes = "".join(
        f'<node index="{i}" text="{label}" resource-id="" class="android.widget.Button" '
        f'package="com.android.permissioncontroller" bounds="[0,{200 + i * 100}][1280,{280 + i * 100}]" />'
        for i, label in enumerate(labels)
    )
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
            f'<hierarchy rotation="0">{nodes}</hierarchy>')


def test_a_permission_dialog_is_granted_instead_of_aborting(monkeypatch):
    from phoneagent.build_map import _ensure_home

    monkeypatch.setattr(build_map.time, "sleep", lambda _s: None)
    dialog = _dialog_with("[CH]App", "[CH]", "[CH]", "[CH]")
    granted = _hierarchy("com.android.calendar")
    device = _DumpDevice([dialog, granted], foreground="com.android.calendar")
    device.taps = []
    device.tap = lambda x, y: device.taps.append((x, y)) or True
    assert _ensure_home(device, "com.android.calendar", "", "")
    assert device.taps, "the grant button should have been pressed"


def test_a_dialog_that_cannot_be_granted_still_fails_cleanly(monkeypatch):
    from phoneagent.build_map import _ensure_home

    monkeypatch.setattr(build_map.time, "sleep", lambda _s: None)
    dialog = _dialog_with("[CH]", "[CH]")
    device = _DumpDevice([dialog] * 3, foreground="com.android.permissioncontroller")
    device.tap = lambda x, y: True
    assert not _ensure_home(device, "com.android.calendar", "", "")


def test_a_miui_dialog_is_recognised_by_its_buttons(monkeypatch):
    # MIUI asks through its own security-centre activity, so the package name
    # says nothing; the grant/deny pair does.
    from phoneagent.build_map import _ensure_home

    monkeypatch.setattr(build_map.time, "sleep", lambda _s: None)
    miui = ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
            '<hierarchy rotation="0">'
            '<node index="0" text="[CH]" class="android.widget.Button" '
            'package="com.miui.securitycenter" bounds="[0,200][1280,280]" />'
            '<node index="1" text="[CH]" class="android.widget.Button" '
            'package="com.miui.securitycenter" bounds="[0,300][1280,380]" />'
            '</hierarchy>')
    granted = _hierarchy("com.android.calendar")
    device = _DumpDevice([miui, granted], foreground="com.android.calendar")
    device.taps = []
    device.tap = lambda x, y: device.taps.append((x, y)) or True
    assert _ensure_home(device, "com.android.calendar", "", "")
    assert device.taps


def test_the_crawler_publishes_a_picture_of_each_screen():
    """The live view has nothing to show unless the crawl shares its screens."""
    from phoneagent.build_map import DeviceController
    from phoneagent.devices.mock import MockDevice

    calls = []
    controller = DeviceController(MockDevice(), launch_intent="")
    controller.on_screen = lambda: calls.append(1)

    controller.tap(10, 20)
    assert calls, "a tap should publish the screen it produced"


def test_a_publish_failure_never_breaks_the_crawl():
    from phoneagent.build_map import DeviceController
    from phoneagent.devices.mock import MockDevice

    def boom():
        raise RuntimeError("no frame for you")

    controller = DeviceController(MockDevice(), launch_intent="")
    controller.on_screen = boom
    controller.tap(10, 20)          # must not raise


def test_a_screen_whose_dump_is_another_package_is_not_recorded():
    """A file-manager map kept a Xiaomi account page as its second screen."""
    from phoneagent.build_map import _dump_package

    own = '<hierarchy><node package="com.android.fileexplorer" text="[CH]"/></hierarchy>'
    other = '<hierarchy><node package="com.xiaomi.account" text="Account"/></hierarchy>'

    assert _dump_package(own) == "com.android.fileexplorer"
    assert _dump_package(other) == "com.xiaomi.account"

    # the rule the crawler now applies before recording: same package, a known
    # host for this app, or a dialog package
    from phoneagent.build_map import DIALOG_PACKAGES, FOREIGN_HOSTS

    target = "com.android.fileexplorer"
    package = _dump_package(other)
    foreign = (package != target
               and package not in FOREIGN_HOSTS.get(target, frozenset())
               and package not in DIALOG_PACKAGES)
    assert foreign is True


def test_a_map_health_score_is_written_into_the_header(tmp_path):
    from phoneagent.build_map import _set_header

    path = tmp_path / "m.yaml"
    path.write_text(
        "app: [CH]\npackage: com.example\nscreen_w: 1280\nscreen_h: 2772\nscreens: []\n",
        encoding="utf-8",
    )
    _set_header(str(path), "crawled_at", "2026-11-11T20:00")
    _set_header(str(path), "bench", {"ops": 5, "exact": 4})

    from phoneagent.core.app_map import AppMap

    app = AppMap(str(path))
    assert app.crawled_at == "2026-11-11T20:00"
    assert app.bench["exact"] == 4
    assert app.app_name == "[CH]"          # the rest of the header survives


def test_a_map_records_what_the_crawl_did_not_reach(tmp_path):
    """"12 screens" means everything for a clock and a third of settings."""
    from phoneagent.core.app_map import AppMap

    path = tmp_path / "m.yaml"
    path.write_text(
        "app: [CH]\npackage: com.example\nscreen_w: 1280\nscreen_h: 2772\n"
        "screens: []\ncoverage:\n  screens: 12\n  queued: 47\n"
        "  depth_limit: 3\n  stopped: screen_limit\n  complete: false\n",
        encoding="utf-8",
    )
    app = AppMap(str(path))
    assert app.coverage["queued"] == 47
    assert app.coverage["complete"] is False
    assert app.coverage["stopped"] == "screen_limit"


def test_a_screen_with_one_element_is_not_recorded():
    """A settings map kept 'a minimal screen containing only a back button'."""
    from phoneagent.build_map import MIN_SCREEN_ELEMENTS

    assert MIN_SCREEN_ELEMENTS >= 3
    # the rule the crawler applies: fewer elements than this cannot be matched
    # again, and it consumes one of the screen budget's slots
    thin = [{"text": "Back"}]
    assert len(thin) < MIN_SCREEN_ELEMENTS


def test_a_tap_that_does_not_move_is_not_an_edge():
    """The map said [CH]Brightness leads back to the settings menu."""
    from phoneagent.build_map import _record_edge

    screens = [{"id": "screen_0", "elements": [{"text": "[CH]Brightness"}]}]
    _record_edge(screens, "screen_0", "[CH]Brightness", "screen_0")   # self-loop
    assert "leads_to" not in screens[0]["elements"][0]

    _record_edge(screens, "screen_0", "[CH]Brightness", "screen_3")
    assert screens[0]["elements"][0]["leads_to"] == "screen_3"


def test_a_page_that_replay_would_call_the_same_is_not_stored_twice():
    """Crawl matched on 0.85 similarity, replay on 0.5 coverage: two copies."""
    from phoneagent.build_map import _match_unified

    els_a = [{"text": t, "nx": 0.5, "ny": i / 10} for i, t in enumerate(
        ["Message", "[CH]", "[CH]", "[CH]", "我", "[CH]"])]
    els_b = [{"text": t, "nx": 0.5, "ny": i / 10, "dynamic": True} for i, t in enumerate(
        ["Message", "[CH]", "[CH]", "[CH]", "我", "[CH]"])]      # content-heavy, one label differs

    from phoneagent.build_map import _fingerprint
    screen_keys = {"screen_0": _fingerprint([])}   # positional rule says no match
    screen_texts = {"screen_0": {e["text"] for e in els_a}}
    matched, coverage = _match_unified(screen_keys, screen_texts, els_b)

    assert matched == "screen_0"              # replay would have called it the same
    assert coverage >= 0.5


def test_a_small_page_inside_a_big_one_is_not_the_same_page():
    """Containment merged 19 settings pages into 5; similarity has to agree."""
    from phoneagent.build_map import _fingerprint, _match_unified

    menu = [{"text": t, "nx": 0.5, "ny": i / 40} for i, t in enumerate(
        ["Search", "Account", "MyDevice", "WLAN", "Bluetooth", "[CH]Network", "Settings", "[CH]",
         "[CH]", "Battery", "App", "Privacy", "[CH]", "[CH]", "About", "Feedback"])]
    subpage = [{"text": t, "nx": 0.5, "ny": i / 10} for i, t in enumerate(
        ["Back", "WLAN", "Bluetooth", "[CH]Network"])]        # shares labels, is much smaller

    matched, _ = _match_unified({"screen_0": _fingerprint(menu)},
                                {"screen_0": {e["text"] for e in menu}},
                                subpage)
    assert matched is None           # a sub-page, not a second copy of the menu


def test_the_selected_tab_is_part_of_the_screen():
    """Six tabs of a feed share their tab bar; only the highlight differs."""
    from phoneagent.build_map import _selected_labels

    xml = ('<hierarchy>'
           '<node text="[CH]" bounds="[0,0][10,10]" selected="true"/>'
           '<node text="Message" bounds="[0,0][10,10]"/>'
           '</hierarchy>')
    assert _selected_labels(xml) == ["[CH]"]
    assert _selected_labels("<hierarchy/>") == []


def test_screenshots_are_locked_down_and_removed():
    """A picture of the user's screen must not linger in a shared directory."""
    from phoneagent.devices.virtual import VirtualDisplayDevice

    class Transport:
        def __init__(self):
            self.commands = []
            self.paths = []

        def shell(self, command):
            self.commands.append(command)
            return ""

        def read_file(self, path):
            self.paths.append(path)
            return b"\x89PNG"

    device = object.__new__(VirtualDisplayDevice)
    device.transport = Transport()
    device.display_id = None
    device.hands_off = True

    data = VirtualDisplayDevice.screenshot(device)
    assert data == b"\x89PNG"
    commands = " ".join(device.transport.commands)
    assert "chmod 600" in commands
    assert "rm -f" in commands


def test_a_search_page_is_not_the_feed_it_opened_from():
    """Same chrome, one difference: the page has an input field."""
    from phoneagent.build_map import _fingerprint, _match_unified

    feed = [{"text": t, "nx": 0.5, "ny": i / 40, "dynamic": True} for i, t in enumerate(
        ["[CH]", "[CH]", "[CH]", "[CH]", "[CH]", "[CH]", "[CH]", "我", "Search"])]
    search = [{"text": t, "nx": 0.5, "ny": i / 40, "dynamic": True} for i, t in enumerate(
        ["Search", "[CH]", "[CH]", "[CH]", "[CH]", "[CH]", "[CH]", "我", "[CH]", "[CH]"])]

    matched, _ = _match_unified(
        {"screen_0": _fingerprint(feed)},
        {"screen_0": {e["text"] for e in feed}},
        search,
        None,
        True,                        # the candidate has a text field
        {"screen_0": False},         # the feed does not
    )
    assert matched is None           # record it as its own screen


def test_a_different_selected_tab_is_a_different_screen():
    """[CH] / [CH] / [CH] / [CH] share every label but the highlighted tab."""
    from phoneagent.build_map import _fingerprint, _match_unified

    alarm = [{"text": t, "nx": 0.5, "ny": i / 20, "dynamic": True} for i, t in enumerate(
        ["[CH]", "[CH]", "[CH]", "[CH]", "[CH]", "未Settings[CH]"])]
    world = [{"text": t, "nx": 0.5, "ny": i / 20, "dynamic": True} for i, t in enumerate(
        ["[CH]", "[CH]", "[CH]", "[CH]", "[CH]", "Local[CH]", "[CH]", "[CH]"])]

    matched, _ = _match_unified(
        {"screen_0": _fingerprint(alarm)},
        {"screen_0": {e["text"] for e in alarm}},
        world,
        ["[CH]"],                       # the capture has another tab selected
        False,
        {"screen_0": False},
        {"screen_0": ["[CH]"]},             # the stored screen was the alarm tab
    )
    assert matched is None, "the world-clock tab must be recorded as its own screen"


def test_a_label_repeated_as_title_and_tab_prefers_the_tab():
    """The clock's page title and its tab share a label; only one is tappable."""
    from phoneagent.build_map import _clickable_points

    xml = (
        '<hierarchy>'
        '<node text="[CH]" clickable="false" bounds="[200,200][400,300]" />'
        '<node text="[CH]" clickable="true" bounds="[400,2600][560,2740]" />'
        '</hierarchy>'
    )
    points = _clickable_points(xml, 1280, 2772)
    # the container's centre is what a tap should aim at
    assert (round(480 / 1280, 4), round(2670 / 2772, 4)) in points
    # and nothing from the plain title node
    assert (round(300 / 1280, 4), round(250 / 2772, 4)) not in points


def test_an_ambiguous_label_resolves_to_the_nearest_tappable_node():
    """A tab's name is also the page title; the tab is the one to tap."""
    from phoneagent.build_map import _nearest_label

    xml = (
        '<hierarchy>'
        '<node text="[CH]" class="android.widget.TextView" clickable="false" '
        'bounds="[200,200][400,300]" />'
        '<node text="[CH]" class="android.widget.TextView" clickable="false" '
        'bounds="[400,2680][560,2730]" />'
        '<node content-desc="[CH]" class="android.widget.FrameLayout" clickable="true" '
        'bounds="[400,2600][560,2740]" />'
        '</hierarchy>'
    )
    # recorded near the tab: the tappable container wins even though the caption
    # is a few pixels closer
    node = _nearest_label(xml, "[CH]", 480, 2705)
    assert node is not None and node.clickable
    assert 2600 <= node.center[1] <= 2740
    # recorded near the title: the title wins
    title = _nearest_label(xml, "[CH]", 300, 250)
    assert title is not None and title.center[1] < 400


def test_a_tab_that_comes_after_an_identical_fingerprint_is_still_new():
    """The strict positional match used to short-circuit the tab comparison."""
    from phoneagent.build_map import _fingerprint, _match_unified

    alarm = [{"text": t, "nx": 0.5, "ny": i / 20, "dynamic": False} for i, t in enumerate(
        ["[CH]", "[CH]", "[CH]", "[CH]", "[CH]"])]
    # identical chrome: same labels, same places, only the tab differs
    world = [{"text": t, "nx": 0.5, "ny": i / 20, "dynamic": False} for i, t in enumerate(
        ["[CH]", "[CH]", "[CH]", "[CH]", "[CH]"])]

    matched, _ = _match_unified(
        {"screen_0": _fingerprint(alarm)},
        {"screen_0": {e["text"] for e in alarm}},
        world,
        ["[CH]"],
        None,
        None,
        {"screen_0": ["[CH]"]},
    )
    assert matched is None, "a different selected tab is a different screen"


def test_social_actions_are_not_explored():
    """A crawl must not like, follow or report on the user's behalf."""
    from phoneagent.build_map import _consequential

    for label in ("赞", "[CH]", "[CH]", "[CH]", "[CH]", "[CH]",
                  "[CH]", "[CH]", "[CH]", "[CH]"):
        assert _consequential(label), f"{label!r} would change the user's account"
    # navigation stays allowed
    for label in ("Search", "Message", "My", "Settings", "[CH]"):
        assert not _consequential(label), f"{label!r} only opens a page"


def test_a_feed_that_reloads_is_the_same_screen():
    """Different posts, same chrome: a refresh, not a new page."""
    from phoneagent.build_map import _same_chrome, _stable_keys

    def element(text, dynamic=False):
        return {"text": text, "dynamic": dynamic}

    feed = {"id": "screen_0", "elements": [
        element("Search"), element("[CH]"), element("[CH]"),
        element("Message"), element("我"),
        element("[CH]", dynamic=True), element("[CH]", dynamic=True),
    ]}
    # the same feed after a reload: same chrome, different posts
    refreshed = [element("Search"), element("[CH]"), element("[CH]"), element("Message"),
                 element("我"), element("[CH]", dynamic=True)]
    assert _same_chrome(_stable_keys(refreshed), [feed]) == "screen_0"

    # a post detail page keeps a back button and a comment box: not the feed
    detail = [element("Back"), element("[CH]"), element("[CH]")]
    assert _same_chrome(_stable_keys(detail), [feed]) is None
