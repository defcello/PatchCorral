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


# from patchcorral.src.data import synthesizers  #imported below to dodge circular import errors
from PySide import QtCore
import re  #For user-defined iteration filters.
import rtmidi
import threading
import time
import yaml



##
#  Returns a list of the available MIDI Input Devices.
#  @return List of tuples "(portNum, portName)".
def getMIDIInDevices():
    midi = rtmidi.MidiIn()
    return list((port, midi.get_port_name(port)) for port in range(midi.get_port_count()))

##
#  Returns a list of the available MIDI Output Devices.
#  @return List of tuples "(portNum, portName)".
def getMIDIOutDevices():
    midi = rtmidi.MidiOut()
    return list((port, midi.get_port_name(port)) for port in range(midi.get_port_count()))

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
    self.device = device
    self.channel = channel
    self.msb = msb
    self.lsb = lsb
    self._pc = pc
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

  ##
  #  Generates a pickle-able state for this object.
  #  @return "None".
  def __getstate__(self):
    return {
      "name": self.name,
      "deviceName": self.device.get_port_name(),
      "channel": self.channel,
      "msb": self.msb,
      "lsb": self.lsb,
      "pc": self._pc,
      "category": self.category,
      "voiceNum": self.voiceNum,
    }

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
    self.device.send_message((0xB0 | (self.channel - 1), 0x00, self.msb))
    self.device.send_message((0xB0 | (self.channel - 1), 0x20, self.lsb))
    self.device.send_message((0xC0 | (self.channel - 1), self._pc))

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
  #  Receives a pickled state and attempts to reproduce the original object.
  #  @return "None".
  def __setstate__(self, state):
    from patchcorral.src.data import synthesizers  #imported here to dodge circular import errors
    state["device"] = synthesizers.getMIDIOutDevice(None, state["deviceName"])
    del state["deviceName"]
    self.__init__(**state)

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

  ## Signals when a MIDI message has been sent or received.
  midiEvent = QtCore.Signal(object)

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
      portNames = list(self.midi.get_port_name(port) for port in range(self.midi.get_port_count()))
      for port, portName in enumerate(portNames):
        if portName == name:
          self.portNum = port
          break
      else:
        raise ValueError('Unable to find device matching name "{}" in list "{}".'.format(name, portNames))
    else:
      portCount = self.midi.get_port_count()
      if 0 > port > portCount:
        raise ValueError('Given port "{}" is outside the expected range (0-{}).'.format(port, portCount))
      self.portNum = port
    if name is None:
      self.portName = self.midi.get_port_name(port)
    else:
      self.portName = name

    #Open the MIDI port!
    self.midi.open_port(self.portNum)

  def get_port_name(self):
    return self.portName

##
#  Class representing a MIDI Input Device.
class MIDIInDevice(MIDIDevice):

  ID = 'Generic USB-MIDI Device'

  ##
  #  Class initializer.
  #  @param id Identifier for the device input and output interfaces.  Can be an integer (index) or
  #    a string (name).
  def __init__(self, port, name=None):
    if name is None:
      name = MIDIInDevice.ID
    self.midi = rtmidi.MidiIn()
    self.midi.setCallback(self.onMIDIMsg)
    super().__init__(port, name)
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
    # print('{}: onMIDIMsg: Recieved data "{}".'.format(id(self), data))
    self.midiEvent.emit(data)
    if self.midiOutDevice is not None:
      with self.forwardingLock:
        if self.midiOutChannel is not None:
          data.setChannel(self.midiOutChannel)
        self.midiOutDevice.send_message(data)

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
    self.midi = rtmidi.MidiOut()
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
      self.send_message(onMsg)
      time.sleep(duration)
      self.send_message(offMsg)
    t = threading.Thread(target=play)
    t.start()

  ##
  #  Sends the given message to the MIDI device.
  #  @param msg rtmidi.MidiMessage object
  #  @return None.
  def send_message(self, msg):
    with self.sendLock:
      self.midi.send_message(msg)
    self.midiEvent.emit(msg)

  ##
  #  Sends the given messages to the MIDI device.
  #  @param msgs Any number of rtmidi.MidiMessage objects.
  #  @return None.
  def sendMessages(self, *msgs):
    for msg in msgs:
      self.midi.send_message(msg)
