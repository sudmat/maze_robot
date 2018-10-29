from .manual_robot import *
from .naive_robot import *

def get_robot(code):
    if code == 0:
        return ManualRobot()
    if code == 1:
        return NaiveRobot()
    else:
        raise RuntimeError('Unknown robot: %s'%code)