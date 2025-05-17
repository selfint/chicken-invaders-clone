from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.vector import Vector


class PowerUp(Widget):

    velocity_x, velocity_y = NumericProperty(0), NumericProperty(-5)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    id = 'PowerUP'

    def update(self):
        self.pos = Vector(*self.velocity) + self.pos


