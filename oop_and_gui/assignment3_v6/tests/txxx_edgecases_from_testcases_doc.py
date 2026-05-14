# tests/test_edgecases_from_testcases_doc.py
import types
import pytest

# -----------------------------
# Edgecases uit Testcases.docx
# -----------------------------
# 1) main.py prepareObservationPhase:
#    - runnen met lege kleurdoos -> fout afvangen?
#    - Size raar getal in config.py proberen
#
# 2) main.py runObservationPhase:
#    - rare sequenceLength (<0, 0, >0)
#    - timeVisible timeBetween
#    - geen/lege lijst met objecten vierkanten
#
# 3) main.py userResponsePhase:
#    - geen/lege lijst met objecten vierkanten
#    - rare sequencelength
#
# 4) main.py checkUserResponse:
#    - reeksen meegeven (ook lege)
#
# 5) vormen.py Vierkant:
#    - x1,y1, zijdelengte rare getallen
#    - niet bestaande kleur meegeven
#
# 6) kleurdoos.py vulKleurdoos:
#    - aantalVierkanten rare getallen


# ---------------------------------------------------------
# Helpers (DummyVierkant) voor prepareObservationPhase
# ---------------------------------------------------------
class DummyVierkant:
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


# =========================
# 1) prepareObservationPhase
# =========================

def test_prepare_observation_phase_empty_kleurdoos_raises(monkeypatch, window_like):
    """
    Edgecase: lege kleurdoos.
    Huidig gedrag: IndexError bij kleurdoos[kleurnummer].
    (Dit is precies wat je testcase noemt: 'fout afvangen?')
    """
    import main

    # size=2 => verwacht 4 kleuren, maar we geven [].
    fake_config = types.SimpleNamespace(getSize=lambda: 2)
    monkeypatch.setattr(main, "config", fake_config)
    monkeypatch.setattr(main.vormen, "Vierkant", DummyVierkant)

    with pytest.raises(IndexError):
        window_like.prepareObservationPhase([])


@pytest.mark.parametrize("size_value, expected_exception", [
    (0, ZeroDivisionError),      # zijde = 600/0
    ("4", TypeError),            # range("4") kan niet + deling met str
    (None, TypeError),           # deling met NoneType
])
def test_prepare_observation_phase_weird_size_raises(monkeypatch, window_like, size_value, expected_exception):
    """
    Edgecase: size raar getal in config.py.
    Huidig gedrag: exception (div/TypeError).
    """
    import main

    fake_config = types.SimpleNamespace(getSize=lambda: size_value)
    monkeypatch.setattr(main, "config", fake_config)
    monkeypatch.setattr(main.vormen, "Vierkant", DummyVierkant)

    # kleurdoos hoeft niet compleet te zijn; we crashen al eerder bij deling/range
    with pytest.raises(expected_exception):
        window_like.prepareObservationPhase(["red"])


def test_prepare_observation_phase_negative_size_returns_empty(monkeypatch, window_like):
    """
    Edgecase: size negatief.
    range(-2) geeft geen iteraties => returns [].
    (Geen exception; wel 'vreemd' gedrag, maar test legt huidig gedrag vast.)
    """
    import main

    fake_config = types.SimpleNamespace(getSize=lambda: -2)
    monkeypatch.setattr(main, "config", fake_config)
    monkeypatch.setattr(main.vormen, "Vierkant", DummyVierkant)

    out = window_like.prepareObservationPhase(["red", "green", "blue", "yellow"])
    assert out == []


# =======================
# 2) runObservationPhase
# =======================

@pytest.mark.parametrize("sequenceLength, expected", [
    (-3, []),   # range(-3) => geen iteraties
    (0, []),    # range(0)  => geen iteraties
])
def test_run_observation_phase_sequenceLength_nonpositive(monkeypatch, window_like, dummy_vierkanten, sequenceLength, expected):
    """
    Edgecase: rare sequenceLength (<0, 0).
    Huidig gedrag: lege lijst terug.
    """
    import main

    # random wordt niet aangeroepen als sequenceLength <= 0
    out = window_like.runObservationPhase(dummy_vierkanten, sequenceLength, timeVisible=10, timeBetween=20)
    assert out == expected


def test_run_observation_phase_empty_vierkanten_and_positive_sequence_raises(monkeypatch, window_like):
    """
    Edgecase: lege lijst vierkanten + sequenceLength > 0.
    Huidig gedrag: aantalNummers = -1, random.randint(0,-1) => ValueError.
    """
    import main

    # forceer dat random.randint echt wordt aangeroepen
    with pytest.raises(ValueError):
        window_like.runObservationPhase([], sequenceLength=1, timeVisible=10, timeBetween=20)


@pytest.mark.parametrize("timeVisible,timeBetween", [
    (-10, 20),   # negatief visible
    (10, -20),   # negatief between
    (-10, -20),  # beide negatief
])
def test_run_observation_phase_negative_timings_do_not_crash_with_dummy_canvas(monkeypatch, window_like, dummy_vierkanten, timeVisible, timeBetween):
    """
    Edgecase: timeVisible/timeBetween rare waarden.
    Met onze DummyCanvas crasht dit niet (hij accepteert negatieve ms).
    In echte Tkinter kan 'after' negatieve waarden anders behandelen.
    """
    import main

    # maak randint deterministisch: altijd 0
    monkeypatch.setattr(main.random, "randint", lambda a, b: 0)

    out = window_like.runObservationPhase(dummy_vierkanten, sequenceLength=2, timeVisible=timeVisible, timeBetween=timeBetween)
    assert out == [0, 0]


# =====================
# 3) userResponsePhase
# =====================

def test_user_response_phase_sequenceLength_zero_returns_empty(monkeypatch, window_like, dummy_vierkanten):
    """
    Edgecase: sequenceLength=0.
    while len(userSequence) < 0 is False => returns [] meteen.
    """
    out = window_like.userResponsePhase(dummy_vierkanten, sequenceLength=0)
    assert out == []


@pytest.mark.xfail(reason="Met lege vierkantenlijst en sequenceLength>0 ontstaat een oneindige while-loop (geen clicks mogelijk).")
def test_user_response_phase_empty_vierkanten_would_hang(monkeypatch, window_like):
    """
    Edgecase: lege lijst vierkanten en sequenceLength > 0.
    Dit is in huidige code niet veilig testbaar zonder timeout-plugin of refactor,
    omdat de while-loop nooit kan eindigen.
    """
    window_like.userResponsePhase([], sequenceLength=1)


@pytest.mark.xfail(reason="Met sequenceLength>0 en geen echte event-loop/clicks kan de while-loop in userResponsePhase blijven draaien.")
def test_user_response_phase_positive_length_needs_clicks(monkeypatch, window_like, dummy_vierkanten):
    """
    Edgecase: sequenceLength > 0 vereist click-events om userSequence te vullen.
    Zonder extra simulatie kan dit hangen (afhankelijk van je DummyCanvas/fixture).
    """
    window_like.userResponsePhase(dummy_vierkanten, sequenceLength=1)


# ======================
# 4) checkUserResponse
# ======================

def test_check_user_response_both_empty_true(window_like):
    """
    Edgecase: lege reeksen meegeven.
    [] == [] => True.
    """
    assert window_like.checkUserResponse([], []) is True


def test_check_user_response_empty_vs_nonempty_false(window_like):
    """
    Edgecase: lege vs niet-lege reeks.
    """
    assert window_like.checkUserResponse([], [1]) is False
    assert window_like.checkUserResponse([1], []) is False


# ======================
# 5) vormen.py Vierkant
# ======================

class CanvasSpy:
    def __init__(self):
        self.calls = []
    def create_rectangle(self, x1, y1, x2, y2, fill=None, outline=None):
        self.calls.append((x1, y1, x2, y2, fill, outline))


def test_vierkant_weird_coordinates_and_negative_side_length_still_calls_canvas():
    """
    Edgecase: x1,y1,zijdelengte rare getallen (negatief/float).
    Verwachting: geen crash; x2/y2 worden simpel berekend.
    """
    import vormen

    canvas = CanvasSpy()
    v = vormen.Vierkant(canvas, x1=-5.5, y1=9999, color="red", zijdeLengte=-10)
    # x2 = -15.5, y2 = 9989
    v.show()
    assert canvas.calls[-1] == (-5.5, 9999, -15.5, 9989, "red", "red")


def test_vierkant_non_existing_color_is_passed_through():
    """
    Edgecase: niet bestaande kleur meegeven.
    Tkinter kan later klagen, maar jouw code geeft hem gewoon door.
    """
    import vormen

    canvas = CanvasSpy()
    v = vormen.Vierkant(canvas, 0, 0, color="notARealColor", zijdeLengte=10)
    v.show()
    assert canvas.calls[-1][-2:] == ("notARealColor", "notARealColor")


# ======================
# 6) kleurdoos.py
# ======================

def test_vulkleurdoos_zero_squares_returns_empty():
    """
    Edgecase: aantalVierkanten = 0.
    grens=0 extra=0 => while niet, return [].
    """
    import kleurdoos
    assert kleurdoos.vulKleurdoos(0) == []


def test_vulkleurdoos_negative_squares_returns_empty():
    """
    Edgecase: aantalVierkanten negatief.
    grens negatief => while-conditie meteen False => [].
    (extra wordt nooit ==1 in deze situatie bij veel negatieve getallen; test legt huidig gedrag vast.)
    """
    import kleurdoos
    assert kleurdoos.vulKleurdoos(-8) == []


@pytest.mark.parametrize("bad_value", ["16", None, 3.14])
def test_vulkleurdoos_non_int_raises(bad_value):
    """
    Edgecase: aantalVierkanten 'raar' type (str/None/float).
    Verwachting: TypeError bij // of %.
    """
    import kleurdoos
    with pytest.raises(TypeError):
        kleurdoos.vulKleurdoos(bad_value)