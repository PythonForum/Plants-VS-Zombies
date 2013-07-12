from sun import Sun
import pygame as pg
from .. import setup as setup, tools

class SunObjects:
    def __init__(self):
        self.large_sun_value = 50
        self.sun_total = 0
        self.suns = []
        self.suns.append(Sun(self.large_sun_value)) #start with one test
        self.sun_timer = 0
        self.sun_spacing = 5
        self.sun_text()
        
    def sun_text(self):
        selected_font = pg.font.Font(setup.FONTS["Fixedsys500c"], 20)
        self.sun_amount = selected_font.render(str(self.sun_total), 1, (255,255,255))
        self.sun_amount_rect = self.sun_amount.get_rect()
    
    def sun_updates(self, surface):
        self.sun_text()

        if (pg.time.get_ticks() - self.sun_timer) > 1000*self.sun_spacing:
            self.sun_timer = pg.time.get_ticks()
            self.suns.append(Sun(self.large_sun_value)) 
        
        for obj in self.suns[:]:
            if obj.image_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
                mouse = pg.mouse.get_pos()
                offset = mouse[0] - obj.image_rect.x, mouse[1] - obj.image_rect.y
                if obj.mask.get_at(offset):
                    self.suns.remove(obj)
                    self.sun_total += obj.value
                    break
            obj.update()
            surface.blit(obj.image, obj.image_rect)
        surface.blit(self.sun_amount, (0,0))
