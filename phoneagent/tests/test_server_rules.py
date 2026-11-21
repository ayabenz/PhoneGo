

def test_a_request_to_stay_is_recognised():
    """Only an explicit "leave it open" keeps the app in front."""
    from phoneagent.server import _wants_to_stay

    assert _wants_to_stay("[CH]Search[CH]") is False
    assert _wants_to_stay("OpenBluetoothSettings") is False
    assert _wants_to_stay("Open[CH]Page") is True
    assert _wants_to_stay("[CH]") is True
    assert _wants_to_stay("keep it open on the note") is True
