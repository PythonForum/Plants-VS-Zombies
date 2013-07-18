"""
Module: splash.py
Overview:
    The splash screen of the game. The first thing the user sees.
Imports:
    pygame as pg
    from .. import setup,tools
Classes:
    Splash(tools._State):
        Methods:
            __init__(self)
            render_font(self,font,size,msg,color=(255,255,255)
            make_text_list(self,font,size,strings,color,start_y,y_space)
            update(self,surface,keys,current_time)
            get_event(self,event)
"""
import pygame as pg
from .. import setup,tools

class Splash(tools._State):
    """This State is updated while our game shows the splash screen."""
    def __init__(self):
        tools._State.__init__(self)
        self.next = "TITLE"
        self.timeout = 5

        self.cover = pg.Surface((setup.SCREEN_SIZE))
        self.cover.fill(0)
        self.cover_alpha = 256
        self.alpha_step  = 3

        self.image = setup.GFX['splash_page_try']
        text = ["Brought to you by","The","python-forum.org","Community"]
        self.rendered_text = self.make_text_list("Fixedsys500c",50,text,(0,0,0),320,50)

    def make_text_list(self,font,size,strings,color,start_y,y_space):
        """Takes a list of strings and returns a list of (rendered_surface,rects).
        The rects are centered on the screen and their y coordinates begin at
        starty, with y_space pixels between each line."""
        rendered_text = []
        for i,string in enumerate(strings):
            msg = self.render_font(font,size,string,color)
            rect = msg.get_rect(center=(setup.SCREEN_RECT.centerx,start_y+i*y_space))
            rendered_text.append((msg,rect))
        return rendered_text

    def render_font(self,font,size,msg,color=(255,255,255)):
        """Takes the name of a loaded font, the size, and the color and returns
        a rendered surface of the msg given."""
        selected_font = pg.font.Font(setup.FONTS[font],size)
        return selected_font.render(msg,1,color)

    def update(self,surface,keys,current_time):
        """Updates the splash screen."""
        self.current_time = current_time
        surface.blit(self.image, (0,0))
        for msg in self.rendered_text:
            surface.blit(*msg)
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        surface.blit(self.cover,(0,0))
        if self.current_time-self.start_time > 1000.0*self.timeout:
            self.done = True

    def get_event(self,event):
        """Get events from Control. Currently changes to next state on any key
        press."""
        if event.type == pg.KEYDOWN:
            self.done = True
