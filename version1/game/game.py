import pyglet
from pyglet.window import key
from .obj import Agent, Obstacle

class Game:

    labels = {0: ('Pause', (255, 255, 255, 255)),
              -1:('Fail', (255, 0, 0, 255)),
              1: ('On Going', (0, 255, 127, 255)),
              2: ('Win', (255, 255, 0, 255))}

    def __init__(self, window, robot, obs_num=4, size=None):
        self.window = window
        self.state = 0
        self._lock_space = False
        self._lock_reset = False
        self.obs_num = obs_num
        self.size = size
        self.agent = None
        self.state_label = None
        self.spec = None
        self.exit = None
        self.robot = robot
        self.obstacles = []
        self.key_handler = key.KeyStateHandler()
        self.obs_batch = None
        self.clock = 0
        self.last_move = 'STAY'
        self.window.push_handlers(self.key_handler)
        pyglet.clock.schedule_interval(self.update, 0.1)
        self.initiate()

    def draw(self):
        self.window.clear()
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', tuple(self.exit)))
        self.agent.draw()
        self.obs_batch.draw()
        self.state_label.draw()
        self.spec.draw()

    def initiate(self):
        self.obs_batch = pyglet.graphics.Batch()
        self.agent = Agent(window=self.window)
        self.obstacles = []
        for i in range(self.obs_num):
            self.obstacles.append(
                Obstacle(self.window, batch=self.obs_batch, move=True)
            )
        xl, yl = self.window.get_size()
        self.spec = pyglet.text.Label(text='Space for pause or continue, R for restart',
                                 x=xl/2, y=0, anchor_x='center')
        exit_width = self.agent.iw
        exit_height = 1.5*self.agent.ih
        self.exit = [xl-exit_width, (yl-exit_height)/2, xl-exit_width, (yl+exit_height)/2,
                     xl, (yl+exit_height)/2, xl, (yl-exit_height)/2]
        self.set_state(0)

    def set_state(self, state):
        win_size = self.window.get_size()
        self.state = state
        self.state_label = pyglet.text.Label(text=self.labels[state][0],
                                       x=win_size[0] / 2, y=win_size[1] - 25, anchor_x='center',
                                       color=self.labels[state][1])

    def dead(self):
        for obs in self.obstacles:
            if self.agent.collide(obs):
                return True
        return False

    def win(self):
        return (self.exit[1] <= self.agent.y) \
               and (self.agent.y+self.agent.ih<= self.exit[3])\
               and (self.agent.x+self.agent.iw >= self.exit[-2]) \
               and (self.key_handler[key.RIGHT] or self.last_move == 'RIGHT')

    def cur_state(self):
        key_board_input = {'RIGHT': self.key_handler[key.RIGHT],
                           'LEFT': self.key_handler[key.LEFT],
                           'UP': self.key_handler[key.UP],
                           'DOWN': self.key_handler[key.DOWN],
                           }
        agent_info = {'position': self.agent.position, 'size': (self.agent.iw, self.agent.ih)}
        obstacle_info = []
        for obs in self.obstacles:
            cur = {'position': obs.position, 'size': (obs.iw, obs.ih),
                   'speed': (obs.sx, obs.sy)}
            obstacle_info.append(cur)
        return {'input': key_board_input, 'state': self.state, 'agent':agent_info, 'obstacles':obstacle_info}

    def update(self, dt):
        self.clock += 1
        if self.dead():
            self.set_state(-1)
        if self.win():
            self.set_state(2)
        if self.key_handler[key.R] and self.state != 1 and not self._lock_reset:
            self.initiate()
            self._lock_reset = True
        if not self.key_handler[key.R]:
            self._lock_reset = False
        if not self.key_handler[key.SPACE]:
            self._lock_space = False
        if self.key_handler[key.SPACE] and self.state not in {-1,2} and not self._lock_space:
            self._lock_space = True
            self.set_state(1 - self.state)
        if self.state == 1:
            cmd = self.robot.next_move(self.cur_state())
            self.last_move = cmd
            self.agent.update_position(cmd)
            for obs in self.obstacles:
                obs.update_position()
