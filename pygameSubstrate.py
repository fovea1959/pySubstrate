import logging

from datetime import datetime

import PIL.Image
import PIL.PngImagePlugin
import pygame

from Substrate import Substrate

import jsons


class PygameSubstrate(Substrate):
    surface: pygame.Surface

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.info("__init__ %s", self)

    def graphics_draw_fill(self, color):
        logging.info("draw_fill %s", color)
        self.surface.fill(color)

    def graphics_draw_point(self, x, y, color):
        # logging.info("draw_point %d,%d %s", x, y, color)
        self.surface.set_at((x, y), color)

    def graphics_initialize(self):
        logging.info("initialize %s %s", self.parameters.width, self.parameters.height)
        self.surface = pygame.display.set_mode((self.parameters.width, self.parameters.height))


def save(substrate, substrate_parameters):
    buffer = pygame.image.tobytes(substrate.surface, 'RGB')
    pil_image = PIL.Image.frombytes('RGB',
                                    (substrate_parameters.width, substrate_parameters.height),
                                    buffer
                                    )
    pnginfo = PIL.PngImagePlugin.PngInfo()

    parameters_json = jsons.dumps(substrate_parameters, verbose=True)
    pnginfo.add_text("substrate_parameters", parameters_json)

    status = {
        "cycles": substrate.cycles,
        "next_crack_id_when_quiesced": substrate.next_crack_id_when_quiesced
    }
    status_json = jsons.dumps(status)
    pnginfo.add_text("substrate_status", status_json)

    pil_image.save('z.png', pnginfo=pnginfo)
    timestamp = datetime.now().strftime("%Y%m%d%Y-%H%M%S")
    pil_image.save(f'{timestamp}.png', pnginfo=pnginfo)

    with open(f'{timestamp}.json', 'w') as f:
        f.write(jsons.dumps({"parameters": substrate_parameters, "status": status}, verbose=True))


def run(substrate_parameters=None):
    substrate = PygameSubstrate(parameters=substrate_parameters)

    pygame.init()
    substrate.update()  # prime the pump
    need_to_exit = False
    paused = False
    was_done = False
    while not need_to_exit:
        step = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                need_to_exit = True
            elif event.type == pygame.TEXTINPUT:
                logging.debug("event %s", event)
                keystroke = event.dict.get('text', '').lower()
                if keystroke == 'p':
                    paused = not paused
                if keystroke == 'q':
                    substrate.quiesced = True
                if keystroke == 's':
                    save(substrate, substrate_parameters)
                if keystroke == ' ':
                    step = True
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                pass
            else:
                pass
        if not paused:
            step = True
        if step and not substrate.done:
            # substrate.done = True
            substrate.update()
            logging.debug("-- cycles=%d cracks=%d %s", substrate.cycles, len(substrate.crack_list()),
                          substrate.crack_list())
        if not was_done and substrate.done:
            save(substrate, substrate_parameters)
            was_done = True
        # logging.debug("updating pygame")
        pygame.display.update()
