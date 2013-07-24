"""
Module: survive.py
Overview:
    This module contains the survive state.
Imports:
    random
    pygame as pg
    from .. import setup,tools
    from ..components import sun_mek,select_mek,plants_mek
Classes:
    Survive(tools._State):
        Methods:
            __init__(self)
            startup(self,current_time,persistant)
            render_font(self,font,size,msg,color=(255,255,255))
            update(self,surface,keys,current_time)
            update_cursor(self,surface)
            get_coordinates(self,mouse)
            get_position_from_coordinates(self,coords)
            update_suns(self,surface)
            update_plants(self,surface)
            update_energy(self,surface)
            clicked_sun(self,event)
            clicked_selector(self,event)
            add_plant(self,event)
            get_event(self,event)
"""

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

    def startup(self,current_time,persistant):
        """Called when this State gains control; preparing the state for play."""
        tools._State.startup(self,current_time,persistant)
        self.mode = "READY"
        self.energy = 200
        self.energy_rect = pg.Rect(31,49,88,32)
        self.available_plants = ["SHOOTER","SUNFLOWER","TOMATO"] #Initialized thusly for testing.
        self.selector = select_mek.Selector(setup.SELECTOR_MARGIN,self.available_plants)
        self.suns = []
        self.plants = []
        self.zombies = []
        self.sun_timer = random.uniform(5,12)
        self.last_sun_time = self.start_time
        self.plant_cursor = None
        self.cursor_rect = None

    def render_font(self,font,size,msg,color=(255,255,255)):
        """Takes the name of a loaded font, the size, and the color and returns
       a rendered surface of the msg given."""
        selected_font = pg.font.Font(setup.FONTS[font],size)
        return selected_font.render(msg,1,color)

    def update(self,surface,keys,current_time):
        """Updates the title screen."""
        self.current_time = current_time
        surface.blit(self.background,(0,0))
        if self.mode == "READY":
            if self.current_time-self.start_time <= 3.0*1000:
                surface.blit(self.ready_msg,self.ready_rect)
            else:
                self.mode = "PLAY"
        self.update_energy(surface)
        self.selector.update(surface,self.current_time)
        self.update_plants(surface)
        self.update_suns(surface)
        self.update_cursor(surface)

    def update_cursor(self,surface):
        """When a plant is selected, updates the cursor and corresponding
        ghost image if applicable."""
        if self.selector.selected:
            mouse = pg.mouse.get_pos()
            self.cursor_rect = self.plant_cursor.get_rect(center=mouse)
            if self.grid_rect.collidepoint(mouse):
                coords = self.get_coordinates(mouse)
                location = self.get_position_from_coordinates(coords)
                surface.blit(self.selector.selected.ghost,location)
            surface.blit(self.plant_cursor,self.cursor_rect)

    def get_coordinates(self,mouse):
        """Return mouse location in the form of grid coordinates."""
        x = (mouse[0]-setup.GRID_MARGIN[0])//setup.CELL_SIZE[0]
        y = (mouse[1]-setup.GRID_MARGIN[1])//setup.CELL_SIZE[1]
        return x,y
    def get_position_from_coordinates(self,coords):
        """Return absolute screen location coresponding to passed coordinates."""
        location = (setup.GRID_MARGIN[0]+setup.CELL_SIZE[0]*coords[0],
                    setup.GRID_MARGIN[1]+setup.CELL_SIZE[1]*coords[1])
        return location

    def update_suns(self,surface):
        """Generates a random sun if enough time has ellapsed, and updates all
        current Sun instances."""
        if self.current_time-self.last_sun_time > self.sun_timer*1000:
            if len(self.suns) < 20:
                self.suns.append(sun_mek.Sun())
                self.sun_timer = random.uniform(5,12)
                self.last_sun_time = self.current_time
        for sun in self.suns:
            sun.update(surface,self.current_time)

    def update_plants(self,surface):
        """Update all plants on the grid."""
        for plant in self.plants:
            plant.update(surface,self.current_time)

    def update_energy(self,surface):
        """Render and blit the energy amount to the screen."""
        energy_txt = self.render_font("Fixedsys500c",35,str(self.energy),(0,0,0))
        energy_txt_rect = energy_txt.get_rect(center=self.energy_rect.center)
        surface.blit(energy_txt,energy_txt_rect)

    def clicked_sun(self,event):
        """Deletes suns and adds energy when clicked."""
        if not self.selector.selected:
            for sun in self.suns[:]:
                if sun.base_rect.collidepoint(event.pos):
                    self.energy = min(self.energy+25,9999)
                    self.suns.remove(sun)
                    return True

    def clicked_selector(self,event):
        """Reacts to mouse clicks on the plant selection panel."""
        for plant in self.selector.plants:
            if plant.rect.collidepoint(event.pos) and plant.ready:
                if self.energy >= plant.cost:
                    self.selector.select_plant(plant)
                    self.plant_cursor = plant.image.copy()
                    return True
        self.selector.selected = None

    def add_plant(self,event):
        """Adds currently selected plant to the grid."""
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
        elif event.type == pg.MOUSEBUTTONDOWN:
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
