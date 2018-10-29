import pyglet
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

agent_image = pyglet.resource.image("agent.png")
obstacle_image = pyglet.resource.image("obstacle.png")
