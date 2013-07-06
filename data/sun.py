

import pygame as pg
import setup as su,tools
import random

class Sun:
    def __init__(self):
        self.image = su.GFX['sun']
        x = self.random_sunX()
        self.image_rect = self.image.get_rect(center=(x,20))
        self.speed = 2
        self.stop = self.random_sunY()
        
    def random_sunX(self):
        '''sun fall at random x axis'''
        return random.randint(1, su.SCREEN_RECT.centerx)
        
    def random_sunY(self):
        '''sun stop on random y axis'''
        return random.randint(1, su.SCREEN_RECT.centery)
        
    def update(self):
        if self.image_rect.centery < self.stop:
            self.image_rect.centery += self.speed
        
