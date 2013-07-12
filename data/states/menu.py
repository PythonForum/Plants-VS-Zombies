"""
Module: title.py
Overview:
    This is currently a placeholder for the Menu State of the game.
Imports:
    pygame as pg
    from .. import setup,tools
Classes:
    Menu(tools._State):
        Methods:
            __init__(self)
            render_font(self,font,size,msg,color=(255,255,255)
            pre_render_options(self)
            get_event(self,event)
            update(self,Surf,keys,mouse)
            timeout(self)
"""
import pygame as pg
from .. import setup,tools

class Menu(tools._State):
    """The State for the main menu."""
    def __init__(self):
        tools._State.__init__(self)
        self.from_bottom = 200
        self.spacer = 70
        self.timeout_limit = 15
        self.opts = ['Survival Mode','Story Mode',
                     'Highscores','Credits','Quit']
        self.next_list = ["SURVIVE","STORY","HIGHS","CREDS"]
        self.title = self.render_font("Fixedsys500c",40,"Menu Screen Placeholder",(0,255,255))
        self.title_rect = self.title.get_rect(center=(setup.SCREEN_RECT.centerx,75))
        self.pre_render_options()

    def render_font(self,font,size,msg,color=(255,255,255)):
        """Returns a message rendered as a Surface."""
        selected_font = pg.font.Font(setup.FONTS[font],size)
        return selected_font.render(msg,1,color)

    def pre_render_options(self):
        """Given a list of menu options, creates rendered versions of both
        selected and unselected messages and corresponding rects."""
        font_deselect = pg.font.Font(setup.FONTS["impact"],25)
        font_selected = pg.font.Font(setup.FONTS["impact"],40)

        rendered_msg = {"des":[],"sel":[]}
        for option in self.opts:
            d_rend = font_deselect.render(option, 1, (255,255,255))
            d_rect = d_rend.get_rect()
            s_rend = font_selected.render(option, 1, (255,0,0))
            s_rect = s_rend.get_rect()
            rendered_msg["des"].append((d_rend,d_rect))
            rendered_msg["sel"].append((s_rend,s_rect))
        self.rendered = rendered_msg

    def get_event(self,event):
        """Catches events passed from Control during the Menu State."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i,opt in enumerate(self.rendered["des"]):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    if i == len(self.next_list):
                        self.quit = True
                    else:
                        self.next = self.next_list[i]
                        self.done = True
                    break

    def update(self,surface,keys,mouse):
        """Update function for Menu State."""
        surface.fill((50,50,150))
        surface.blit(self.title,self.title_rect)
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (setup.SCREEN_RECT.centerx,self.from_bottom+i*self.spacer)
            if opt[1].collidepoint(pg.mouse.get_pos()):
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                surface.blit(rend_img,rend_rect)
            else:
                surface.blit(opt[0],opt[1])
        self.timeout()

    def timeout(self):
        """Timeout and return to title screen after 15 seconds."""
        if pg.time.get_ticks()-self.start_time > self.timeout_limit*1000:
            self.next = "TITLE"
            self.done = True