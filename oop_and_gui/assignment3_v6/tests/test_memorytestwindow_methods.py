# tests/test_memorytestwindow_methods.py
import types
import pytest

def test_countdown_updates_label_and_waits(window_like):
    window_like.countDown(3)
    # range(time+1,0,-1) => 4 iteraties
    assert len(window_like.statusInfoLabel.config_calls) == 4
    assert window_like.statusInfoLabel.after_calls == [1000,1000,1000,1000]
    assert window_like.statusInfoLabel.text.startswith("Counting down:")

def test_prepare_observation_phase_creates_correct_number_of_squares(monkeypatch, window_like):
    import main
    from tests.conftest import DummyVierkant

    # Fake config: size=2 (dus 4 vierkanten)
    fake_config = types.SimpleNamespace(getSize=lambda: 2)
    monkeypatch.setattr(main, "config", fake_config)

    # Patch vormen.Vierkant naar DummyVierkant
    monkeypatch.setattr(main.vormen, "Vierkant", DummyVierkant)

    kleurdoos = ["red","green","blue","yellow"]
    vierkanten = window_like.prepareObservationPhase(kleurdoos)

    assert len(vierkanten) == 4
    # kleuren moeten in volgorde uit kleurdoos komen
    assert [v.color for v in vierkanten] == kleurdoos
    # canvas is geleegd
    assert window_like.canvas.deleted[-1] == "all"
    # label aangepast
    assert window_like.statusInfoLabel.text == "Get ready!"

def test_run_observation_phase_returns_deterministic_sequence(monkeypatch, window_like, dummy_vierkanten):
    import main

    # random.randint deterministic
    seq = [2, 0, 3]
    it = iter(seq)
    monkeypatch.setattr(main.random, "randint", lambda a,b: next(it))

    # Patch BlinkSquare zodat we alleen calls registreren
    calls = []
    def fake_blink(vierkanten, nummer, timeVisible):
        calls.append((nummer, timeVisible))
    monkeypatch.setattr(window_like, "BlinkSquare", fake_blink)

    result = window_like.runObservationPhase(dummy_vierkanten, sequenceLength=3, timeVisible=111, timeBetween=222)

    assert result == [2,0,3]
    assert calls == [(2,111),(0,111),(3,111)]
    # timeBetween wordt via canvas.after aangeroepen (3x)
    assert window_like.canvas.after_calls.count(222) == 3

def test_blink_square_hides_then_shows(window_like, dummy_vierkanten):
    v = dummy_vierkanten[1]
    window_like.BlinkSquare(dummy_vierkanten, nummer=1, timeVisible=50)
    assert v.hide_calls == 1
    assert v.show_calls == 1
    assert 50 in window_like.canvas.after_calls

def test_check_user_response_true_calls_after(window_like):
    assert window_like.checkUserResponse([1,2], [1,2]) is True
    assert 500 in window_like.canvas.after_calls

def test_check_user_response_false(window_like):
    assert window_like.checkUserResponse([1,2], [2,1]) is False

def test_handle_square_click_appends_and_blinks(monkeypatch, window_like, dummy_vierkanten):
    # Patch BlinkSquare om call te checken
    blink_calls = []
    monkeypatch.setattr(window_like, "BlinkSquare", lambda v, n, t: blink_calls.append((n,t)))

    userSequence = []
    out = window_like.handleSquareClick(dummy_vierkanten, 2, userSequence)

    assert userSequence == [2]
    assert out == [2]
    assert blink_calls == [(2, 500)]  # hardcoded 500 in jouw code

def test_user_response_phase_binds_clicks_and_lambda_captures_correct_index(monkeypatch, window_like, dummy_vierkanten):
    """
    Unit-testbare kern: er worden bindings gezet en de callbacks gebruiken de juiste index.
    We simuleren clicks door de callbacks zelf aan te roepen.
    """
    # Zorg dat show() geen echte canvas calls doet (DummyVierkant doet al niets)
    # Run response phase met sequenceLength = len(vierkanten) zodat we elk bind “klik” simuleren.
    seq_len = len(dummy_vierkanten)

    # Monkeypatch canvas.tag_bind om callback op te slaan en NIET direct aan te roepen
    # (anders krijg je te veel appends binnen dezelfde loop).
    # We laten de methode lopen en roepen daarna de callbacks aan.
    # Om de while-loop te laten stoppen, patchen we window_like.canvas.update zodat
    # hij na de eerste bind-ronde onze callbacks uitvoert.
    callbacks = []
    original_tag_bind = window_like.canvas.tag_bind

    def tag_bind_capture(item_id, event_str, cb):
        callbacks.append(cb)
        original_tag_bind(item_id, event_str, cb)

    window_like.canvas.tag_bind = tag_bind_capture

    # Patch update: na de eerste update roepen we callbacks aan (simuleer clicks)
    state = {"fired": False}
    original_update = window_like.canvas.update

    def update_and_fire():
        original_update()
        if not state["fired"] and callbacks:
            state["fired"] = True
            # Simuleer clicks in volgorde 0..n-1
            for cb in callbacks:
                cb(event=None)

    window_like.canvas.update = update_and_fire

    user_seq = window_like.userResponsePhase(dummy_vierkanten, sequenceLength=seq_len)
    assert user_seq == list(range(seq_len))