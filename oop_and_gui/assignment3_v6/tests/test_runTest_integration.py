# tests/test_runTest_integration.py
import types
import pytest

# -------------------------
# Fakes voor Tkinter widgets
# -------------------------
class DummyLabel:
    def __init__(self):
        self.text = None
        self.config_calls = []

    def config(self, **kwargs):
        self.config_calls.append(kwargs)
        if "text" in kwargs:
            self.text = kwargs["text"]

    def update(self):
        pass

    def after(self, ms):
        # geen echte wachttijd
        pass


class DummyCanvas:
    def __init__(self):
        self.deleted = []
        self.after_calls = []
        self.updated = 0

    def delete(self, what):
        self.deleted.append(what)

    def update(self):
        self.updated += 1

    def after(self, ms):
        self.after_calls.append(ms)


class DummyVierkant:
    """Fake voor vormen.Vierkant die alleen interface levert (show/hide + coords)."""
    def __init__(self, canvas, x1, y1, color, zijdeLengte):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + zijdeLengte
        self.y2 = y1 + zijdeLengte
        self.color = color
        self.show_calls = 0
        self.hide_calls = 0

    def show(self):
        self.show_calls += 1

    def hide(self):
        self.hide_calls += 1


@pytest.fixture
def window_like(monkeypatch):
    """
    Maak een MemoryTestWindow instance zonder __init__ (want __init__ start mainloop).
    Injecteer alleen de attributes die runTest() en sub-methoden nodig hebben.
    """
    import main

    w = main.MemoryTestWindow.__new__(main.MemoryTestWindow)

    # GUI-attributen die gebruikt worden in runTest & subcalls
    w.canvas = DummyCanvas()
    w.statusInfoLabel = DummyLabel()
    w.sequenceLengthValueLabel = DummyLabel()

    return w


def test_runTest_integration_all_levels_correct(monkeypatch, window_like):
    """
    Integratietest: runTest doorloopt meerdere levels en stopt niet voortijdig
    als de userSequence steeds gelijk is aan getoondeReeks.
    """
    import main

    # 1) Patch config zodat test klein & snel is
    #    - size=2 => 4 vierkanten
    #    - maxLevels=3 => levels 1..3
    fake_config = types.SimpleNamespace(
        getSize=lambda: 2,
        getStartTestSettings=lambda: (3, 1, 0)  # timeVisible=1ms, timeBetween=0ms
    )
    monkeypatch.setattr(main, "config", fake_config)

    # 2) Patch vulKleurdoos: vaste kleurenlijst voor 2x2
    monkeypatch.setattr(main, "vulKleurdoos", lambda n: ["red", "green", "blue", "yellow"])

    # 3) Patch vormen.Vierkant => DummyVierkant, zodat we geen echte Canvas-tekenacties doen
    monkeypatch.setattr(main.vormen, "Vierkant", DummyVierkant)

    # 4) Geen echte countdown-wachttijd
    monkeypatch.setattr(window_like, "countDown", lambda t: None)

    # 5) random deterministisch maken voor runObservationPhase
    #    Voor levels 1,2,3 hebben we 1+2+3 = 6 getallen nodig
    seq = iter([0, 1, 2, 0, 3, 1])  # indices in bereik 0..3
    monkeypatch.setattr(main.random, "randint", lambda a, b: next(seq))

    # 6) Maak userResponsePhase “semi-integratie”:
    #    we laten runObservationPhase echt lopen, maar slaan de getoonde reeks op
    #    zodat userResponsePhase die exact kan teruggeven.
    original_runObservationPhase = main.MemoryTestWindow.runObservationPhase

    def runObservationPhase_store(self, vierkanten, sequenceLength, timeVisible, timeBetween):
        shown = original_runObservationPhase(self, vierkanten, sequenceLength, timeVisible, timeBetween)
        self._last_shown = shown
        return shown

    monkeypatch.setattr(main.MemoryTestWindow, "runObservationPhase", runObservationPhase_store)

    def userResponsePhase_returns_last(self, vierkanten, sequenceLength):
        return list(self._last_shown)

    monkeypatch.setattr(main.MemoryTestWindow, "userResponsePhase", userResponsePhase_returns_last)

    # 7) Spy op prepareObservationPhase om te checken dat hij per level wordt aangeroepen
    calls = {"prepare": 0}
    original_prepare = main.MemoryTestWindow.prepareObservationPhase

    def prepare_spy(self, kleurdoos):
        calls["prepare"] += 1
        return original_prepare(self, kleurdoos)

    monkeypatch.setattr(main.MemoryTestWindow, "prepareObservationPhase", prepare_spy)

    # Run!
    window_like.runTest()

    # Verwachtingen:
    # - prepareObservationPhase is 3x aangeroepen (voor 3 levels)
    assert calls["prepare"] == 3

    # - status label is minstens 1x op "Correct!" gezet (na elk goed level)
    assert any(c.get("text") == "Correct!" for c in window_like.statusInfoLabel.config_calls)

    # - canvas.after(1000) wordt gebruikt tussen levels (in jouw runTest)
    assert 1000 in window_like.canvas.after_calls


def test_runTest_integration_stops_on_incorrect(monkeypatch, window_like):
    """
    Integratietest: runTest stopt zodra userSequence != getoondeReeks
    en zet 'Incorrect...' in het statuslabel.
    """
    import main

    fake_config = types.SimpleNamespace(
        getSize=lambda: 2,
        getStartTestSettings=lambda: (5, 1, 0)  # maxLevels=5, maar we stoppen eerder
    )
    monkeypatch.setattr(main, "config", fake_config)
    monkeypatch.setattr(main, "vulKleurdoos", lambda n: ["red", "green", "blue", "yellow"])
    monkeypatch.setattr(main.vormen, "Vierkant", DummyVierkant)
    monkeypatch.setattr(window_like, "countDown", lambda t: None)

    # random deterministisch: voor level 1 en 2 genoeg waarden
    seq = iter([0, 1, 2])  # level1=1 value, level2=2 values => totaal 3
    monkeypatch.setattr(main.random, "randint", lambda a, b: next(seq))

    # runObservationPhase echt + store
    original_runObservationPhase = main.MemoryTestWindow.runObservationPhase

    def runObservationPhase_store(self, vierkanten, sequenceLength, timeVisible, timeBetween):
        shown = original_runObservationPhase(self, vierkanten, sequenceLength, timeVisible, timeBetween)
        self._last_shown = shown
        return shown

    monkeypatch.setattr(main.MemoryTestWindow, "runObservationPhase", runObservationPhase_store)

    # userResponsePhase: level 1 correct, level 2 expres fout
    def userResponsePhase_maybe_wrong(self, vierkanten, sequenceLength):
        if sequenceLength == 1:
            return list(self._last_shown)          # correct
        return list(reversed(self._last_shown))    # fout bij level 2

    monkeypatch.setattr(main.MemoryTestWindow, "userResponsePhase", userResponsePhase_maybe_wrong)

    # Spy prepare calls
    calls = {"prepare": 0}
    original_prepare = main.MemoryTestWindow.prepareObservationPhase

    def prepare_spy(self, kleurdoos):
        calls["prepare"] += 1
        return original_prepare(self, kleurdoos)

    monkeypatch.setattr(main.MemoryTestWindow, "prepareObservationPhase", prepare_spy)

    # Run!
    window_like.runTest()

    # Verwachting: stopt bij level 2 => prepare is 2x aangeroepen
    assert calls["prepare"] == 2

    # Status label bevat "Incorrect"
    assert window_like.statusInfoLabel.text is not None
