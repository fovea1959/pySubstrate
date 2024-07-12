import logging
import math
import random
import textwrap

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

import jsons


STEP = 0.42


class Crack:
    x: float
    y: float
    t: float

    xs: float
    ys: float
    t_inc: float

    curved: bool

    sand_color: tuple
    sand_p: float
    sand_g: float

    degrees_drawn: float

    crack_id: int

    x_start: float
    y_start: float
    cycle_start: int

    def __init__(self, crack_id=None):
        self.crack_id = crack_id

    def __eq__(self, other):
        return self.crack_id == other.crack_id


class Array2D:
    def __init__(self, n_rows=None, n_cols=None, initial_value=None):
        self._buf = []
        for _ in range(n_rows * n_cols):
            self._buf.append(initial_value)
        self._n_cols = n_cols
        self._n_rows = n_rows

    def __getitem__(self, *args):
        row, col = args[0][0], args[0][1]
        return self._buf[col + row * self._n_cols]

    def __setitem__(self, *args):
        row, col, value = args[0][0], args[0][1], args[1]
        self._buf[col + row * self._n_cols] = value

    def fill(self, value):
        for i in range(self._n_rows * self._n_cols):
            self._buf[i] = value


def hex_to_rgb(value):
    """
    https://stackoverflow.com/a/42011375

    Convert color`s value in hex format to RGB format.

    >>> hex_to_rgb('fff')
    (255, 255, 255)
    >>> hex_to_rgb('ffffff')
    (255, 255, 255)
    >>> hex_to_rgb('#EBF442')
    (235, 244, 66)
    >>> hex_to_rgb('#000000')
    (0, 0, 0)
    >>> hex_to_rgb('#000')
    (0, 0, 0)
    >>> hex_to_rgb('#54433f')
    (84, 67, 63)
    >>> hex_to_rgb('#f7efed')
    (247, 239, 237)
    >>> hex_to_rgb('#191616')
    (25, 22, 22)
    """

    if value[0] == '#':
        value = value[1:]

    len_value = len(value)

    if len_value not in [3, 6]:
        raise ValueError('Incorrect a value hex {}'.format(value))

    if len_value == 3:
        value = ''.join(i * 2 for i in value)
    return tuple(int(i, 16) for i in textwrap.wrap(value, 2))


@dataclass
class SubstrateParameters:
    height: int = 0
    width: int = 0
    initial_cracks: int = 3
    max_num: int = 0    # # of cracks
    circle_percent: int = 10
    fg_color: tuple[int, int, int] = (0, 0, 0)
    bg_color: tuple[int, int, int] = (255, 255, 255)
    parsed_colors: list[tuple[int, int, int]] = field(default_factory=lambda: [(128, 128, 128)])
    grains: int = 64
    max_cycles: Optional[int] = None
    wireframe: bool = False
    seamless: bool = False
    seed: Optional[tuple[int, tuple[int], Optional[int]]] = None

    def set_color_list(self, color_list=None):
        parsed_color_list = []
        if color_list is not None:
            for c in color_list:
                if type(c) is tuple:
                    parsed_color_list.append(c)
                elif type(c) is str:
                    parsed_color_list.append(hex_to_rgb(c))

        self.parsed_colors = parsed_color_list


class Substrate(ABC):
    next_crack_id: int
    cracks: list  # of cracks
    c_grid: Array2D  # of ints
    off_img: Array2D  # of pixels (RGB)
    max_cycles: int
    cycles: int
    initialized: bool
    quiesced: bool
    was_quiesced: bool
    next_crack_id_when_quiesced: Optional[int]
    logger: logging.Logger
    parameters: SubstrateParameters

    def __init__(self, parameters=None):
        self.parameters = parameters
        self.next_crack_id = 0
        self.cracks = []
        self.c_grid = Array2D(self.parameters.width, self.parameters.height, 10001)
        self.off_img = Array2D(self.parameters.width, self.parameters.height, self.parameters.bg_color)
        self.cycles = 0
        self.initialized = False
        self.quiesced = False
        self.was_quiesced = False
        self.next_crack_id_when_quiesced = None
        self.done = False
        self.logger = logging.getLogger('Substrate')

    def start_crack(self, cr: Crack):
        self.logger.info("Starting crack %d", cr.crack_id)
        found = False
        timeout = 0
        px = py = 0  # superfluous
        while not found and timeout < 10000:
            timeout = timeout + 1
            px = random.randint(0, self.parameters.width - 1)
            py = random.randint(0, self.parameters.height - 1)

            if self.c_grid[px, py] < 10000:
                found = True

        if not found:
            # we timed out, use default values
            px = cr.x
            py = cr.y

            if px < 0:
                px = 0
            if px >= self.parameters.width:
                px = self.parameters.width - 1

            if py < 0:
                py = 0
            if py >= self.parameters.height:
                py = self.parameters.height - 1

            self.c_grid[px, py] = cr.t

        old_a = a = self.c_grid[px, py]

        if random.choice([True, False]):
            a = a - 90 + random.uniform(-2, 2.1)  # (frand(4.1) - 2)
        else:
            a = a + 90 + random.uniform(-2, 2.1)  # (frand(4.1) - 2)

        if random.randint(0, 100) < self.parameters.circle_percent:
            cr.curved = True
            cr.degrees_drawn = 0

            r = 10 + (random.uniform(0, (self.parameters.width + self.parameters.height) / 2.0))
            if random.choice([True, False]):
                r = -r

            # arc length = r * theta => inc = theta = arc length / r
            radian_inc = STEP / r
            cr.t_inc = math.degrees(radian_inc)

            cr.ys = r * math.sin(radian_inc)
            cr.xs = r * (1 - math.cos(radian_inc))
        else:
            cr.curved = False

        cr.x_start = cr.x = px + (0.61 * math.cos(math.radians(a)))
        cr.y_start = cr.y = py + (0.61 * math.sin(math.radians(a)))
        cr.cycle_start = self.cycles
        cr.t = cr.t_start = a
        self.logger.debug("starting crack %d, starting from %s (angle %f), my angle %f",
                          cr.crack_id, (px, py), old_a, a)

    def make_crack(self):
        if len(self.cracks) < self.parameters.max_num and not self.quiesced:
            self.logger.debug("creating %d", self.next_crack_id)
            cr = Crack(crack_id=self.next_crack_id)
            self.next_crack_id += 1
            self.logger.debug("made crack = %d", cr.crack_id)
            self.cracks.append(cr)
            cr.sand_p = 0
            cr.sand_g = random.uniform(-0.01, 0.19)  # (frand(0.2) - 0.01)
            cr.sand_color = random.choice(self.parameters.parsed_colors)
            cr.curved = False
            cr.degrees_drawn = 0

            cr.x = random.randint(0, self.parameters.width - 1)
            cr.y = random.randint(0, self.parameters.height - 1)
            cr.t = random.uniform(0, 360)

            self.start_crack(cr)
        else:
            self.logger.debug("make_crack: done! next_crack_id %d, quiesced %s", self.next_crack_id, str(self.quiesced))

    def trans_point(self, x1, y1, myc, a):
        x1 = int(x1)
        y1 = int(y1)
        if 0 <= x1 < self.parameters.width and 0 <= y1 < self.parameters.height:
            if a >= 1.0:
                self.off_img[x1, y1] = myc
            else:
                o_r, o_g, o_b = self.off_img[x1, y1]
                r, g, b = myc
                n_r = o_r + (r - o_r) * a
                n_g = o_g + (g - o_g) * a
                n_b = o_b + (b - o_b) * a
                c = (n_r, n_g, n_b)
                self.off_img[x1, y1] = c
                return c
        return self.parameters.bg_color

    def region_color(self, cr: Crack):
        rx = float(cr.x)
        ry = float(cr.y)
        openspace = True

        while openspace:
            rx += (0.81 * math.sin(cr.t * math.pi/180))
            ry -= (0.81 * math.cos(cr.t * math.pi/180))

            cx = int(rx)
            cy = int(ry)
            if self.parameters.seamless:
                cx %= self.parameters.width
                cy %= self.parameters.height

            if 0 <= cx < self.parameters.width and 0 <= cy < self.parameters.height:
                if self.c_grid[cx, cy] > 10000:
                    pass
                else:
                    openspace = False
            else:
                openspace = False

        cr.sand_g += random.uniform(-0.050, 0.050)  # (frand(0.1) - 0.050)
        max_g = 1.0

        if cr.sand_g < 0:
            cr.sand_g = 0

        if cr.sand_g > max_g:
            cr.sand_g = max_g

        grains = self.parameters.grains

        w = cr.sand_g / (grains - 1)

        for i in range(grains):
            draw_x = (cr.x + (rx - cr.x) * math.sin(cr.sand_p + math.sin(float(i * w))))
            draw_y = (cr.y + (ry - cr.y) * math.sin(cr.sand_p + math.sin(float(i * w))))

            if self.parameters.seamless:
                draw_x = (draw_x + self.parameters.width) % self.parameters.width
                draw_y = (draw_y + self.parameters.height) % self.parameters.height

            c = self.trans_point(draw_x, draw_y, cr.sand_color, (0.1 - i / (grains * 10)))
            self.graphics_draw_point(int(draw_x), int(draw_y), c)

    def update(self):
        if not self.initialized:
            if self.parameters.seed is None:
                self.parameters.seed = random.getstate()
                self.logger.info("seed is %s, %s", type(self.parameters.seed), self.parameters.seed)
            else:
                random.setstate(self.parameters.seed)
            self.off_img.fill(self.parameters.bg_color)
            self.graphics_initialize()
            self.graphics_batch_start()
            self.graphics_draw_fill(self.parameters.bg_color)
            for _ in range(self.parameters.initial_cracks):
                self.make_crack()
            self.graphics_batch_end()
            self.initialized = True
        if self.quiesced and not self.was_quiesced:
            self.next_crack_id_when_quiesced = self.next_crack_id
            self.was_quiesced = True
        self.cycles += 1
        self.graphics_batch_start()
        for crack in list(self.cracks):
            self.move_draw_crack(crack)
        self.graphics_batch_end()
        if self.parameters.max_cycles is not None and self.parameters.max_cycles > 0:
            if self.cycles > self.parameters.max_cycles:
                self.done = True
        if len(self.cracks) == 0:
            self.done = True

    def crack_list(self):
        return tuple(cr.crack_id for cr in self.cracks)

    def move_draw_crack(self, cr: Crack):
        #  self.logger.debug("Crack %d start", cr.crack_id)
        old = (cr.x, cr.y)
        if not cr.curved:
            cr.x += float(STEP) * math.cos(cr.t * math.pi/180)
            cr.y += float(STEP) * math.sin(cr.t * math.pi/180)
        else:
            cr.x += cr.ys * math.cos(cr.t * math.pi/180)
            cr.y += cr.ys * math.sin(cr.t * math.pi/180)
            cr.x += cr.xs * math.cos(cr.t * math.pi/180 - math.pi/2)
            cr.y += cr.xs * math.sin(cr.t * math.pi/180 - math.pi/2)
            cr.t += cr.t_inc
            cr.degrees_drawn += abs(cr.t_inc)

        cx = int(cr.x + random.uniform(0.33, 0.66))  # (frand(0.66) - 0.33))
        cy = int(cr.y + random.uniform(0.33, 0.66))  # (frand(0.66) - 0.33))

        if self.parameters.seamless:
            # not sure if we needed to check for negative wrap?
            cx = (cx + self.parameters.width) % self.parameters.width
            cy = (cy + self.parameters.height) % self.parameters.height

        if 0 <= cx < self.parameters.width and 0 <= cy <= self.parameters.height:
            # draw sand painter if we are not wireframe
            if not self.parameters.wireframe:
                self.region_color(cr)

            # draw fg_color crack
            ccccc = self.parameters.fg_color
            """
            if cr.crack_id == 0:
                ccccc = (0, 255, 0)
            if cr.crack_id == 4:
                ccccc = (255, 0, 0)
            """
            self.off_img[cx, cy] = ccccc
            self.graphics_draw_point(cx, cy, ccccc)

            if cr.curved and cr.degrees_drawn > 360:
                self.logger.debug("Crack %d ending, 360 degree curve", cr.crack_id)
                # completed the circle
                # REWORK
                # self.start_crack(cr)
                self.kill_crack(cr)
                self.logger.debug("Crack list %s", str(self.crack_list()))
                # END REWORK
                self.make_crack()
                self.make_crack()
                self.logger.debug("Crack list %s", str(self.crack_list()))

            else:
                self.logger.debug("Crack %d (%s) was @ %s, now @ %s = %s",
                                  cr.crack_id, str(cr.t), old, (cx, cy), self.c_grid[cx, cy])
                if self.c_grid[cx, cy] > 10000 or (abs(self.c_grid[cx, cy] - cr.t) < 5):
                    # continue cracking
                    self.c_grid[cx, cy] = int(cr.t)
                elif abs(self.c_grid[cx, cy]) > 2:
                    self.logger.debug("Crack %d ending, c_grid > 2", cr.crack_id)
                    # REWORK
                    # self.start_crack(cr)
                    self.kill_crack(cr)
                    self.logger.debug("Crack list %s", str(self.crack_list()))
                    # end REWORK
                    self.make_crack()
                    self.make_crack()
                    self.logger.debug("Crack list %s", str(self.crack_list()))
                else:
                    self.logger.debug("Crack %d was funny", cr.crack_id)
        else:
            # out of bounds
            self.logger.debug("Crack %d was @ %s, now @ %s, out of bounds", cr.crack_id, old, (cx, cy))

            # REWORK
            # cr.x = random.randint(0, self.width-1)
            # cr.y = random.randint(0, self.height-1)
            # cr.t = random.uniform(0, 360.0)
            # self.start_crack(cr)
            self.kill_crack(cr)
            self.logger.debug("Crack list %s", str(self.crack_list()))
            # end REWORK

            self.make_crack()
            self.make_crack()
            self.logger.debug("Crack list %s", str(self.crack_list()))

    def kill_crack(self, cr: Crack = None, reason: dict = None):
        self.logger.info("Crack %d dying: start=%s, end=%s, length=%f, lifetime=%d", cr.crack_id,
                         (cr.x_start, cr.y_start), (cr.x, cr.y),
                         math.sqrt((cr.x_start - cr.x) ** 2 + (cr.y_start - cr.y) ** 2),
                         self.cycles - cr.cycle_start
                         )
        self.cracks.remove(cr)

    @abstractmethod
    def graphics_batch_start(self):
        pass

    @abstractmethod
    def graphics_batch_end(self):
        pass

    @abstractmethod
    def graphics_draw_point(self, x, y, color):
        pass

    @abstractmethod
    def graphics_draw_fill(self, color):
        pass

    @abstractmethod
    def graphics_initialize(self):
        pass
