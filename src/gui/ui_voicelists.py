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
import traceback



##
#  Base class for voice list widgets.
class VoiceListWidget(QtGui.QWidget):

  ## Currently-assigned patchcorral.src.engine.mididevice.MIDIVoiceList object.
  voiceList = None

  class TableWidget(QtGui.QTableWidget):

    keyPressed = QtCore.Signal(QtGui.QKeyEvent)

    def keyPressEvent(self, event):
      super().keyPressEvent(event)
      self.keyPressed.emit(event)

  def __init__(self, parent, synthNav):
    super().__init__(parent)
    self.synthNav = synthNav
    assert self.voiceList is not None, '"self.voiceList" needs to be populated by the subclass.'
    self.voiceMap = {}
    if len(self.voiceList) == 0:
      self.cols = mididevice.MIDIVoice.tags
    else:
      self.cols = list(self.voiceList[0].keys())
    self.numCols = len(self.cols)
    #Create widgets.
    self.tw_currVoices = self.TableWidget(0, self.numCols, self)
    self.tw_currVoices.setHorizontalHeaderLabels(self.cols)
    #Lay it out.
    self.vbox = QtGui.QVBoxLayout(self)
    self.vbox.addWidget(self.tw_currVoices)
    #Populate voices.
    self.setVoiceList(self.voiceList)
    #Connect signals.
    self.tw_currVoices.keyPressed.connect(self.onKeypressEvent)

  def onKeypressEvent(self, event):
    pass

  def refreshCurrVoices(self):
    print("refreshCurrVoices called")
    rowCountI = self.tw_currVoices.rowCount()
    rowCountF = min(len(self.voiceList), 1000)
    self.tw_currVoices.clearContents()
    print("refreshCurrVoices setting row count")
    self.tw_currVoices.setRowCount(rowCountF)
    assert self.tw_currVoices.rowCount() == rowCountF, '{} != {}'.format(self.tw_currVoices.rowCount(), rowCountF)
    print("refreshCurrVoices entering for loops")
    for row, voice in zip(range(rowCountF), self.voiceList):
      for col, attr in enumerate(self.cols):
        item = self.tw_currVoices.item(row, col)
        if item is None or item is 0:
          item = QtGui.QTableWidgetItem(str(voice[attr]))
          isNewItem = True
        else:
          item.setText(str(voice[attr]))
          isNewItem = False
        # self.voiceMap[voice] = item
        item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
        item.voice = voice
        if isNewItem:
          self.tw_currVoices.setItem(row, col, item)
    print("refreshCurrVoices returning")

  def setVoiceList(self, voiceList):
    oVoiceList = self.voiceList
    if isinstance(voiceList, str):
      voiceList = self.synthNav.getVoiceList(voiceList)
    self.voiceList = voiceList
    try:
      self.refreshCurrVoices()
    except:
      self.voiceList = oVoiceList
      self.refreshCurrVoices()
      raise
    else:
      try:
        self.voiceList.listModified.disconnect(self.refreshCurrVoices)
      except:
        traceback.print_exc()
    self.voiceList.listModified.connect(self.refreshCurrVoices)

##
#  Widget displaying voices that remain after applying the selected filters.
class FilteredVoiceListWidget(VoiceListWidget):

  voiceDoubleClicked = QtCore.Signal(mididevice.MIDIVoice)

  def __init__(self, parent, synthNav):
    self.voiceList = synthNav.getFilteredVoiceList()
    super().__init__(parent, synthNav)
    self.tw_currVoices.itemDoubleClicked.connect(self.onItemDoubleClicked)
    self.tw_currVoices.itemSelectionChanged.connect(self.onItemSelectionChanged)

  def onItemDoubleClicked(self, item):
    self.voiceDoubleClicked.emit(item.voice)

  def onItemSelectionChanged(self):
    selectedItems = self.tw_currVoices.selectedItems()
    if len(selectedItems) > 0:
      selectedItems[0].voice.pc()

  def onKeypressEvent(self, event):
    if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
      self.synthNav.getVoiceList('queued').adds(item.voice for item in self.tw_currVoices.selectedItems())
      
class VoiceListSelectWidget(QtGui.QComboBox):

  selectionChanged = QtCore.Signal(str)
  
  def __init__(self, parent, synthNav):
    super().__init__(parent)
    self.addItems(list(synthNav.voiceLists.keys()))
    self.currentIndexChanged.connect(self.onCurrentIndexChanged)
    
  def onCurrentIndexChanged(self, idx):
    self.selectionChanged.emit(self.itemText(idx))

##
#  Widget displaying voices in the currently-selected user list.
class VoiceListEditWidget(VoiceListWidget):

  def __init__(self, parent, synthNav, voiceList="queued"):
    self.voiceList = synthNav.getVoiceList(voiceList)
    super().__init__(parent, synthNav)
    self.pb_clearQueue = QtGui.QPushButton("Clear Queue")
    self.vbox.addWidget(self.pb_clearQueue)
    self.pb_clearQueue.pressed.connect(self.onClearButtonPressed)
    self.tw_currVoices.itemDoubleClicked.connect(self.onItemDoubleClicked)

  def onClearButtonPressed(self):
    self.voiceList.clear()

  def onItemDoubleClicked(self, item):
    item.voice.pc()

  def onKeypressEvent(self, event):
    if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
      items = self.tw_currVoices.selectedItems()
      try:
        item = items[0]
      except IndexError:
        pass
      else:
        item.voice.pc()
    elif event.key() in [QtCore.Qt.Key_Delete]:
      currCell = [self.tw_currVoices.currentRow(), self.tw_currVoices.currentColumn()]
      items = self.tw_currVoices.selectedItems()
      self.voiceList.remove(*(item.voice for item in items))
      if currCell[0] >= self.tw_currVoices.rowCount():
        currCell[0] = self.tw_currVoices.rowCount()
      self.tw_currVoices.setCurrentCell(*currCell)

