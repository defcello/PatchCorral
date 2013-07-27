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

from patchcorral.src.data.synthesizers.nordstage2 import mididevice as nordstage2
from patchcorral.src.data.synthesizers.rolandfantomxr import mididevice as rolandfantomxr
from patchcorral.src.data.synthesizers.generalmidi import mididevice as generalmidi
from patchcorral.src.engine import mididevice
import re



SYNTHESIZERS = {
  nordstage2.MIDIOutDevice.ID: nordstage2,
  rolandfantomxr.MIDIOutDevice.ID: rolandfantomxr,
  'Delta 1010LT MIDI': mididevice,
  'Scarlett 18i20 USB': mididevice,
  'default': generalmidi,
}

##
#  Resolves the given information to a MIDI device.
#  @param midiDevs List of 2-tuples "(port number, device name)".
#  @param port Integer.  If "None", will be resolved using "name".
#  @param name String.  If "None", will be resolved using "port".
#  @return 3-tuple "(port, name, src.data.synthesizers.*.mididevice module)".
def _getMIDIDevice(midiDevs, port=None, name=None):
  #The challenge is we have to resolve the TYPE of synthesizer.  The name is
  #going to be the easiest way to pull this off.
  if port is None:
    if name is None:
      raise ValueError('Must provide at least the "name" or "port" to identify a MIDI device.')
    for dev in midiDevs:
      if dev[1] == name:
        port = dev[0]
        break
    else:
      raise ValueError('Unable to find device matching name "{}" in list "{}".'.format(name, midiDevs))
  if name is None:
    for dev in midiDevs:
      if dev[0] == port:
        name = dev[1]
        break
    else:
      raise ValueError('Unable to find device matching port "{}" in list "{}".'.format(port, midiDevs))
  #Strip out the core ID.
  m = re.match(r'(?:\d- )?(.*)', name)
  if m is None:
    raise ValueError('Unable to parse synthesizer ID from name "{}".'.format(name))
  id = m.group(1)
  #Match the ID to a mididevice and return.
  try:
    return port, name, SYNTHESIZERS[id]
  except KeyError:
    return port, name, SYNTHESIZERS['default']

##
#  Resolves a given port OR name to a MIDI Input device.
#  @param port Integer.  If "None", will be resolved using "name".
#  @param name String.  If "None", will be resolved using "port".
#  @param midiDevs List of 2-tuples "(port number, device name)".  If "None",
#    will be resolved using a fresh device query.
#  @return engine.mididevice.MIDIInDevice object.
def getMIDIInDevice(port=None, name=None, midiDevs=None):
  if midiDevs is None:
    midiDevs = mididevice.getMIDIInDevices()
  port, name, dev = _getMIDIDevice(midiDevs, port, name)
  return dev.MIDIInDevice(port, name)

##
#  Resolves a given port OR name to a MIDI Output device.
#  @param port Integer.  If "None", will be resolved using "name".
#  @param name String.  If "None", will be resolved using "port".
#  @param midiDevs List of 2-tuples "(port number, device name)".  If "None",
#    will be resolved using a fresh device query.
#  @return engine.mididevice.MIDIOutDevice object.
def getMIDIOutDevice(port=None, name=None, midiDevs=None):
  if midiDevs is None:
    midiDevs = mididevice.getMIDIOutDevices()
  port, name, dev = _getMIDIDevice(midiDevs, port, name)
  return dev.MIDIOutDevice(port, name)
