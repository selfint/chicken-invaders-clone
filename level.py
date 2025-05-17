from chicken import Chicken
from random import randint, random


class Level:

    speed = Chicken.speed

    def __init__(self, screen_size):
        self.chickens = []
        self.direction = 1
        self.grid = []
        self.screen_size = screen_size
        self.level = 0
        self.in_place = False
        self.boss_level = False
        self.direction = -self.speed / 10.0, 0

    def new_level(self, level):
        self.level = level

        if self.level % 5 == 0:
            self.grid.append([self.screen_size[0] / 2.0, self.screen_size[1] / 2.0])
            self.boss_level = True
        else:
            for i in range(1, 7):
                for j in range(3, 6):
                    self.grid.append([250 + 250 * i, 250 * j])
            self.boss_level = False

    def upload_to(self, target):
        a = random()
        if a < 0.5:
            red = True
        else:
            red = False
        for chicken in self.chickens:
            if chicken not in target.children:
                target.add_widget(chicken)
                if red:
                    chicken.source = 'source/chicken2.png'
                else:
                    chicken.source = 'source/chicken1.png'

                if chicken.boss:
                    chicken.source = 'source/boss.png'
                else:
                    chicken.source = 'source/chicken12.png'

    def clear(self):
        self.chickens = []
        self.grid = []

    def start(self):
        if len(self.chickens) == 0:
            if self.boss_level:
                self.chickens.append(Chicken(pos=(1000, 2000),
                                             hp=20 * self.level,
                                             bhp=20 * self.level,
                                             boss=True,
                                             food=15))

            else:
                for i in range(len(self.grid)):
                    self.chickens.append(Chicken(pos=(1000, 2000),
                                                 hp=self.level + 3,
                                                 bhp=self.level + 3,
                                                 food=randint(1, 4)))
            self.in_place = False

        if not self.in_place:
            self.in_place = True
            if len(self.chickens) == len(self.grid):
                for i in range(len(self.chickens)):
                    a = self.chickens[i].pos
                    b = self.grid[i]
                    c = False
                    if b[0] - self.speed * 2.5 < a[0] < b[0] + self.speed * 2.5:
                        if b[1] - self.speed < a[1] < b[1] + self.speed:
                            self.chickens[i].pos = self.grid[i]
                            c = True
                    if not c:
                        self.chickens[i].update(destination=self.grid[i])
                        self.in_place = False

    def update(self):
        rightmost = 0
        leftmost = 10000
        for chicken in self.chickens:
            if chicken.x < leftmost:
                leftmost = chicken.x
            if chicken.right > rightmost:
                rightmost = chicken.right

        if rightmost >= self.screen_size[0] and self.direction[0] == self.speed / 10.0:
            self.direction = -self.speed / 10.0, self.direction[1]
        elif leftmost <= 0 and self.direction[0] == -self.speed / 10.0:
            self.direction = self.speed / 10.0, self.direction[1]

        for chicken in self.chickens:
            chicken.update(direction=self.direction)
