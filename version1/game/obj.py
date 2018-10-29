import pyglet
import random
from .resources import agent_image, obstacle_image

class GameObject(pyglet.sprite.Sprite):

    def __init__(self, img, window, *args, **kwargs):
        super(GameObject, self).__init__(img=img,*args, **kwargs)
        self.sx = 0
        self.sy = 0
        self.xlim, self.ylim = window.get_size()
        self.iw = img.width
        self.ih = img.height
        self.init_position()

    def set_position(self, x, y):
        if x < 0:
            x = 0
        if x+self.sx+self.iw > self.xlim:
            x = self.xlim-self.iw
        if y < 0:
            y = 0
        if y+self.sy+self.ih > self.ylim:
            y = self.ylim-self.ih
        self.position = x, y

    def init_position(self):
        pass

    def update_position(self, *args):
        pass

    def edge_state(self):
        left = int(self.x == 0)
        down = int(self.y == 0)
        right = int(self.x+self.iw == self.xlim)
        up = int(self.y+self.ih == self.ylim)
        return left, down, right, up

    def collide(self, another):
        points = [(self.x, self.y), (self.x+self.iw, self.y),
                  (self.x, self.y+self.ih), (self.x+self.iw, self.y+self.ih)]
        x_range = another.x, another.x + another.iw
        y_range = another.y, another.y + another.ih
        for p in points:
            if x_range[0] <= p[0] <= x_range[1] and y_range[0] <= p[1] <= y_range[1]:
                return True
        return False

class Obstacle(GameObject):

    step = 10

    def __init__(self, window, move=False, *args, **kwargs):
        super().__init__(img=obstacle_image, window=window, *args, **kwargs)
        self.move = move

    def init_position(self):
        self.set_position(random.randint(self.iw*2, self.xlim), random.randint(0, self.ylim))

    def update_position(self, *args):
        self.change_speed()
        x = self.x+self.sx
        y = self.y+self.sy
        self.set_position(x, y)

    def change_speed(self):
        if not self.move:
            return
        edge_state = self.edge_state()
        if not any(edge_state):
            f = random.randint(0, 8)
            if f == 0 or self.sx == self.sy == 0:
                self.sx = random.randint(-1, 1)*self.step
                self.sy = random.randint(-1, 1)*self.step
        else:
            if edge_state[0] == 1:
                self.sx = self.step
            if edge_state[1] == 1:
                self.sy = self.step
            if edge_state[2] == 1:
                self.sx = -self.step
            if edge_state[3] == 1:
                self.sy = -self.step

class Agent(GameObject):

    step = 20

    def __init__(self, window, *args, **kwargs):
        super().__init__(img=agent_image, window=window, *args, **kwargs)

    def init_position(self):
        self.set_position(0, self.ylim/2-self.ih/2)

    def update_position(self, cmd, *args):

        if cmd == 'RIGHT':
            self.set_position(self.x+self.step, self.y)
        if cmd == 'LEFT':
            self.set_position(self.x-self.step, self.y)
        if cmd == 'UP':
            self.set_position(self.x, self.y+self.step)
        if cmd == 'DOWN':
            self.set_position(self.x, self.y-self.step)
        if cmd == 'STAY':
            pass
