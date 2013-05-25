## @file
#  Module for communicating with Nord Stage 2 connected over USB MIDI.
#  @date 3/8/2013 Created file.  -jc
#  @author John Crawford

from .. import MIDIDevice
import rtmidi


PROGRAMS = [
  MIDIDevice.MIDIVoice('ChildrenOfEden', 0, 3, 98, '', 'D:20:4'),
]

class MIDIInDevice(MIDIDevice.MIDIInDevice):

  ##
  #  @param defaultChannel If given, will use this channel by default for all outgoing commands.
  def __init__(self, id='Nord Stage 2 MIDI'):
    MIDIDevice.MIDIInDevice.__init__(self, id)


class MIDIOutDevice(MIDIDevice.MIDIOutDevice):

  cc = {
    'Organ': {
      'Enable': 101,
    },
    'Piano': {
      'Enable': 107,
      'Type': 8,
      'Model': 29,
    },
    'Synth': {
      'Enable': 113,
      'Waveform Select': 44,
    },
  }

  synthSamples = {
    'SplitChoirAH': 20,
    'Choir ste': 21,
    'StringOrchestra': 39,
    'Harp': 43,
    'Celeste': 71,
  }

  pianoProgs = {
    'Grand Grand Imperial Bdorf': (0, 0),
    'Upright BlueSwede Ostl&Alm': (40, 0),
    'E.Piano1 EPiano 2 Mk I ClosIdeal': (49, 3),
  }

  ##
  #  @param defaultChannel If given, will use this channel by default for all outgoing commands.
  def __init__(self, id='Nord Stage 2 MIDI', defaultChannel=None):
    MIDIDevice.MIDIOutDevice.__init__(self, id, PROGRAMS, defaultChannel)

    #Select the first available program.
    self.programChange(self.voices[0])
    # msgs = []
    # msgs.append(rtmidi.MidiMessage.controllerEvent(self._defaultChannel, 0x00, 0))
    # msgs.append(rtmidi.MidiMessage.controllerEvent(self._defaultChannel, 0x20, 3))
    # msgs.append(rtmidi.MidiMessage.programChange(self._defaultChannel, 98))
    # for msg in msgs:
      # self.sendMessages(msg)

  ##
  #  @param group "Synth", "Piano", "Organ", "Bank A", "Bank B", "Bank C", "Bank D",
  #  @param program Program to select.  This may be an integer or a valid name.
  #  @param slot "A" or "B"
  def controlChange(self, group, program, slot):
    self.focusSlot(slot)
    msgs = []
    if group == 'Synth':
      if not isinstance(program, int):
        program = self.synthSamples[program]
      msgs.append(rtmidi.MidiMessage.controllerEvent(self._defaultChannel, self.cc['Synth']['Waveform Select'], program))
    elif group == 'Piano':
      if not isinstance(program, int):
        program = self.pianoProgs[program]
      msgs.append(rtmidi.MidiMessage.controllerEvent(self._defaultChannel, self.cc['Piano']['Type'], program[0]))
      msgs.append(rtmidi.MidiMessage.controllerEvent(self._defaultChannel, self.cc['Piano']['Model'], program[1]))
    else:
      raise ValueError('Unexpected group "{0}".'.format(group))
    self.sendMessages(*msgs)

  ##
  #  Enables/Disables the given group.
  #  @param group "Synth", "Piano", "Organ"
  #  @param slot "A" or "B"
  #  @param setting If "True", will enable the slot.  If "False", will disable the slot.
  #  @param exclusive If "True", will ensure that all other groups in the slot are disabled.
  def enableGroup(self, group, slot, setting=True, exclusive=False):
    self.focusSlot(slot)
    setting = 127 if setting else 0
    msgs = []
    for key in self.cc.keys():
      if key == group:
        msgs.append(rtmidi.MidiMessage.controllerEvent(self._defaultChannel, self.cc[group]['Enable'], setting))
      elif exclusive:
        msgs.append(rtmidi.MidiMessage.controllerEvent(self._defaultChannel, self.cc[key]['Enable'], 0))
    self.sendMessages(*msgs)

  ##
  #  Gives focus to the given slot.
  #  @param slot "A" or "B"
  #  @param channel Integer 0-15
  def focusSlot(self, slot):
    if slot not in ['A', 'B']:
      raise ValueError('Unexpected slot value "{0}".  Expecated "A" or "B".'.format(slot))
    slot = 0 if slot == 'A' else 127
    msg = rtmidi.MidiMessage.controllerEvent(self._defaultChannel, 68, slot)
    self.sendMessages(msg)