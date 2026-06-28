import pygame

class GraphRenderer:
    def __init__(self, game):
        self.game = game

    def draw(self):
        x, y, w, h = self.game.graph_rect

        pygame.draw.rect(self.game.surface, (25, 28, 34), self.game.graph_rect)
        pygame.draw.line(self.game.surface, (80, 80, 80), (x, y), (x + w, y), 2)

        padding = 20
        gx = x + padding
        gy = y + 30
        gw = w - padding * 2
        gh = h - 70

        title = self.game.uiFont.render("Population Over Time", True, (240, 240, 240))
        self.game.surface.blit(title, (x + 10, y + 4))

        values = (
            list(self.game.food_history)
            + list(self.game.prey1_history)
            + list(self.game.prey2_history)
            + list(self.game.pred_history)
        )
        max_val = max(values) if values else 10
        max_val = max(max_val, 10)

        def make_points(history):
            pts = []
            data = list(history)
            if len(data) < 2:
                return pts

            for i, val in enumerate(data):
                px = gx + int(i * (gw / max(1, self.game.max_history - 1)))
                py = gy + gh - int((val / max_val) * gh)
                pts.append((px, py))
            return pts

        for i in range(5):
            yy = gy + int(i * gh / 4)
            pygame.draw.line(self.game.surface, (50, 50, 50), (gx, yy), (gx + gw, yy), 1)
            label_val = int(max_val - i * (max_val / 4))
            label = self.game.smallFont.render(str(label_val), True, (180, 180, 180))
            self.game.surface.blit(label, (gx + 5, yy - 10))

        food_points = make_points(self.game.food_history)
        prey1_points = make_points(self.game.prey1_history)
        prey2_points = make_points(self.game.prey2_history)
        pred_points = make_points(self.game.pred_history)

        if len(food_points) >= 2:
            pygame.draw.lines(self.game.surface, (80, 220, 120), False, food_points, 2)
        if len(prey1_points) >= 2:
            pygame.draw.lines(self.game.surface, (90, 180, 255), False, prey1_points, 2)
        if len(prey2_points) >= 2:
            pygame.draw.lines(self.game.surface, (255, 210, 90), False, prey2_points, 2)
        if len(pred_points) >= 2:
            pygame.draw.lines(self.game.surface, (255, 90, 90), False, pred_points, 2)

