"""
Module: main.py
Overview:
    The main function is defined here. It simply creates an instance of
    tools.Control and adds the game states to its dictionary using
    tools.setup_states.  There should be no need (theoretically) to edit
    the tools.Control class.  All modifications should occur in this module
    and in the setup module.
Imports:
    from . import setup,tools
    from .states import title
Functions:
    main()
"""
from . import setup,tools
from .states import title,splash,menu,creds,story,survive,highscore#, game

def main():
    """Add states to control here."""
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {"SPLASH" : splash.Splash(),
                  "TITLE"  : title.Title(),
                  "MENU"   : menu.Menu(),
                  'CREDS'  : creds.Credits(),
                  'STORY'  : story.Story(),
                  'SURVIVE': survive.Survive(),
                  'HIGHS'  : highscore.Highscore()}
    run_it.setup_states(state_dict,"SPLASH")
    run_it.main()
