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
#  Initializes the GUI for SynthNav.

from PySide import QtGui, QtCore
from patchcorral.src.engine import mididevice
from patchcorral.src.engine import midirecplay
import traceback



class RecPlayWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    super().__init__(parent)
    self.synthNav = synthNav
    self.setWindowTitle('PatchCorral - MIDI Recording and Playback')
    self.midirecplay = midirecplay.MIDIRecPlay()
    #Build the widgets.
    self.widget_midiInDevices = QtGui.QComboBox()
    for portNum, portName in mididevice.getMIDIInDevices():
      self.widget_midiInDevices.addItem(portName, (portNum, portName))
    label_midiInDevices = QtGui.QLabel('MIDI Input Device:')
    label_midiInDevices.setBuddy(self.widget_midiInDevices)
    self.widget_midiOutDevices = QtGui.QComboBox()
    for dev in self.synthNav.getMIDIOutDevs():
      self.widget_midiOutDevices.addItem(dev.portName, dev)
    label_midiOutDevices = QtGui.QLabel('MIDI Output Device:')
    label_midiOutDevices.setBuddy(self.widget_midiOutDevices)
    button_record = QtGui.QPushButton("Record")
    button_play = QtGui.QPushButton("Play")
    button_stop = QtGui.QPushButton("Stop")
    #Lay it out.
    vbox_main = QtGui.QVBoxLayout(self)
    vbox_main.addWidget(label_midiInDevices)
    vbox_main.addWidget(self.widget_midiInDevices)
    vbox_main.addWidget(label_midiOutDevices)
    vbox_main.addWidget(self.widget_midiOutDevices)
    hbox_buttons = QtGui.QHBoxLayout()
    hbox_buttons.addWidget(button_record)
    hbox_buttons.addWidget(button_play)
    hbox_buttons.addWidget(button_stop)
    vbox_main.addLayout(hbox_buttons)
    #Connect to signals.
    button_record.pressed.connect(self._onRecord)
    button_play.pressed.connect(self._onPlay)
    button_stop.pressed.connect(self._onStop)
    self.widget_midiInDevices.currentIndexChanged.connect(self._onMIDIInDeviceSelect)
    self.widget_midiOutDevices.currentIndexChanged.connect(self._onMIDIOutDeviceSelect)

  def _onRecord(self):
    print('_onRecord called')
    try:
      self.midirecplay.startRecording()
    except:
      traceback.print_exc()

  def _onPlay(self):
    print('_onPlay called')
    try:
      self.midirecplay.startPlaying(loop=True)
    except:
      traceback.print_exc()

  def _onStop(self):
    print('_onStop called')
    try:
      if self.midirecplay.isRecording():
        self.midirecplay.stopRecording()
      elif self.midirecplay.isPlaying():
        self.midirecplay.stopPlaying()
    except:
      traceback.print_exc()
    
  def _onMIDIInDeviceSelect(self, index):
    print('_onMIDIInDeviceSelect called')
    try:
      self.midirecplay.open(*self.widget_midiInDevices.itemData(index))
    except:
      traceback.print_exc()
  
  def _onMIDIOutDeviceSelect(self, index):
    print('_onMIDIOutDeviceSelect called')
    try:
      self.midirecplay.setMIDIOutDevice(self.widget_midiOutDevices.itemData(index))
    except:
      traceback.print_exc()
