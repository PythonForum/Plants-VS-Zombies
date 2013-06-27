
import pygame

class Control:
    def __init__(self):
        pygame.init()
        self.screensize = (400,400)
        self.screen = pygame.display.set_mode(self.screensize)
        pygame.display.set_caption('Plants VS Zombies')
        self.clock = pygame.time.Clock()
        self.gamestate = True
        self.mainloop()
        
    def update(self):
        pass 
        
    def mainloop(self):
        while self.gamestate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamestate = False
            self.update()
            pygame.display.flip()
            
if __name__ == '__main__':
    app = Control()
