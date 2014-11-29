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

## @file
#  An example script for creating an iterator and using it to step through programs on a
#  Roland Fantom XR.
#  @author John Crawford
#  @date 3/12/2013 Created file.  -jc

import os
os.chdir(r'P:\Music Library Tools\PatchCorral')
from patchcorral.src.engine import mididevice
from patchcorral.src.engine import midirecplay
from patchcorral.src.data import synthesizers
import sys
import threading
from PySide import QtGui
import time

app = QtGui.QApplication(sys.argv)
roland = synthesizers.getMIDIOutDevice(name='FANTOM-X')
nord = synthesizers.getMIDIInDevice(name='Nord Stage 2 MIDI')
from patchcorral.src.engine import midirecplay
rp = midirecplay.MIDIRecPlay()
rp.setMIDIInDevice(nord)
rp.setMIDIOutDevice(roland)
rp.startRecording()

def evalThread():
  pdb.set_trace()

t = threading.Thread(target=evalThread)
t.start()
  
app.exec_()


#######################

rp.stopRecording()
rp.startPlaying(None, True)
