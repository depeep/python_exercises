import pygame


class DummySound:
    def play(self):
        pass


class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load_image(self, key, path, size=None, convert_alpha=True):
        img = pygame.image.load(path)
        img = img.convert_alpha() if convert_alpha else img.convert()

        if size:
            img = pygame.transform.smoothscale(img, size)

        self.images[key] = img
        return img

    def get_image(self, key):
        return self.images.get(key)

    def load_sound(self, key, path):
        try:
            snd = pygame.mixer.Sound(path)
            self.sounds[key] = snd
        except Exception:
            self.sounds[key] = DummySound()
        return self.sounds[key]

    def get_sound(self, key):
        return self.sounds.get(key, DummySound())