import logging
import math
import random

from abc import ABC, abstractmethod
from dataclasses import dataclass


STEP=0.42


@dataclass
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

    crack_num: int # not sure this is needed

    def __init__(self, number):
        self.crack_num = number


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


@dataclass
class Substrate(ABC):
    height: int
    width: int
    initial_cracks: int
    max_num: int    # # of cracks?
    grains: int
    circle_percent: int
    fg_color: tuple
    bg_color: tuple
    cracks: list # of cracks
    c_grid: Array2D # of ints
    off_img: Array2D # of pixels (RGB)
    parsed_colors: list # of RGBA
    max_cycles: int
    cycles: int
    wireframe: bool
    seamless: bool
    initialized: bool
    quiesced : bool
    logger: logging.Logger

    def __init__(self, height=None, width=None, initial_cracks=3, max_num=100, fg_color=(0, 0, 0), bg_color=(255, 255, 255)):
        self.height = height
        self.width = width
        self.initial_cracks = initial_cracks
        self.max_num = max_num
        self.grains = 0
        self.circle_percent = 0
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.cracks = []
        self.c_grid = Array2D(width, height, 10001)
        self.off_img = Array2D(width, height, self.bg_color)
        self.parsed_colors = [(0, 255, 0)]
        self.max_cycles = 0
        self.cycles = 0
        self.wireframe = False
        self.seamless = False
        self.seed = None
        self.initialized = False
        self.quiesced = False
        self.done = False
        self.logger = logging.getLogger('Substrate')

    def start_crack(self, cr: Crack):
        self.logger.info ("Starting crack %d", cr.crack_num)
        found = False
        timeout = 0
        px = py = 0 # superfluous
        while not found and timeout < 10000:
            timeout = timeout + 1
            px = random.randint(0, self.width-1)
            py = random.randint(0, self.height-1)

            if self.c_grid[px,py] < 10000:
                found = True

        if not found:
            # we timed out, use default values
            px = cr.x
            py = cr.y

            if px < 0:
                px = 0
            if px >= self.width:
                px = self.width-1

            if py < 0:
                py = 0
            if py >= self.height:
                py = self.height - 1

            self.c_grid[px, py] = cr.t

        a = self.c_grid[px, py]

        if random.choice([True, False]):
            a = a - 90 * random.uniform(-2, 2.1) # (frand(4.1) - 2)
        else:
            a = a + 90 * random.uniform(-2, 2.1) # (frand(4.1) - 2)

        if random.randint(0, 100) < self.circle_percent:
            cr.curved = True
            cr.degrees_drawn = 0

            r = 10 + (random.uniform(0, (self.width + self.height) / 2.0))
            if random.choice([True, False]):
                r = -r

            # arc length = r * theta => inc = theta = arc length / r
            radian_inc = STEP / r
            cr.t_inc = math.degrees(radian_inc)

            cr.ys = r * math.sin(radian_inc)
            cr.xs = r * (1 - math.cos(radian_inc))
        else:
            cr.curved = False

        cr.x = px + (0.61 * math.cos(math.radians(a)))
        cr.y = py + (0.61 * math.sin(math.radians(a)))
        cr.t = a

    def make_crack(self):
        if len(self.cracks) < self.max_num and not self.quiesced:
            cr = Crack(len(self.cracks))
            self.logger.debug("made crack = %d", cr.crack_num)
            self.cracks.append(cr)
            cr.sand_p = 0
            cr.sand_g = random.uniform(-0.01, 0.19) # (frand(0.2) - 0.01)
            cr.sand_color = random.choice(self.parsed_colors)
            cr.curved = False
            cr.degrees_drawn = 0

            cr.x = random.randint(0, self.width-1)
            cr.y = random.randint(0, self.height-1)
            cr.t = random.uniform(0, 360)

            self.start_crack(cr)

    def trans_point(self, x1, y1, myc, a):
        if 0 <= x1 < self.width and 0 <= y1 < self.height:
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
        return self.bg_color

    def region_color (self, cr: Crack):
        rx = float(cr.x)
        ry = float(cr.y)
        openspace = True

        while openspace:
            rx += (0.81 * math.sin(cr.t * math.pi/180))
            ry -= (0.81 * math.cos(cr.t * math.pi/180))

            cx = int(rx)
            cy = int(ry)
            if self.seamless:
                cx %= self.width
                cy %= self.height

            if 0 <= cx < self.width and 0 <= cy < self.height:
                if self.c_grid[cx, cy] > 10000:
                    pass
                else:
                    openspace = False
            else:
                openspace = False

        cr.sand_g += random.uniform (-0.050, 0.050) # (frand(0.1) - 0.050)
        max_g = 1.0

        if cr.sand_g < 0:
            cr.sand_g = 0

        if cr.sand_g > max_g:
            cr.sand_g = max_g

        grains = self.grains

        w = cr.sand_g / (grains - 1)

        for i in range(grains):
            draw_x = (cr.x + (rx - cr.x) * math.sin(cr.sand_p + math.sin(float (i * w))))
            draw_y = (cr.y + (ry - cr.y) * math.sin(cr.sand_p + math.sin(float (i * w))))

            if self.seamless:
                draw_x = (draw_x + self.width) % self.width
                draw_y = (draw_y + self.height) % self.height

            c = self.trans_point(draw_x, draw_y, cr.sand_color, (0.1 - i / (grains * 10)))
            self.graphics_draw_point(draw_x, draw_y, c)

    def update(self):
        if not self.initialized:
            self.off_img.fill(self.bg_color)
            self.graphics_initialize()
            self.graphics_draw_fill(self.bg_color)
            for _ in range(self.initial_cracks):
                self.make_crack()
            self.initialized = True
        for i in range(len(self.cracks)):
            self.move_draw_crack(self.cracks[i])
        self.cycles += 1
        if self.max_cycles is not None and self.max_cycles > 0 and self.cycles > self.max_cycles:
            self.done = True

    def move_draw_crack(self, cr: Crack):
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

        cx = int(cr.x + random.uniform(0.33, 0.66)) # (frand(0.66) - 0.33))
        cy = int(cr.y + random.uniform(0.33, 0.66)) # (frand(0.66) - 0.33))

        if self.seamless:
            cx = (cx + self.width) % self.width    # not sure if we needed to check for negative wrap?
            cy = (cy + self.height) % self.height

        if 0 <= cx < self.width and 0 <= cy <= self.height:
            # draw sand painter if we are not wireframe
            if not self.wireframe:
                self.region_color(cr)

            # draw fg_color crack
            self.off_img[cx,cy] = self.fg_color
            self.graphics_draw_point(cx, cy, self.fg_color)

            if cr.curved and cr.degrees_drawn > 360:
                # completed the circle
                self.start_crack(cr)
                self.make_crack()
            else:
                if self.c_grid[cx,cy] > 10000 or (abs(self.c_grid[cx,cy] - cr.t) < 5):
                    # continue cracking
                    self.c_grid[cx,cy] = cr.t
                elif abs(self.c_grid[cx,cy] > 2):
                    self.start_crack(cr)
                    self.make_crack()
        else:
            # out of bounds
            cr.x = random.randint(0, self.width-1)
            cr.y = random.randint(0, self.height-1)
            cr.t = random.uniform(0, 360.0)
            self.start_crack(cr)
            self.make_crack()
            
    @abstractmethod
    def graphics_draw_point(self, x, y, color):
        pass

    @abstractmethod
    def graphics_draw_fill(self, color):
        pass

    @abstractmethod
    def graphics_initialize(self):
        pass
