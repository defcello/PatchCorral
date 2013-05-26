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

from synthesizers.roland_fantom import RolandFantomXR
from synthesizers.nord import NordStage2
from synthesizers import MIDIDevice
from webpages import COEVoices
import itertools
import re
import rtmidi



class MIDIDeviceLocationError(Exception):
  pass
class NotEnoughArgs(Exception):
  pass

## MIDIOutDevices (Just the Roland for now...)
midiOutDeviceIDs = MIDIDevice.getMIDIOutDevices()
print '\nFound MIDI Out Devices: "{0}"'.format(midiOutDeviceIDs)
MIDI_OUT_ROLAND = None
for port, name in midiOutDeviceIDs:
  if re.match(r'.*FANTOM-X.*', name):
    #Roland Fantom-XR Found!
    MIDI_OUT_ROLAND = NordStage2.MIDIOutDevice(port, 15)
    break
if MIDI_OUT_ROLAND is None:
  raise MIDIDeviceLocationError('Unable to find Roland USB Device.  ;_;')

## MIDIInDevice(s)
#Figure out the MIDI Input devices.
midiInDeviceIDs = MIDIDevice.getMIDIInDevices()
print '\nFound MIDI In Devices: "{0}"'.format(midiOutDeviceIDs)
#Find the Nord
MIDI_IN_NORD_USB = None
MIDI_IN_GEN_USB = None
for port, name in midiInDeviceIDs:
  if MIDI_IN_NORD_USB is None and re.match(r'.*Nord Stage 2 MIDI.*', name):
    #Keyboard 1 found!
    MIDI_IN_NORD_USB = NordStage2.MIDIInDevice(port)
  # elif MIDI_IN_GEN_USB is None and re.match(r'.*USB2\.0-MIDI.*', name):
  elif MIDI_IN_GEN_USB is None and re.match(r'.*CASIO USB-MIDI.*', name):
    #Keyboard 2 found!
    MIDI_IN_GEN_USB = MIDIDevice.MIDIInDevice(port)
  #Keyboard 3 is directly connected to the Roland Fantom-XR.
#If we found the Nord, map its input to the "Keyboard 1" channel.
if MIDI_IN_NORD_USB is None:
  print '\n\n\nERROR: Unable to find Nord USB device (for "Keyboard 1").  ;_;'
else:
  print '\nFound Nord MIDI Device (for "Keyboard 1")!  d(^o^)b'
  #Have this input device forward its messages to the Roland Fantom-XR.
  MIDI_IN_NORD_USB.setMIDIOutDevice(MIDI_OUT_ROLAND, COEVoices.PARTS['Keyboard 1'].getChannel())
#If we found the generic USB->MIDI device,
if MIDI_IN_GEN_USB is None:
  print '\n\n\nERROR: Unable to find USB->MIDI device (for "Keyboard 2").  ;_;'
else:
  print '\nFound Generic USB->MIDI Device (for "Keyboard 2")!  d(^o^)b'
  #Have this input device forward its messages to the Roland Fantom-XR.
  MIDI_IN_GEN_USB.setMIDIOutDevice(MIDI_OUT_ROLAND, COEVoices.PARTS['Keyboard 2'].getChannel())

## Number of instrument selection buttons to show in a single row on HTML pages.
INSTRUMENTS_PER_LINE = 3

## Global for storing current settings until we figure out how to properly use "POST"...
CURRENT_SETTINGS = {}
for instrument in itertools.chain(COEVoices.PARTS.keys()):  #, ['Configuration']):
  CURRENT_SETTINGS[instrument] = {}

##
#  Returns a page suitable for the given inputs.
#  @param postVals Dictionary of lists
#  @param getVals Dictionary of lists
#  @return HTML document.
def getPage(path, postVals, getVals):
  try:
    return getInstrumentPage(postVals, getVals)
  except NotEnoughArgs:
    return getHomePage()

##
#  Returns the home page.
#  @return HTML document.
def getHomePage():
  #Start with the header.
  page = """
  <!doctype html>
  <html>
    <head>
      <link rel="stylesheet" href="style.css" />
      <meta http-equiv="content-type" content="text/html;charset=UTF-8" />
      <meta name="HandheldFriendly" content="True">
      <meta name="MobileOptimized" content="320">
      <meta name="viewport" content="width=device-width">
      <title>Children of Eden - Part Select</title>
    </head>
    <body>
      <p>Which part are you playing?</p>
      <form target="" method="GET">
  """

  #Add the available instruments.
  instruments = list(COEVoices.PARTS.keys())
  instruments.sort()
  for instrument in instruments:
    page += '<input type="submit" name="instrument" value="{0}" />'.format(instrument)

  #Finish the page and return.
  page += """
      </form>
    </body>
  </html>
  """
  return page

##
#  Returns the program selection page for the given instrument.
#  @param postVals Dictionary of lists
#  @param getVals Dictionary of lists
#  @return HTML document.
def getInstrumentPage(postVals, getVals):
  global INSTRUMENTS_PER_LINE
  #Get the selected instrument.
  instrument = getVals.get('instrument', [])
  if len(instrument) == 0:
    raise NotEnoughArgs('onPost: Not enough arguments (instrument="{0}"")'.format(instrument))
  instrument = instrument[0]

  #Get the song number.
  if postVals is None or 'songNum' not in postVals:
    try:
      songNum = CURRENT_SETTINGS[instrument]['songNum']
    except KeyError:
      songNum = 0
  else:
    songNum = int(postVals.get('songNum')[0])
  CURRENT_SETTINGS[instrument]['songNum'] = songNum

  #Build the header.
  page = """
    <!doctype html>
    <html>
      <head>
        <link rel="stylesheet" href="style.css" />
        <meta http-equiv="content-type" content="text/html;charset=UTF-8" />
        <meta name="HandheldFriendly" content="True">
        <meta name="MobileOptimized" content="320">
        <meta name="viewport" content="width=device-width">
        <title>Children of Eden - {0} Controls</title>
      </head>
      <body>
        <h1>{0}</h1>
        <h3>Song {1}</h3>
        <p>
  """.format(instrument, songNum + 1)

  #Insert the command buttons.
  if instrument == 'Configuration':
    page += getAdminForm()
  else:
    page += getInstrumentForm(instrument, songNum)

  #Close up the tags and return.
  page += """
      </body>
    </html>
  """
  return page

##
#  Issues MIDI_OUT_ROLAND messages based on the values POST'ed.
#  @param postVals Dictionary of lists
#  @param getVals Dictionary of lists
#  @return None.
def onPost(postVals, getVals):
  instrument = getVals.get('instrument', [])
  program = postVals.get('program', [])
  keyboards = ['Keyboard {}'.format(keysNum) for keysNum in range(1,4)]

  if len(instrument) == 0 or len(program) == 0:
    # print 'ERROR: onPost: Not enough arguments (instrument="{0}"; program="{1}")'.format(instrument, program)
    return
  instrument = instrument[0]
  program = program[0]
  COEVoices.PARTS[instrument].selectInstrument(MIDI_OUT_ROLAND, program)
  if instrument == 'Sound FX':
    #As an added bonus, play the sound!
    # print 'Sending Note'
    if program == 'Thunder SFX':
      MIDI_OUT_ROLAND.playNote(15, 'C0', 127, COEVoices.PARTS[instrument].getChannel())
    elif program == 'Rain SFX':
      MIDI_OUT_ROLAND.playNote(5, 'C2', 127, COEVoices.PARTS[instrument].getChannel())
    elif program == 'Applause SFX':
      MIDI_OUT_ROLAND.playNote(5, 'C3', 100, COEVoices.PARTS[instrument].getChannel())
    else:
      MIDI_OUT_ROLAND.playNote(5, 'C3', 127, COEVoices.PARTS[instrument].getChannel())
    # print 'Done Sending Note'

##
#  Returns the code for the instrument selection buttons.
#  @param instrument String
#  @param songNum Int
#  @return HTML code.
def getInstrumentForm(instrument, songNum):
  page = ''
  page += """
        <form target="" method="POST">
  """

  #Populate the song selection.
  page += """
        <p>
  """
  if songNum > 0:
    page += """
          <button type="submit" formmethod="post" name="songNum" value="{0}">&lt;--</button>
    """.format(songNum - 1)
  if songNum < (COEVoices.PARTS[instrument].getNumSongs() - 1):
    page += """
          <button type="submit" formmethod="post" name="songNum" value="{0}">--&gt;</button>
    """.format(songNum + 1)
  page += """
        </p>
  """

  #Populate the buttons.
  for idx, prog in enumerate(COEVoices.PARTS[instrument].getInstruments(songNum)):
    if idx % INSTRUMENTS_PER_LINE == 0:
      page += """
          <p>
      """
    page += """
            <input type="submit" name="program" value="{0}" />
    """.format(prog)
    if (idx % INSTRUMENTS_PER_LINE) == (INSTRUMENTS_PER_LINE - 1):
      page += """
          </p>
      """
  page += """
        </form>
  """
  return page

##
#  Returns the HTML code for the administrator controls.
#  @return HTML code.
def getAdminForm():
  #We need to list a selection of available input devices mapped to the Keyboard parts.
  page = """
        <form target="" method="POST">
  """
  midiInDevices = MIDIDevice.getAvailableMIDIInDevices()
  for keysNum in range(1,4):
    keyboard = 'Keyboard {}'.format(keysNum)
    page += """
          <h1>{keyboard}</h1>
          <p>
    """.format(keyboard=keyboard)
    for device in midiInDevices:
      page += """
            <input type="submit" name="{keyboard}/device" value="{device}">
      """.format(keyboard=keyboard, device=device)
    page += """
          </p>
        </form>
    """
  return page


