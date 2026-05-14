# tests/conftest.py
import types
import pytest

class DummyLabel:
    def __init__(self):
        self.text = None
        self.config_calls = []
        self.after_calls = []
        self.updated = 0

    def config(self, **kwargs):
        # Tkinter gebruikt vaak config(text="...")
        self.config_calls.append(kwargs)
        if "text" in kwargs:
            self.text = kwargs["text"]

    def update(self):
        self.updated += 1

    def after(self, ms):
        self.after_calls.append(ms)

class DummyCanvas:
    def __init__(self):
        self.created = []         # lijst van rectangles (x1,y1,x2,y2,fill,outline)
        self.deleted = []
        self.after_calls = []
        self.updated = 0
        self._next_id = 1
        self.bindings = {}        # (item_id, event_str) -> callback

    def create_rectangle(self, x1, y1, x2, y2, fill=None, outline=None):
        item_id = self._next_id
        self._next_id += 1
        self.created.append((item_id, x1, y1, x2, y2, fill, outline))
        return item_id

    def tag_bind(self, item_id, event_str, callback):
        self.bindings[(item_id, event_str)] = callback

    def delete(self, what):
        self.deleted.append(what)

    def update(self):
        self.updated += 1

    def after(self, ms):
        self.after_calls.append(ms)

class DummyVierkant:
    """Fake Vierkant met dezelfde interface als vormen.Vierkant."""
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
def dummy_canvas():
    return DummyCanvas()

@pytest.fixture
def dummy_label():
    return DummyLabel()

@pytest.fixture
def dummy_vierkanten(dummy_canvas):
    # maak 4 vierkanten met vaste coords/kleuren
    return [
        DummyVierkant(dummy_canvas, 0, 0, "red", 10),
        DummyVierkant(dummy_canvas, 10, 0, "green", 10),
        DummyVierkant(dummy_canvas, 0, 10, "blue", 10),
        DummyVierkant(dummy_canvas, 10, 10, "yellow", 10),
    ]

@pytest.fixture
def window_like(dummy_canvas, dummy_label):
    """
    Maakt een MemoryTestWindow-object zonder __init__ (dus zonder mainloop),
    en injecteert alleen wat methoden nodig hebben.
    """
    import main  # pas aan als jouw bestand anders heet
    w = main.MemoryTestWindow.__new__(main.MemoryTestWindow)
    w.canvas = dummy_canvas
    w.statusInfoLabel = dummy_label
    w.sequenceLengthValueLabel = DummyLabel()
    return w