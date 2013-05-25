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
