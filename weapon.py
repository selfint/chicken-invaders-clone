from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.vector import Vector
from kivy.graphics.vertex_instructions import *
from math import atan, pi


class Weapon(Widget):

    kind = StringProperty("")
    source = StringProperty("source/{}.png".format(kind))
    power = NumericProperty(1)
    radius = NumericProperty(0)

    velocity_x, velocity_y = NumericProperty(0), NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    width, height = NumericProperty(0), NumericProperty(0)
    size = ReferenceListProperty(width, height)

    angle = NumericProperty(0)
    acc = NumericProperty(1.0005)

    ids = {"Weapon": True}

    def update(self):
        self.velocity_x *= self.acc
        self.velocity_y *= self.acc
        if self.velocity_x > 0:
            self.angle = atan(float(self.velocity_y) / self.velocity_x) * 180 / pi - 90
        elif self.velocity_x < 0:
            self.angle = atan(float(self.velocity_y) / self.velocity_x) * 180 / pi + 90
        else:
            self.angle = 0
        self.pos = Vector(*self.velocity) + self.pos

        if self.radius > 0:
            if self.width < self.radius / 2.0:
                self.width += self.power * 2
                self.height += self.power * 2
                self.pos[0] -= self.power * 1
                self.pos[1] -= self.power * 1

    def update_source(self, kind):
        self.source = "source/{}.png".format(kind)
        self.kind = kind
        if kind == "green" or kind == "greenb":
            self.resize(34, 102)
            self.acc = 1.01

        if kind == "red":
            self.resize(34, 75)
            self.acc = 1.02

        if kind == "yellow":
            self.resize(70, 70)
            self.acc = 1
            self.radius = 300 * self.power

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.size = width, height
