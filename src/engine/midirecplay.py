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
from patchcorral.src.data import synthesizers
from PySide import QtCore
import rtmidi
import time
import threading
import traceback



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
    self._isRecording = False
    self.player = MIDIPlay()
    
  ##
  #  Returns the MIDIPlay object used for playback of recordings.
  #  Use with care!
  #  @return MIDIPlay object.
  def getPlayer(self):
    return self.player
    
  def isPlaying(self):
    return self.player.isPlaying()
  
  def isRecording(self):
    return self._isRecording

  ##
  #  Opens the given MIDI input port for recording.
  #  @param port Integer.  If "None", will be resolved using "name".
  #  @param name String.  If "None", will be resolved using "port".
  #  @param midiDevs List of 2-tuples "(port number, device name)".  If "None",
  #    will be resolved using a fresh device query.
  def open(self, port=None, name=None, midiDevs=None):
    if self.midi is not None:
      self.close()
      self.midi = None
    if port is None and name is None:
      port = self.port
      name = self.name
    if port is None and name is None:
      raise ValueError("Must provide a port number or port name.")
    midi = synthesizers.getMIDIInDevice(port, name, midiDevs)
    self.setMIDIInDevice(midi)

  def close(self):
    assert self.midi is not None, "No MIDI Device available to close!"
    self.midi.closePort()
    self.midi.midiEvent.disconnect(self._onEventReceived)
    self.midi = None
    
  def setMIDIInDevice(self, midi):
    if self.midi is not None:
      self.close()
    self.midi = midi
    self.port = midi.portNum
    self.name = midi.portName
    self.midi.midiEvent.connect(self._onEventReceived)
    
  def setMIDIOutDevice(self, midi):
    self.player.setMIDIOutDevice(midi)

  def startRecording(self):
    if not self.isPlaying():
      self.startTime = None
      self.recording = []
      self._isRecording = True
    else:
      raise Exception('Cannot record while playing back!')

  def stopRecording(self):
    self._isRecording = False
    for ch in range(1, 17):
      self.recording.append( (time.time() - self.startTime, rtmidi.MidiMessage.allNotesOff(ch)) )

  def _onEventReceived(self, data):
    # print("_onEventReceived called; recording is {}".format(self.recording))
    self.eventReceived.emit(data)
    if self._isRecording:
      if self.startTime is None:
        self.startTime = time.time()
      self.recording.append( (time.time() - self.startTime, data) )

  def startPlaying(self, midiOutDevice=None, loop=False):
    if self._isRecording:
      raise Exception('Cannot play back while recording!')
    self.player.loopPlayback(loop)
    self.player.play(self.recording, midiOutDevice)

  def stopPlaying(self):
    self.player.stop()

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
    super().__init__()
    self.recording = recording
    self.midiOutDevice = midiOutDevice
    self.playbackThread = None
    self._keepPlaying = False
    self.startTime = None
    self.loopMode = False
    
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
  def play(self, recording=None, midiOutDevice=None):
    if self.playbackThread is not None:
      raise Exception('Playback is already active.')
    if recording is not None:
      self.recording = recording
    if self.recording is None:
      raise ValueError('No recording has been provided!')
    if midiOutDevice is not None:
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
      while self._keepPlaying:
        self.startTime = time.time()
        for playTime, data in self.recording:
          while self._keepPlaying:
            #Wait for the right time to trigger the event.
            currDur = time.time() - self.startTime
            sleepDur = playTime - currDur
            if sleepDur > 0:
              if sleepDur > 0.3:
                time.sleep(0.3)
              else:
                time.sleep(sleepDur)
            break
          if self.midiOutDevice is not None:
            self.midiOutDevice.sendMessage(data)
          self.playbackEvent.emit(data)
        if not self.loopMode:
          break
    except:
      traceback.print_exc()
    finally:
      self.playbackThread = None
      self.startTime = None
      self.stop()
      self.playbackStopped.emit()
      
  ##
  #  Gets/sets the looping playback setting.
  #  @param val If "True", playback will loop indefinitely.  If "False",
  #    playback will stop after one iteration.  If "None", the value will go
  #    unchanged.
  #  @return "True" if playback is set to loop indefinitely; "False" if playback
  #    is set to stop after one iteration.
  def loopPlayback(self, val=None):
    if val is not None:
      self.loopMode = val
    return self.loopMode
    
  def setMIDIOutDevice(self, dev):
    self.midiOutDevice = dev

  ##
  #  Stops playback of the MIDI sequence.  Note that this may take at least 0.3
  #  seconds to actually stop, but this function will not block for that to
  #  occur.
  def stop(self):
    self._keepPlaying = False
