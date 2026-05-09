#  mocht ik in plaats van vierkanten andere vormen willen gebuiken, dan worden hier de klassen beschreven

class Vierkant:
    def __init__(self, canvas, x1, y1, color, zijdeLengte):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + zijdeLengte
        self.y2 = y1 + zijdeLengte
        self.color = color

    def hide(self):
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="white", outline="white")  # rechthoek verwijderen door hem wit te maken
    
    def show(self):
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color, outline=self.color)   