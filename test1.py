import logging
import pygame
from Substrate import Substrate


class MySubstrate(Substrate):
    surface: pygame.Surface

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.info("__init__ %s", self)

    def graphics_draw_fill(self, color):
        logging.info("draw_fill %s", color)
        self.surface.fill(color)

    def graphics_draw_point(self, x, y, color):
        logging.info("draw_point %d,%d %s", x, y, color)
        self.surface.set_at((x, y), color)

    def graphics_initialize(self):
        logging.info("initialize %s %s", self.width, self.height)
        self.surface = pygame.display.set_mode((self.width, self.height))


def main():
    logging.basicConfig(level=logging.DEBUG)

    pygame.init()

    substrate = MySubstrate(height=400, width=400, bg_color=(255, 0, 0))
    substrate.wireframe = True

    while not substrate.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                substrate.done = True
        substrate.update()
        logging.debug("updating pygame")
        pygame.display.update()



if __name__ == '__main__':
    main()
