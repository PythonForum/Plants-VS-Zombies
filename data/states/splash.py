

import pygame as pg
from .. import setup as su,tools
import os



class Splash(tools._State):
    """This State is updated while our game shows the splash screen."""
    def __init__(self):
        tools._State.__init__(self)
        self.next = 'TITLE'
        
        self.python_image = su.GFX['python_powered']
        self.python_image_rect = self.python_image.get_rect(center=(su.SCREEN_RECT.centerx,75))
        
        self.pygame_image = su.GFX['pygame_powered']
        self.pygame_image_rect = self.pygame_image.get_rect(center=(su.SCREEN_RECT.centerx,200))
        
        self.forum_image = su.GFX['forum'] #not sure what forum logo is or will be
        self.forum_image_rect = self.forum_image.get_rect(center=(su.SCREEN_RECT.centerx,400))
        
        self.forum_name = self.render_font("Fixedsys500c",30,"python-forum.org",(0,0,0))
        self.forum_name_rect = self.forum_name.get_rect(center=(su.SCREEN_RECT.centerx,520))
        
    def render_font(self,font,size,msg,color=(255,255,255)):
        """Takes the name of a loaded font, the size, and the color and returns
        a rendered surface of the msg given."""
        RenderFont = pg.font.Font(su.FONTS[font],size)
        return RenderFont.render(msg,1,color)

    def update(self, Surf, keys,mouse):
        """Updates the splash screen."""
        Surf.fill((255,255,255))
        Surf.blit(self.python_image, self.python_image_rect)
        Surf.blit(self.pygame_image, self.pygame_image_rect)
        Surf.blit(self.forum_image, self.forum_image_rect)
        Surf.blit(self.forum_name, self.forum_name_rect)

    def get_event(self,event):
        """Get events from Control.  Currently changes to next state after 3 seconds"""
        if pg.time.get_ticks() - self.start_time > 3000: #- self.start_time > 4000:
            self.done = True
