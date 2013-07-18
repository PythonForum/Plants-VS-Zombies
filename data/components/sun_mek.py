import random
import pygame as pg
from .. import setup

class Sun(object):
    """A class for our happy energy-giving sun sprites."""
    memoed_base = {}  #Cache for base image rotations.
    memoed_yellow = {}  #Cache for yellow image rotations.
    def __init__(self,plant=None):
        self.from_plant = plant
        sun_center = self.get_initial_center()
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
        self.current_time = 0.0

    def get_initial_center(self):
        """Find where the sun initially spawns (as well as its final position)
        dependent on whether the sun is from a plant or randomly generated."""
        if not self.from_plant:
            x_center = random.uniform(setup.GRID_MARGIN[0],
                                      setup.GRID_MARGIN[0]+setup.CELL_SIZE[0]*9)
            y_center = -setup.CELL_SIZE[1]//2
            self.final_y = (setup.GRID_MARGIN[1]+setup.CELL_SIZE[1]//2 +
                            setup.CELL_SIZE[1]*random.randint(0,4))
        else:
            x_center = random.uniform(plant.rect.x,plant.rect.x+setup.CELL_SIZE[0])
            y_center = self.final_y = plant.rect.centery
        return (x_center,y_center)

    def update(self,surface,current_time):
        """Updates the image and blits to the given surface.  Method of updating
        changes depending on whether it is a plant generated sun or a randomly
        generated sun."""
        self.current_time = current_time
        self.animate()
        if not self.from_plant:
            self.base_rect.centery = min(self.base_rect.centery+self.fall_speed,
                                         self.final_y)
            self.yellow_rect.centery = min(self.yellow_rect.centery+self.fall_speed,
                                           self.final_y)
        surface.blit(self.yellow_image,self.yellow_rect)
        surface.blit(self.base_image,self.base_rect)

    def animate(self):
        """Calculates the angle of the sprite and calculates (or retreives if
        cached) the appropriate frame."""
        self.angle = (self.angle+self.ang_speed)%360.0
        self.base_image = self.memo_rotations(self.memoed_base,self.angle,
                                              self.original_base)
        self.yellow_image = self.memo_rotations(self.memoed_yellow,-self.angle,
                                                self.original_yellow)
        self.base_rect = self.base_image.get_rect(center=self.base_rect.center)
        self.yellow_rect = self.yellow_image.get_rect(center=self.yellow_rect.center)

    def memo_rotations(self,memo_dict,angle,original_image):
        """Caches rotations to save processing of the expensive rotozoom."""
        if angle in memo_dict:
            return memo_dict[angle]
        else:
            rotation = pg.transform.rotozoom(original_image,angle,1)
            memo_dict[angle] = rotation
            return rotation
