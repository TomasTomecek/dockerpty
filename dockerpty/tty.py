# docker-pyty: tty.py
#
# Copyright 2014 Chris Corbyn <chris@w3style.co.uk>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import termios
import tty


class RawTerminal(object):
    """
    RawTerminal provides wrapper functionality to temporarily make the tty raw.

    This is useful when streaming data from a pseudo-terminal into the tty.

    Example:

        with RawTerminal(sys.stdin):
            do_things_in_raw_mode()
    """

    def __init__(self, fd):
        """
        Initialize a raw terminal for the tty with stdin attached to `fd`.

        Initializing the RawTerminal has no immediate side effects. The
        `start()` method must be invoked, or `with raw_terminal:` used before
        the terminal is affected.
        """

        self.fd = fd
        self.original_attributes = None


    def __enter__(self):
        """
        Invoked when a `with` block is first entered.
        """

        self.start()
        return self


    def __exit__(self, *_):
        """
        Invoked when a `with` block is finished.
        """

        self.stop()


    def start(self):
        """
        Saves the current terminal attributes and makes the tty raw.

        This method returns None immediately.
        """

        self.original_attributes = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)


    def stop(self):
        """
        Restores the terminal attributes back to before setting raw mode.

        If the raw terminal was not started, does nothing.
        """

        if self.original_attributes is not None:
            termios.tcsetattr(
                self.fd,
                termios.TCSADRAIN,
                self.original_attributes,
            )