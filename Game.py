# Arcana - A tile-based RPG
#
# By Chris Herborth (https://github.com/Taffer)
# MIT license, see LICENSE.md for details.

import os
import platform
import pygame
import pygame.freetype
import pygame.gfxdraw
import time

from lib import pytweening
from src.GameSettings import GameSettings
from src.SplashScreen import SplashScreen
from typing import Final


class Game:
    IDENTITY: Final = 'ca.taffer.Arcana'
    TITLE: Final = 'Arcana'

    PYGAME_VERSION: Final = (2, 0, 1)  # Expected minimum Pygame version.
    SETTINGS_FILE: Final = 'Settings.json'
    SETTINGS_DEFAULT: Final = {
        'WINDOW_WIDTH':  1280,
        'WINDOW_HEIGHT':  720,

        # Default settings.
        'music_volume': 1.0,
        'sfx_volume': 1.0,
        'voice_volume': 1.0,
        'overall_volume': 1.0,

        'lang': 'en'
    }

    def __init__(self) -> None:
        self.rsrc = {}  # TODO: Dictionary-like object that handles mods. Can also pre-load using a co-routine.
        self.settings = GameSettings(self.find_config_dir(), Game.SETTINGS_FILE, Game.SETTINGS_DEFAULT)
        self.text = {}  # TODO: Dictionary-like object that handles localization.

        self.window = None

        if Game.PYGAME_VERSION > pygame.version.vernum:
            # TODO: Localize error messages?
            raise SystemExit(f"Arcana can't run on Pygame version {pygame.version.ver}, it's too old.")

        pygame.init()
        self.create_window()

        screens = [
            pygame.image.load('assets-tmp/Antarctica without ice.jpg').convert(),
        ]
        self.screen = SplashScreen(self.window, screens, 3, pytweening.easeInQuad)

    def find_config_dir(self) -> str:
        ''' Based on the OS, find the configuration directory.
        '''
        system = platform.system()
        if system == 'Linux':
            return os.path.join(os.getenv('HOME'), '.config', Game.IDENTITY)
        elif system == 'Windows':
            return os.path.join(os.getenv('LOCALAPPDATA'), Game.IDENTITY)
        else:
            raise RuntimeError(f'Unsupported system: {system}')

    def create_window(self):
        self.window = pygame.display.set_mode((self.settings.get('WINDOW_WIDTH'), self.settings.get('WINDOW_HEIGHT')))
        pygame.display.set_caption(Game.TITLE)

        #icon = pygame.image.load(self.rsrc['assets/icon.png']).convert_alpha()
        #pygame.display.set_icon(icon)

        ignore_events = [pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN,
                         pygame.VIDEORESIZE, pygame.VIDEOEXPOSE, pygame.AUDIODEVICEADDED, pygame.AUDIODEVICEREMOVED,
                         pygame.FINGERMOTION, pygame.FINGERDOWN, pygame.FINGERUP, pygame.MULTIGESTURE,
                         pygame.DROPBEGIN, pygame.DROPCOMPLETE, pygame.DROPFILE, pygame.DROPTEXT, pygame.MIDIIN, pygame.MIDIOUT,
                         pygame.CONTROLLERDEVICEADDED, pygame.JOYDEVICEADDED, pygame.CONTROLLERDEVICEREMOVED,
                         pygame.JOYDEVICEREMOVED, pygame.CONTROLLERDEVICEREMAPPED]
        pygame.event.set_blocked(ignore_events)

    def run(self) -> None:
        # Run the game loop.
        playing = True

        prev_time = time.time()
        while playing:
            self.draw()

            now = time.time()
            dt = now - prev_time
            prev_time = now

            self.update(dt)

            if self.screen.done:
                playing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                elif event.type == pygame.KEYDOWN:
                    self.keypressed(event)
                elif event.type == pygame.KEYUP:
                    self.keyreleased(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.mousemoved(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousedown(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouseup(event)
                elif event.type == pygame.USEREVENT:
                    self.userevent(event)

            pygame.display.flip()

        pygame.quit()

    def update(self, dt: float) -> None:
        self.screen.update(dt)

    def draw(self) -> None:
        self.screen.draw()

    def keypressed(self, event: pygame.event.Event) -> None:
        pass

    def keyreleased(self, event: pygame.event.Event) -> None:
        pass

    def mousemoved(self, event: pygame.event.Event) -> None:
        pass

    def mousedown(self, event: pygame.event.Event) -> None:
        pass

    def mouseup(self, event: pygame.event.Event) -> None:
        pass

    def userevent(self, event: pygame.event.Event) -> None:
        pass
