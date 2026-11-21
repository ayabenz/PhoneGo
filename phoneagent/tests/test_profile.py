"""Per-app profiles: which texts are this phone's data, which are structure.

The map that shipped before profiles contained "yangqinREDMI K90 Ultra" and
three Wi-Fi SSIDs as if they were navigation. These tests pin the behaviour
that keeps that out of a distributable map.
"""

from __future__ import annotations

import yaml

from phoneagent.core.app_map import AppMap
from phoneagent.core.profile import (
    Profile,
    _extract_json,
    heuristic_profile,
    load_profile,
    sanitize_map,
    save_profile,
)


def test_dynamic_patterns_match_but_preserved_texts_never_do():
    profile = Profile(dynamic_patterns=[r"^\d+\.\d+\.\d+\.\d+$", r"^.{8,}$"],
                      preserve_navigation=["Settings"])
    assert profile.is_dynamic("3.0.305.0")
    assert profile.is_dynamic("yangqinREDMI K90 Ultra")
    # preserved wins even when a pattern would match
    assert not profile.is_dynamic("Settings")
    assert not profile.is_dynamic("")
    assert not profile.is_dynamic("Bluetooth")


def test_bad_regex_in_a_profile_is_ignored():
    profile = Profile(dynamic_patterns=[r"([unclosed", r"^\d+$"])
    assert profile.is_dynamic("123")
    assert not profile.is_dynamic("Bluetooth")


def test_heuristic_flags_device_names():
    profile = heuristic_profile("Settings", "com.android.settings",
                                ["Bluetooth", "Settings", "yangqinREDMI K90 Ultra", "10.0.0.1"])
    assert profile.is_dynamic("yangqinREDMI K90 Ultra")
    assert profile.is_dynamic("10.0.0.1")
    assert not profile.is_dynamic("Bluetooth")


def test_truncated_json_is_not_salvaged():
    assert _extract_json('{"dynamic_patterns": ["^\\d+$"') is None
    assert _extract_json('{"dynamic_patterns": []}') == {"dynamic_patterns": []}


def test_profile_round_trips_through_yaml(tmp_path):
    profile = Profile(app="Settings", package="com.android.settings",
                      dynamic_patterns=[r"^\d+$"], preserve_navigation=["Bluetooth"],
                      source="llm")
    path = tmp_path / "settings.yaml"
    save_profile(profile, str(path))
    again = load_profile(str(path))
    assert again is not None
    assert again.dynamic_patterns == profile.dynamic_patterns
    assert again.preserve_navigation == ["Bluetooth"]


def test_sanitize_drops_noise_but_keeps_navigation(tmp_path):
    source = {
        "app": "Settings", "package": "com.android.settings",
        "screens": [{"id": "screen_0", "elements": [
            {"text": "Bluetooth", "center": [0.5, 0.5], "leads_to": "screen_1"},
            {"text": "yangqinREDMI K90 Ultra", "center": [0.5, 0.6], "leads_to": "screen_1"},
            {"text": "1101,已Connection,WLAN [CH]。,SecurityNetwork", "center": [0.5, 0.7]},
        ]}],
    }
    path = tmp_path / "map.yaml"
    path.write_text(yaml.safe_dump(source, allow_unicode=True), encoding="utf-8")

    profile = Profile(dynamic_patterns=[r"^yangqin", r"^\d+,已Connection"],
                      preserve_navigation=["Bluetooth"])
    report = sanitize_map(str(path), profile, str(tmp_path / "clean.yaml"))

    assert report["marked"] == 2
    clean = yaml.safe_load((tmp_path / "clean.yaml").read_text(encoding="utf-8"))
    texts = [e["text"] for e in clean["screens"][0]["elements"]]
    assert texts == ["Bluetooth", "<dynamic>", "<dynamic>"]
    assert clean["screens"][0]["elements"][1]["redacted"] is True

    # and the real reader agrees: the noise is gone from the catalog
    app_map = AppMap(str(tmp_path / "clean.yaml"))
    descriptions = [op.description for op in app_map.build_operations().values()]
    assert any("Bluetooth" in d for d in descriptions)
    assert not any("yangqin" in d for d in descriptions)
