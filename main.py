from kivy.app import App
from kivy.uix.widget import Widget

# from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

# from kivy.graphics.vertex_instructions import *
from kivy.graphics.context_instructions import *
from kivy.properties import *
from kivy.core.window import Window
from math import pow, sqrt
from kivy.uix.image import Image
from random import random, choice

from spaceship import Spaceship
from level import Level
from power import PowerUp
from food import Food
from present import Present
from missile import Missile

Window.fullscreen = "auto"
size = [2560, 1600]


class Game(Widget):

    b1x, b1y = NumericProperty(0), NumericProperty(0)
    b2x, b2y = NumericProperty(0), NumericProperty(0)
    spaceship = ObjectProperty(None)
    stage = NumericProperty(1)
    drop_rate = 20  # seconds
    keys = True

    # infrastructure

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        pressed_key = keycode[1]
        self.pressed_keys[pressed_key] = True
        if pressed_key == "q":
            self.drop(0)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        released_key = keycode[1]
        self.pressed_keys[released_key] = False
        return True

    # game

    def __init__(self):
        super(Game, self).__init__()
        self.b1x, self.b1y = 0, 0
        self.b2x, self.b2y = 0, 3200

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.pressed_keys = {
            "up": False,
            "down": False,
            "right": False,
            "left": False,
            "spacebar": False,
            "enter": False,
        }

        red_frq = 0.33
        green_frq = 0.33
        yellow_frq = 0.33
        self.presents = []
        for i in range(int(red_frq * 100)):
            self.presents.append("red")
        for i in range(int(green_frq * 100)):
            self.presents.append("green")
        for i in range(int(yellow_frq * 100)):
            self.presents.append("yellow")
        self.level = Level(size)
        self.eggs = []
        self.power_ups = []
        self.explosions = []
        self.explosion = Image()
        self.wait = False
        Clock.schedule_interval(self.drop, self.drop_rate / 1)

    def drop(self, dt):
        if random() < 0.7:
            p = PowerUp(pos=(100 + random() * (self.width - 100), self.height))
            self.add_widget(p)
            self.power_ups.append(p)
        else:
            kind = choice(self.presents)
            self.add_widget(Present(pos=(random() * self.width, 1600), kind=kind))

    def scroll_background(self, dt):
        increment = self.height / 200.0
        self.b1y -= increment
        self.b2y -= increment
        if self.b1y + self.height <= 0:
            self.b1y = self.b2y
        if self.b2y <= 0:
            self.b2y = self.height * 2

    def new_level(self, dt):
        self.stage += 1
        self.level.clear()
        self.level.new_level(self.stage)
        self.level.start()
        self.level.upload_to(self)
        self.wait = False

    def respawn(self):
        self.explosion = Image(
            source="source/explosion.gif",
            id="Ex",
            anim_delay=0,
            pos=(
                self.spaceship.x - self.spaceship.width / 2.0,
                self.spaceship.y - self.spaceship.height / 2.0,
            ),
            size=(self.spaceship.width * 5, self.spaceship.height * 5),
            anim_loop=1,
            allow_stretch=True,
            keep_data=False,
            color=(1, 1, 1, 1),
        )
        self.add_widget(self.explosion)
        self.spaceship.reset()
        Clock.schedule_once(self.clean, 0.6)
        self.spaceship.pos = self.width / 2.0, -self.height / 5.0
        self.canvas.ask_update()

    def add_widget(self, widget, index=0, canvas=None):
        super(Game, self).add_widget(widget)
        # print 'add', len(self.children), widget.id

    def remove_widget(self, widget):
        super(Game, self).remove_widget(widget)
        # print 'remove', len(self.children), widget.id

    def clean(self, dt):
        for child in self.children:
            if child.id == "Ex":
                self.remove_widget(child)

    def update(self, dt):
        self.canvas.ask_update()
        # autofire
        # self.pressed_keys['spacebar'] = True

        for child in self.children:
            if child.id == "Present":
                child.update()
                if distance(child.center, self.spaceship.center) < 100:
                    if self.spaceship.weapon == child.kind:
                        self.spaceship.power += 1
                    else:
                        self.spaceship.weapon = child.kind
                    self.remove_widget(child)

        if self.spaceship.food >= 100:
            self.spaceship.food -= 100
            self.spaceship.missiles += 1

        if self.spaceship not in self.children and self.spaceship.can_respawn:
            self.spaceship.pos = (self.width / 2, -100)
            self.add_widget(self.spaceship)

        else:
            if self.spaceship.can_respawn:
                self.spaceship.update(self.pressed_keys)

        if len(self.level.chickens) == 0 and not self.wait:
            self.wait = True
            self.add_widget(
                Label(
                    text="Level {}".format(self.stage + 1),
                    pos=(size[0] / 2.0, size[1] / 2.0),
                    font_size=50,
                    id="Level Label",
                )
            )
            Clock.schedule_once(self.new_level, 2)

        if not self.wait:
            for child in self.children:
                if child.id == "Level Label":
                    self.remove_widget(child)
        self.level.update()

        for shot in self.spaceship.shots:
            if shot not in self.children:
                self.add_widget(shot)
            shot.update()

        for child in self.children:
            if child.id == "Food":
                child.velocity_y -= 1
                child.update()
                if distance(child.pos, self.spaceship.pos) < 100:
                    self.remove_widget(child)
                    self.spaceship.food += child.amount
                if child.y <= -10:
                    if child.velocity_y < -1:
                        child.velocity_y *= -1
                        child.velocity_y /= 1.5
                    else:
                        self.remove_widget(child)

        for power_up in self.power_ups:
            power_up.update()
            if distance(power_up.center, self.spaceship.center) < 100:
                self.spaceship.power += 1
                self.remove_widget(power_up)
                self.power_ups.remove(power_up)

            if power_up.top < 0:
                self.remove_widget(power_up)
                self.power_ups.remove(power_up)

        if self.level.in_place:
            for chicken in self.level.chickens:
                e = chicken.lay_egg()
                if e:
                    if e not in self.children:
                        self.eggs.append(e)
                        self.add_widget(e)

        for egg in self.eggs:
            egg.update()
            if distance(egg.center, self.spaceship.center) < 100:
                if not self.spaceship.shield:
                    self.respawn()
                    self.remove_widget(egg)
                    self.eggs.remove(egg)

            if egg.top < 0:
                self.remove_widget(egg)
                self.eggs.remove(egg)

        else:
            self.level.start()

        for chicken in self.level.chickens:
            if distance(chicken.center, self.spaceship.center) < self.width / 15.0:
                if not self.spaceship.shield:
                    self.respawn()

        for shot in self.spaceship.shots:
            if shot.y > self.height:
                self.remove_widget(shot)
                self.spaceship.shots.remove(shot)

            if shot.id == "Weapon":
                for chicken in self.level.chickens:
                    dmg = False
                    # if shot.radius > 0:
                    if False:
                        if (
                            distance(chicken.center, shot.center)
                            < chicken.width / 2.0 + shot.height / 2.0
                        ):
                            dmg = True

                    elif (
                        distance(chicken.center, (shot.center[0], shot.top))
                        < chicken.width / 2.0 + shot.height / 2.0
                    ):
                        dmg = True
                    if dmg:
                        self.damage_chicken(chicken, shot)

            if shot.id == "Missile":
                if self.get_center_x() - 100 <= shot.x <= self.get_center_x() + 100:
                    if self.get_center_y() - 100 <= shot.y <= self.get_center_y() + 100:
                        self.remove_widget(shot)
                        self.spaceship.shots.remove(shot)
                        for child in self.children:
                            if child.id == "Chicken":
                                child.hp -= shot.power
                                if child.hp <= 0:
                                    self.remove_chicken(child)

        # constrain spaceship

        if self.spaceship.x <= 0:
            self.spaceship.x = 0

        if self.spaceship.right >= self.width:
            self.spaceship.right = self.width

        if self.spaceship.y <= 0:
            self.spaceship.y = 0

        if self.spaceship.top >= self.height:
            self.spaceship.top = self.height

    def damage_chicken(self, chicken, shot):

        if shot.power > 0:
            a = chicken.hp
            p = shot.power
            shot.power -= a
            chicken.hp -= p
            if chicken.hp <= 0:
                self.remove_chicken(chicken)
            if shot.power <= 0:
                if shot in self.spaceship.shots:
                    self.spaceship.shots.remove(shot)
                if shot in self.children:
                    self.remove_widget(shot)

        if shot.radius > 0:
            shot.power += 5
            shot.radius = 100 * shot.power
            shot.width -= p * 20
            shot.height -= p * 20
            shot.pos[0] += p * 10
            shot.pos[1] += p * 10

    def remove_chicken(self, chicken):
        self.spaceship.score += chicken.bhp * 100
        if chicken in self.children:
            self.remove_widget(chicken)
        if chicken in self.level.chickens:
            self.level.grid.remove(self.level.grid[self.level.chickens.index(chicken)])
            self.level.chickens.remove(chicken)
        for i in range(chicken.food):
            self.add_widget(
                Food(
                    center=chicken.center,
                    amount=1,
                    velocity_x=random() * 10 - 5,
                    velocity_y=random() * 10 - 5,
                )
            )


def distance(pos1, pos2):

    return sqrt(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2))


class MainApp(App):

    def build(self):
        game = Game()
        Clock.schedule_interval(game.scroll_background, 0)
        Clock.schedule_interval(game.update, 0)
        return game


MainApp().run()
