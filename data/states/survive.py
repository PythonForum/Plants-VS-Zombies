import random
import pygame as pg
from .. import setup,tools
from ..components import sun_mek,select_mek,plants_mek

class Survive(tools._State):
    """This State is updated while our game shows the Survive screen."""
    def __init__(self):
        tools._State.__init__(self)
        self.background = setup.GFX["survival"]
        self.ready_msg = self.render_font("impact",70,"Get Ready!")
        self.ready_rect = self.ready_msg.get_rect(center=setup.SCREEN_RECT.center)
        self.grid_rect = pg.Rect(setup.GRID_MARGIN,(setup.CELL_SIZE[0]*9,
                                                    setup.CELL_SIZE[1]*5))

    def reset(self):
        self.mode = "READY"
        self.energy = 200
        self.energy_rect = pg.Rect(31,49,88,32)
        self.available_plants = ["SHOOTER","SUNFLOWER"] #Initialized thusly for testing.
        self.selector = select_mek.Selector(setup.SELECTOR_MARGIN,self.available_plants)
        self.suns = []
        self.plants = []
        self.zombies = []
        self.current_time = pg.time.get_ticks()
        self.sun_timer = random.uniform(5,15)
        self.last_sun_time = self.start_time
        self.plant_cursor = None
        self.cursor_rect = None

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
        self.update_energy(surface)
        self.selector.update(surface)
        self.update_plants(surface)
        self.update_suns(surface)
        self.update_cursor(surface)

    def update_cursor(self,surface):
        if self.selector.selected:
            mouse = pg.mouse.get_pos()
            self.cursor_rect = self.plant_cursor.get_rect(center=mouse)
            if self.grid_rect.collidepoint(mouse):
                coords = self.get_coordinates(mouse)
                location = self.get_position_from_coordinates(coords)
                surface.blit(self.selector.selected.ghost,location)
            surface.blit(self.plant_cursor,self.cursor_rect)

    def get_coordinates(self,mouse):
        x = (mouse[0]-setup.GRID_MARGIN[0])//setup.CELL_SIZE[0]
        y = (mouse[1]-setup.GRID_MARGIN[1])//setup.CELL_SIZE[1]
        return x,y
    def get_position_from_coordinates(self,coords):
        location = (setup.GRID_MARGIN[0]+setup.CELL_SIZE[0]*coords[0],
                    setup.GRID_MARGIN[1]+setup.CELL_SIZE[1]*coords[1])
        return location

    def update_suns(self,surface):
        if self.current_time-self.last_sun_time > self.sun_timer*1000:
            if len(self.suns) < 10:
                self.suns.append(sun_mek.Sun())
                self.sun_timer = random.uniform(5,15)
                self.last_sun_time = self.current_time
        for sun in self.suns:
            sun.update(surface)

    def update_plants(self,surface):
        for plant in self.plants:
            plant.update(surface)

    def update_energy(self,surface):
        energy_txt = self.render_font("Fixedsys500c",35,str(self.energy),(0,0,0))
        energy_txt_rect = energy_txt.get_rect(center=self.energy_rect.center)
        surface.blit(energy_txt,energy_txt_rect)

    def clicked_sun(self,event):
        if not self.selector.selected:
            for sun in self.suns[:]:
                if sun.base_rect.collidepoint(event.pos):
                    self.energy = min(self.energy+25,9999)
                    self.suns.remove(sun)
                    return True

    def clicked_selector(self,event):
        for plant in self.selector.plants:
            if plant.rect.collidepoint(event.pos) and plant.ready:
                if self.energy >= plant.cost:
                    self.selector.select_plant(plant)
                    self.plant_cursor = plant.image.copy()
                    return 1
        else:
            self.selector.selected = None

    def startup(self,persistant):
        tools._State.startup(self,persistant)
        self.reset()

    def add_plant(self,event):
        if self.selector.selected:
            name = self.selector.selected.name
            coords = self.get_coordinates(event.pos)
            location = self.get_position_from_coordinates(coords)
            if not any(plant.coordinates==coords for plant in self.plants):
                self.plants.append(plants_mek.PLANT_DICT[name](coords,location))
                self.energy -= self.selector.selected.cost
                self.selector.selected.deployed()
                self.selector.selected = None

    def get_event(self,event):
        """Get events from Control."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next = "MENU"
                self.done = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.mode == "PLAY":
                if event.button == 1:
                    if self.clicked_sun(event):
                        pass
                    elif self.selector.rect.collidepoint(event.pos):
                        self.clicked_selector(event)
                    elif self.grid_rect.collidepoint(event.pos):
                        self.add_plant(event)
                elif event.button == 3:
                    self.selector.selected = None
