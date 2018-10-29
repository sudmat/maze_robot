import pyglet
from game.game import Game
from robot import get_robot
import sys

obs_num = 5
robot = 0
if len(sys.argv) >= 2:
    obs_num = int(sys.argv[1])
if len(sys.argv) >= 3:
    robot = int(sys.argv[2])

game_window = pyglet.window.Window()
g = Game(window=game_window, robot=get_robot(robot), obs_num=obs_num)

@game_window.event
def on_draw():
    g.draw()

if __name__ == '__main__':
    pyglet.app.run()