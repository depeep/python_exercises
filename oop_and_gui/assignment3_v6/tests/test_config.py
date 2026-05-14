# tests/test_config.py
import config

def test_get_start_test_settings_returns_tuple():
    c = config.Config()
    maxLevels, timeVisible, timeBetween = c.getStartTestSettings()
    assert isinstance(maxLevels, int)
    assert isinstance(timeVisible, int)
    assert isinstance(timeBetween, int)

def test_get_window_config_returns_expected_shapes():
    c = config.Config()
    windowGeometry, canvasWidth, canvasHeight, basisLettertype = c.getWindowConfig()
    assert isinstance(windowGeometry, str)
    assert isinstance(canvasWidth, int)
    assert isinstance(canvasHeight, int)
    assert isinstance(basisLettertype, tuple)
    assert len(basisLettertype) == 3  # ("Arial", 20, "bold") in jouw code

def test_get_and_set_size():
    c = config.Config()
    old = c.getSize()
    c.setSize(old + 1)
    assert c.getSize() == old + 1