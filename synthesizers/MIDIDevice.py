## @file
#  Defines a base class for MIDI devices.
#  @date 03/08/2013 Created file.  -jc
#  @author John Crawford

import re  #For user-defined iteration filters.
import rtmidi
import threading
import time



##
#  Returns a list of the available MIDI Input Devices.
#  @return List of tuples "(portNum, portName)".
def getMIDIInDevices():
    midi = rtmidi.RtMidiIn()
    return list((port, midi.getPortName(port)) for port in range(midi.getPortCount()))

##
#  Returns a list of the available MIDI Output Devices.
#  @return List of tuples "(portNum, portName)".
def getMIDIOutDevices():
    midi = rtmidi.RtMidiOut()
    return list((port, midi.getPortName(port)) for port in range(midi.getPortCount()))

##
#  Class representing a specific MIDI voice.
class MIDIVoice(object):

  ##
  #  Class constructor.
  #  @param name String
  #  @param msb Most Significant Bit
  #  @param lsb Least Significant Bit
  #  @param pc Program Change value
  #  @param category Category of the voice
  #  @param voiceNum Number of the voice as displayed on the device
  def __init__(self, name, msb, lsb, pc, category=None, voiceNum=None):
    self.name = name
    self.msb = msb
    self.lsb = lsb
    self._pc = pc
    self.category = category
    self.voiceNum = voiceNum

  ##
  #  Sends the MIDI messages that will select this voice on the given device.
  #  @param device MIDIDevice object
  #  @param channel Channel number (0-15)
  #  @return None.
  def pc(self, device, channel):
    device.sendMessage(rtmidi.MidiMessage.controllerEvent(channel, 0x00, self.msb))
    device.sendMessage(rtmidi.MidiMessage.controllerEvent(channel, 0x20, self.lsb))
    device.sendMessage(rtmidi.MidiMessage.programChange(channel, self._pc))

  ##
  #  Method for converting this object to string.  Prints out essential information.
  def __str__(self):
    return (
      'Name: {0}\n'.format(self.name) +
      'Category: {0}\n'.format(self.category) +
      'VoiceNum: {0}\n'.format(self.voiceNum) +
      'MSB: {0}\n'.format(self.msb) +
      'LSB: {0}\n'.format(self.lsb) +
      'PC: {0}\n'.format(self._pc)
    )

##
#  Class representing a MIDI Device.  This is an abstract base class that doesn't do anything on its
#  own.
class MIDIDevice(object):

  ##
  #  Class initializer.
  #  @param id Identifier for the device interface.  Can be an integer (index) or a string (name).
  #  @pre "self.midi" has been initialized.
  def __init__(self, id):
    # self.midi = None  #INITIALIZE THIS IN THE SUBCLASS!
    self.portNum = None
    self.portName = None

    #Find the MIDI Input details.
    if isinstance(id, int):
      #Selecting interface by port number.
      portCount = self.midi.getPortCount()
      if 0 > id > portCount:
        raise ValueError('Given id "{0}" is outside the expected range (0-{1}).'.format(id, portCount))
      self.portNum = id
      self.portName = self.midi.getPortName(id)
    elif isinstance(id, basestring):
      #Selecting interface by port name.
      self.portName = id
      portNames = list(self.midi.getPortName(port) for port in range(self.midi.getPortCount()))
      for port, portName in enumerate(portNames):
        if portName == id:
          self.portNum = port
          break
      else:
        raise ValueError('Unable to find id "{0}" in ports "{1}".'.format(id, portNames))

    #Open the MIDI port!
    self.midi.openPort(self.portNum)

##
#  Class representing a MIDI Input Device.
class MIDIInDevice(MIDIDevice):

  ##
  #  Class initializer.
  #  @param id Identifier for the device input and output interfaces.  Can be an integer (index) or
  #    a string (name).
  def __init__(self, id):
    self.midi = rtmidi.RtMidiIn()
    self.midi.setCallback(self.onMIDIMsg)
    MIDIDevice.__init__(self, id)
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
    # print 'id(self): onMIDIMsg: Recieved data "{0}".'.format(data)
    with self.forwardingLock:
      if self.midiOutChannel is not None:
        data.setChannel(self.midiOutChannel)
      if self.midiOutDevice is not None:
        self.midiOutDevice.sendMessage(data)

##
#  Class representing a MIDI Output Device.
class MIDIOutDevice(MIDIDevice):

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
  #  @param id Identifier for the device input and output interfaces.  Can be an integer (index) or
  #    a string (name).
  #  @param voices List of MIDIVoice objects available from this MIDI Device.
  #  @param defaultChannel If given, will use this channel by default for all outgoing commands.
  def __init__(self, id, voices, defaultChannel=None):
    self.midi = rtmidi.RtMidiOut()
    MIDIDevice.__init__(self, id)
    self.voices = voices
    self._defaultChannel = defaultChannel
    self.currVoice = {}
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
    if isinstance(note, basestring):
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
  #  Changes the program on the given channel to the supplied voice.
  #  @param voice MIDIVoice object
  #  @param channel Channel to issue the program change on.  If "None", will use the default channel
  #    for this object.
  #  @return The give MIDIVoice object for convenience.
  def programChange(self, voice, channel=None):
    if channel is None:
      if self._defaultChannel is None:
        raise ValueError('No default channel defined and no channel given.')
      channel = self._defaultChannel
    self.currVoice[channel] = voice
    voice.pc(self, channel)
    return voice

  ##
  #  Sends the given message to the MIDI device.
  #  @param msg rtmidi.MidiMessage object
  #  @return None.
  def sendMessage(self, msg):
    with self.sendLock:
      self.midi.sendMessage(msg)

  ##
  #  Sends the given messages to the MIDI device.
  #  @param msgs Any number of rtmidi.MidiMessage objects (e.g. "re.match(r'SYNTH', v.category)").
  #  @return None.
  def sendMessages(self, *msgs):
    for msg in msgs:
      self.midi.sendMessage(msg)