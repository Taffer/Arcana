# Arcana - Screen base class
#
# By Chris Herborth (https://github.com/Taffer)
# MIT license, see LICENSE.md for details.

import pygame


class ScreenBase:
    def __init__(self, surface: pygame.Surface):
        ''' Create a new Screen.

        Screens manage drawing the display contents.
        '''
        self.surface = surface  # Rendering surface.
        self.done = True  # Screen is done displaying itself.

    def update(self, dt: float):
        ''' Update any screen contents.
        '''
        pass

    def draw(self):
        ''' Draw the screen's contents.
        '''
        pass
