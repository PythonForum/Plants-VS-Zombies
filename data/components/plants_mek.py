import pygame as pg
from .. import setup

class _Plant(object):
    def __init__(self,coords,location,sheet_coords,name):
        self.coordinates = coords
        self.rect = pg.Rect(location,setup.CELL_SIZE)
        sheet = setup.GFX["plant_sheet"].copy()
        self.fps = 5.0
        self.animation_timer = 0.0
        self.frames = self.get_frames(sheet_coords,sheet)
        self.frame = 0
        self.image = self.frames[self.frame]
        self.name = name

        self.life = 4

    def get_frames(self,coords,sheet):
        frames = []
        for coord in coords:
            sheet_location = (coord[0]*setup.CELL_SIZE[0],coord[1]*setup.CELL_SIZE[1])
            frames.append(sheet.subsurface(sheet_location,setup.CELL_SIZE))
        return frames

    def animate(self):
        current_time = pg.time.get_ticks()
        if current_time - self.animation_timer > 1000//self.fps:
            self.frame = (self.frame+1)%len(self.frames)
            self.image = self.frames[self.frame]
            self.animation_timer = current_time

    def action(self):
        pass

    def update(self,surface):
        self.animate()
        surface.blit(self.image,self.rect)


class Shooter(_Plant):
    def __init__(self,coords,location):
        frame_coords = [(0,0),(1,0)]
        _Plant.__init__(self,coords,location,frame_coords,"SHOOTER")

class Sunflower(_Plant):
    def __init__(self,coords,location):
        _Plant.__init__(self,coords,location,[(0,1)],"SUNFLOWER")

PLANT_DICT = {"SHOOTER"   : Shooter,
              "SUNFLOWER" : Sunflower}
