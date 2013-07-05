


import pygame as pg
from .. import setup as su,tools

class Credits(tools._State):
    """This State is updated while our game shows the Credit screen."""
    def __init__(self):
        tools._State.__init__(self)
        self.name_list = [
            'person1',
            'person2',
            'person3',
            'person4',
            'person5',
            'person6',
            'person7',
            'person8',
        ]
        
        self.names = []
        for name in self.name_list:
            obj = self.render_font("Fixedsys500c",40, name)
            obj_rect = obj.get_rect(center=(su.SCREEN_RECT.centerx,su.SCREEN_RECT.centery))
            self.names.append([obj, obj_rect])
        
        self.ne_key = self.render_font("Fixedsys500c",20,"[Press Any Key]",(255,255,0))
        self.ne_key_rect = self.ne_key.get_rect(center=(su.SCREEN_RECT.centerx,500))
        self.blink = False
        self.timer = 0.0

    def render_font(self,font,size,msg,color=(255,255,255)):
        """Takes the name of a loaded font, the size, and the color and returns
        a rendered surface of the msg given."""
        RenderFont = pg.font.Font(su.FONTS[font],size)
        return RenderFont.render(msg,1,color)

    def update(self,Surf,keys,mouse):
        """Updates the title screen."""
        Surf.fill((0,0,0))

        for name in self.names:
            Surf.blit(name[0], name[1])
        if pg.time.get_ticks() - self.timer > 1000/5.0:
            self.blink = not self.blink
            self.timer = pg.time.get_ticks()
        if self.blink:
            Surf.blit(self.ne_key,self.ne_key_rect)

    def get_event(self,event):
        """Get events from Control.  Currently changes to next state on any key
        press."""
        if event.type == pg.KEYDOWN:
            self.next = "MENU"
            self.done = True
