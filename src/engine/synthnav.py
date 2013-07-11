################################################################################
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
################################################################################

## @file
#  Engine for the Synthesizer Navigator (SynthNav).

from . import addressabletree
from . import yamlfile
from . import mididevice
from src.data import synthesizers
import re
import itertools



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
  return dev.MIDIInDevice(port)

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
    return port, name, synthesizers.SYNTHESIZERS[id]
  except KeyError:
    return port, name, synthesizers.SYNTHESIZERS['default']

##
#  Class for navigating voices within a single synthesizer.  Supports generation
#  of filtered lists of its voices, saving those filtered lists to file, and a
#  favorites list of voices.
class SynthNav():

  ##
  #  Class initializer.
  #  @return "None".
  def __init__(self):
    self.userdataFile = yamlfile.File('userdata.yaml')
    self.userdata = self.userdataFile.getRoot()  #Note that any modifications to this will modify
                                                 #the internal structure of "userdataFile".
    if self.userdata is None:
      self.userdata = addressabletree.AddressableTree()
      self.userdataFile.setRoot(self.userdata)
    self.midiInDevs = None
    self.midiOutDevs = None
    self.currFilter = None
    #Call initialization functions.
    self.refreshMIDIDevices()
    self.voiceLists = {
      'favorites': self.MIDIVoiceList(),
    }
    self.newVoiceList(name='all')
    self.newVoiceList(name='filtered')
    self.newVoiceList(name='queued')

  ##
  #  Class for maintaintg lists of voice objects.
  class MIDIVoiceList:
    
    ##
    #  Class constructor.
    #  @param voices List of src.engine.mididevice.MIDIVoice objects.
    #  @return "None".
    def __init__(self, voices=None):
      if voices is None:
        voices = []
      self.voices = set(voices)
      
    ##
    #  Add the given voice to the list.
    #  @param voice src.engine.mididevice.MIDIVoice object.
    #  @return "None".
    def add(self, voice):
      self.voices.add(voice)
      
    ##
    #  Add the given voices to the list.
    #  @param voices List of src.engine.mididevice.MIDIVoice objects.
    #  @return "None".
    def adds(self, voices):
      self.voices |= set(voices)
      
    ##
    #  Enables users to reference a particular voice in the list.
    #  @param key Integer index.
    def __getitem__(self, key):
      print('getitem called with key {}'.format(key))
      return list(self.voices)[key]
      
    ##
    #  Iterates over the voice list.  This is what gets called by
    #  "for ... in ...".
    #  @return Iterator object.
    def __iter__(self):
      print('iter called')
      return iter(self.voices)
      
    ##
    #  Magic method for getting the length of the list.
    def __len__(self):
      return len(self.voices)
      
    ##
    #  Removes the given voice from the list.
    #  @param voice src.engine.mididevice.MIDIVoice object.
    #  @return "None".
    def remove(self, voice):
      self.voices.remove(voice)
      
    ##
    #  Returns an iterator that, as it is iterated, will apply the current voice
    #  by calling it's "pc" method.
    #  @return Iterator object.
    def iterPC(self):
      for voice in self.voices:
        voice.pc()
        yield voice

  ##
  #  Adds the given voice to the "favorites" list.
  #  @param voice mididevice.MIDIVoice object.  If "None", will use the
  #    currently-selected voice.
  #  @return "None".
  def addFavoriteVoice(self, voice):
    self.voiceLists['favorites'].add(voice)
    
  def getCurrCategories(self):
    return set(x.category for x in self.voiceLists['filtered'])
    
  def getCurrChannels(self):
    return set(x.channel for x in self.voiceLists['filtered'])
    
  def getCurrFilter(self):
    return self.currFilter
    
  def getCurrLSBs(self):
    return set(x.lsb for x in self.voiceLists['filtered'])
    
  def getCurrMidiOutDevPortNames(self):
    return set(x.device.portName for x in self.voiceLists['filtered'])
    
  def getCurrMidiOutDevPortNums(self):
    return set(x.device.portNum for x in self.voiceLists['filtered'])
    
  def getCurrMSBs(self):
    return set(x.msb for x in self.voiceLists['filtered'])
    
  def getCurrPCs(self):
    return set(x._pc for x in self.voiceLists['filtered'])
    
  def getCurrVoiceNums(self):
    return set(x.voiceNum for x in self.voiceLists['filtered'])
  
  ##
  #  Returns the voices that are currently available from the filtered list.
  #  @return SynthNav.MIDIVoiceList object.
  def getFilteredVoiceList(self):
    return self.voiceLists['filtered']
    
  ##
  #  Returns the currently-available MIDI output devices.
  #  @return A list of MIDIOutDevice objects.
  def getMIDIOutDevs(self):
    return self.midiOutDevs

  ##
  #  Returns an iterator that steps over the voices.  Supports filtering.
  #  @param filter Python statement that can be evaluated such that "v" stands for a MIDIVoice
  #    object.
  #  @param voices Optional list of voices to filter.  If "None", will use the unfiltered master
  #    list.
  #  @return Iterator object that returns MIDIVoice objects.
  def iter(self, filter='True', voices=None):
    if voices is None:
      voiceList = self.fullVoiceList
    else:
      voiceList = voices
    for v in self.fullVoiceList:
      if eval(filter):
        yield v

  ##
  #  Returns the voice list corresponding with the given name.
  #  @param name Name of the voice list to load.  Stock names are "favorites",
  #    "filtered", "all", and "queued" (uses "all" by default).
  #  @return SynthNav.MIDIVoiceList object.
  def getVoiceList(self, name='all'):
    return self.voiceLists[name]

  ##
  #  Creates a new voice list using the given filter.
  #  @param filter Filter string for generating the list (see
  #    mididevice.MIDIOutDevice.iter for more information).
  #  @param name If not "None", will store the newly created list under the
  #    given name.
  #  @param voices List of voices to use as the unfiltered data.  If "None",
  #    will use the unfiltered master voice list.
  #  @return "None".
  def newVoiceList(self, filter='True', name=None, voices=None):
    ret = self.MIDIVoiceList(self.iter(filter, voices))
    if name is not None:
      self.voiceLists[name] = ret
    return ret

  ##
  #  Refreshes the internal list of available MIDI devices.
  #  @return "None".
  def refreshMIDIDevices(self):
    self.midiInDevs = mididevice.getMIDIInDevices()
    midiOutDevs = mididevice.getMIDIOutDevices()
    self.midiOutDevs = list((getMIDIOutDevice(dev[0], dev[1]) for dev in midiOutDevs))
    self.fullVoiceList = list(itertools.chain(*(x.getVoiceList() for x in self.midiOutDevs)))

  ##
  #  Stores the given voice list to the given name.
  #  @param name Name to store the list under.
  #  @param voices SynthNav.MIDIVoiceList object.
  #  @return "None".
  def saveVoiceList(self, name, voices):
    self.voiceLists[name] = voices

  ##
  #  Applies the given voice.
  #  @param voice src.engine.mididevice.MIDIVoice object.
  #  @return "None".
  def selectVoice(self, voice):
    voice.pc()
