import math
import pygame as pg
from .. import setup


class Selector(object):
    """Class representing our plant selector window."""
    def __init__(self,location,plant_names):
        self.image = setup.GFX["selector"]
        self.rect = self.image.get_rect(topleft=location)
        self.pad_item = (self.rect.x+19,self.rect.y+3)
        self.spacer = 77
        self.plant_dict = {"SHOOTER"   : ShooterSelect,
                           "SUNFLOWER" : SunflowerSelect,
                           "TOMATO"    : TomatoSelect}
        self.plants = self.setup_plants(plant_names)
        self.selected = False
        self.current_time = 0.0

    def setup_plants(self,plant_names):
        """Add the plants passed by their names into the selector window."""
        plants = []
        for i,plant in enumerate(plant_names):
            location = (self.pad_item[0]+self.spacer*i,self.pad_item[1])
            plants.append(self.plant_dict[plant](location))
        return plants

    def select_plant(self,plant):
        """Set a clicked plant to selected."""
        self.selected = plant

    def update(self,surface,current_time):
        """Update entire selector window."""
        self.current_time = current_time
        surface.blit(self.image,self.rect)
        for plant in self.plants:
            plant.update(surface,self.selected,self.current_time)


class _SelectPlant(object):
    """Prototype for plants in the selector window."""
    def __init__(self,location,sheet_coord,name):
        self.rect = pg.Rect(location,setup.CELL_SIZE)
        sheet = setup.GFX["plant_sheet"].copy()
        sheet_location = (sheet_coord[0]*setup.CELL_SIZE[0],sheet_coord[1]*setup.CELL_SIZE[1])
        self.image = sheet.subsurface(sheet_location,setup.CELL_SIZE)
        self.name = name
        self.time_for_recharge = 5.0
        self.current_time = 0.0
        self.timer = 0.0
        self.setup_cost(50)
        self.ready = True
        self.make_all_highlights()

    def deployed(self):
        """This function is called if a selected plant is placed on the grid."""
        self.ready = False
        self.timer = pg.time.get_ticks() #A direct call here is justified.
        self.recharge_highlight = pg.Surface((setup.CELL_SIZE)).convert_alpha()
        self.recharge_highlight.fill((0,0,0,200))

    def make_all_highlights(self):
        """Creates the highlights for hovering and selected plants and
        creates an initial surface and rect for the recharge highlight."""
        self.highlight = pg.Surface((self.rect.width+2,self.rect.height+21)).convert_alpha()
        self.select_highlight = self.highlight.copy()
        self.highlight.fill((100,100,255,100))
        self.select_highlight.fill((0,0,0,100))
        self.recharge_highlight = pg.Surface((setup.CELL_SIZE)).convert_alpha()
        self.recharge_rect = self.recharge_highlight.get_rect()
        self.ghost = self.make_ghost()

    def make_ghost(self):
        """Creates the semi-transparent ghost image that appears at the location
        a plant would grow if confirmed.  As the images already contain
        per-pixel-alpha, it is necessary to change the alpha as follows; using
        pygame.Surface.set_alpha won't work unfortunately."""
        ghost = self.image.copy()
        array = pg.surfarray.pixels_alpha(ghost)
        for j,y in enumerate(array):
            for i,x in enumerate(y):
                array[j][i] = max(array[j][i]-80,0)
        return ghost

    def make_recharge_highlight(self):
        """Creates the clock style recharging highlight. I wanted to use
        pygame.draw.arc for this but unfortunately that draw method is badly
        written and leaves moire patterns."""
        elapsed = self.current_time-self.timer
        percent_recharged = elapsed/(self.time_for_recharge*1000)
        angle = 2*math.pi*percent_recharged
        x = self.recharge_rect.centerx+50*math.cos(angle)
        y = self.recharge_rect.centery+50*math.sin(angle)
        pg.draw.line(self.recharge_highlight,(0,0,0,0),
                     self.recharge_rect.center,(x,y),5)
        if percent_recharged >= 1:
            self.ready = True
        return self.recharge_highlight

    def setup_cost(self,cost):
        """Creates rendered cost and appropriately centered rect."""
        self.cost = cost
        target_rect = pg.Rect(self.rect.x,self.rect.bottom,setup.CELL_SIZE[0],21)
        font = pg.font.Font(setup.FONTS["Fixedsys500c"],20)
        self.cost_txt = font.render(str(self.cost),1,(0,0,0))
        self.cost_txt_rect = self.cost_txt.get_rect(center=target_rect.center)

    def update(self,surface,selected,current_time):
        """Updates for selector window plants, including highlights and
        recharging."""
        self.current_time = current_time
        if self != selected:
            if self.ready and self.rect.collidepoint(pg.mouse.get_pos()):
                surface.blit(self.highlight,self.rect)
        else:
            surface.blit(self.select_highlight,self.rect)
        surface.blit(self.image,self.rect)
        if not self.ready:
            surface.blit(self.make_recharge_highlight(),self.rect)
        surface.blit(self.cost_txt,self.cost_txt_rect)


class ShooterSelect(_SelectPlant):
    def __init__(self,location):
        _SelectPlant.__init__(self,location,(0,0),"SHOOTER")
        self.setup_cost(100)
        self.time_for_recharge = 10.0

class TomatoSelect(_SelectPlant):
    def __init__(self,location):
        _SelectPlant.__init__(self,location,(2,2),"TOMATO")

class SunflowerSelect(_SelectPlant):
    def __init__(self,location):
        _SelectPlant.__init__(self,location,(0,1),"SUNFLOWER")
