import random
import pygame as pg
from .. import setup

class Sun(object):
    def __init__(self,plant=None):
        self.from_plant = plant
        if not self.from_plant:
            x_center = random.uniform(setup.GRID_MARGIN[0],
                                      setup.GRID_MARGIN[0]+setup.CELL_SIZE[0]*9)
            y_center = -setup.CELL_SIZE[1]//2
            self.final_y = (setup.GRID_MARGIN[1]+setup.CELL_SIZE[1]//2 +
                            setup.CELL_SIZE[1]*random.randint(0,4))
        else:
            x_center = random.uniform(plant.rect.x,plant.rect.x+setup.CELL_SIZE[0])
            y_center = self.final_y = plant.rect.centery
        sun_center = (x_center,y_center)

        self.angle = 0
        self.ang_speed = 2
        self.fall_speed = 2
        original_image = setup.GFX["sun_mek"]
        self.original_base = original_image.subsurface((0,0,72,72))
        self.original_yellow = original_image.subsurface((0,72,72,72))
        self.base_image = self.original_base.copy()
        self.yellow_image = self.original_yellow.copy()
        self.base_rect = self.base_image.get_rect(center=sun_center)
        self.yellow_rect = self.yellow_image.get_rect(center=sun_center)

    def update(self,surface):
        self.animate()
        if not self.from_plant:
            self.base_rect.centery = min(self.base_rect.centery+self.fall_speed,
                                         self.final_y)
            self.yellow_rect.centery = min(self.yellow_rect.centery+self.fall_speed,
                                           self.final_y)
        surface.blit(self.yellow_image,self.yellow_rect)
        surface.blit(self.base_image,self.base_rect)

    def animate(self):
        self.angle = (self.angle+self.ang_speed)%360.0
        self.base_image = pg.transform.rotozoom(self.original_base,self.angle,1)
        self.yellow_image = pg.transform.rotozoom(self.original_yellow,-self.angle,1)
        self.base_rect = self.base_image.get_rect(center=self.base_rect.center)
        self.yellow_rect = self.yellow_image.get_rect(center=self.yellow_rect.center)