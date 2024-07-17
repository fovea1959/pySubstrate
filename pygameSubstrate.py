import logging

from datetime import datetime

import PIL.Image
import PIL.PngImagePlugin
import pygame
import pygame_gui

from Substrate import Substrate

import jsons


class PygameSubstrate(Substrate):
    surface: pygame.Surface
    window_surface: pygame.Surface
    form_surface: pygame.Surface
    manager: pygame_gui.UIManager
    show_form: bool

    def __init__(self, **kwargs):
        logging.info("__init__ %s", self)
        super().__init__(**kwargs)
        self.show_form = False

    def graphics_batch_start(self):
        pass

    def graphics_batch_end(self):
        # logging.debug("updating pygame")
        pygame.display.update()

    def graphics_draw_fill(self, color):
        logging.info("draw_fill %s", color)
        self.surface.fill(color)

    def graphics_draw_point(self, x, y, color):
        # logging.info("draw_point %d,%d %s", x, y, color)
        self.surface.set_at((x, y), color)

    def graphics_initialize(self):
        logging.info("initialize %s %s", self.parameters.width, self.parameters.height)
        self.window_surface = pygame.display.set_mode((self.parameters.width, self.parameters.height))
        self.surface = pygame.Surface((self.parameters.width, self.parameters.height))

    def update(self):
        super().update()
        self.window_surface.blit(self.surface, (0, 0))
        if self.show_form:
            self.manager.draw_ui(self.form_surface)
            self.window_surface.blit(self.form_surface, (0, 0))


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


def transparent_surface(size, alpha, color=(0, 0, 0)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((color[0], color[1], color[2], alpha))
    return surf


def run(substrate_parameters=None):
    substrate = PygameSubstrate(parameters=substrate_parameters)

    pygame.init()

    substrate.update()  # prime the pump

    substrate.form_surface = transparent_surface((640, 480), 0x80, (128, 128, 128))
    substrate.manager = pygame_gui.UIManager((640, 480))
    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                                text='Say Hello',
                                                manager=substrate.manager)

    need_to_exit = False
    paused = False
    was_done = False
    clock = pygame.time.Clock()

    while not need_to_exit:
        time_delta = clock.tick(60) / 1000.0
        step = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                need_to_exit = True
            elif event.type == pygame.KEYDOWN:
                key = event.dict.get('key', None)
                if key == 27:
                    need_to_exit = True
            elif event.type == pygame.TEXTINPUT:
                logging.debug("event %s", event)
                keystroke = event.dict.get('text', '').lower()
                if keystroke == 'p':
                    paused = not paused
                elif keystroke == 'q':
                    substrate.quiesced = True
                elif keystroke == 's':
                    save(substrate, substrate_parameters)
                elif keystroke == ' ':
                    step = True
                elif keystroke == '?':
                    substrate.show_form = not substrate.show_form
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                pass
            else:
                pass
            substrate.manager.process_events(event)
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
        substrate.manager.update(time_delta)

