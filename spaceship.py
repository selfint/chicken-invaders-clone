from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.vector import Vector
from kivy.clock import Clock
from random import random

from weapon import *
from missile import Missile


class Spaceship(Widget):

    # physics
    velocity_x, velocity_y = NumericProperty(0), NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    shield = NumericProperty(1)

    # engine and speed limits, and commands
    commands = {}
    engine = NumericProperty(0)
    limit = 10
    speed = 3

    # spaceship properties, for the game
    food = NumericProperty(0)
    missiles = NumericProperty(5)
    ###########################################
    # power
    power = NumericProperty(1)

    heat = NumericProperty(0)
    score = NumericProperty(0)
    lives = NumericProperty(5)
    weapon_cooldown = 0
    fired_missile = False

    # explosion animation
    can_respawn = True
    time1 = 0
    time2 = 0

    # weapon
    default_kind = 'green'
    weapon = default_kind
    shots = []
    upgraded_weapon = {'green': 'greenb'}
    fired_weapon = False

    # enable cheats
    cheats = False

    def update(self, pressed_keys):
            self.commands = pressed_keys
            if self.shield > 0.05:
                if not self.cheats:
                    self.shield -= 0.005
            else:
                self.shield = 0

            if self.heat > 2:
                self.heat -= 2
            else:
                self.heat = 0

            if self.cheats:
                self.heat = 0

            if self.weapon_cooldown > 2:
                self.weapon_cooldown -= 2
            else:
                self.weapon_cooldown = 0

            if pressed_keys['up']:
                self.velocity_y += self.speed

            elif pressed_keys['down']:
                self.velocity_y += -self.speed

            if pressed_keys['right']:
                self.velocity_x += self.speed

            elif pressed_keys['left']:
                self.velocity_x += -self.speed

            if pressed_keys['spacebar']:
                self.shoot()

            else:
                self.fired_weapon = False

            if pressed_keys['enter']:
                self.fire_missile()

            else:
                self.fired_missile = False

            friction = 0.3

            if self.velocity_x > 0.5:
                self.velocity_x -= friction
                if self.velocity_x > self.limit:
                    self.velocity_x = self.limit

            elif self.velocity_x < -0.5:
                self.velocity_x += friction
                if self.velocity_x < -self.limit:
                    self.velocity_x = -self.limit

            else:
                self.velocity_x = 0

            if self.velocity_y > 0.5:
                self.velocity_y -= friction
                if self.velocity_y > self.limit:
                    self.velocity_y = self.limit

            elif self.velocity_y < -0.5:
                self.velocity_y += friction
                if self.velocity_y < -self.limit:
                    self.velocity_y = -self.limit

            else:
                self.velocity_y = 0

            self.pos = Vector(*self.velocity) + self.pos
            self.engine = 2 + self.velocity_y / 10.0

    def shoot(self):
        # cool weapon
        if self.heat >= 400:
            self.weapon_cooldown = self.heat

        # actually shoot
        if self.weapon_cooldown == 0:
            self.velocity_y -= 5
            self.pos[1] -= 15

            shots = self.get_shot(self.weapon, self.power)
            self.fired_weapon = True
            for shot in shots:
                shot.velocity_y = 15
                self.shots.append(shot)

    def fire_missile(self):
        if self.missiles > 0 and not self.fired_missile:
            if not self.fired_missile:
                self.missiles -= 1
                self.fired_missile = True
                missile = Missile()
                missile.center = self.center
                if missile.x > 1200:
                    missile.velocity_x = (2560 / 2 - missile.x) / 100.0
                else:
                    missile.velocity_x = (2560 / 2 - missile.x) / 100.0

                if missile.y > 800:
                    missile.velocity_y = (800 - missile.y) / 100.0
                else:
                    missile.velocity_y = (800 - missile.y) / 100.0
                self.shots.append(missile)

    def get_shot(self, kind, power):
        if kind == 'green':
            if self.fired_weapon:
                self.weapon_cooldown = 40
                self.heat += 50
            else:
                self.weapon_cooldown = 20
                self.heat += 30
            shot_power = 1
            if power >= 6:
                shot_power += power / 5
            if power >= 5:
                a = Weapon()
                b = Weapon()
                c = Weapon()
                d = Weapon()
                e = Weapon()
                a.width *= 2
                a.height *= 2
                b.width *= 2
                b.height *= 2
                c.width *= 2
                c.height *= 2
                a.pos = self.pos[0] + 20 , self.top - 50
                b.pos = self.pos[0] + 45 , self.top - 25
                c.pos = self.pos[0] + 70 , self.top - 10
                d.pos = self.pos[0] + 95 , self.top - 25
                e.pos = self.pos[0] + 120, self.top - 50
                a.power = shot_power + 1
                b.power = shot_power + 1
                c.power = shot_power + 1
                d.power = shot_power
                e.power = shot_power

                a.update_source(kind)
                b.update_source(self.upgraded_weapon[kind])
                c.update_source(self.upgraded_weapon[kind])
                d.update_source(self.upgraded_weapon[kind])
                e.update_source(kind)
                return [a, b, c, d, e]

            elif power >= 4:
                a = Weapon()
                b = Weapon()
                c = Weapon()
                c.width *= 2
                c.height *= 2
                a.pos = self.pos[0] + 30, self.top - 25
                b.pos = self.pos[0] + 105, self.top - 25
                c.pos = self.pos[0] + 67.5, self.top - 10
                a.power = shot_power
                b.power = shot_power
                c.power = shot_power * 2
                a.update_source(kind)
                b.update_source(kind)
                c.update_source(self.upgraded_weapon[kind])
                return [a, b, c]

            elif power >= 3:
                a = Weapon()
                b = Weapon()
                c = Weapon()
                a.pos = self.pos[0] + 30, self.top - 25
                b.pos = self.pos[0] + 105, self.top - 25
                c.pos = self.pos[0] + 67.5, self.top - 10
                a.power = shot_power
                b.power = shot_power
                c.power = shot_power
                a.update_source(kind)
                b.update_source(kind)
                c.update_source(kind)
                return [a, b, c]
            elif power >= 2:
                a = Weapon()
                b = Weapon()
                a.pos = self.pos[0] + 40, self.top - 25
                b.pos = self.pos[0] + 95, self.top - 25
                a.power = shot_power
                b.power = shot_power
                a.update_source(kind)
                b.update_source(kind)
                return [a, b]

            elif power >= 1:
                a = Weapon()
                a.pos = self.pos[0] + 67.5, self.top - 10
                a.power = shot_power
                a.update_source(kind)
                return [a]

        if kind == 'red':
            if self.fired_weapon:
                self.weapon_cooldown = 40
                self.heat += 60
            else:
                self.weapon_cooldown = 20
                self.heat += 40
            shot_power = 1
            if power >= 5:
                shot_power += power / 5
            if power >= 4:
                a = Weapon()
                b = Weapon()
                c = Weapon()
                a.pos = self.pos[0] + 30, self.top - 10
                b.pos = self.pos[0] + 67.5, self.top - 5
                c.pos = self.pos[0] + 105, self.top - 10
                a.power = shot_power
                a.velocity_x = -3
                b.power = shot_power
                c.velocity_x = 3
                c.power = shot_power
                a.update_source(kind)
                b.update_source(kind)
                c.update_source(kind)
                return [a, b, c]
            elif power >= 3:
                a = Weapon()
                b = Weapon()
                c = Weapon()
                a.pos = self.pos[0] + 30, self.top - 10
                b.pos = self.pos[0] + 67.5, self.top - 5
                c.pos = self.pos[0] + 105, self.top - 10
                a.power = shot_power
                b.power = shot_power
                c.power = shot_power
                a.update_source(kind)
                b.update_source(kind)
                c.update_source(kind)
                return [a, b, c]
            elif power >= 2:
                a = Weapon()
                b = Weapon()
                a.pos = self.pos[0] + 30, self.top - 10
                b.pos = self.pos[0] + 105, self.top - 10
                a.power = shot_power
                b.power = shot_power
                a.update_source(kind)
                b.update_source(kind)
                return [a, b]
            elif power >= 1:
                a = Weapon()
                a.pos = self.pos[0] + 67.5, self.top - 10
                a.power = shot_power
                a.update_source(kind)
                return [a]

        if kind == 'yellow':
            if self.fired_weapon:
                self.weapon_cooldown = 200
                self.heat += 300
            else:
                self.weapon_cooldown = 150
                self.heat += 250
            shot_power = 1
            if power >= 2:
                shot_power += power / 2
            if power >= 10:
                a = Weapon()
                b = Weapon()
                c = Weapon()
                a.pos = self.pos[0] + 30, self.top - 10
                b.pos = self.pos[0] + 67.5, self.top - 10
                c.pos = self.pos[0] + 105, self.top - 10
                a.power = shot_power
                a.velocity_x = -3
                b.power = shot_power
                c.power = shot_power
                c.velocity_x = 3
                a.update_source(kind)
                b.update_source(kind)
                c.update_source(kind)
                return [a, b, c]

            elif power >= 5:
                a = Weapon()
                c = Weapon()
                a.pos = self.pos[0] + 30, self.top - 10
                c.pos = self.pos[0] + 105, self.top - 10
                a.power = shot_power
                a.velocity_x = -3
                c.power = shot_power
                c.velocity_x = 3
                a.update_source(kind)
                c.update_source(kind)
                return [a, c]

            elif power >= 1:
                a = Weapon()
                a.pos = self.pos[0] + 67.5, self.top - 10
                a.width *= 2
                a.height *= 2
                a.power = shot_power
                a.update_source(kind)
                return [a]

    def reset(self):
        if self.power > 1:
            self.power -= 1
        self.shield = 1
        Clock.schedule_once(self.explode, 1)
        self.can_respawn = False
        if not self.cheats:
            self.lives -= 1

    def explode(self, dt):
        self.can_respawn = True
