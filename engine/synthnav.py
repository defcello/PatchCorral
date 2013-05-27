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



def getMIDIInDevice(port=None, name=None, midiDevs=None):
  if midiDevs is None:
    midiDevs = mididevice.getMIDIInDevices()
  return _getMIDIDevice(port, midiDevs, name).MIDIInDevice(port)

def getMIDIOutDevice(port=None, name=None, midiDevs=None):
  if midiDevs is None:
    midiDevs = mididevice.getMIDIOutDevices()
  return _getMIDIDevice(port, midiDevs, name).MIDIOutDevice(port)

def _getMIDIDevice(port, midiDevs, name=None):
  #The challenge is we have to resolve the TYPE of synthesizer.  The name is going to be the easiest
  #way to pull this off.
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
  return synthesizers.SYNTHESIZERS[id]

##
#  Class for navigating voices within a single synthesizer.  Supports generation of filtered lists
#  of its voices, saving those filtered lists to file, and a favorites list of voices.
class SynthNav():

  ##
  #  Class initializer.
  #  @return "None".
  def __init__(self):
    self.iter = None
    self.userdataFile = yamlfile.File('userdata.yaml')
    self.userdata = self.userdataFile.getRoot()  #Note that any modifications to this will modify
                                                 #the internal structure of "userdataFile".
    self.midiInDevs = None
    self.midiOutDevs = None
    self.currVoiceList = None
    self.favVoicesList = None
    self.currMIDIOutDev = None
    self.currVoiceIdx = None
    #Call initialization functions.
    self.refreshMIDIDevices()

  ##
  #  Adds the given voice to the "favorites" list.
  #  @param voice mididevice.MIDIVoice object.  If "None", will use the currently-selected voice.
  #  @return "None".
  def addFavoriteVoice(self, voice=None):
    if voice is None:
      voice = self.getCurrVoice()
    favorites = self.userdata.get((self.currMIDIOutDev.ID, 'favorites'), [])
    if voice not in favorites:
      favorites.append(voice)
    self.userdata[(self.currMIDIOutDev.ID, 'favorites')] = favorites
    self.userdataFile.save()

  ##
  #  Returns the current synthesizer voice details.
  #  @return mididevice.MIDIVoice object.
  def getCurrVoice(self):
    return self.currVoiceList[self.currVoiceIdx]

  ##
  #  Returns the index of the current synthesizer voice in the current voice list.
  #  @Return 0-based integer.
  def getCurrVoiceIdx(self):
    return self.currVoiceIdx

  ##
  #  Returns an iterator that steps over the current voice list.
  #  @param filter For convenience, if not "None", will repopulate the current voice list using the
  #    given filter.
  #  @return Iterator object that returns MIDIVoice objects.
  def iter(self, filter=None):
    if filter is not None:
      self.newVoiceList(filter)
    for v in self.currVoiceList:
      yield v

  ##
  #  Loads the voice list under the given name and sets it as the current voice list.
  #  @param name Name of the voice list to load.
  #  @return "None".
  #  @throws KeyError If the given name could not be resolved.
  def loadVoiceList(self, name='favorites'):
    if self.currVoiceIdx is not None:
      currVoice = self.currVoiceList[self.currVoiceIdx]
    self.currVoiceList = self.userdata[(self.currMIDIOutDev.ID, name)]
    #Try to reselect the previous voice.
    try:
      self.currVoiceIdx = self.currVoiceList.index(currVoice)
    except ValueError:
      self.currVoiceIdx = None

  ##
  #  Creates a new voice list using the given filter.
  #  @param filter Filter string for generating the list (see mididevice.MIDIOutDevice.iter for more
  #    information).
  #  @return "None".
  def newVoiceList(self, filter='True'):
    if self.currVoiceIdx is not None:
      currVoice = self.currVoiceList[self.currVoiceIdx]
    self.currVoiceList = list(self.currMIDIOutDev.iter(filter))
    #Try to reselect the previous voice.
    try:
      self.currVoiceIdx = self.currVoiceList.index(currVoice)
    except ValueError:
      self.currVoiceIdx = None

  ##
  #  Refreshes the internal list of available MIDI devices.
  #  @return "None".
  def refreshMIDIDevices(self):
    self.midiInDevs = mididevice.getMIDIInDevices()
    self.midiOutDevs = mididevice.getMIDIOutDevices()

  ##
  #  Stores the current voice list to the given name.
  #  @param name Name to store the list under.
  #  @return "None".
  def saveVoiceList(self, name):
    self.userdata.set((self.currMIDIOutDev.ID, name), self.currVoiceList)
    self.userdataFile.save()

  ##
  #  Applies the voice at the given index of the current voice list to the synthesizer, making it
  #  the current synthesizer voice.
  #  @param idx 0-based integer.
  #  @return "None".
  def selectVoice(self, idx):
    #We want it to throw an index error if there's a problem without messing up the state of the
    #object, so order matters!
    voice = self.currVoiceList[idx]
    self.currVoiceIdx = idx

  ##
  #  Sets the MIDI input device to the one matching the given ID.
  #  @param id String name of the device or the port number (integer).
  #  @return "None".
  def setMIDIInDevice(self, id)
    if isinstance(id, int):
      self.currMIDIInDev = getMIDIInDevice(id, None, self.midiInDevs)
    else:
      self.currMIDIInDev = getMIDIInDevice(None, id, self.midiInDevs)

  ##
  #  Sets the MIDI output device to the one matching the given ID.
  #  @param id String name of the device or the port number (integer).
  #  @return "None".
  def setMIDIOutDevice(self, id)
    if isinstance(id, int):
      self.currMIDIOutDev = getMIDIOutDevice(id, None, self.midiOutDevs)
    else:
      self.currMIDIOutDev = getMIDIOutDevice(None, id, self.midiOutDevs)
    #Initialize the userdata file for the new device.
    if self.userdata.get( (self.currMIDIOutDev.ID, 'favorites') ) is None:
      self.userdata.set((self.currMIDIOutDev.ID, 'favorites'), [])   
      self.userdataFile.save()
    
