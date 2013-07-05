"""This is a collaborative effort between members of the python-forum.org
community to create a game (using the pygame API) together.
Program is licensed under the GPL3 and can be used and edited freely.
No warranty of any kind expressed or implied.

-appended by Mekire June 30th, 2013.
"""
import pygame as pg
import sys
from data.main import main

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass 
    pg.quit();sys.exit()
