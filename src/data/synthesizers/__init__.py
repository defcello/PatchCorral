﻿####################################################################################################
# Copyright 2013 John Crawford
#
# This file is part of SynthServer.
#
# SynthServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SynthServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SynthServer.  If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

from src.data.synthesizers.nordstage2 import mididevice as nordstage2
from src.data.synthesizers.rolandfantomxr import mididevice as rolandfantomxr
from src.data.synthesizers.generalmidi import mididevice as generalmidi



SYNTHESIZERS = {
  nordstage2.MIDIOutDevice.ID: nordstage2,
  rolandfantomxr.MIDIOutDevice.ID: rolandfantomxr,
  'default': generalmidi,
}