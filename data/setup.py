"""
Module: setup.py
Overview:
    This module initializes the display and creates dictionaries of resources.
Imports:
    pygame as pg
    os
    from . import tools
Global Constants:
    SCREEN_SIZE
    ORIGINAL_CAPTION
    SCREEN
    SCREEN_RECT
    FONTS
    MUSIC
    GFX
    SFX
"""
import pygame as pg
import os
from . import tools

SCREEN_SIZE = 800,600
ORIGINAL_CAPTION = "Botany vs Biomass"

#Initialization
##os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.display.set_caption(ORIGINAL_CAPTION)

SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

#Resource loading (Fonts and music just contain path names).
FONTS = tools.load_all_fonts(os.path.join("resources","fonts"))
MUSIC = tools.load_all_music(os.path.join("resources","music"))
GFX   = tools.load_all_gfx(os.path.join("resources","graphics"))
SFX   = tools.load_all_sfx(os.path.join("resources","sound"))