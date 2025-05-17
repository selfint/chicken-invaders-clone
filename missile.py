from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.properties import *
from weapon import Weapon


class Missile(Weapon):

    source = StringProperty('source/missile.png')
    id = 'Missile'
    power = NumericProperty(30)
    size = 100, 100



