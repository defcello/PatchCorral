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
#  Voices to be used with the musical "Children of Eden".

from engine.mididevice import MIDIVoice
import itertools
import traceback



## Mappings of Instrument Names to Patches in the Roland Fantom-XR
PATCHES = {
  'Accordion': [
    MIDIVoice('Accordion It', 121, 1, 21, 'ACCORDION', 'GM 051'),  #Not great, but sufficient
    MIDIVoice('Accordion Fr', 121, 0, 21, 'ACCORDION', 'GM 050'),
  ],
  'Analog Seq.': [
    MIDIVoice('Candy Bell', 87, 64, 60, 'BELL', 'PR-A 061'),  #Nice!
    MIDIVoice('Beat Vox', 87, 67, 83, 'VOX', 'PR-D 084'),
    MIDIVoice('Beat Vox', 87, 1, 27, 'VOX', 'USER 156'),
  ],
  'Analog Synth': [
    MIDIVoice('Analog Bell', 93, 11, 63, 'BELL', 'XP-C 064'),  #Not great, but sufficient
    MIDIVoice('AnalogMaster', 93, 6, 17, 'SYNTH BRASS', 'XP-D 274'),
  ],
  'Analog Synth Pad': [
    MIDIVoice('Sine Pad', 121, 1, 89, 'SOFT PAD', 'GM 174'),  #Not bad!
    MIDIVoice('Introductory', 93, 5, 75, 'BRIGHT PAD', 'XP-D 204'),
    MIDIVoice('AnalogMaster', 93, 6, 17, 'SYNTH BRASS', 'XP-D 274'),
    MIDIVoice('Analog Bell', 93, 11, 63, 'BELL', 'XP-C 064'),
    MIDIVoice('M12 Strings', 93, 13, 16, 'STRINGS', 'XP-C 273'),
    MIDIVoice('Sawed String', 93, 14, 52, 'SOFT PAD', 'XP-C 437'),
    MIDIVoice('JP-8 Phase', 87, 71, 100, 'SOFT PAD', 'PR-H 101'),
    MIDIVoice('Machine Str', 87, 0, 99, 'STRINGS', 'USER 100'),  #Too stringsy
    MIDIVoice('JP-8 Phase', 87, 1, 122, 'SOFT PAD', 'USER 251'),  #Too slow
    MIDIVoice('FS Sqr Pad', 87, 67, 99, 'SOFT PAD', 'PR-D 100'),  #Nice, but too slow
    MIDIVoice('Electric Pad', 87, 68, 17, 'BRIGHT PAD', 'PR-E 018'),  #OMGSLOWWWWWWW
    MIDIVoice('Machine Str', 87, 70, 32, 'STRINGS', 'PR-G 033'),  #Slow and too harsh
  ],
  'Angels Sing': [
    MIDIVoice('Choir Aahs 2', 87, 67, 86, 'VOX', 'PR-D 087'),  #Good enough
    MIDIVoice('Angelic Pad', 93, 9, 120, 'VOX', 'XP-E 377'),  #Not bad.
    MIDIVoice('Film Cue', 87, 71, 111, 'VOX', 'PR-H 112'),
    MIDIVoice('Choral Sweep', 87, 71, 112, 'VOX', 'PR-H 113'),
    MIDIVoice('StChrMm/Ah S', 93, 9, 127, 'VOX', 'XP-E 384'),  #Too much "Mmmm", but might work.
    MIDIVoice('Angels Choir', 87, 67, 88, 'VOX', 'PR-D 089'),  #Not angelic enough
    MIDIVoice('Film Cue', 87, 0, 117, 'VOX', 'USER 118'),  #Not angelic enough
    MIDIVoice('Choral Sweep', 87, 1, 71, 'VOX', 'USER 200'),  #Too synthy
    MIDIVoice('Angelique', 87, 67, 89, 'VOX', 'PR-D 090'),  #Great start, but drops off
    MIDIVoice('Morning Star', 87, 67, 93, 'VOX', 'PR-D 094'),  #Nice start, but weird climbing sound
  ],
  'Applause SFX': [
    MIDIVoice('Applause', 121, 0, 126, 'SOUND FX', 'GM 247'),
  ],
  'Balafoni': [
    MIDIVoice('Balafon SRX', 93, 20, 91, 'MALLET', 'XP-B 220'),  #Spot on
  ],
  'Bass in Face': [
    MIDIVoice('Mini Like!', 87, 69, 127, 'SYNTH BASS', 'PR-F 128'),  #Good, but mono-tonic
    MIDIVoice('Da Chronic', 87, 1, 21, 'SYNTH BASS', 'USER 150'),   #Good, but mono-tonic
    MIDIVoice('Nu Bace', 87, 1, 34, 'SYNTH BASS', 'USER 163'),  #Too subtle
    MIDIVoice('MC-404 Bass', 87, 65, 38, 'SYNTH BASS', 'PR-B 039'),  #Meh, and mono-tonic
    MIDIVoice('SH-101 Bs 1', 87, 65, 39, 'SYNTH BASS', 'PR-B 040'),  #Mono-tonic
    MIDIVoice('Kickin\' Bass', 87, 65, 66, 'SYNTH BASS', 'PR-B 067'),  #Annoying percussion
    MIDIVoice('R&B Bass 4', 87, 65, 79, 'SYNTH BASS', 'PR-B 080'),  #It's a sine wave...
    MIDIVoice('Nu Bace', 87, 69, 126, 'SYNTH BASS', 'PR-F 127'),  #Weak mid-range
  ],
  'Bass Kalimba': [
    MIDIVoice('Kalimba', 93, 20, 85, 'MALLET', 'XP-B 214'),  #A little too sustained, but sounds good
    MIDIVoice('Kalimba', 121, 0, 108, 'PLUCKED', 'GM 199'),
    MIDIVoice('Kalimbatch', 93, 20, 86, 'MALLET', 'XP-B 215'),
    MIDIVoice('Kalimbells', 87, 64, 54, 'BELL', 'PR-A 055'),  #Not sure...
  ],
  'Bass Marimba': [
    MIDIVoice('Marimba', 121, 0, 12, 'MALLET', 'GM 030'),  #Bingo
    MIDIVoice('Marimba w', 121, 1, 12, 'MALLET', 'GM 031'),
  ],
  'Bassoon': [
    MIDIVoice('Bassoon III', 93, 8, 64, 'WIND', 'XP-E 193'),  #Excellent, but Mono-tonic
    MIDIVoice('Bassoon', 121, 0, 70, 'WIND', 'GM 146'),  #Sounds fake
    MIDIVoice('Bassoon', 87, 65, 127, 'WIND', 'PR-B 128'),  #Sounds fake
  ],
  'Beauty Vox': [
    MIDIVoice('StChrMm/Ah S', 93, 9, 127, 'VOX', 'XP-E 384'),  #Pretty good!
    MIDIVoice('RealChoirSRX', 93, 9, 126, 'VOX', 'XP-E 383'),
    MIDIVoice('Mmms & Aaahs', 93, 10, 0, 'VOX', 'XP-E 385'),
    MIDIVoice('Choir /Mod', 93, 10, 1, 'VOX', 'XP-E 386'),
    MIDIVoice('Film Cue', 87, 0, 117, 'VOX', 'USER 118'),  #Too slow
    MIDIVoice('Choir Aahs 2', 87, 67, 86, 'VOX', 'PR-D 087'),  #Too choiry
    MIDIVoice('Film Cue', 87, 71, 111, 'VOX', 'PR-H 112'),
    MIDIVoice('Angelic Pad', 93, 9, 120, 'VOX', 'XP-E 377'),  #Pretty good, though not quiet "beauty"
  ],
  'Bell Pad': [
    MIDIVoice('Dreaming Box', 87, 64, 56, 'BELL', 'PR-A 057'),  #Works for me
    MIDIVoice('HimalayaThaw', 87, 69, 42, 'BELL', 'PR-F 043'),
    MIDIVoice('Bell Monitor', 87, 69, 44, 'BELL', 'PR-F 045'),
    MIDIVoice('SpectrumBell', 93, 5, 120, 'BELL', 'XP-D 249'),
    MIDIVoice('Troika Ride', 93, 11, 62, 'BELL', 'XP-C 063'),
    MIDIVoice('HybridKemong', 93, 20, 73, 'BELL', 'XP-B 202'),
    MIDIVoice('HimalayaThaw', 87, 0, 9, 'BELL', 'USER 010'),  #Double-hit is bad
    MIDIVoice('Dreaming Box', 87, 0, 126, 'BELL', 'USER 127'),  #Nice, but drops out too quickly
    MIDIVoice('Himalaya Ice', 87, 64, 55, 'BELL', 'PR-A 056'),  #Annoying vibe, but otherwise good
  ],
  'Bell Synth': [
    MIDIVoice('Ballad Bells', 87, 69, 43, 'BELL', 'PR-F 044'),  #Good enough
  ],
  'Big Organ': [
    MIDIVoice('Church Org.2', 121, 1, 19, 'ORGAN', 'GM 046'),
    MIDIVoice('Mid Pipe Org', 87, 69, 58, 'ORGAN', 'PR-F 059'),
    MIDIVoice('Grand Pipe', 87, 64, 91, 'ORGAN', 'PR-A 092'),  #Pretty good, but annoying pitch bend
    MIDIVoice('Grand Pipe', 87, 0, 57, 'ORGAN', 'USER 058'),  #Awkwardly big
    MIDIVoice('R&B Organ 2', 87, 64, 83, 'ORGAN', 'PR-A 084'),  #Annoying percussion
  ],
  'Big Strings': [
    MIDIVoice('SymphStrings', 93, 3, 12, 'STRINGS', 'XP-A 013'),  #Good enough!
    MIDIVoice('Epic Strings', 93, 3, 0, 'STRINGS', 'XP-A 001'),  #Harsh
    MIDIVoice('Full Strings', 87, 0, 2, 'STRINGS', 'USER 003'),  #Empty sounding
    MIDIVoice('LargeStrings', 93, 3, 88, 'STRINGS', 'XP-A 089'),  #Too quick, not enough depth
    MIDIVoice('Full Strings', 87, 70, 18, 'STRINGS', 'PR-G 019'),  #Shallow
  ],
  'Breathy String Pad': [
    MIDIVoice('Warm Strings', 87, 65, 103, 'STRINGS', 'PR-B 104'),  #Works for me
    MIDIVoice('MistOver5ths', 87, 68, 18, 'BRIGHT PAD', 'PR-E 019'),
    MIDIVoice('Tronic Str', 87, 70, 31, 'STRINGS', 'PR-G 032'),
    MIDIVoice('SymphStrings', 93, 3, 12, 'STRINGS', 'XP-A 013'),
    MIDIVoice('Introductory', 93, 5, 75, 'BRIGHT PAD', 'XP-D 204'),
    MIDIVoice('Old Tale', 93, 7, 78, 'STRINGS', 'XP-E 079'),
    MIDIVoice('Ethno Strngs', 93, 21, 57, 'SOFT PAD', 'XP-B 314'),
  ],
  'Brite Synth': [
    MIDIVoice('Sleeper', 87, 67, 76, 'OTHER SYNTH', 'PR-D 077'),  #Good!
    MIDIVoice('Ice Rain', 121, 0, 96, 'OTHER SYNTH', 'GM 182'),
    MIDIVoice('Fantasia', 121, 0, 88, 'OTHER SYNTH', 'GM 172'),
    MIDIVoice('ImitatEP Pad', 93, 3, 100, 'OTHER SYNTH', 'XP-A 101'),
    MIDIVoice('Andes', 93, 4, 81, 'OTHER SYNTH', 'XP-D 082'),
    MIDIVoice('Once Upon A', 93, 9, 110, 'OTHER SYNTH', 'XP-E 367'),
    MIDIVoice('Reflections', 93, 14, 1, 'OTHER SYNTH', 'XP-C 386'),
  ],
  'Brite Synth Bells': [
    MIDIVoice('Ballad Bells', 87, 69, 43, 'BELL', 'PR-F 044'),  #Great!
    MIDIVoice('Bell Monitor', 87, 69, 44, 'BELL', 'PR-F 045'),
    MIDIVoice('Victoriana 1', 93, 9, 43, 'BELL', 'XP-E 300'),
    MIDIVoice('Victoriana 2', 93, 9, 45, 'BELL', 'XP-E 302'),
    MIDIVoice('Troika Ride', 93, 11, 62, 'BELL', 'XP-C 063'),
    MIDIVoice('Wind Bells', 93, 20, 81, 'BELL', 'XP-B 210'),
    MIDIVoice('Dreaming Box', 87, 0, 126, 'BELL', 'USER 127'),
    MIDIVoice('Dreaming Box', 87, 64, 56, 'BELL', 'PR-A 057'),
  ],
  'Celesta': [
    MIDIVoice('FS Celesta', 87, 64, 49, 'KEYBOARDS', 'PR-A 050'),  #Great!
    MIDIVoice('Celesta', 121, 0, 8, 'KEYBOARDS', 'GM 025'),
    MIDIVoice('Celesta SRX', 93, 9, 39, 'KEYBOARDS', 'XP-E 296'),
  ],
  'Chapel Organ': [
    MIDIVoice('Puff Organ', 121, 1, 20, 'ORGAN', 'GM 049'),  #Winner!
    MIDIVoice('Chapel Organ', 87, 64, 90, 'ORGAN', 'PR-A 091'),  #Good, but not touch sensitive
    MIDIVoice('OrgFlutes S2', 93, 9, 63, 'ORGAN', 'XP-E 320'),  #Okay...
  ],
  'Chorused Piano': [
    MIDIVoice('St.EuroPiano', 93, 9, 18, 'AC.PIANO', 'XP-E 275'),  #Perfect
  ],
  'Church Organ': [
    MIDIVoice('R&B Organ 1', 87, 64, 82, 'ORGAN', 'PR-A 083'),  #Nice!
    MIDIVoice('60\'s Org 1', 87, 64, 87, 'ORGAN', 'PR-A 088'),
    MIDIVoice('FS SoapOpera', 87, 64, 89, 'ORGAN', 'PR-A 090'),
    MIDIVoice('Organ 1', 121, 0, 16, 'ORGAN', 'GM 037'),
    MIDIVoice('70\'s E.Organ', 121, 3, 16, 'ORGAN', 'GM 040'),
    MIDIVoice('Church Org.1', 121, 0, 19, 'ORGAN', 'GM 045'),
    MIDIVoice('Church Org.3', 121, 2, 19, 'ORGAN', 'GM 047'),
    MIDIVoice('GreenB /Pdl', 93, 11, 71, 'ORGAN', 'XP-C 072'),
    MIDIVoice('Hush B3 SRX', 93, 11, 77, 'ORGAN', 'XP-C 078'),
    MIDIVoice('Real Organ', 93, 11, 78, 'ORGAN', 'XP-C 079'),
    MIDIVoice('Absolute B3', 93, 11, 86, 'ORGAN', 'XP-C 087'),
    MIDIVoice('Suitcase B3', 93, 11, 88, 'ORGAN', 'XP-C 089'),
    MIDIVoice('Leslied B3', 93, 11, 91, 'ORGAN', 'XP-C 092'),
    MIDIVoice('60s Brothers', 93, 11, 106, 'ORGAN', 'XP-C 107'),
    MIDIVoice('R&R B3 SRX', 93, 11, 114, 'ORGAN', 'XP-C 115'),
    MIDIVoice('B3Sermon SRX', 93, 11, 115, 'ORGAN', 'XP-C 116'),
    MIDIVoice('ShimmerOrgan', 93, 11, 125, 'ORGAN', 'XP-C 126'),
    MIDIVoice('AnimalModSRX', 93, 11, 126, 'ORGAN', 'XP-C 127'),
    MIDIVoice('PalisadesSRX', 93, 12, 3, 'ORGAN', 'XP-C 132'),
    MIDIVoice('Farfisorium', 93, 12, 9, 'ORGAN', 'XP-C 138'),
    MIDIVoice('FS SoapOpera', 87, 0, 113, 'ORGAN', 'USER 114'),  #Cheesy
  ],
  'Cimbalom': [
    MIDIVoice('HamrDulcimer', 93, 19, 89, 'PLUCKED', 'XP-B 090'),  #Perfect
  ],
  'D-50 Stack': [
    MIDIVoice('D50 OrganSRX', 93, 12, 16, 'ORGAN', 'XP-C 145'),  #Works for me!
    MIDIVoice('D50Belpd1SRX', 93, 13, 124, 'OTHER SYNTH', 'XP-C 381'),
    MIDIVoice('D50Belpd2SRX', 93, 13, 125, 'OTHER SYNTH', 'XP-C 382'),
    MIDIVoice('D50Belpd3SRX', 93, 13, 126, 'OTHER SYNTH', 'XP-C 383'),
  ],
  'Dig. Rhodes': [
    MIDIVoice('FM-777', 87, 64, 35, 'EL.PIANO', 'PR-A 036'),  #Good
    MIDIVoice('Sine EP', 93, 11, 18, 'EL.PIANO', 'XP-C 019'),
  ],
  'Dulcimer': [
    MIDIVoice('HamrDulcimer', 93, 19, 89, 'PLUCKED', 'XP-B 090'),  #Good
  ],
  'Electric Piano': [
    MIDIVoice('EP mkI', 87, 69, 5, 'EL.PIANO', 'PR-F 006'),  #Nice sound, with a risky stereo ping pong
    MIDIVoice('Celestial EP', 87, 64, 21, 'EL.PIANO', 'PR-A 022'),  #Nice, but muted
    MIDIVoice('1983 EP', 87, 69, 32, 'EL.PIANO', 'PR-F 033'),  #Good, but not enough percussion
    MIDIVoice('E.Piano 1', 121, 0, 4, 'EL.PIANO', 'GM 010'),  #Too soft
  ],
  'English Horn': [
    MIDIVoice('English Horn', 87, 65, 126, 'WIND', 'PR-B 127'),  #Good enough
    MIDIVoice('English Horn', 121, 0, 69, 'WIND', 'GM 145'),  #Heavy attack, but otherwise good
  ],
  'Ethereal': [
    MIDIVoice('Space Voice', 121, 0, 91, 'VOX', 'GM 176'),  #Not ghosty enough
    MIDIVoice('SynVox', 121, 0, 54, 'VOX', 'GM 115'),  #Too vocal
    MIDIVoice('SmockyVoices', 93, 9, 123, 'VOX', 'XP-E 380'),  #Weird fluctuating volume, and too slow release
    MIDIVoice('Ethereal SRX', 93, 13, 112, 'SYNTH FX', 'XP-C 369'),  #Weird, but nice!
  ],
  'Ethnic Bassoon': [
    MIDIVoice('Shanai', 121, 0, 111, 'ETHNIC', 'GM 202'),  #Okay
    MIDIVoice('FS Lochscape', 87, 68, 88, 'ETHNIC', 'PR-E 089'),  #Blech
  ],
  'Ethnic Harp': [
    MIDIVoice('ClarsahHarpS', 93, 10, 16, 'PLUCKED', 'XP-E 401'),  #Nice sound, a little too sensitive on the volume though
    MIDIVoice('Afro Harp', 93, 19, 67, 'PLUCKED', 'XP-B 068'),  #Pretty good
    MIDIVoice('ClarsahHarpS', 93, 10, 16, 'PLUCKED', 'XP-E 401'),  #Too dynamic in volume
  ],
  'Ethnic Pluck': [
    MIDIVoice('ClarsahHarpS', 93, 10, 16, 'PLUCKED', 'XP-E 401'),  #Nice sound, a little too sensitive on the volume though
    MIDIVoice('Asian Pizz', 93, 19, 56, 'PLUCKED', 'XP-B 057'),
    MIDIVoice('Afro Harp', 93, 19, 67, 'PLUCKED', 'XP-B 068'),
    MIDIVoice('AsianOrcPizz', 93, 20, 46, 'STRINGS', 'XP-B 175'),
    MIDIVoice('AncientTimes', 93, 9, 112, 'OTHER SYNTH', 'XP-E 369'),  #Not liking the vocals
  ],
  'Evoc. Bell Synth': [
    MIDIVoice('Ballad Bells', 87, 69, 43, 'BELL', 'PR-F 044'),  #Great!
    MIDIVoice('Bell Orchest', 93, 20, 77, 'BELL', 'XP-B 206'),  #Too subtle
    MIDIVoice('SpectrumBell', 93, 5, 120, 'BELL', 'XP-D 249'),  #Harsh; high-pitched
  ],
  'Evol. Synth': [
    MIDIVoice('Story Harp', 87, 67, 79, 'OTHER SYNTH', 'PR-D 080'),  #Works
  ],
  'Explosion SFX': [
    MIDIVoice('Explosion', 121, 3, 127, 'SOUND FX', 'GM 256'),
  ],
  'Fantasia JV': [
    MIDIVoice('EP mkI', 87, 69, 5, 'EL.PIANO', 'PR-F 006'),  #Good with risky ping-pong
    MIDIVoice('FirstDigital', 93, 11, 35, 'EL.PIANO', 'XP-C 036'),
    MIDIVoice('Victoriana 1', 93, 9, 43, 'BELL', 'XP-E 300'),
  ],
  'Fantasy Vox': [
    MIDIVoice('ChoirOoh/Aft', 87, 67, 87, 'VOX', 'PR-D 088'),  #Might work!
    MIDIVoice('Angels Choir', 87, 67, 88, 'VOX', 'PR-D 089'),
    MIDIVoice('Morning Star', 87, 67, 93, 'VOX', 'PR-D 094'),
    MIDIVoice('Film Cue', 87, 71, 111, 'VOX', 'PR-H 112'),
    MIDIVoice('SynVox', 121, 0, 54, 'VOX', 'GM 115'),
    MIDIVoice('StChrMm/Ah S', 93, 9, 127, 'VOX', 'XP-E 384'),
    MIDIVoice('Ethereal SRX', 93, 13, 112, 'SYNTH FX', 'XP-C 369'),
    MIDIVoice('Film Cue', 87, 0, 117, 'VOX', 'USER 118'),  #Nice, but slow attack
    MIDIVoice('Itopia', 121, 1, 91, 'VOX', 'GM 177'),  #Annoying swell
    MIDIVoice('Choir Aahs 2', 87, 67, 86, 'VOX', 'PR-D 087'),  #Too warm
    MIDIVoice('Lost Voices', 87, 71, 115, 'VOX', 'PR-H 116'),  #Slow attack and weird pad
  ],
  'Fast Strings': [
    MIDIVoice('Staccato VS', 87, 0, 38, 'STRINGS', 'USER 039'),  #Good enough
    MIDIVoice('2-way Sect.', 87, 65, 102, 'STRINGS', 'PR-B 103'),
    MIDIVoice('Staccato VS', 87, 70, 26, 'STRINGS', 'PR-G 027'),
    MIDIVoice('Fast Section', 93, 3, 10, 'STRINGS', 'XP-A 011'),
    MIDIVoice('Pop Strings', 93, 3, 91, 'STRINGS', 'XP-A 092'),
  ],
  'Flutey Organ': [
    MIDIVoice('Puff Organ', 121, 1, 20, 'ORGAN', 'GM 049'),  #Winner!
    MIDIVoice('OrgFlute 8\'S', 93, 9, 65, 'ORGAN', 'XP-E 322'),
    MIDIVoice('Psyche Pipes', 93, 9, 66, 'ORGAN', 'XP-E 323'),
    MIDIVoice('ChrchPipes S', 93, 9, 67, 'ORGAN', 'XP-E 324'),
    MIDIVoice('Organ&Recdr', 93, 9, 68, 'ORGAN', 'XP-E 325'),
    MIDIVoice('PalisadesSRX', 93, 12, 3, 'ORGAN', 'XP-C 132'),
    MIDIVoice('OrgFlutes S1', 93, 9, 62, 'ORGAN', 'XP-E 319'),  #Great!  But not touch sensitive...
    MIDIVoice('OrgFlutes S3', 93, 9, 64, 'ORGAN', 'XP-E 321'),  #Nice, but not touch sensitive
  ],
  'Gamelan': [
    MIDIVoice('Gamelan Ems', 93, 19, 9, 'MALLET', 'XP-B 010'),  #Good
  ],
  'Gentle Pad': [
    MIDIVoice('FS Soft Pad', 87, 67, 103, 'SOFT PAD', 'PR-D 104'),  #Great!
    MIDIVoice('Soft Breeze', 87, 67, 104, 'SOFT PAD', 'PR-D 105'),
    MIDIVoice('Digitvox', 87, 71, 73, 'BRIGHT PAD', 'PR-H 074'),
    MIDIVoice('OBSftPad SRX', 93, 14, 36, 'SOFT PAD', 'XP-C 421'),
    MIDIVoice('Too Heaven', 93, 14, 45, 'SOFT PAD', 'XP-C 430'),
    MIDIVoice('Digitvox', 87, 0, 92, 'BRIGHT PAD', 'USER 093'),  #Weird attack
  ],
  'Harmonium': [
    MIDIVoice('Puff Organ', 121, 1, 20, 'ORGAN', 'GM 049'),  #Winner!
    MIDIVoice('Harmonium', 93, 9, 71, 'ORGAN', 'XP-E 328'),  #Perfect match
  ],
  'Harp': [
    MIDIVoice('Pearly Harp', 87, 0, 98, 'PLUCKED', 'USER 099'),  #Good
    MIDIVoice('Aerial Harp', 87, 68, 78, 'PLUCKED', 'PR-E 079'),
    MIDIVoice('Pearly Harp', 87, 71, 117, 'PLUCKED', 'PR-H 118'),
    MIDIVoice('Harp', 121, 0, 46, 'PLUCKED', 'GM 101'),
    MIDIVoice('Harp SRX', 93, 10, 22, 'PLUCKED', 'XP-E 407'),
    MIDIVoice('Warm Harp', 93, 10, 24, 'PLUCKED', 'XP-E 409'),
  ],
  'Harp/Bells': [
    MIDIVoice('Story Harp', 87, 67, 79, 'OTHER SYNTH', 'PR-D 080'),  #Works
    MIDIVoice('LostParadise', 87, 67, 80, 'OTHER SYNTH', 'PR-D 081'),
  ],
  'Harpsichord': [
    MIDIVoice('Harpsi.o', 121, 3, 6, 'KEYBOARDS', 'GM 022'),  #Good enough
    MIDIVoice('Harpsichord', 121, 0, 6, 'KEYBOARDS', 'GM 019'),  #Works, but a little muddy
    MIDIVoice('HpsBackSRX 1', 93, 9, 27, 'KEYBOARDS', 'XP-E 284'),
    MIDIVoice('Hps F/B SRX', 93, 9, 30, 'KEYBOARDS', 'XP-E 287'),
    MIDIVoice('FullHarpsi 2', 93, 9, 37, 'KEYBOARDS', 'XP-E 294'),
    MIDIVoice('Continuo Pdl', 93, 9, 38, 'KEYBOARDS', 'XP-E 295'),
    MIDIVoice('HpsFrntSRX 1', 93, 9, 24, 'KEYBOARDS', 'XP-E 281'),  #No touch sensitivity
    MIDIVoice('FullHarpsi 1', 93, 9, 36, 'KEYBOARDS', 'XP-E 293'),  #Eeek!  Too loud!
  ],
  'Hazy Pad': [
    MIDIVoice('WarmReso Pad', 87, 67, 102, 'SOFT PAD', 'PR-D 103'),  #Might work
    MIDIVoice('Soft Breeze', 87, 67, 104, 'SOFT PAD', 'PR-D 105'),
    MIDIVoice('FS Syn Str', 87, 67, 107, 'SOFT PAD', 'PR-D 108'),
    MIDIVoice('Sonic Surfer', 87, 68, 9, 'BRIGHT PAD', 'PR-E 010'),
    MIDIVoice('MistOver5ths', 87, 68, 18, 'BRIGHT PAD', 'PR-E 019'),
    MIDIVoice('Steam Pad', 93, 5, 81, 'SOFT PAD', 'XP-D 210'),
    MIDIVoice('Old Tale', 93, 7, 78, 'STRINGS', 'XP-E 079'),
    MIDIVoice('FS Hollow', 87, 67, 100, 'SOFT PAD', 'PR-D 101'),  #Not confident
  ],
  'Hi Ethnic Flute': [
    MIDIVoice('LongDistance', 87, 68, 85, 'ETHNIC', 'PR-E 086'),  #Good!
    MIDIVoice('Shakuhachi', 93, 21, 18, 'FLUTE', 'XP-B 275'),
    MIDIVoice('Shakuhachi', 121, 0, 77, 'ETHNIC', 'GM 153'),  #Clumsy
    MIDIVoice('Ethnic Flute', 93, 8, 41, 'FLUTE', 'XP-E 170'),  #Sounds like a Western flute to me
    MIDIVoice('LongDistance', 87, 1, 19, 'ETHNIC', 'USER 148'),  #So-so
  ],
  'Huff N\' Stuff': [
    MIDIVoice('EP mkI', 87, 69, 5, 'EL.PIANO', 'PR-F 006'),  #Nice sound, with a risky stereo ping pong
    MIDIVoice('Celestial EP', 87, 64, 21, 'EL.PIANO', 'PR-A 022'),  #Too muted
    MIDIVoice('1983 EP', 87, 69, 32, 'EL.PIANO', 'PR-F 033'),  #Good, but not enough percussion
    MIDIVoice('E.Piano 1', 121, 0, 4, 'EL.PIANO', 'GM 010'),  #Too quiet
  ],
  'JC Strat.': [
    MIDIVoice('Strat Gtr', 87, 64, 123, 'EL.GUITAR', 'PR-A 124'),  #Okay
    MIDIVoice('JC Strat Bdy', 87, 64, 124, 'EL.GUITAR', 'PR-A 125'),  #Annoying double-attack
  ],
  'JP-8 String': [
    MIDIVoice('JP Strings 1', 87, 67, 105, 'SOFT PAD', 'PR-D 106'),  #Good!
    MIDIVoice('JP8 Str1 SRX', 93, 13, 13, 'STRINGS', 'XP-C 270'),  #A little slow on the attack
    MIDIVoice('JP Strings 2', 87, 67, 106, 'SOFT PAD', 'PR-D 107'),
    MIDIVoice('JP8 Str2 SRX', 93, 13, 14, 'STRINGS', 'XP-C 271'),
    MIDIVoice('JP+OB StrSRX', 93, 13, 15, 'STRINGS', 'XP-C 272'),
  ],
  'Kalimba': [
    MIDIVoice('Kalimbatch', 93, 20, 86, 'MALLET', 'XP-B 215'),  #Great!
    MIDIVoice('Kalimba', 93, 20, 85, 'MALLET', 'XP-B 214'),  #Good!
    MIDIVoice('Kalimba', 121, 0, 108, 'PLUCKED', 'GM 199'),
    MIDIVoice('Kalimbells', 87, 64, 54, 'BELL', 'PR-A 055'),  #A little harsh
  ],
  'Log Drums': [
    MIDIVoice('Big Logs SRX', 93, 21, 95, 'PERCUSSION', 'XP-B 352'),  #Okay, but a little fake...
    MIDIVoice('LogDetunrSRX', 93, 20, 89, 'MALLET', 'XP-B 218'),  #Detune is a little weird
  ],
  'Low Strings': [
    MIDIVoice('SymphStrings', 93, 3, 12, 'STRINGS', 'XP-A 013'),  #Good enough
  ],
  'Magic Bell': [
    MIDIVoice('Victoriana 2', 93, 9, 45, 'BELL', 'XP-E 302'),  #Good enough
    MIDIVoice('Troika Ride', 93, 11, 62, 'BELL', 'XP-C 063'),  #Weird detune, but might work
    MIDIVoice('Candy Bell', 87, 64, 60, 'BELL', 'PR-A 061'),  #Nice, but double-attack
    MIDIVoice('Himalaya Ice', 87, 64, 55, 'BELL', 'PR-A 056'),  #A little slow, but good
    MIDIVoice('HimalayaThaw', 87, 0, 9, 'BELL', 'USER 010'),  #Annoying second attack
  ],
  'Mandolin': [
    MIDIVoice('Mandolin', 93, 19, 74, 'PLUCKED', 'XP-B 075'),  #Works for me!
    MIDIVoice('Mandolin', 121, 2, 25, 'AC.GUITAR', 'GM 060'),  #A little fake
  ],
  'Marimba': [
    MIDIVoice('Marimba', 121, 0, 12, 'MALLET', 'GM 030'),  #Good!
    MIDIVoice('Marimba w', 121, 1, 12, 'MALLET', 'GM 031'),
  ],
  'Mellow Accordion': [
    MIDIVoice('Accordion Fr', 121, 0, 21, 'ACCORDION', 'GM 050'),  #Good enough
  ],
  'Music Box': [
    MIDIVoice('Music Box', 121, 0, 10, 'BELL', 'GM 027'),  #Works for me
    MIDIVoice('FS Musicbox', 87, 64, 52, 'BELL', 'PR-A 053'),  #Better, but still mallety
    MIDIVoice('Music Bells', 87, 64, 51, 'BELL', 'PR-A 052'),  #Too mallety
    MIDIVoice('Music Box 2', 87, 69, 48, 'BELL', 'PR-F 049'),  #Double-hit
    MIDIVoice('MusicBellSRX', 93, 9, 40, 'BELL', 'XP-E 297'),  #Way too much sustain
  ],
  'Muted Guitar': [
    MIDIVoice('Muted Gtr Pk', 87, 64, 111, 'EL.GUITAR', 'PR-A 112'),  #Good enough
    MIDIVoice('MutedDsBlief', 93, 12, 37, 'DIST.GUITAR', 'XP-C 166'),
    MIDIVoice('Comp Muted', 93, 20, 9, 'EL.GUITAR', 'XP-B 138'),
    MIDIVoice('MutedAmbient', 93, 20, 23, 'EL.GUITAR', 'XP-B 152'),
  ],
  'Octa Rhodes': [
    MIDIVoice('Heavens Tine', 93, 11, 33, 'EL.PIANO', 'XP-C 034'),  #Good!
  ],
  'One Octave Rhodes': [
    MIDIVoice('80\'s FM', 93, 11, 31, 'EL.PIANO', 'XP-C 032'),  #Good!
  ],
  'Organ': [
    MIDIVoice('60s Brothers', 93, 11, 106, 'ORGAN', 'XP-C 107'),  #Good enough
    MIDIVoice('Organ 1', 121, 0, 16, 'ORGAN', 'GM 037'),  #Maybe...
    MIDIVoice('R&B Organ 1', 87, 64, 82, 'ORGAN', 'PR-A 083'),  #Good, but lacks touch sensitivity
    MIDIVoice('HarmoOrg/Mod', 93, 5, 117, 'ORGAN', 'XP-D 246'),
    MIDIVoice('GreenB /Pdl', 93, 11, 71, 'ORGAN', 'XP-C 072'),
    MIDIVoice('Bookin\'B SRX', 93, 11, 76, 'ORGAN', 'XP-C 077'),
    MIDIVoice('AllStarB3SRX', 93, 11, 83, 'ORGAN', 'XP-C 084'),
    MIDIVoice('Absolute B3', 93, 11, 86, 'ORGAN', 'XP-C 087'),
    MIDIVoice('BalladB /Mod', 93, 11, 89, 'ORGAN', 'XP-C 090'),
    MIDIVoice('B3 888000004', 93, 11, 105, 'ORGAN', 'XP-C 106'),
    MIDIVoice('FullDraw Org', 87, 1, 89, 'ORGAN', 'USER 218'),  #Maybe, but lacks touch sensitivity
    MIDIVoice('VKHold4Speed', 87, 0, 22, 'ORGAN', 'USER 023'),  #TOO LOUD!
    MIDIVoice('FullDraw Org', 87, 64, 74, 'ORGAN', 'PR-A 075'),  #Not touch-sensitive
  ],
  'Pad': [
    MIDIVoice('Jupiter-X', 87, 1, 126, 'SOFT PAD', 'USER 255'),  #Works for me!
    MIDIVoice('FS Soft Pad', 87, 67, 103, 'SOFT PAD', 'PR-D 104'),
    MIDIVoice('Jupiter-X', 87, 71, 94, 'SOFT PAD', 'PR-H 095'),
  ],
  'Piano': [
    MIDIVoice('Piano 1w', 121, 1, 0, 'AC.PIANO', 'GM 002'),
  ],
  'Pitched African Drums': [
    MIDIVoice('Balafon SRX', 93, 20, 91, 'MALLET', 'XP-B 220'),  #Better than nothing...
  ],
  'Pizz. Strings': [
    MIDIVoice('Pizz Sect', 93, 3, 46, 'STRINGS', 'XP-A 047'),  #Good enough
    MIDIVoice('RoomPizz SRX', 93, 7, 60, 'STRINGS', 'XP-E 061'),  #Good
    MIDIVoice('Full Pizz ff', 93, 3, 48, 'STRINGS', 'XP-A 049'),  #Pretty good
    MIDIVoice('DelicatePizz', 87, 1, 8, 'STRINGS', 'USER 137'),  #Good enough
    MIDIVoice('DelicatePizz', 87, 65, 110, 'STRINGS', 'PR-B 111'),
    MIDIVoice('Vls PizzHall', 87, 65, 111, 'STRINGS', 'PR-B 112'),
    MIDIVoice('Orch Pizz', 87, 65, 112, 'STRINGS', 'PR-B 113'),
    MIDIVoice('Pizz\'Stac VS', 87, 70, 28, 'STRINGS', 'PR-G 029'),
    MIDIVoice('PizzicatoStr', 121, 0, 45, 'STRINGS', 'GM 100'),
    MIDIVoice('Full Pizz mp', 93, 3, 5, 'STRINGS', 'XP-A 006'),
    MIDIVoice('Full Pizz pp', 93, 3, 47, 'STRINGS', 'XP-A 048'),
    MIDIVoice('4Sect. Pz ff', 93, 3, 49, 'STRINGS', 'XP-A 050'),
    MIDIVoice('Vc Pizz /sw', 93, 3, 75, 'STRINGS', 'XP-A 076'),
    MIDIVoice('LA Pizz', 93, 6, 7, 'STRINGS', 'XP-D 264'),
    MIDIVoice('Nite Pizzico', 93, 7, 62, 'STRINGS', 'XP-E 063'),
    MIDIVoice('Stage Pizz', 93, 7, 61, 'STRINGS', 'XP-E 062'),  #No reverb
  ],
  'Plucky Synth': [
    MIDIVoice('Analog Piano', 93, 5, 106, 'AC.PIANO', 'XP-D 235'),  #Good enough
    MIDIVoice('Moogy Pulse', 93, 11, 58, 'KEYBOARDS', 'XP-C 059'),
    MIDIVoice('JP8 Clav SRX', 93, 11, 59, 'KEYBOARDS', 'XP-C 060'),
    MIDIVoice('Pulse Clavi', 87, 64, 43, 'KEYBOARDS', 'PR-A 044'),  #Eh...
    MIDIVoice('P5 Pluck', 93, 4, 79, 'OTHER SYNTH', 'XP-D 080'),  #No.
  ],
  'Pop Keys (w/reverb)': [
    MIDIVoice('Balladeer', 87, 64, 27, 'EL.PIANO', 'PR-A 028'),  #Might be good enough
    MIDIVoice('EP Belle', 87, 69, 34, 'EL.PIANO', 'PR-F 035'),  #A little loud
    MIDIVoice('EP Belle', 87, 0, 46, 'EL.PIANO', 'USER 047'),  #Too loud!
  ],
  'Pod Pad (swirling)': [
    MIDIVoice('Sawed String', 93, 14, 52, 'SOFT PAD', 'XP-C 437'),  #Good enough for me
    MIDIVoice('Sine Pad', 121, 1, 89, 'SOFT PAD', 'GM 174'),
    MIDIVoice('Evolution X', 87, 71, 106, 'SOFT PAD', 'PR-H 107'),  #Nice, but annoying detune
    MIDIVoice('WarmReso Pad', 87, 67, 102, 'SOFT PAD', 'PR-D 103'),  #Too heavy
    MIDIVoice('Evolution X', 87, 1, 60, 'SOFT PAD', 'USER 189'),  #Not liking the detune
  ],
  'Pop Pad': [
    MIDIVoice('Sine Pad', 121, 1, 89, 'SOFT PAD', 'GM 174'),  #Good enough.
    MIDIVoice('Introductory', 93, 5, 75, 'BRIGHT PAD', 'XP-D 204'),
    MIDIVoice('M12 Strings', 93, 13, 16, 'STRINGS', 'XP-C 273'),
    MIDIVoice('JP-8 Phase', 87, 1, 122, 'SOFT PAD', 'USER 251'),
    MIDIVoice('Machine Str', 87, 0, 99, 'STRINGS', 'USER 100'),
    MIDIVoice('Machine Str', 87, 70, 32, 'STRINGS', 'PR-G 033'),
    MIDIVoice('AnalogMaster', 93, 6, 17, 'SYNTH BRASS', 'XP-D 274'),
    MIDIVoice('Analog Bell', 93, 11, 63, 'BELL', 'XP-C 064'),
    MIDIVoice('Sawed String', 93, 14, 52, 'SOFT PAD', 'XP-C 437'),
    MIDIVoice('FS Soft Pad', 87, 67, 103, 'SOFT PAD', 'PR-D 104'),
    MIDIVoice('JP-8 Phase', 87, 71, 100, 'SOFT PAD', 'PR-H 101'),  #Too slow
  ],
  'Pop Synth Pad': [
    MIDIVoice('FS Soft Pad', 87, 67, 103, 'SOFT PAD', 'PR-D 104'),  #Director's Choice
    MIDIVoice('Jupiter-X', 87, 1, 126, 'SOFT PAD', 'USER 255'),
    MIDIVoice('MistOver5ths', 87, 68, 18, 'BRIGHT PAD', 'PR-E 019'),
    MIDIVoice('Fat Stacks', 87, 68, 26, 'BRIGHT PAD', 'PR-E 027'),
    MIDIVoice('Jupiter-X', 87, 71, 94, 'SOFT PAD', 'PR-H 095'),
    MIDIVoice('Introductory', 93, 5, 75, 'BRIGHT PAD', 'XP-D 204'),
    MIDIVoice('JP SquPadSRX', 93, 14, 42, 'SOFT PAD', 'XP-C 427'),
  ],
  'Pop Vox Pad': [
    MIDIVoice('StChrMm/Ah S', 93, 9, 127, 'VOX', 'XP-E 384'),  #Works for me
    MIDIVoice('Angelic Pad', 93, 9, 120, 'VOX', 'XP-E 377'),  #Maybe...
    MIDIVoice('Choir', 93, 9, 119, 'VOX', 'XP-E 376'),
    MIDIVoice('VoxSaws Lead', 93, 13, 49, 'SOFT LEAD', 'XP-C 306'),
    MIDIVoice('Choral Sweep', 87, 71, 112, 'VOX', 'PR-H 113'),
    MIDIVoice('Angels Choir', 87, 67, 88, 'VOX', 'PR-D 089'),  #SLOW!
    MIDIVoice('Choral Sweep', 87, 1, 71, 'VOX', 'USER 200'),  #Blech
  ],
  'Pretty Electric Piano': [
    MIDIVoice('Crystal EP', 87, 0, 95, 'EL.PIANO', 'USER 096'),  #GREAT!
    MIDIVoice('Crystal EP', 87, 64, 20, 'EL.PIANO', 'PR-A 021'),
    MIDIVoice('FM EPad', 87, 64, 36, 'EL.PIANO', 'PR-A 037'),
  ],
  'Pretty Pop Electric Piano': [
    MIDIVoice('Crystal EP', 87, 0, 95, 'EL.PIANO', 'USER 096'),  #GREAT!
    MIDIVoice('Crystal EP', 87, 64, 20, 'EL.PIANO', 'PR-A 021'),
    MIDIVoice('FM EPad', 87, 64, 36, 'EL.PIANO', 'PR-A 037'),
  ],
  'Pretty Pad': [
    MIDIVoice('Flange Dream', 87, 71, 103, 'SOFT PAD', 'PR-H 104'),  #Slow attack, but might work
    MIDIVoice('FS Soft Pad', 87, 67, 103, 'SOFT PAD', 'PR-D 104'),  #Too subtle
    MIDIVoice('JP-8 Phase', 87, 71, 100, 'SOFT PAD', 'PR-H 101'),  #Gets loud!
    MIDIVoice('Miracle Pad', 93, 5, 76, 'BRIGHT PAD', 'XP-D 205'),  #Annoying throb
    MIDIVoice('Flange Dream', 87, 1, 16, 'SOFT PAD', 'USER 145'),  #Annoying throb
    MIDIVoice('Polar Morn', 87, 1, 74, 'BRIGHT PAD', 'USER 203'),  #Harsh
    MIDIVoice('Silk Pad', 87, 67, 101, 'SOFT PAD', 'PR-D 102'),  #Nah...
    MIDIVoice('InfinitePhsr', 87, 0, 110, 'BRIGHT PAD', 'USER 111'),  #HARSH!
  ],
  'Pulse Keys': [
    MIDIVoice('Pulse EPno', 87, 64, 32, 'EL.PIANO', 'PR-A 033'),  #Should work
    MIDIVoice('Pulse Keys', 93, 4, 78, 'OTHER SYNTH', 'XP-D 079'),  #Nice, but too touch sensitive
    MIDIVoice('Moogy Pulse', 93, 11, 58, 'KEYBOARDS', 'XP-C 059'),
  ],
  'Rain SFX': [
    MIDIVoice('Rain', 121, 1, 122, 'SOUND FX', 'GM 222'),
  ],
  'Recorder': [
    MIDIVoice('Tnr Recorder', 93, 8, 46, 'FLUTE', 'XP-E 175'),  #Lousy, but not shit
    MIDIVoice('Sop Recorder', 93, 8, 45, 'FLUTE', 'XP-E 174'),  #No...
    MIDIVoice('Recorder', 121, 0, 74, 'FLUTE', 'GM 150'),  #Really?  That's supposed to be a recorder?
  ],
  'Reedy Ethnic Instr.': [
    MIDIVoice('Shanai', 121, 0, 111, 'ETHNIC', 'GM 202'),  #Maybe...
    MIDIVoice('FS PipeDream', 87, 68, 87, 'ETHNIC', 'PR-E 088'),  #Annoying breath instrument on hard note
  ],
  'Res. Pad': [
    MIDIVoice('Mod Dare', 87, 68, 13, 'BRIGHT PAD', 'PR-E 014'),  #Eh...
  ],
  'Rhodes': [
    MIDIVoice('70\'EP Bs', 93, 11, 23, 'EL.PIANO', 'XP-C 024'),  #Fine
  ],
  'Romance Exp.': [
    MIDIVoice('Crystal EP', 87, 0, 95, 'EL.PIANO', 'USER 096'),  #Better than nothing...
  ],
  'Shimmery Bells': [
    MIDIVoice('Victoriana 2', 93, 9, 45, 'BELL', 'XP-E 302'),  #Good enough for me
    MIDIVoice('Candy Bell', 87, 64, 60, 'BELL', 'PR-A 061'),  #Double-attack, but might work
    MIDIVoice('Music Bells', 87, 64, 51, 'BELL', 'PR-A 052'),  #Not terribly shimmery...
    MIDIVoice('SpectrumBell', 93, 5, 120, 'BELL', 'XP-D 249'),  #Too heavy
  ],
  'Simple Organ': [
    MIDIVoice('X Perc Organ', 87, 69, 54, 'ORGAN', 'PR-F 055'),  #Annoying percussion, but better than harsh
    MIDIVoice('IronFarf SRX', 93, 12, 7, 'ORGAN', 'XP-C 136'),  #Harsh, but the best so far.
    MIDIVoice('LoFi PercOrg', 87, 64, 80, 'ORGAN', 'PR-A 081'),  #Not touch sensitive enough
    MIDIVoice('X Perc Organ', 87, 0, 35, 'ORGAN', 'USER 036'),  #Annoying percussion
    MIDIVoice('60\'s Organ 1', 121, 2, 16, 'ORGAN', 'GM 039'),  #Not touch-sensitive
    MIDIVoice('GreenB /Pdl', 93, 11, 71, 'ORGAN', 'XP-C 072'),  #Not touch-sensitive
    MIDIVoice('Mello', 93, 11, 72, 'ORGAN', 'XP-C 073'),  #Not touch-sensitive
    MIDIVoice('CabnetSeries', 93, 11, 85, 'ORGAN', 'XP-C 086'),  #Not touch-sensitive
    MIDIVoice('Suitcase B3', 93, 11, 88, 'ORGAN', 'XP-C 089'),  #Nice, but not touch-sensitive
    MIDIVoice('B3 888000004', 93, 11, 105, 'ORGAN', 'XP-C 106'),  #Not touch-sensitive
    MIDIVoice('BalladB3 SRX', 93, 11, 117, 'ORGAN', 'XP-C 118'),  #Not touch-sensitive
  ],
  'Simple Rhodes': [
    MIDIVoice('FS Wurly', 87, 0, 65, 'EL.PIANO', 'USER 066'),  #Works for me
    MIDIVoice('FS 70\'EP', 87, 64, 12, 'EL.PIANO', 'PR-A 013'),
    MIDIVoice('FS Wurly', 87, 64, 29, 'EL.PIANO', 'PR-A 030'),
    MIDIVoice('StageCabinet', 87, 69, 28, 'EL.PIANO', 'PR-F 029'),
    MIDIVoice('E.Piano 1', 121, 0, 4, 'EL.PIANO', 'GM 010'),
    MIDIVoice('70\'EP Bs', 93, 11, 23, 'EL.PIANO', 'XP-C 024'),
  ],
  'Spikey Synth': [
    MIDIVoice('Moogy Pulse', 93, 11, 58, 'KEYBOARDS', 'XP-C 059'),  #A little harsh, but might work
    MIDIVoice('SpikedChzSRX', 93, 14, 20, 'OTHER SYNTH', 'XP-C 405'),  #Way too harsh
  ],
  'String Pad': [
    MIDIVoice('FS Strings', 87, 65, 101, 'STRINGS', 'PR-B 102'),  #A little too prominent
    MIDIVoice('LushStrings2', 93, 3, 90, 'STRINGS', 'XP-A 091'),  #Nice, but a little slow on the attack
    MIDIVoice('Warm Strings', 87, 65, 103, 'STRINGS', 'PR-B 104'),  #Too much attack
    MIDIVoice('Fast Cellos', 93, 7, 11, 'STRINGS', 'XP-E 012'),  #Eeek!
  ],
  'Strings': [
    MIDIVoice('FS Strings', 87, 65, 101, 'STRINGS', 'PR-B 102'),  #Nice, but a tad slow
    MIDIVoice('Full Strings', 87, 70, 18, 'STRINGS', 'PR-G 019'),  #Tricky dynamics, but expressive
    MIDIVoice('Jupiter 2004', 87, 71, 81, 'BRIGHT PAD', 'PR-H 082'),  #Works for me
    MIDIVoice('LushStrings2', 93, 3, 90, 'STRINGS', 'XP-A 091'),  #Nice, but slow
    MIDIVoice('Full Strings', 87, 0, 2, 'STRINGS', 'USER 003'),  #Harsh
    MIDIVoice('2-way Sect.', 87, 65, 102, 'STRINGS', 'PR-B 103'),  #Too heavy
  ],
  'Stringy Pad': [
    MIDIVoice('JP Strings 1', 87, 67, 105, 'SOFT PAD', 'PR-D 106'),  #Okay...
    MIDIVoice('FS Syn Str', 87, 67, 107, 'SOFT PAD', 'PR-D 108'),
    MIDIVoice('In The Pass', 87, 68, 15, 'BRIGHT PAD', 'PR-E 016'),
    MIDIVoice('MistOver5ths', 87, 68, 18, 'BRIGHT PAD', 'PR-E 019'),
    MIDIVoice('WarmVlns SRX', 93, 7, 0, 'STRINGS', 'XP-E 001'),
    MIDIVoice('SynStrings', 93, 7, 81, 'STRINGS', 'XP-E 082'),
    MIDIVoice('Sawed String', 93, 14, 52, 'SOFT PAD', 'XP-C 437'),
  ],
  'Sus String Pad': [
    MIDIVoice('FS Strings', 87, 65, 101, 'STRINGS', 'PR-B 102'),  #Fine by me!
    MIDIVoice('2-way Sect.', 87, 65, 102, 'STRINGS', 'PR-B 103'),
    MIDIVoice('Warm Strings', 87, 65, 103, 'STRINGS', 'PR-B 104'),
    MIDIVoice('LushStrings2', 93, 3, 90, 'STRINGS', 'XP-A 091'),
    MIDIVoice('WarmVlns SRX', 93, 7, 0, 'STRINGS', 'XP-E 001'),
    MIDIVoice('Fast Cellos', 93, 7, 11, 'STRINGS', 'XP-E 012'),
    MIDIVoice('SynStrings', 93, 7, 81, 'STRINGS', 'XP-E 082'),
  ],
  'Synth Bells': [
    MIDIVoice('Ballad Bells', 87, 69, 43, 'BELL', 'PR-F 044'),  #Good enough
    MIDIVoice('Candy Bell', 87, 64, 60, 'BELL', 'PR-A 061'),
    MIDIVoice('Himalaya Ice', 87, 64, 55, 'BELL', 'PR-A 056'),
    MIDIVoice('5th Key', 87, 64, 64, 'BELL', 'PR-A 065'),
    MIDIVoice('Bell Monitor', 87, 69, 44, 'BELL', 'PR-F 045'),
    MIDIVoice('SpectrumBell', 93, 5, 120, 'BELL', 'XP-D 249'),
    MIDIVoice('MusicBellSRX', 93, 9, 40, 'BELL', 'XP-E 297'),
    MIDIVoice('Victoriana 1', 93, 9, 43, 'BELL', 'XP-E 300'),
    MIDIVoice('Troika Ride', 93, 11, 62, 'BELL', 'XP-C 063'),
    MIDIVoice('Analog Bell', 93, 11, 63, 'BELL', 'XP-C 064'),
    MIDIVoice('Wind Bells', 93, 20, 81, 'BELL', 'XP-B 210'),
    MIDIVoice('FS Musicbox', 87, 64, 52, 'BELL', 'PR-A 053'),  #Not very synthetic
  ],
  'Synth Keys': [
    MIDIVoice('Analog Piano', 93, 5, 106, 'AC.PIANO', 'XP-D 235'),  #Okay...
  ],
  'Synth Keys (neutral sound)': [
    MIDIVoice('Analog Piano', 93, 5, 106, 'AC.PIANO', 'XP-D 235'),  #Okay...
  ],
  'Synth Pad': [
    MIDIVoice('FS Soft Pad', 87, 67, 103, 'SOFT PAD', 'PR-D 104'),  #Director-Approved, but too bloody quiet!
    MIDIVoice('Introductory', 93, 5, 75, 'BRIGHT PAD', 'XP-D 204'),
  ],
  'Synth Strings': [
    MIDIVoice('JP Strings 1', 87, 67, 105, 'SOFT PAD', 'PR-D 106'),  #Good!
    MIDIVoice('SynStrings', 93, 7, 81, 'STRINGS', 'XP-E 082'),  #Maybe
    MIDIVoice('LushStrings2', 93, 3, 90, 'STRINGS', 'XP-A 091'),  #Nice, but slow
    MIDIVoice('M12 Strings', 93, 13, 16, 'STRINGS', 'XP-C 273'),  #LOUD!!!!!
    MIDIVoice('Stereo Tron!', 93, 3, 114, 'STRINGS', 'XP-A 115'),  #Too old
  ],
  'Thunder SFX': [
    MIDIVoice('Thunder', 121, 2, 122, 'SOUND FX', 'GM 223'),
  ],
  'Tremolo Strings': [
    MIDIVoice('Full Tremolo', 93, 3, 30, 'STRINGS', 'XP-A 031'),  #Good enough
    MIDIVoice('F.StrTrm/Mrc', 93, 3, 33, 'STRINGS', 'XP-A 034'),
    MIDIVoice('F.Str Trm/sw', 93, 3, 34, 'STRINGS', 'XP-A 035'),
    MIDIVoice('Tremolo /', 93, 7, 94, 'ORCHESTRA', 'XP-E 095'),
    MIDIVoice('TremOrc /Mod', 93, 7, 95, 'ORCHESTRA', 'XP-E 096'),
    MIDIVoice('Tremolo Str', 121, 0, 44, 'STRINGS', 'GM 099'),  #Too legato
  ],
  'Vibes': [
    MIDIVoice('FS Vibe', 87, 64, 66, 'MALLET', 'PR-A 067'),  #Great!
  ],
  'Vibes (motor on)': [
    MIDIVoice('Vibraphone!', 93, 11, 66, 'MALLET', 'XP-C 067'),  #Good enough...
    MIDIVoice('Vibraphone', 121, 0, 11, 'MALLET', 'GM 028'),  #Lacks motor
    MIDIVoice('Vibrations', 87, 64, 65, 'MALLET', 'PR-A 066'),  #Lacks motor
  ],
  'Vocal Pad': [
    MIDIVoice('ChoirOoh/Aft', 87, 67, 87, 'VOX', 'PR-D 088'),  #Works for me.
    MIDIVoice('Choir Aahs 2', 87, 67, 86, 'VOX', 'PR-D 087'),  #Maybe...
    MIDIVoice('Angels Choir', 87, 67, 88, 'VOX', 'PR-D 089'),
    MIDIVoice('Morning Star', 87, 67, 93, 'VOX', 'PR-D 094'),
    MIDIVoice('Lost Voices', 87, 71, 115, 'VOX', 'PR-H 116'),
    MIDIVoice('Humming', 121, 1, 53, 'VOX', 'GM 114'),
    MIDIVoice('X.. Vox SRX', 93, 9, 125, 'VOX', 'XP-E 382'),
    MIDIVoice('StChrMm/Ah S', 93, 9, 127, 'VOX', 'XP-E 384'),
    MIDIVoice('Mmms & Aaahs', 93, 10, 0, 'VOX', 'XP-E 385'),
    MIDIVoice('Angelic Pad', 93, 9, 120, 'VOX', 'XP-E 377'),  #Too human
  ],
  'Vox (AH)': [
    MIDIVoice('Aah Vox', 87, 67, 92, 'VOX', 'PR-D 093'),  #Good enough for now.
    MIDIVoice('Lost Voices', 87, 71, 115, 'VOX', 'PR-H 116'),
    MIDIVoice('Choir Aahs', 121, 0, 52, 'VOX', 'GM 111'),
    MIDIVoice('Chorus Aahs', 121, 1, 52, 'VOX', 'GM 112'),
    MIDIVoice('Sing! /Mod', 93, 9, 122, 'VOX', 'XP-E 379'),
    MIDIVoice('X.. Vox SRX', 93, 9, 125, 'VOX', 'XP-E 382'),
    MIDIVoice('Choir Aahs 1', 87, 67, 85, 'VOX', 'PR-D 086'),  #Not human enough
    MIDIVoice('Choir Aahs 2', 87, 67, 86, 'VOX', 'PR-D 087'),  #Not human enough
  ],
  'Vox and Beast SFX': [
    MIDIVoice('Paradise', 87, 71, 113, 'VOX', 'PR-H 114'),  #Might work
    MIDIVoice('Syn Opera', 87, 67, 94, 'VOX', 'PR-D 095'),
    MIDIVoice('Syn Opera', 87, 1, 119, 'VOX', 'USER 248'),  #WTF
  ],
  'Warm Pad': [
    MIDIVoice('Warm Pad', 121, 0, 89, 'SOFT PAD', 'GM 173'),  #Good.
    MIDIVoice('WarmReso Pad', 87, 67, 102, 'SOFT PAD', 'PR-D 103'),  #BLOOOEOOOOEHEHHEA
    MIDIVoice('Old,Warm OBX', 93, 14, 23, 'OTHER SYNTH', 'XP-C 408'),  #AAAA!
  ],
  'Warm Strings': [
    MIDIVoice('WarmVlns SRX', 93, 7, 0, 'STRINGS', 'XP-E 001'),  #Works for me
    MIDIVoice('Warm Strings', 87, 65, 103, 'STRINGS', 'PR-B 104'),  #Maybe
    MIDIVoice('Warm Vc Sect', 93, 3, 74, 'STRINGS', 'XP-A 075'),  #Not very warm
    MIDIVoice('Warm Section', 93, 3, 18, 'STRINGS', 'XP-A 019'),  #Not very warm...
    MIDIVoice('Warm Vln Sec', 93, 3, 55, 'STRINGS', 'XP-A 056'),  #Not very warm...
  ],
  'Wasteland Pad': [
    MIDIVoice('Nu Epic Pad', 87, 71, 101, 'SOFT PAD', 'PR-H 102'),  #Closest to the recording
    # MIDIVoice('JP Strings 1', 87, 67, 105, 'SOFT PAD', 'PR-D 106'),
    # MIDIVoice('Evolution X', 87, 1, 60, 'SOFT PAD', 'USER 189'),
    # MIDIVoice('Evolution X', 87, 71, 106, 'SOFT PAD', 'PR-H 107'),
    # MIDIVoice('Riven Pad', 87, 0, 103, 'SOFT PAD', 'USER 104'),
    # MIDIVoice('Riven Pad', 87, 71, 95, 'SOFT PAD', 'PR-H 096'),
    # MIDIVoice('Consolament', 87, 71, 96, 'SOFT PAD', 'PR-H 097'),
    # MIDIVoice('Antique Str', 93, 3, 112, 'SOFT PAD', 'XP-A 113'),
    # MIDIVoice('Retro Pad', 93, 5, 79, 'SOFT PAD', 'XP-D 208'),
  ],
  'Wave Bells': [
    MIDIVoice('SpectrumBell', 93, 5, 120, 'BELL', 'XP-D 249'),  #Good enough for now
    MIDIVoice('Troika Ride', 93, 11, 62, 'BELL', 'XP-C 063'),
    MIDIVoice('Analog Bell', 93, 11, 63, 'BELL', 'XP-C 064'),
    MIDIVoice('HybridKemong', 93, 20, 73, 'BELL', 'XP-B 202'),
    MIDIVoice('Bell Orchest', 93, 20, 77, 'BELL', 'XP-B 206'),
    MIDIVoice('Wind Bells', 93, 20, 81, 'BELL', 'XP-B 210'),
    MIDIVoice('Himalaya Ice', 87, 64, 55, 'BELL', 'PR-A 056'),  #Annoying
    MIDIVoice('5th Key', 87, 64, 64, 'BELL', 'PR-A 065'),  #Nah
    MIDIVoice('Bell Monitor', 87, 69, 44, 'BELL', 'PR-F 045'),  #Not touch sensitive
    MIDIVoice('Syn Mallet', 121, 1, 98, 'BELL', 'GM 185'),  #Too synthy
  ],
  'West Coast': [
  ],
  'Wind SFX': [
    MIDIVoice('WIND', 121, 3, 122, 'SOUND FX', 'GM 224'),
  ],
  'Woody Electric Piano': [
    MIDIVoice('Wood EPiano', 93, 20, 84, 'MALLET', 'XP-B 213'),  #Hard to tell out of context
    MIDIVoice('LA Piano', 87, 64, 11, 'AC.PIANO', 'PR-A 012'),  #Maybe
  ],
}

##
#  Class for representing a musical part.
class Part():

  ##
  #  Class initializer.
  #  @param name Name of the part
  #  @param channel MIDI channel that is used for the part
  #  @param instBySong List of lists of instruments grouped by song number in the order that they
  #    are played.
  #  @return None.
  def __init__(self, name, channel, instBySong):
    self.name = name
    self.channel = channel
    self.instAll = list(set(itertools.chain(*list(song for song in instBySong))))
    self.instAll.sort()
    self.instBySong = instBySong
    self._validate()

  ##
  #  Validates the song list by verifying each instrument has a matching entry in the patch list.
  def _validate(self):
    #Check that all instruments have matching entries in PATCHES.
    for inst in self.instAll:
      if inst not in PATCHES:
        print('ERROR: Validation for "{0}" part found that instrument "{1}" has no match in PATCHES.'.format(
          self.name,
          inst,
        ))

  ##
  #  Returns the channel number for this part.
  def getChannel(self):
    return self.channel

  ##
  #  Returns a list of the instrument names corresponding ot the given song number.
  #  @return List of strings.
  def getInstruments(self, songNum=None):
    if songNum is None:
      return self.instAll
    try:
      return self.instBySong[songNum]
    except IndexError:
      traceback.print_exc()
      return self.instAll

  ##
  #  Returns the number of songs defined for this part.
  #  @return Integer.
  def getNumSongs(self):
    return len(self.instBySong)

  ##
  #  Selects the given instrument on the synthesizer.
  #  @param instrument Instrument name string
  #  @return None.
  def selectInstrument(self, midiDevice, instrument):
    try:
      voice = PATCHES[instrument][0]
    except IndexError:
      print('No programs available for "{0}".  Selecting piano.'.format(instrument))
      voice = PATCHES['Piano'][0]
    midiDevice.programChange(voice, self.channel)

## Details on the different musical parts and their instrumentations.
PARTS = {
  'Keyboard 1': Part(
    'Keyboard 1',
    2,  #Channel 2
    [
      ['Piano', 'Synth Bells', 'Harp', 'Fantasia JV', 'Pod Pad (swirling)', ],                      #Song 1
      ['Piano', ],                                                                                  #Song 2
      ['Piano', ],                                                                                  #Song 3
      ['Piano', 'Strings', 'Bass Marimba', 'Simple Rhodes', ],                                      #Song 4
      ['Harp', ],                                                                                   #Song 5
      ['Piano', ],                                                                                  #Song 6
      ['Piano', 'Harp', ],                                                                          #Song 7
      ['Electric Piano', 'Piano', ],                                                                #Song 8
      ['Vibes', 'Piano', ],                                                                         #Song 9
      ['Piano', ],                                                                                  #Song 10
      ['Piano', ],                                                                                  #Song 11
      ['Synth Pad', 'Piano', ],                                                                     #Song 12
      ['Piano', ],                                                                                  #Song 13
      ['Huff N\' Stuff', 'Chorused Piano', ],                                                       #Song 14
      ['Harp', ],                                                                                   #Song 15
      ['Piano', ],                                                                                  #Song 16
      ['Piano', ],                                                                                  #Song 17
      ['Piano', 'Pop Synth Pad', ],                                                                 #Song 18
      ['Piano', ],                                                                                  #Song 19
      ['Piano', 'Synth Pad', ],                                                                     #Song 20
      ['Piano', ],                                                                                  #Song 21
      ['Piano', ],                                                                                  #Song 22
      ['Piano', 'Huff N\' Stuff', ],                                                                #Song 23
      ['Harp', ],                                                                                   #Song 24
      ['Electric Piano', 'Piano', ],                                                                #Song 25
      ['West Coast', ],                                                                             #Song 26
      ['Piano', 'Organ', ],                                                                         #Song 27
      ['Piano', 'Beauty Vox', ],                                                                    #Song 28
      ['Piano', ],                                                                                  #Song 29
      ['Magic Bell', 'Bassoon', 'Piano', 'Stringy Pad', 'Synth Bells', ],                           #Song 30
      ['Piano', ],                                                                                  #Song 31
      ['D-50 Stack', 'Dig. Rhodes', 'Piano', 'Fantasy Vox', ],                                      #Song 32
      ['Piano', 'West Coast', 'D-50 Stack', ],                                                      #Song 33
      ['Piano', ],                                                                                  #Song 34
      ['Electric Piano', ],                                                                         #Song 35
      ['Piano', 'Synth Keys (neutral sound)', ],                                                    #Song 36
      ['Electric Piano', ],                                                                         #Song 37
      ['Romance Exp.', 'Piano', ],                                                                  #Song 38
      ['Piano', 'Electric Piano', ],                                                                #Song 39
      ['Piano', ],                                                                                  #Song 40
      ['Piano', ],                                                                                  #Song 41
      ['Piano', 'Pop Vox Pad', 'Synth Pad', ],                                                      #Song 42
      ['Harp', 'Synth Bells', 'Piano', ],                                                           #Song 43
      ['Piano', 'Electric Piano', ],                                                                #Song 44
    ],
  ),
  'Keyboard 2': Part(
    'Keyboard 2',
    3,  #Channel 3
    [
      ['Sus String Pad', 'Synth Bells', 'Marimba', ],                                               #Song 1
      [                                                                                             #Song 2
        'Electric Piano', 'String Pad', 'Pop Keys (w/reverb)', 'Synth Bells', 'Brite Synth Bells',
        'Pretty Pad',
      ],
      ['Marimba', 'Pretty Electric Piano', ],                                                       #Song 3
      ['Pop Pad', 'Harp', 'Bass Marimba', ],                                                        #Song 4
      ['Harmonium', 'Pop Pad', 'Harp/Bells', ],                                                     #Song 5
      ['Pad', 'Strings', 'Vox (AH)', 'Warm Pad', ],                                                 #Song 6
      [                                                                                             #Song 7
        'Flutey Organ', 'Bell Synth', 'Pop Pad', 'Chapel Organ', 'Electric Piano', 'Strings',
        'Evoc. Bell Synth', 'Pop Pad', 'Pretty Pop Electric Piano', 'Synth Bells',
      ],
      ['Pretty Pad', 'Music Box', 'Wave Bells', 'Ethereal', ],                                      #Song 8
      ['Harp', 'Strings', 'One Octave Rhodes', 'Pizz. Strings', ],                                  #Song 9
      ['Electric Piano', ],                                                                         #Song 10
      ['Harp', 'Bell Synth', 'Strings', 'Bell Synth', ],                                            #Song 11
      ['Synth Bells', 'Pad', 'Electric Piano', 'String Pad', 'Low Strings', ],                      #Song 12
      ['Marimba', 'Electric Piano', 'Low Strings', ],                                               #Song 13
      ['Ethnic Pluck', 'Electric Piano', 'Vocal Pad', ],                                            #Song 14
      ['Harmonium', 'Pop Pad', ],                                                                   #Song 15
      ['Electric Piano', ],                                                                         #Song 16
      [                                                                                             #Song 17
        'Chapel Organ', 'Synth Pad', 'Big Organ', 'Dulcimer', 'Fantasia JV', 'Dulcimer',
        'Pop Pad',
      ],
      ['Synth Pad', 'Analog Synth Pad', 'Electric Piano', ],                                        #Song 18
      ['Electric Piano', 'Evol. Synth', 'Warm Strings', 'Synth Pad', ],                             #Song 19
      ['Electric Piano', 'Simple Rhodes', 'Pop Pad', 'Kalimba', 'Synth Pad', ],                     #Song 20
      ['Synth Pad', 'Ethnic Harp', 'Electric Piano', 'Chapel Organ', 'Strings', 'Dulcimer', ],      #Song 21
      ['Gentle Pad', ],                                                                             #Song 22
      ['Dulcimer', 'Ethnic Pluck', 'Low Strings', 'Organ', 'Big Organ', 'Wasteland Pad', ],         #Song 23
      ['Synth Bells', 'Electric Piano', ],                                                          #Song 24
      ['Harp', 'Strings', ],                                                                        #Song 25
      ['Cimbalom', 'Gamelan', 'Dulcimer', ],                                                        #Song 26
      ['Harp', 'Strings', ],                                                                        #Song 27
      ['Pop Pad', 'D-50 Stack', 'Wave Bells', ],                                                    #Song 28
      ['Electric Piano', ],                                                                         #Song 29
      ['Hazy Pad', 'Reedy Ethnic Instr.', 'Marimba', 'Hi Ethnic Flute', 'Electric Piano', ],        #Song 30
      ['Flutey Organ', 'Harp', ],                                                                   #Song 31
      ['Fantasia JV', 'Beauty Vox', 'Bass Kalimba', ],                                              #Song 32
      ['Electric Piano', 'Warm Strings', ],                                                         #Song 33
      ['Low Strings', 'Electric Piano', 'Bell Synth', ],                                            #Song 34
      ['Bell Synth', 'Dulcimer', 'Simple Organ', ],                                                 #Song 35
      ['Electric Piano', 'Synth Keys', 'Bell Synth', ],                                             #Song 36
      ['Bell Pad', 'Harp', 'Beauty Vox', ],                                                         #Song 37
      ['Angels Sing', ],                                                                            #Song 38
      ['Dulcimer', 'Strings', ],                                                                    #Song 39
      ['Harp', 'Strings', 'Synth Keys', 'Beauty Vox', ],                                            #Song 40
      ['Organ', ],                                                                                  #Song 41
      ['Harp', 'Electric Piano', ],                                                                 #Song 42
      ['Strings', 'Harp', 'Electric Piano', ],                                                      #Song 43
      ['Strings', ],                                                                                #Song 44
    ],
  ),
  'Keyboard 3': Part(
    'Keyboard 3',
    1,  #Channel 1
    [
      ['Rhodes', 'Organ', 'Harp', 'Pop Pad', 'Breathy String Pad', 'Strings'],                      #Song 1
      ['Rhodes'],                                                                                   #Song 2
      [],                                                                                           #Song 3
      ['Marimba', 'Bass Marimba'],                                                                  #Song 4
      ['Music Box', 'Electric Piano'],                                                              #Song 5
      [],                                                                                           #Song 6
      ['Rhodes', 'Electric Piano', 'Spikey Synth', 'Harp/Bells', 'Tremolo Strings'],                #Song 7
      ['Harp', 'Analog Seq.', 'Pop Pad'],                                                           #Song 8
      ['Recorder', 'Mellow Accordion', 'Accordion'],                                                #Song 9
      [],                                                                                           #Song 10
      ['Electric Piano', 'Evoc. Bell Synth', 'Pitched African Drums', 'Pop Synth Pad'],             #Song 11
      ['Electric Piano', 'Harp', 'Synth Pad', 'Woody Electric Piano', 'Res. Pad'],                  #Song 12
      ['Simple Organ', 'Church Organ'],                                                             #Song 13
      ['Dig. Rhodes', 'Electric Piano'],                                                            #Song 14
      ['Music Box'],                                                                                #Song 15
      ['Low Strings', 'Synth Bells'],                                                               #Song 16
      ['Pretty Pad', 'Dig. Rhodes', 'Dulcimer', 'Pulse Keys', 'Fantasia JV'],                       #Song 17
      ['Muted Guitar', 'Fantasia JV'],                                                              #Song 18
      ['Electric Piano', 'Shimmery Bells', 'Plucky Synth', 'Synth Bells'],                          #Song 19
      ['Electric Piano', 'Marimba', 'Vox and Beast SFX'],                                           #Song 20
      ['Vox and Beast SFX', 'Electric Piano', 'Strings', 'Synth Bells'],                            #Song 21
      ['Harp'],                                                                                     #Song 22
      ['Big Strings', 'Log Drums', 'Ethnic Pluck', 'Mandolin', 'Big Organ'],                        #Song 23
      ['Synth Bells'],                                                                              #Song 24
      ['Electric Piano', 'Strings'],                                                                #Song 25
      ['Balafoni'],                                                                                 #Song 26
      ['Pop Pad', 'Harp'],                                                                          #Song 27
      ['Piano', 'Harpsichord', 'JP-8 String', 'Bass in Face'],                                      #Song 28
      [],                                                                                           #Song 29
      ['Recorder', 'Bass Marimba', 'Electric Piano', 'English Horn', 'Bassoon', 'Brite Synth'],     #Song 30
      ['Recorder', 'Electric Piano'],                                                               #Song 31
      ['JC Strat.', 'Vibes', 'Pop Pad', 'Fantasy Vox'],                                             #Song 32
      ['Strings', 'Pop Pad', 'D-50 Stack'],                                                         #Song 33
      ['Spikey Synth', 'Big Organ', 'Ethnic Pluck', 'Strings'],                                     #Song 34
      [],                                                                                           #Song 35
      ['Pop Pad', 'Harp', 'Celesta', 'Fast Strings'],                                               #Song 36
      [],                                                                                           #Song 37
      ['Pop Pad', 'Fantasia JV'],                                                                   #Song 38
      [],                                                                                           #Song 39
      ['Synth Bells', 'Dulcimer', 'Electric Piano'],                                                #Song 40
      [],                                                                                           #Song 41
      ['Electric Piano'],                                                                           #Song 42
      ['Electric Piano', 'Harp', 'Synth Bells', 'Rhodes'],                                          #Song 43
      ['Electric Piano', 'Analog Seq.', 'Pop Pad'],                                                 #Song 44
    ],
  ),
  'Sound FX': Part(
    'Sound FX',
    4,  #Channel 5
    [
      ['Thunder SFX', 'Rain SFX', 'Wind SFX', 'Explosion SFX', 'Applause SFX',],
    ],
  ),
  'Master List': Part(
    'Master List',
    5,  #Channel 6
    [
      [
        'Accordion', 'Analog Seq.', 'Analog Synth', 'Analog Synth Pad', 'Angels Sing', 'Balafoni', 'Bass in Face', 'Bass Kalimba', 'Bass Marimba', 'Bassoon', 'Beauty Vox', 'Bell Pad', 'Big Organ', 'Big Strings', 'Breathy String Pad', 'Brite Synth Bells', 'Brite Synth', 'Celesta', 'Chapel Organ', 'Chorused Piano', 'Church Organ', 'Cimbalom', 'D-50 Stack', 'Dig. Rhodes', 'Dulcimer', 'Electric Piano', 'English Horn', 'Ethereal', 'Ethnic Bassoon', 'Ethnic Harp', 'Ethnic Pluck', 'Evoc. Bell Synth', 'Evol. Synth', 'Fantasia JV', 'Fantasy Vox', 'Fast Strings', 'Flutey Organ', 'Gamelan', 'Gentle Pad', 'Harmonium', 'Harp', 'Harp/Bells', 'Harpsichord', 'Hazy Pad', 'Hi Ethnic Flute', 'Huff N\' Stuff', 'JC Strat.', 'JP-8 String', 'Kalimba', 'Log Drums', 'Low Strings', 'Magic Bell', 'Mandolin', 'Marimba', 'Mellow Accordion', 'Music Box', 'Muted Guitar', 'Octa Rhodes', 'One Octave Rhodes', 'Organ', 'Pad', 'Piano', 'Pitched African Drums', 'Pizz. Strings', 'Plucky Synth', 'Pod Pad (swirling)', 'Pop Keys (w/reverb)', 'Pop Pad', 'Pop Synth Pad', 'Pop Vox Pad', 'Pretty Electric Piano', 'Pretty Pad', 'Pulse Keys', 'Recorder', 'Reedy Ethnic Instr.', 'Res. Pad', 'Rhodes', 'Romance Exp.', 'Shimmery Bells', 'Simple Organ', 'Simple Rhodes', 'Spikey Synth', 'String Pad', 'Strings', 'Stringy Pad', 'Sus String Pad', 'Synth Bells', 'Synth Keys (neutral sound)', 'Synth Keys', 'Synth Pad', 'Synth Strings', 'Tremolo Strings', 'Vibes (motor on)', 'Vibes', 'Vocal Pad', 'Vox (AH)', 'Vox and Beast SFX', 'Warm Pad', 'Warm Strings', 'Wasteland Pad', 'Wave Bells', 'West Coast', 'Woody Electric Piano',
      ],
    ],
  ),
}

