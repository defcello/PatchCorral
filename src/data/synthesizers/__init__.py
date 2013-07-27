####################################################################################################
# Copyright 2013 John Crawford
#
# This file is part of PatchCorral.
#
# PatchCorral is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PatchCorral is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PatchCorral.  If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

from src.data.synthesizers.nordstage2 import mididevice as nordstage2
from src.data.synthesizers.rolandfantomxr import mididevice as rolandfantomxr
from src.data.synthesizers.generalmidi import mididevice as generalmidi
from src.engine import mididevice



SYNTHESIZERS = {
  nordstage2.MIDIOutDevice.ID: nordstage2,
  rolandfantomxr.MIDIOutDevice.ID: rolandfantomxr,
  'Delta 1010LT MIDI': mididevice,
  'Scarlett 18i20 USB': mididevice,
  'default': generalmidi,
}
