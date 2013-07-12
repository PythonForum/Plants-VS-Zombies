
import pygame as pg
from .. import setup, tools
import random

class Sun:
    def __init__(self, value):
        self.value = value
        self.image = setup.GFX['sun']
        self.mask = pg.mask.from_surface(self.image)

        x = self.random_sunX()
        self.image_rect = self.image.get_rect(center=(x,-self.image.get_size()[1])) #start above screen
        self.speed = 2
        self.stop = self.random_sunY()
        
    def random_sunX(self):
        '''sun fall at random x axis'''
        return random.randint(1, setup.SCREEN_SIZE[0])
        
    def random_sunY(self):
        '''sun stop on random y axis'''
        return random.randint(setup.SCREEN_RECT.centery // 2, setup.SCREEN_RECT.centery)
        
    def update(self):
        if self.image_rect.centery < self.stop:
            self.image_rect.centery += self.speed
        
