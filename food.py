from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.properties import *
from random import random


class Food(Widget):

    velocity_x, velocity_y = NumericProperty(0), NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    amount = NumericProperty(0)
    angle = NumericProperty(0)
    increment = random() * 5 + 1
    id = 'Food'

    def update(self):
        self.pos = Vector(*self.velocity) + self.pos
        self.angle += self.increment
