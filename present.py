from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.properties import *


class Present(Widget):

    velocity_x, velocity_y = NumericProperty(0), NumericProperty(-4)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    kind = StringProperty('red')
    source = StringProperty('source/{} present.png'.format(kind))
    id = 'Present'

    def update(self):
        self.pos = Vector(*self.velocity) + self.pos
        self.source = 'source/{} present.png'.format(self.kind)
