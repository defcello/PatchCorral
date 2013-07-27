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

from . import mididevice
from . import synthnav
from PySide import QtCore
import time



##
#  Class for capturing and playing back MIDI events.
class MIDIRecPlay(QtCore.QObject):

  recordingStarted = QtCore.Signal()
  eventReceived = QtCore.Signal(object)
  recordingStopped = QtCore.Signal()
  playbackStarted = QtCore.Signal()
  playbackEvent = QtCore.Signal(object)
  playbackStopped = QtCore.Signal()

  ##
  #  Class constructor.
  #  @param port Integer.  If "None", will be resolved using "name".
  #  @param name String.  If "None", will be resolved using "port".
  #  @param midiDevs List of 2-tuples "(port number, device name)".  If "None",
  #    will be resolved using a fresh device query.
  def __init__(self, port=None, name=None, midiDevs=None):
    super().__init__()
    self.port = port
    self.name = name
    self.midi = None
    self.recording = []
    self.startTime = None
    self.isRecording = False
    self.isPlaying = False
    self.player = MIDIPlay()

  ##
  #  Opens the given MIDI input port for recording.
  #  @param port Integer.  If "None", will be resolved using "name".
  #  @param name String.  If "None", will be resolved using "port".
  #  @param midiDevs List of 2-tuples "(port number, device name)".  If "None",
  #    will be resolved using a fresh device query.
  def open(self, port=None, name=None, midiDevs=None):
    if self.midi is not None:
      self.close()
    if port is None and name is None:
      port = self.port
      name = self.name
    if port is None and name is None:
      raise ValueError("Must provide a port number or port name.")
    module = synthnav.getMIDIInDevice(port, name, midiDevs)
    self.midi = module.MIDIInDevice(name)
    self.port = port
    self.name = name
    self.midi.eventReceived.connect(self._onEventReceived)
    self.midiOutDevice = None

  def close(self):
    assert self.midi is not None, "No MIDI Device available to close!"
    self.midi.closePort()
    self.midi.eventReceived.disconnect(self._onEventReceived)
    self.midi = None

  def startRecording(self):
    if not self.isPlaying:
      self.isRecording = True
    else:
      raise Exception('Cannot record while playing back!')

  def stopRecording(self):
    self.isRecording = False

  def _onEventReceived(self, data):
    self.eventReceived.emit(data)
    if self.isRecording:
      if self.startTime is None:
        self.startTime = time.time()
      self.recording.append( (time.time() - self.startTime, data) )

  def startPlaying(self, midiOutDevice=None):
    if midiOutDevice is not None:
      self.midiOutDevice = midiOutDevice
    if not self.isRecording:
      self.isPlaying = True
    else:
      raise Exception('Cannot play back while recording!')

  def stopPlaying(self):
    self.isPlaying = False

##
#  Plays a given list of 2-tuples "(delay in seconds, MIDI event)".
class MIDIPlay(QtCore.QObject):

  playbackStarted = QtCore.Signal()
  playbackEvent = QtCore.Signal(object)
  playbackStopped = QtCore.Signal()

  ##
  #  Class constructor.
  #  @param recording List of 2-tuples "(delay in seconds, MIDI event)".
  #  @param midiOutDevice patchcorral.src.engine.mididevice.MIDIOutDevice object.
  def __init__(self, recording=None, midiOutDevice=None):
    self.recording = recording
    self.midiOutDevice = midiOutDevice
    self.playbackThread = None
    self._keepPlaying = False
    
  ##
  #  Indicates if playback is active.
  #  @return "True" if playback is active; "False" otherwise.
  def isPlaying(self):
    return self.playbackThread is not None

  ##
  #  Initiates playback of the given recording.
  #  @param recording List of 2-tuples "(delay in seconds, MIDI event)".  If
  #    "None", will use the previously-used recording.
  #  @param midiOutDevice patchcorral.src.engine.mididevice.MIDIOutDevice object.
  #    If "None", will use the previously-used.
  #  @return "None".
  def start(self, recording=None, midiOutDevice=None):
    if self.playbackThread is not None:
      raise Exception('Playback is already active.')
    if recording is None:
      recording = self.recording
    else:
      self.recording = recording
    if recording is None:
      raise ValueError('No recording has been provided!')
    if midiOutDevice is None:
      midiOutDevice = self.midiOutDevice
    else:
      self.midiOutDevice = midiOutDevice
    self.playbackThread = threading.Thread(target=self._play)
    self._keepPlaying = True
    self.playbackThread.start()

  ##
  #  Plays this object's recording.
  def _play(self):
    self.playbackStarted.emit()
    try:
      assert self.startTime is None, "Playback already running!"
      self.startTime = time.time()
      for playTime, data in self.recording:
        while self._keepPlaying:
          #Wait for the right time to trigger the event.
          currDur = time.time() - self.startTime
          sleepDur = currDur - playTime
          if sleepDur > 0:
            if sleepDur > 0.3:
              time.sleep(0.3)
            else:
              time.sleep(sleepDur)
        if self.midiOutDevice is not None:
          self.midiOutDevice.sendMessage(data)
        self.playbackEvent.emit(data)
    finally:
      self.playbackStopped.emit()
      self.playbackThread = None
      self.stop()

  ##
  #  Stops playback of the MIDI sequence.  Note that this may take at least 0.3
  #  seconds to actually stop, but this function will not block for that to
  #  occur.
  def stop(self):
    self._keepPlaying = False
