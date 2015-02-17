################################################################################
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
################################################################################

## @file
#  Engine for the Synthesizer Navigator (SynthNav).

from . import addressabletree
from . import yamlfile
from . import mididevice
from patchcorral.src.data import synthesizers
from PySide import QtCore
import re
import itertools




##
#  Class for maintaining lists of voice objects.
class MIDIVoiceList(QtCore.QObject):

  listModified = QtCore.Signal()

  ##
  #  Class constructor.
  #  @param voices List of src.engine.mididevice.MIDIVoice objects.
  #  @return "None".
  def __init__(self, voices=None):
    super().__init__(None)
    if voices is None:
      voices = []
    self.voiceList = set(voices)

  ##
  #  Add the given voice to the list.
  #  @param voice src.engine.mididevice.MIDIVoice object.
  #  @return "None".
  def add(self, voice):
    self.voiceList.add(voice)
    self.listModified.emit()

  ##
  #  Add the given voices to the list.
  #  @param voices List of src.engine.mididevice.MIDIVoice objects.
  #  @return "None".
  def adds(self, voices):
    self.voiceList |= set(voices)
    self.listModified.emit()

  ##
  #  Removes all voices from the list.
  #  @return "None".
  def clear(self):
    self.voiceList = set()
    self.listModified.emit()

  ##
  #  Enables users to reference a particular voice in the list.
  #  @param key Integer index.
  def __getitem__(self, key):
    return list(self.voiceList)[key]

  def __getstate__(self):
    return self.voiceList

  ##
  #  Returns a copy of the internal voice list.
  #  @return List of mididevice.MIDIVoice objects.
  def getVoices(self, voices=None):
    return list(self.voiceList)

  ##
  #  Iterates over the voice list.  This is what gets called by
  #  "for ... in ...".
  #  @return Iterator object.
  def __iter__(self):
    return iter(self.voiceList)

  ##
  #  Returns an iterator that, as it is iterated, will apply the current voice
  #  by calling it's "pc" method.
  #  @return Iterator object.
  def iterPC(self):
    for voice in self.voiceList:
      voice.pc()
      yield voice

  ##
  #  Magic method for getting the length of the list.
  def __len__(self):
    return len(self.voiceList)

  ##
  #  Removes the given voice from the list.
  #  @param voices Any number of src.engine.mididevice.MIDIVoice objects.
  #  @return "None".
  def remove(self, *voices):
    for voice in voices:
      self.voiceList.remove(voice)
    self.listModified.emit()

  def __setstate__(self, state):
    self.voiceList = state

  ##
  #  Sets the internal voice list to the given list.
  #  @param voices List of mididevice.MIDIVoice objects.
  #  @return "None".
  def setVoices(self, voices):
    self.voiceList = set(voices)
    self.listModified.emit()

##
#  Class for navigating voices within a single synthesizer.  Supports generation
#  of filtered lists of its voices, saving those filtered lists to file, and a
#  favorites list of voices.
class SynthNav(QtCore.QObject):

  ## Emits when the user has changed the voice filter.  Emits the new filter string.
  filterChanged = QtCore.Signal(str)

  ## Dictionary of voice lists with names as keys and MIDIVoiceList objects as values.
  voiceLists = None

  ##
  #  Class initializer.
  #  @return "None".
  def __init__(self, userdataFileName):
    super().__init__()
    self.midiInDevs = None
    self.midiOutDevs = None
    self.currFilter = None
    self.userdataFile = None
    self.userdata = None
    self.voiceLists = None
    #Call initialization functions.
    self.refreshMIDIDevices()
    self.loadUserData(userdataFileName)
    self.newVoiceList(name='all')
    self.newVoiceList(name='filtered')
    self.newVoiceList('False', 'queued', [])
    self.subscribeVoiceLists()

  ##
  #  Adds the given voice to the "favorites" list.
  #  @param voice mididevice.MIDIVoice object.  If "None", will use the
  #    currently-selected voice.
  #  @return "None".
  def addFavoriteVoice(self, voice):
    self.voiceLists['favorites'].add(voice)

  ##
  #  Manipulates the filter being used by the "filtered" voice list.
  #  @param filter String with a Python expression.  See "SynthNav.newVoiceList"
  #    for more information.  If "None", nothing will change.
  #  @param voices List of voices to use as the unfiltered data.  If "None",
  #    will use the unfiltered master voice list.
  #  @return New filter string (or current if "filter" is "None").
  #  @post "filtered" voice list will be repopulated.
  def filter(self, filter=None, voices=None):
    if filter is not None:
      self.newVoiceList(filter, 'filtered', voices)
    return self.currFilter

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
  #  @return MIDIVoiceList object.
  def getFilteredVoiceList(self):
    return self.voiceLists['filtered']

  ##
  #  Returns the currently-available MIDI output devices.
  #  @return A list of MIDIOutDevice objects.
  def getMIDIOutDevs(self):
    return self.midiOutDevs

  ##
  #  Returns the voice list corresponding with the given name.
  #  @param name Name of the voice list to load.  Stock names are "favorites",
  #    "filtered", "all", and "queued" (uses "all" by default).
  #  @return MIDIVoiceList object.
  def getVoiceList(self, name='all'):
    return self.voiceLists[name]

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
    d = {}
    exec('def f(v): return {}'.format(filter), d)
    f = d['f']
    for v in voiceList:
      if f(v):
        yield v
        
  def loadUserData(self, userdataFileName):
    self.userdataFile = yamlfile.File(userdataFileName)
    userdata = self.userdataFile.getRoot()  #Note that any modifications to this will modify
                                            #the internal structure of "userdataFile".
    self.userdata = {'voiceLists': {}}
    if userdata is not None and 'voiceLists' in userdata:
      for k, v in userdata['voiceLists'].items():
        self.userdata['voiceLists'][k] = MIDIVoiceList(v)
    if 'favorites' not in self.userdata['voiceLists']:
      self.userdata['voiceLists'] = {
        'favorites': MIDIVoiceList(),
      }
    self.voiceLists = self.userdata['voiceLists']

  ##
  #  Creates a new voice list using the given filter.
  #  @param filter Filter string for generating the list (see
  #    mididevice.MIDIOutDevice.iter for more information).
  #  @param name If not "None", will store the newly created list under the
  #    given name.  If the name is already being use by another list, this
  #    method will populate that existing list with the new voices.
  #  @param voices List of voices to use as the unfiltered data.  If "None",
  #    will use the unfiltered master voice list.
  #  @return "None".
  def newVoiceList(self, filter='True', name=None, voices=None):
    if voices is None:
      voices = self.fullVoiceList
    try:
      ret = self.voiceLists[name]
    except KeyError:
      ret = MIDIVoiceList(self.iter(filter, voices))
      if name is not None:
        assert isinstance(ret, MIDIVoiceList)
        self.voiceLists[name] = ret
    else:
      ret.setVoices(self.iter(filter, voices))
    if name == 'filtered':  #Do this at the end so listeners get the updated voice list as well.
      self.currFilter = filter
      self.filterChanged.emit(filter)
    return ret

  ##
  #  Refreshes the internal list of available MIDI devices.
  #  @return "None".
  def refreshMIDIDevices(self):
    self.midiInDevs = mididevice.getMIDIInDevices()
    midiOutDevs = mididevice.getMIDIOutDevices()
    self.midiOutDevs = list((synthesizers.getMIDIOutDevice(dev[0], dev[1]) for dev in midiOutDevs))
    self.fullVoiceList = list((itertools.chain(*(x.getVoiceList() for x in self.midiOutDevs))))

  def saveUserData(self):
    userdata = {'voiceLists': {}}
    for k, v in self.userdata['voiceLists'].items():
      if k not in ('all', 'queued', 'filtered'):
        userdata['voiceLists'][k] = list(v)
    self.userdataFile.setRoot(userdata)
    self.userdataFile.save()

  ##
  #  Stores the given voice list to the given name.
  #  @param name Name to store the list under.
  #  @param voices MIDIVoiceList object.
  #  @return "None".
  def saveVoiceList(self, name, voices):
    assert isinstance(voices, MIDIVoiceList)
    self.voiceLists[name] = voices

  ##
  #  Applies the given voice.
  #  @param voice src.engine.mididevice.MIDIVoice object.
  #  @return "None".
  def selectVoice(self, voice):
    voice.pc()

  def subscribeVoiceLists(self):
    for name, voiceList in self.voiceLists.items():
      if name not in ('all', 'queued', 'filtered'):
        voiceList.listModified.connect(self.saveUserData)
