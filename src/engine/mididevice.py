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
#  Defines a base class for MIDI devices.
#  @date 03/08/2013 Created file.  -jc
#  @author John Crawford

from patchcorral.src.data import synthesizers
from PySide import QtCore
import re  #For user-defined iteration filters.
import rtmidi
import threading
import time
import yaml



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
#  Resolves a given port OR name to a MIDI Input device.
#  @param port Integer.  If "None", will be resolved using "name".
#  @param name String.  If "None", will be resolved using "port".
#  @param midiDevs List of 2-tuples "(port number, device name)".  If "None",
#    will be resolved using a fresh device query.
#  @return engine.mididevice.MIDIInDevice object.
def getMIDIInDevice(port=None, name=None, midiDevs=None):
  if midiDevs is None:
    midiDevs = getMIDIInDevices()
  port, name, dev = _getMIDIDevice(midiDevs, port, name)
  return dev.MIDIInDevice(port)
##
#  Returns a list of the available MIDI Input Devices.
#  @return List of tuples "(portNum, portName)".
def getMIDIInDevices():
    midi = rtmidi.RtMidiIn()
    return list((port, midi.getPortName(port)) for port in range(midi.getPortCount()))

##
#  Resolves a given port OR name to a MIDI Output device.
#  @param port Integer.  If "None", will be resolved using "name".
#  @param name String.  If "None", will be resolved using "port".
#  @param midiDevs List of 2-tuples "(port number, device name)".  If "None",
#    will be resolved using a fresh device query.
#  @return engine.mididevice.MIDIOutDevice object.
def getMIDIOutDevice(port=None, name=None, midiDevs=None):
  if midiDevs is None:
    midiDevs = getMIDIOutDevices()
  port, name, dev = _getMIDIDevice(midiDevs, port, name)
  return dev.MIDIOutDevice(port, name)

##
#  Returns a list of the available MIDI Output Devices.
#  @return List of tuples "(portNum, portName)".
def getMIDIOutDevices():
    midi = rtmidi.RtMidiOut()
    return list((port, midi.getPortName(port)) for port in range(midi.getPortCount()))

##
#  Class representing a specific MIDI voice.
class MIDIVoice():

  tags = [
    'name',
    'msb',
    'lsb',
    '_pc',
    'device.portNum',
    'device.portName',
    'channel',
    'category',
    'voiceNum',
  ]

  ##
  #  Class constructor.
  #  @param name String
  #  @param device MIDIOutDevice object
  #  @param channel MIDI Channcel (1-16)
  #  @param msb Most Significant Bit
  #  @param lsb Least Significant Bit
  #  @param pc Program Change value
  #  @param category Category of the voice
  #  @param voiceNum Number of the voice as displayed on the device
  def __init__(self, name, device, channel, msb, lsb, pc, category=None, voiceNum=None):
    self.name = name
    self.msb = msb
    self.lsb = lsb
    self._pc = pc
    self.device = device
    self.channel = channel
    self.category = category
    self.voiceNum = voiceNum

  def __getitem__(self, key):
    keys = key.split('.')
    v = self
    for k in keys:
      try:
        v = getattr(v, k)
      except AttributeError:
        raise KeyError('Unable to find key {}.'.format(key))
    return v

  def __iter__(self):
    return (tag for tag in self.tags)

  def items(self):
    for key in iter(self):
      yield key, self[key]

  def keys(self):
    return iter(self)

  ##
  #  Sends the MIDI messages that will select this voice on the given device.
  #  @return None.
  def pc(self):
    self.device.sendMessage(rtmidi.MidiMessage.controllerEvent(self.channel, 0x00, self.msb))
    self.device.sendMessage(rtmidi.MidiMessage.controllerEvent(self.channel, 0x20, self.lsb))
    self.device.sendMessage(rtmidi.MidiMessage.programChange(self.channel, self._pc))

  ##
  #  For use by PyYAML.
  def __repr__(self):
    return '{}({})'.format(
      self.__class__.__name__,
      ', '.join('{}={}'.format(attr, val) for attr, val in self.items()),
    )

  def __setitem__(self, key, val):
    keys = key.split('.')
    v = self
    for k in keys[:-1]:
      try:
        v = getattr(v, k)
      except AttributeError:
        raise KeyError('Unable to find key {}.'.format(key))
    setattr(v, keys[-1], val)

  ##
  #  Method for converting this object to string.  Prints out essential information.
  def __str__(self):
    return '\n'.join('{}: {}'.format(key, val) for key, val in self.items())

  def values(self):
    for key in iter(self):
      yield self[key]

##
#  Class representing a MIDI Device.  This is an abstract base class that
#  doesn't do anything on its own.  Subclasses must populate "self.midi" with
#  an rtmidi object.
class MIDIDevice(QtCore.QObject):

  ##
  #  Class initializer.
  #  @param id Identifier for the device interface.  Can be an integer (index) or a string (name).
  #  @pre "self.midi" has been initialized.
  def __init__(self, port, name):
    super().__init__()
    # self.midi = None  #INITIALIZE THIS IN THE SUBCLASS!

    #Resolve missing details.
    if port is None:
      if name is None:
        raise ValueError('Must provide at least the "name" or "port" to identify a MIDI device.')
      portNames = list(self.midi.getPortName(port) for port in range(self.midi.getPortCount()))
      for port, portName in enumerate(portNames):
        if portName == name:
          self.portNum = port
          break
      else:
        raise ValueError('Unable to find device matching name "{}" in list "{}".'.format(name, portNames))
    else:
      portCount = self.midi.getPortCount()
      if 0 > port > portCount:
        raise ValueError('Given port "{}" is outside the expected range (0-{}).'.format(port, portCount))
      self.portNum = port
    if name is None:
      self.portName = self.midi.getPortName(port)
    else:
      self.portName = name

    #Open the MIDI port!
    self.midi.openPort(self.portNum)

  def getPortName(self):
    return self.portName

##
#  Class representing a MIDI Input Device.
class MIDIInDevice(MIDIDevice):

  eventReceived = QtCore.Signal(object)

  ##
  #  Class initializer.
  #  @param id Identifier for the device input and output interfaces.  Can be an integer (index) or
  #    a string (name).
  def __init__(self, id):
    self.midi = rtmidi.RtMidiIn()
    self.midi.setCallback(self.onMIDIMsg)
    super().__init__(id)
    self.midiOutDevice = None
    self.midiOutChannel = None
    self.forwardingLock = threading.Lock()

  ##
  #  Enables/disables forwarding of incoming MIDI events to the given output device.
  #  @param midiOutDevice MIDIOutDevice object.  If "None", will disable forwarding.
  #  @param channel If not "None", will change the channel of any incoming messages to this channel
  #    before forwarding it to the output device.
  #  @return None.
  def setMIDIOutDevice(self, midiOutDevice=None, channel=None):
    if not isinstance(midiOutDevice, MIDIOutDevice):
      raise ValueError('Given midiOutDevice "{0}" is of type "{1}"; expected type "MIDIOutDevice".'.format(
        midiOutDevice,
        type(midiOutDevice),
      ))
    if channel is not None and 0 > channel > 15:
      raise ValueError('Unexpected channel value "{0}".  Expected integer 0-15 or "None".'.format(channel))
    with self.forwardingLock:
      self.midiOutDevice = midiOutDevice
      self.midiOutChannel = channel

  def onMIDIMsg(self, data):
    print 'id(self): onMIDIMsg: Recieved data "{0}".'.format(data)
    self.eventReceived.emit(data)
    if self.midiOutDevice is not None:
      with self.forwardingLock:
        if self.midiOutChannel is not None:
          data.setChannel(self.midiOutChannel)
        self.midiOutDevice.sendMessage(data)

##
#  Class representing a MIDI Output Device.
class MIDIOutDevice(MIDIDevice):

  ID = 'Generic USB-MIDI Device'

  ## Number of the note "A0", usually the lowest supported note on the MIDI device.
  noteNumA0 = 21

  ## Offsets for the different note letters
  noteOffsets = {
    'Ab': 11,
    'A': 0,
    'A#': 1,
    'Bb': 1,
    'B': 2,
    'C': 3,
    'C#': 4,
    'Db': 4,
    'D': 5,
    'D#': 6,
    'Eb': 6,
    'E': 7,
    'F': 8,
    'F#': 9,
    'Gb': 9,
    'G': 10,
    'G#': 11,
  }

  ##
  #  Class initializer.
  #  @param port Integer port number for the MIDI device.
  #  @param name String name of the MIDI device.  If "None", will use this class's ID string.
  #  @param voices List of MIDIVoice objects available from this MIDI Device.
  #  @param defaultChannel If given, will use this channel by default for all outgoing commands.
  def __init__(self, port, name=None, voices=None, defaultChannel=None):
    if name is None:
      name = MIDIOutDevice.ID
    if voices is None:
      voices = []
    self.midi = rtmidi.RtMidiOut()
    super().__init__(port, name)
    self.voices = voices
    self._defaultChannel = defaultChannel
    self.sendLock = threading.Lock()

  ##
  #  Sets/Gets the default MIDI channel.
  #  @param defaultChannel Integer 0-15.
  #  @return Current default channel ("None" if a default hasn't been defined).
  def defaultChannel(self, defaultChannel=None):
    if defaultChannel is not None:
      if self._defaultChannel is None:
        raise ValueError('No default channel defined and no channel given.')
      self._defaultChannel = defaultChannel
    return self._defaultChannel

  ##
  #  Returns the full list of voices available from this device.
  def getVoiceList(self):
    return list(self.voices)

  ##
  #  Returns an iterator that steps over the voices.  Supports filtering.
  #  @param filter Python statement that can be evaluated such that "v" stands for a MIDIVoice
  #    object.
  #  @return Iterator object that returns MIDIVoice objects.
  def iter(self, filter='True'):
    for v in self.voices:
      if eval(filter):
        yield v

  ##
  #  Converts the given note name to a MIDI note number.
  #  @param noteName String
  #  @return Integer
  def noteName2Num(self, noteName):
    m = re.match(r'^([A-Ga-g][#b]?)(-?\d)$', noteName)
    if m is None:
      raise ValueError('Unable to parse note name "{0}".'.format(noteName))
    return self.noteNumA0 + self.noteOffsets[m.group(1)] + 12 * int(m.group(2))

  ##
  #  Plays the given note for the given number of seconds.  Returns immediately (doesn't block).
  #  @param duration Seconds to play (float or int)
  #  @param noteNum Note to play
  #  @param vel Velocity to play at
  #  @param channel Channel to play on.  If "None", will use default channel for object.
  #  @return None.
  def playNote(self, duration, note, vel, channel=None):
    if channel is None:
      if self._defaultChannel is None:
        raise ValueError('No default channel defined and no channel given.')
      channel = self._defaultChannel
    if isinstance(note, str):
      note = self.noteName2Num(note)
    onMsg = rtmidi.MidiMessage.noteOn(channel, note, vel)
    offMsg = rtmidi.MidiMessage.noteOff(channel, note)
    def play():
      self.sendMessage(onMsg)
      time.sleep(duration)
      self.sendMessage(offMsg)
    t = threading.Thread(target=play)
    t.start()

  ##
  #  Sends the given message to the MIDI device.
  #  @param msg rtmidi.MidiMessage object
  #  @return None.
  def sendMessage(self, msg):
    with self.sendLock:
      self.midi.sendMessage(msg)

  ##
  #  Sends the given messages to the MIDI device.
  #  @param msgs Any number of rtmidi.MidiMessage objects.
  #  @return None.
  def sendMessages(self, *msgs):
    for msg in msgs:
      self.midi.sendMessage(msg)
