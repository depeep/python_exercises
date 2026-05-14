# tests/test_vormen.py
import vormen

class CanvasSpy:
    def __init__(self):
        self.calls = []

    def create_rectangle(self, x1, y1, x2, y2, fill=None, outline=None):
        self.calls.append((x1,y1,x2,y2,fill,outline))

def test_vierkant_show_draws_colored_rectangle():
    canvas = CanvasSpy()
    v = vormen.Vierkant(canvas, 10, 20, "red", 30)  # x2=40, y2=50
    v.show()
    assert canvas.calls[-1] == (10,20,40,50,"red","red")

def test_vierkant_hide_draws_white_rectangle():
    canvas = CanvasSpy()
    v = vormen.Vierkant(canvas, 10, 20, "red", 30)
    v.hide()
    assert canvas.calls[-1] == (10,20,40,50,"white","white")