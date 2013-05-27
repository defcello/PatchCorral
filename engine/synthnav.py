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
#  Engine for the Synthesizer Navigator (SynthNav).

from data import synthesizers
import yamlfile
import mididevice


getMIDIInDevice(port, name=None):
  if name is None:
    midiDevs = mididevice.getMIDIInDevices()
    for dev in midiDevs:
      if dev[0] == port:
        name = dev[1]
  raise ValueError('Unable to find device matching name "{}" in list "{}".'.format(name, midiDevs))

getMIDIOutDevice(port, name=None):
  if name is None:
    midiDevs = mididevice.getMIDIOutDevices()
  getMIDIInDevice(name, midiDevs)

class SynthNav():

  def __init__(self):
    self.iter = None
    self.userdataFile = yamlfile.File('userdata.yaml')
    self.userdata = self.userdataFile.getRoot()
    self.favorites = self.userdata.get('favorites', {})
    self.midiInDevs = None
    self.midiOutDevs = None
    self.currVoiceList = None
    self.favVoicesList = None
    self.currMIDIOutDev = None
    self.refreshMIDIDevices()

  def refreshMIDIDevices(self):
    self.midiInDevs = mididevice.getMIDIInDevices()
    self.midiOutDevs = mididevice.getMIDIOutDevices()

  def addFavoriteVoice(self):
    pass

  def newVoiceList(self, filter='True'):
    pass

  def prevVoice(self):
    pass

  def nextVoice(self):
    pass

  def getCurrVoice(self):
    pass

  def saveVoiceList(self, name):
    pass
  
  ##
  #  Sets the MIDI out device to the one matching the given ID.
  #  @param id String name of the device or the port number (integer).
  #  @return "None".
  def setMIDIOutDevice(self, id)
    

  def loadVoiceList(self, name):
    pass

