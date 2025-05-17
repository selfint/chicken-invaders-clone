from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.vector import Vector
from random import random, randint
from math import sin

from egg import Egg


class Chicken(Widget):

    velocity_x, velocity_y = NumericProperty(0), NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    speed = 20.0
    hp = NumericProperty(3)
    bhp = NumericProperty(3)
    a = NumericProperty(0)
    b = 0
    c = random() * 0.1 + 0.05
    egg_rate = 0.001
    eggs = 3
    food = NumericProperty(0)
    id = 'Chicken'
    source = StringProperty('source/boss.png')
    boss = BooleanProperty(False)

    def update(self, destination=None, direction=None):
        self.a = sin(self.b)
        self.b += self.c
        if not destination and direction:
            self.velocity = direction
            self.pos = Vector(*self.velocity) + self.pos
            self.canvas.ask_update()

        elif destination and not direction:
            self.velocity_x = (destination[0] - self.pos[0]) / self.speed

            if self.pos[1] > destination[1]:
                self.velocity_y = -(self.pos[1] - destination[1]) / self.speed
            else:
                self.velocity_y = (self.pos[1] - destination[1]) / self.speed

            self.pos = Vector(*self.velocity) + self.pos

    def lay_egg(self):
        if random() < self.egg_rate and self.eggs > 0:
            self.eggs -= 1
            return Egg(pos=(self.x + self.width / 2 - 20,
                            self.y))
        else:
            return None
