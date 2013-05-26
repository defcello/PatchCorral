####################################################################################################
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

## @file
#  An example script for creating an iterator and using it to step through programs on a
#  Roland Fantom XR.
#  @author John Crawford
#  @date 3/12/2013 Created file.  -jc

import os
os.chdir(r'X:\2013.03.07 - Python Web Server with MIDI Controller\synthesizers')
from roland_fantom.RolandFantomXR import MIDIOutDevice
m = MIDIOutDevice(1)


i = m.iter("'SOFT PAD' == v.category")
v = m.programChange(i.next())


m.playNote(1, 'C3', 100)
m.playNote(1, 'E3', 100)
m.playNote(1, 'G3', 100)
m.playNote(1, 'C4', 100)
