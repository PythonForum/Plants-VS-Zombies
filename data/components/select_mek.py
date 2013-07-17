import pygame as pg
from .. import setup

class Selector(object):
    def __init__(self,location,plant_names):
        self.image = setup.GFX["selector"]
        self.rect = self.image.get_rect(topleft=location)
        self.pad_item = (self.rect.x+19,self.rect.y+3)
        self.spacer = 77
        self.plant_dict = {"SHOOTER"   : ShooterSelect,
                           "SUNFLOWER" : SunflowerSelect}
        self.plants = self.setup_plants(plant_names)
        self.selected = False

    def setup_plants(self,plant_names):
        plants = []
        for i,plant in enumerate(plant_names):
            location = (self.pad_item[0]+self.spacer*i,self.pad_item[1])
            plants.append(self.plant_dict[plant](location))
        return plants

    def select_plant(self,plant):
        self.selected = plant

    def update(self,surface):
        surface.blit(self.image,self.rect)
        for plant in self.plants:
            plant.update(surface,self.selected)

class _SelectPlant(object):
    def __init__(self,location,sheet_coord,name):
        self.rect = pg.Rect(location,setup.CELL_SIZE)
        sheet = setup.GFX["plant_sheet"].copy()
        sheet_location = (sheet_coord[0]*setup.CELL_SIZE[0],sheet_coord[1]*setup.CELL_SIZE[1])
        self.image = sheet.subsurface(sheet_location,setup.CELL_SIZE)
        self.name = name
        self.time_for_recharge = 5.0
        self.timer = 0.0
        self.setup_cost(50)
        self.ready = True
        self.highlight = pg.Surface((self.rect.width+2,self.rect.height+21)).convert_alpha()
        self.select_highlight = self.highlight.copy()
        self.highlight.fill((100,100,255,100))
        self.select_highlight.fill((0,0,0,100))
        self.ghost = self.make_ghost()

    def make_ghost(self):
        ghost = self.image.copy()
        array = pg.surfarray.pixels_alpha(ghost)
        for j,y in enumerate(array):
            for i,x in enumerate(y):
                array[j][i] = max(array[j][i]-80,0)
        return ghost

    def setup_cost(self,cost):
        self.cost = cost
        target_rect = pg.Rect(self.rect.x,self.rect.bottom,setup.CELL_SIZE[0],21)
        font = pg.font.Font(setup.FONTS["Fixedsys500c"],20)
        self.cost_txt = font.render(str(self.cost),1,(0,0,0))
        self.cost_txt_rect = self.cost_txt.get_rect(center=target_rect.center)

    def update(self,surface,selected):
        if self != selected:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                surface.blit(self.highlight,self.rect)
        else:
            surface.blit(self.select_highlight,self.rect)
        surface.blit(self.image,self.rect)
        surface.blit(self.cost_txt,self.cost_txt_rect)


class ShooterSelect(_SelectPlant):
    def __init__(self,location):
        _SelectPlant.__init__(self,location,(0,0),"SHOOTER")
        self.setup_cost(100)
        self.time_for_recharge = 10.0


class SunflowerSelect(_SelectPlant):
    def __init__(self,location):
        _SelectPlant.__init__(self,location,(0,1),"SUNFLOWER")
