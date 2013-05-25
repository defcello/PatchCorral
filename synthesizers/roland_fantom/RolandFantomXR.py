## @file
#  Module for communicating with Roland Fantom-XR connected over USB MIDI.
#  @date 3/8/2013 Created file.  -jc
#  @author John Crawford

from . import UserVoices, PRA, PRB, PRC, PRD, PRE, PRF, PRG, PRH, GM, SRX04, SRX05, SRX06, SRX07, SRX09
import itertools
from synthesizers import MIDIDevice
import rtmidi



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

class MIDIOutDevice(MIDIDevice.MIDIOutDevice):
  
  def __init__(self, id='FANTOM-X', defaultChannel=None):
    voices = list(itertools.chain(*map(
      lambda x: x.PATCHES,
      [
        UserVoices, PRA, PRB, PRC, PRD, PRE, PRF, PRG, PRH, GM, SRX04, SRX05, SRX06, SRX07, SRX09,
      ],
    )))
    MIDIDevice.MIDIOutDevice.__init__(self, id, voices, defaultChannel)
      
