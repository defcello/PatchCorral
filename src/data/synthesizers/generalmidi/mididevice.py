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
#  Module for communicating with Roland Fantom-XR connected over USB MIDI.
#  @date 3/8/2013 Created file.  -jc
#  @author John Crawford

from . import GM
from patchcorral.src.engine import mididevice
import itertools



#Available categories:
# AC.BRASS
# AC.GUITAR
# AC.PIANO
# ACCORDION
# BASS
# BEAT&GROOVE
# BELL
# BRIGHT PAD
# COMBINATION
# DIST.GUITAR
# DRUMS
# EL.GUITAR
# EL.PIANO
# ETHNIC
# FLUTE
# FRETTED
# HARD LEAD
# HARMONICA
# HIT&STAB
# KEYBOARDS          #Clavinet, Harpsichord, Celesta
# MALLET
# ORCHESTRA
# ORGAN
# OTHER SYNTH
# PERCUSSION
# PLUCKED
# PULSATING
# SAX
# SOFT LEAD
# SOFT PAD
# SOUND FX
# STRINGS
# SYNTH BASS
# SYNTH BRASS
# SYNTH FX
# TECHNO SYNTH
# VOX
# WIND

class MIDIOutDevice(mididevice.MIDIOutDevice):

  ID = 'Microsoft GS Wavetable Synth'

  ##
  #  Class initializer.
  #  @param port Integer port number for the MIDI device.
  #  @param name String name of the MIDI device.  If "None", will use this class's ID string. 
  #  @param defaultChannel If given, will use this channel by default for all outgoing commands.
  def __init__(self, port, name, defaultChannel=None):
    patches = list(GM.PATCHES)
    voices = []
    for ch in range(1, 17):
      for vname, msb, lsb, pc, group, vnn in patches:
        voices.append(mididevice.MIDIVoice(vname, self, ch, msb, lsb, pc, group, vnn))
    super().__init__(port, name, voices, defaultChannel)

