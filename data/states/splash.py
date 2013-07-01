import pygame as pg
from .. import setup as su,tools

class Splash(tools._State):
    """This State is updated while our game shows the splash screen."""
    def __init__(self):
        tools._State.__init__(self)
        self.next = "TITLE"
        self.timeout = 4

        self.python_image = su.GFX['python_powered']
        self.python_image_rect = self.python_image.get_rect(center=(su.SCREEN_RECT.centerx,75))

        self.pygame_image = su.GFX['pygame_powered']
        self.pygame_image_rect = self.pygame_image.get_rect(center=(su.SCREEN_RECT.centerx,200))

    def update(self,Surf,keys,mouse):
        """Updates the title screen."""
        Surf.fill((255,255,255))
        Surf.blit(self.python_image, self.python_image_rect)
        Surf.blit(self.pygame_image, self.pygame_image_rect)
        if pg.time.get_ticks()-self.start_time > 1000.0*self.timeout:
            self.done = True

    def get_event(self,event):
        """Get events from Control. Currently changes to next state on any key
        press."""
        if event.type == pg.KEYDOWN:
            self.done = True