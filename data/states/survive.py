import random
import pygame as pg
from .. import setup,tools

CELL_SIZE = (72,72)
MARGIN = (75,165)
SELECT_MARGIN = (169,3)
SELECT_SPACER = 77

class Survive(tools._State):
    """This State is updated while our game shows the Survive screen."""
    def __init__(self):
        tools._State.__init__(self)
        self.background = setup.GFX["survival"]
        self.mode = "READY"
        self.ready_msg = self.render_font("impact",70,"Get Ready!")
        self.ready_rect = self.ready_msg.get_rect(center=setup.SCREEN_RECT.center)

        self.energy = 50
        self.energy_rect = pg.Rect(31,49,88,32)
        self.available_plants = [SunFlower(0),Shooter(1)] #Initialized thusly for testing.
        self.suns = []
        self.plants = []
        self.zombies = []

        self.current_time = pg.time.get_ticks()
        self.sun_timer = random.uniform(5,15)
        self.last_sun_time = self.start_time

    def render_font(self,font,size,msg,color=(255,255,255)):
        """Takes the name of a loaded font, the size, and the color and returns
       a rendered surface of the msg given."""
        selected_font = pg.font.Font(setup.FONTS[font],size)
        return selected_font.render(msg,1,color)

    def update(self,surface,keys,mouse):
        """Updates the title screen."""
        surface.blit(self.background,(0,0))
        self.current_time = pg.time.get_ticks()
        if self.mode == "READY":
            if self.current_time-self.start_time <= 3.0*1000:
                surface.blit(self.ready_msg,self.ready_rect)
            else:
                self.mode = "PLAY"
        self.update_selector(surface)
        self.update_energy(surface)
        self.update_suns(surface)

    def update_selector(self,surface):
        for plant in self.available_plants:
            plant.update(surface)

    def update_suns(self,surface):
        if self.current_time-self.last_sun_time > self.sun_timer*1000:
            if len(self.suns) < 10:
                self.suns.append(Sun())
                self.sun_timer = random.uniform(5,15)
                self.last_sun_time = self.current_time
        for sun in self.suns:
            sun.update(surface)

    def update_energy(self,surface):
        energy_txt = self.render_font("Fixedsys500c",35,str(self.energy),(0,0,0))
        energy_txt_rect = energy_txt.get_rect(center=self.energy_rect.center)
        surface.blit(energy_txt,energy_txt_rect)

    def get_event(self,event):
        """Get events from Control.  Currently changes to next state on any key
       press."""
        if event.type == pg.KEYDOWN:
            self.next = "MENU"
            self.done = True
        if event.type == pg.MOUSEBUTTONDOWN:
            for sun in self.suns[:]:
                if sun.base_rect.collidepoint(event.pos):
                    self.energy = min(self.energy+25,9999)
                    self.suns.remove(sun)
                    break

class Sun(object):
    def __init__(self,plant=None):
        self.from_plant = plant
        if not self.from_plant:
            x_center = random.uniform(MARGIN[0],MARGIN[0]+CELL_SIZE[0]*9)
            y_center = -CELL_SIZE[1]//2
            self.final_y = MARGIN[1]+CELL_SIZE[1]//2+CELL_SIZE[1]*random.randint(0,4)
        else:
            x_center = random.uniform(plant.rect.x,plant.rect.x+CELL_SIZE[0])
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

class _SelectPlant(object):
    def __init__(self,location,sheet_coord,name):
        topleft = (SELECT_MARGIN[0]+SELECT_SPACER*location,SELECT_MARGIN[1])
        self.rect = pg.Rect(topleft,CELL_SIZE)
        sheet = setup.GFX["plant_sheet"].copy()
        sheet_location = (sheet_coord[0]*CELL_SIZE[0],sheet_coord[1]*CELL_SIZE[1])
        self.image = sheet.subsurface(sheet_location,CELL_SIZE)
        self.name = name
        self.time_for_recharge = 5.0
        self.timer = 0.0
        self.setup_cost(50)
        self.ready = True
        self.highlight = pg.Surface(self.rect.size).convert_alpha()
        self.highlight.fill((100,100,255,100))

    def setup_cost(self,cost):
        self.cost = cost
        target_rect = pg.Rect(self.rect.x,self.rect.bottom,CELL_SIZE[0],21)
        font = pg.font.Font(setup.FONTS["Fixedsys500c"],20)
        self.cost_txt = font.render(str(self.cost),1,(0,0,0))
        self.cost_txt_rect = self.cost_txt.get_rect(center=target_rect.center)

    def update(self,surface):
        surface.blit(self.image,self.rect)
        surface.blit(self.cost_txt,self.cost_txt_rect)
        if self.rect.collidepoint(pg.mouse.get_pos()):
            surface.blit(self.highlight,self.rect)


class Shooter(_SelectPlant):
    def __init__(self,location):
        _SelectPlant.__init__(self,location,(0,0),"SHOOTER")
        self.setup_cost(100)
        self.time_for_recharge = 10.0


class SunFlower(_SelectPlant):
    def __init__(self,location):
        _SelectPlant.__init__(self,location,(0,1),"SUNFLOWER")
        self.cost = 50