# Arcana settings object
#
# By Chris Herborth (https://github.com/Taffer)
# MIT license, see LICENSE.md for details.

import json
import os


class GameSettings:
    def __init__(self, path: str, filename: str, defaults: dict) -> None:
        ''' Create a GameSettings from the given .ini file.

        Defaults are copied, so new settings are applied properly.
        '''
        self.filename = os.path.join(path, filename)
        self.ini = dict(defaults)

        if not os.path.exists(self.filename):
            # Save (and use) defaults.
            self.save()
        else:
            with open(self.filename) as fp:
                data = json.load(fp)
                for k, v in data.items():
                    # Overwrite any defaults with actual values.
                    self.ini[k] = v

    def save(self) -> None:
        parts = os.path.split(self.filename)
        if not os.path.exists(parts[0]):
            os.makedirs(parts[0])

        if os.path.exists(self.filename):
            os.unlink(self.filename)

        with open(self.filename, 'w') as fp:
            json.dump(self.ini, fp)

    def get(self, key: str) -> any:
        return self.ini[key]

    def set(self, key: str, value: any) -> None:
        self.ini[key] = value
