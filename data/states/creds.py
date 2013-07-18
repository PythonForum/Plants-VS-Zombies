import pygame as pg
from .. import setup,tools

class Credits(tools._State):
    """This State is updated while our game shows the Credit screen."""
    def __init__(self):
        tools._State.__init__(self)
        self.spacing = 100
        self.scroll_speed = 1
        self.name_list = ['person1',
                          'person2',
                          'person3',
                          'person4',
                          'person5',
                          'person6',
                          'person7',
                          'person8']
        self.render_list()
        self.ne_key = self.render_font("Fixedsys500c",20,"[Press Any Key]",(255,255,0))
        self.ne_key_rect = self.ne_key.get_rect(center=(setup.SCREEN_RECT.centerx,500))
        self.blink = False
        self.timer = 0.0

    def render_list(self):
        self.names = []
        for i,name in enumerate(self.name_list):
            obj = self.render_font("Fixedsys500c",40, name)
            obj_rect = obj.get_rect(center=(setup.SCREEN_RECT.centerx,
                                            setup.SCREEN_RECT.bottom+i*self.spacing))
            self.names.append([obj, obj_rect])

    def render_font(self,font,size,msg,color=(255,255,255)):
        """Takes the name of a loaded font, the size, and the color and returns
       a rendered surface of the msg given."""
        selected_font = pg.font.Font(setup.FONTS[font],size)
        return selected_font.render(msg,1,color)

    def update(self,surface,keys,current_time):
        """Updates the title screen."""
        self.current_time = current_time
        surface.fill((0,0,0))

        for num, name in enumerate(self.names[:]):
            if self.names[num][1].bottom > 0:
                surface.blit(name[0], name[1])
            elif self.names[-1][1].bottom < 0:
                self.next = "MENU"
                self.done = True
            self.names[num][1][1] -= self.scroll_speed

        if self.current_time-self.timer > 1000/5.0:
            self.blink = not self.blink
            self.timer = self.current_time
        if self.blink:
            surface.blit(self.ne_key,self.ne_key_rect)

    def cleanup(self):
        """Add variables that should persist to the self.persist dictionary.
       Then reset State.done to False."""
        self.render_list()
        self.done = False
        return self.persist

    def get_event(self,event):
        """Get events from Control.  Currently changes to next state on any key
       press."""
        if event.type == pg.KEYDOWN:
            self.next = "MENU"
            self.done = True
