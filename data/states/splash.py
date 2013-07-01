

import pygame as pg
from .. import setup as su,tools
import os



class Splash(tools._State):
    """This State is updated while our game shows the splash screen."""
    def __init__(self):
        tools._State.__init__(self)
        #self.title = self.render_font("Fixedsys500c",40,"Splash Screen Place Holder")
        #self.title_rect = self.title.get_rect(center=(su.SCREEN_RECT.centerx,75))
       # self.ne_key = self.render_font("Fixedsys500c",20,"[Press Any Key]",(255,255,0))
       # self.ne_key_rect = self.ne_key.get_rect(center=(su.SCREEN_RECT.centerx,500))
        #self.blink = False
        self.timer = 0.0
        self.next_state = False
        
        self.python_image = su.GFX['python_powered']
        self.python_image_rect = self.python_image.get_rect(center=(su.SCREEN_RECT.centerx,75))
        
        self.pygame_image = su.GFX['pygame_powered']
        self.pygame_image_rect = self.pygame_image.get_rect(center=(su.SCREEN_RECT.centerx,200))
        
   # def render_font(self,font,size,msg,color=(255,255,255)):
    #    """Takes the name of a loaded font, the size, and the color and returns
    #    a rendered surface of the msg given."""
    #    RenderFont = pg.font.Font(su.FONTS[font],size)
    #    return RenderFont.render(msg,1,color)

    def update(self,Surf,keys,mouse):
        """Updates the title screen."""
        Surf.fill((255,255,255))
        Surf.blit(self.python_image, self.python_image_rect)
        Surf.blit(self.pygame_image, self.pygame_image_rect)
        if pg.time.get_ticks() - self.timer > 4000:
            self.next_state = True
            self.timer = pg.time.get_ticks()

    def get_event(self,event):
        """Get events from Control.  Currently changes to next state on any key
        press."""
        if self.next_state:
            self.next = "TITLE"
            self.done = True
