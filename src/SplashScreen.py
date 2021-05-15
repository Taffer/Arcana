# Arcana - Splash Screen
#
# By Chris Herborth (https://github.com/Taffer)
# MIT license, see LICENSE.md for details.

import pygame

from .ScreenBase import ScreenBase


class SplashScreen(ScreenBase):
    ''' Display a succession of splash screens, fading in/out between them.
    '''

    FADE_IN = 0  # Currently fading in an image.
    DISPLAY = 1  # Currently displaying an image.
    FADE_OUT = 2  # Currently fading out an image.

    def __init__(self, surface: pygame.Surface, splash_images: list, duration: float, tween):
        ''' Create a Splash Screen displaying the list of images.

        @param surface          Where to draw the splash screen.
        @param splash_images    List of splash image Surfaces to display.
        @param duration         Time in seconds to fade in/display/fade out.
        @param tween            PyTweening function used for the fades.
        '''
        super().__init__(surface)

        self.done = False  # We have images to display!

        self.images = splash_images
        self.duration = duration
        self.tween = tween

        screen_rect = self.surface.get_rect()
        self.mask = pygame.Surface((screen_rect.width, screen_rect.height))
        self.mask.fill(pygame.Color('black'))
        self.mask.set_alpha(255)  # Solid at first.

        # Resize images, if necessary.
        for i in range(len(self.images)):
            image_rect = self.images[i].get_rect()
            if image_rect.width != screen_rect.width or image_rect.height != screen_rect.height:
                self.images[i] = pygame.transform.smoothscale(self.images[i], (screen_rect.width, screen_rect.height))

        self.current_image = 0  # Count through the images as we go.
        self.current_state = SplashScreen.FADE_IN
        self.current_duration = 0

    def update(self, dt: float):
        ''' Update the splash screen.
        '''
        self.current_duration += dt

        if self.current_state == SplashScreen.FADE_IN:
            if self.current_duration > self.duration:
                self.current_duration -= self.duration

                self.current_state = SplashScreen.DISPLAY

                self.mask.set_alpha(0)
            else:
                # Alpha has to go from 255 to 0 over duration.
                alpha = 255 - int(255 * self.tween(self.current_duration / self.duration))
                self.mask.set_alpha(alpha)

        elif self.current_state == SplashScreen.FADE_OUT:
            if self.current_duration > self.duration:
                self.current_duration -= self.duration

                self.current_state = SplashScreen.FADE_IN

                self.current_image += 1
                if self.current_image >= len(self.images):
                    self.done = True
            else:
                # Alpha has to go from 0 to 255 over duration.
                alpha = int(255 * self.tween(self.current_duration / self.duration))
                self.mask.set_alpha(alpha)

        else:  # SpashScreen.DISPLAY
            if self.current_duration > self.duration:
                self.current_duration -= self.duration

                self.current_state = SplashScreen.FADE_OUT

    def draw(self):
        self.surface.blit(self.images[self.current_image], (0, 0))
        self.surface.blit(self.mask, (0, 0))
