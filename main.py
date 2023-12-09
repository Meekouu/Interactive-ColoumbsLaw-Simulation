import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions

# Create a Pyglet window
window = pyglet.window.Window(800, 600, "Physics Simulation")

# Create a Pymunk space
space = pymunk.Space()
space.gravity = 0, -1000  # Set the gravity (adjust as needed)

# Create a dynamic body
body = pymunk.Body(1, 1666)  # Mass and moment of inertia
body.position = 400, 500  # Initial position
shape = pymunk.Circle(body, 30)  # Create a circle shape
space.add(body, shape)  # Add body and shape to the space

# Set up drawing options
options = DrawOptions()

# Pyglet update function
@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)

# Pyglet update function
def update(dt):
    space.step(1 / 60)  # Step the simulation forward

# Schedule the update function
pyglet.clock.schedule_interval(update, 1 / 60)

# Run the Pyglet application
pyglet.app.run()
