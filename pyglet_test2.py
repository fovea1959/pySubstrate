# https://stackoverflow.com/a/62948934

from pyglet import *
from pyglet.gl import *

key = pyglet.window.key


class collision():
    def rectangle(x, y, target_x, target_y, width=32, height=32, target_width=32, target_height=32):
        # Assuming width/height is *dangerous* since this library might give false-positives.
        if (x >= target_x and x < (target_x + target_width)) or ((x + width) >= target_x and (x + width) <= (target_x + target_width)):
            if (y >= target_y and y < (target_y + target_height)) or ((y + height) >= target_y and (y + height) <= (target_y + target_height)):
                return True
        return False

class GenericSprite(pyglet.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(255,255,255), batch=None, group=None):
        self.texture = pyglet.image.SolidColorImagePattern((*color, 255)).create_image(width, height)
        super(GenericSprite, self).__init__(self.texture, batch=batch, group=group)
        self.x = x
        self.y = y

    def change_color(self, r, g, b):
        self.texture = pyglet.image.SolidColorImagePattern((r, g, b, 255)).create_image(self.width, self.height)

class Block(GenericSprite):
    def __init__(self, x, y, batch, group):
        super(Block, self).__init__(x, y, 30, 30, color=(255, 255, 255), batch=batch, group=group)

class Player(GenericSprite):
    def __init__(self, x, y, batch, group):
        super(Player, self).__init__(x, y, 30, 30, color=(55, 255, 55), batch=batch, group=group)

class main(pyglet.window.Window):
    def __init__ (self, width=800, height=600, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)
        self.keys = {}
        self.status_labels = {}

        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.Group(0)
        self.foreground = pyglet.graphics.Group(1)

        self.player_obj = Player(40, 40, self.batch, self.foreground)
        self.status_labels['player_position'] = pyglet.text.Label(f'Player position: x={self.player_obj.x}, y={self.player_obj.y}, x+w={self.player_obj.x+self.player_obj.width}, y+h={self.player_obj.y+self.player_obj.height}', x=10, y=self.height-30, batch=self.batch, group=self.background)
        self.blocks = {}
        for index, i in enumerate(range(10, 120, 30)):
            self.blocks[i] = Block(i, 10, self.batch, self.background)
            self.status_labels[f'block{i+1}_position'] = pyglet.text.Label(f'Block #{index+1}: left={self.blocks[i].x}, bottom={self.blocks[i].y}, top={self.blocks[i].y+self.blocks[i].height}, right={self.blocks[i].x+self.blocks[i].width}', x=10, y=self.height-(50+(index*16)), batch=self.batch, group=self.background)

        self.alive = 1

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_key_release(self, symbol, modifiers):
        try:
            del self.keys[symbol]
        except:
            pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE: # [ESC]
            self.alive = 0

        self.keys[symbol] = True

    def render(self):
        self.clear()

        for key_down in self.keys:
            if key_down == key.D:
                self.player_obj.x += 1
            elif key_down == key.A:
                self.player_obj.x -= 1
            elif key_down == key.W:
                self.player_obj.y += 1
            elif key_down == key.S:
                self.player_obj.y -= 1

        self.status_labels['player_position'].text = f'Player position: x={self.player_obj.x}, y={self.player_obj.y}, x+w={self.player_obj.x+self.player_obj.width}, y+h={self.player_obj.y+self.player_obj.height}'
        for index, i in enumerate(range(10, 120, 30)):
            if collision.rectangle(self.player_obj.x, self.player_obj.y, self.blocks[i].x, self.blocks[i].y, width=30, height=30, target_width=30, target_height=30):
                # self.blocks[i].change_color(255,55,55)
                self.status_labels[f'block{i+1}_position'].color = (255,55,55,255)
            else:
                self.status_labels[f'block{i+1}_position'].color = (55,255,55,255)

        self.batch.draw()

        self.flip()

    def run(self):
        while self.alive == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()

if __name__ == '__main__':
    x = main()
    x.run()