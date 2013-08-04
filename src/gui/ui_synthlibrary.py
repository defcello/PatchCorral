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
from patchcorral.src.engine import synthnav, mididevice
from . import ui_midirecplay



class MainWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    super().__init__(parent)
    self.synthNav = synthNav
    self.setWindowTitle('PatchCorral')
    self.setGeometry(300, 300, 800, 600)
    #Build the widgets.
    widget_filter = FilterWidget(self, self.synthNav)
    widget_voice_list = FilteredVoiceListWidget(self, self.synthNav)
    widget_queued_list = QueuedVoiceListWidget(self, self.synthNav)
    widget_recplay = ui_midirecplay.RecPlayWidget(self, self.synthNav)
    #Lay it out.
    hbox_main = QtGui.QHBoxLayout(self)
    splitter_main = QtGui.QSplitter(QtCore.Qt.Orientation.Horizontal, self)

    splitter_filtering = QtGui.QSplitter(QtCore.Qt.Orientation.Vertical, splitter_main)  #For customizing size of filtering widgets
    widget_filters = QtGui.QWidget(splitter_filtering)  #Groups filter widgets
    vbox_filters = QtGui.QVBoxLayout()  #Layout for filter widgets
    vbox_filters.addWidget(widget_filter)
    widget_filters.setLayout(vbox_filters)
    splitter_filtering.addWidget(widget_filters)
    splitter_filtering.addWidget(widget_voice_list)

    splitter_rhs = QtGui.QSplitter(QtCore.Qt.Orientation.Vertical, splitter_main)
    splitter_rhs.addWidget(widget_queued_list)
    splitter_rhs.addWidget(widget_recplay)
    
    splitter_main.addWidget(splitter_filtering)
    splitter_main.addWidget(splitter_rhs)
    hbox_main.addWidget(splitter_main)

class FilterWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    self.synthNav = synthNav
    super().__init__(parent)
    self.synthFilter = None
    self.channelFilter = None
    self.categoryFilter = None
    #Create Widgets
    # Synth Select
    self.lw_synth = QtGui.QListWidget(self)
    self.lw_synth.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.lw_synth.addItems([x.getPortName() for x in self.synthNav.getMIDIOutDevs()])
    # Channel Select
    self.lw_channel = QtGui.QListWidget(self)
    self.lw_channel.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.lw_channel.addItems(list(str(x) for x in self.synthNav.getCurrChannels()))
    # Category Select
    self.lw_category = QtGui.QListWidget(self)
    self.lw_category.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.lw_category.addItems(list(self.synthNav.getCurrCategories()))
    # Custom Filter
    self.widget_filter_custom = CustomFilterWidget(self, self.synthNav)
    #Lay it out.
    vbox = QtGui.QVBoxLayout(self)
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(self.lw_synth)
    hbox.addWidget(self.lw_channel)
    hbox.addWidget(self.lw_category)
    vbox.addLayout(hbox)
    vbox.addWidget(self.widget_filter_custom)
    #Connect to signals.
    self.lw_synth.itemSelectionChanged.connect(self.onSynthSelectionChanged)
    self.lw_channel.itemSelectionChanged.connect(self.onChannelSelectionChanged)
    self.lw_category.itemSelectionChanged.connect(self.onCategorySelectionChanged)
    self.widget_filter_custom.pb_clearFilter.clicked.connect(self.onFilterClear)

  def onFilterClear(self):
    for item in self.lw_synth.selectedItems():
      item.setSelected(False)
    for item in self.lw_channel.selectedItems():
      item.setSelected(False)
    for item in self.lw_category.selectedItems():
      item.setSelected(False)

  def onSynthSelectionChanged(self):
    ofilter = self.synthFilter
    selectedItems = self.lw_synth.selectedItems()
    if len(selectedItems) == 0:
      nfilter = None
    else:
      nfilter = 'and v.device.portName in [\'{}\']'.format('\', \''.join(
        item.text() for item in self.lw_synth.selectedItems()
      ))
    self.widget_filter_custom.updateFilter(nfilter, ofilter)
    self.synthFilter = nfilter

  def onChannelSelectionChanged(self):
    ofilter = self.channelFilter
    selectedItems = self.lw_channel.selectedItems()
    if len(selectedItems) == 0:
      nfilter = None
    else:
      nfilter = 'and v.channel in [{}]'.format(', '.join(
        item.text() for item in self.lw_channel.selectedItems()
      ))
    self.widget_filter_custom.updateFilter(nfilter, ofilter)
    self.channelFilter = nfilter

  def onCategorySelectionChanged(self):
    ofilter = self.categoryFilter
    selectedItems = self.lw_category.selectedItems()
    if len(selectedItems) == 0:
      nfilter = None
    else:
      nfilter = 'and v.category in [\'{}\']'.format('\', \''.join(
        item.text() for item in self.lw_category.selectedItems()
      ))
    self.widget_filter_custom.updateFilter(nfilter, ofilter)
    self.categoryFilter = nfilter

class CustomFilterWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    self.synthNav = synthNav
    super().__init__(parent)
    #Create widgets.
    self.le_filter = QtGui.QLineEdit('True', self)
    self.pb_applyFilter = QtGui.QPushButton('Apply', self)
    self.pb_clearFilter = QtGui.QPushButton('Clear', self)
    #Lay it out.
    vbox = QtGui.QVBoxLayout(self)
    vbox.addWidget(QtGui.QLabel(
      'Params: {}'.format(','.join('v.{}'.format(key) for key in self.synthNav.getVoiceList('all')[0].keys())),
      self,
    ))
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(self.le_filter)
    hbox.addWidget(self.pb_clearFilter)
    hbox.addWidget(self.pb_applyFilter)
    vbox.addLayout(hbox)
    #Connect signals.
    self.synthNav.filterChanged.connect(self.le_filter.setText)
    self.pb_applyFilter.clicked.connect(self.onApplyButtonPressed)
    self.pb_clearFilter.clicked.connect(self.onClearButtonPressed)

  ##
  #  Callback for when the "Apply" button is pressed.
  #  @post Current filter will be applied to the engine.
  #  @return "None".
  def onApplyButtonPressed(self):
    self.synthNav.filter(self.le_filter.text())

  ##
  #  Callback for when the "Clear" button is pressed.
  #  @post Current filter will be replaced with "True" and will be applied to
  #    the engine.
  #  @return "None".
  def onClearButtonPressed(self):
    self.synthNav.filter('True')

  ##
  #  Updates the custom filter.
  #  @param n New filter string.  If "None", will use an empty string.
  #  @param o Original filter string to replace.  If "None", "n" will be
  #    appended to the current filter string.
  #  @return "None".
  #  @post The new filter will be applied to the engine.
  def updateFilter(self, n, o=None):
    currFilter = self.le_filter.text()
    if o is None:
      if n is not None:
        self.synthNav.filter('{} {}'.format(currFilter, n).strip())
    else:
      if n is None:
        n = ''
      self.synthNav.filter(currFilter.replace(o, n).strip())

class VoiceListWidget(QtGui.QWidget):

  class TableWidget(QtGui.QTableWidget):
    
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)
    
    def keyPressEvent(self, event):
      super().keyPressEvent(event)
      self.keyPressed.emit(event)

  def __init__(self, parent, synthNav):
    super().__init__(parent)
    self.synthNav = synthNav
    assert hasattr(self, 'voiceList'), '"self.voiceList" needs to be populated by the subclass.'
    self.voiceMap = {}
    if len(self.voiceList) == 0:
      self.cols = mididevice.MIDIVoice.tags
    else:
      self.cols = list(self.voiceList[0].keys())
    self.numCols = len(self.cols)
    #Create widgets.
    self.tw_currVoices = self.TableWidget(0, self.numCols, self)
    self.tw_currVoices.setHorizontalHeaderLabels(self.cols)
    self.refreshCurrVoices()
    #Lay it out.
    self.vbox = QtGui.QVBoxLayout(self)
    self.vbox.addWidget(self.tw_currVoices)
    #Connect signals.
    self.voiceList.listModified.connect(self.refreshCurrVoices)
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
    # import pdb; pdb.set_trace()
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

class FilteredVoiceListWidget(VoiceListWidget):

  def __init__(self, parent, synthNav):
    self.voiceList = synthNav.getFilteredVoiceList()
    super().__init__(parent, synthNav)
    self.tw_currVoices.itemDoubleClicked.connect(self.onItemDoubleClicked)

  def onItemDoubleClicked(self, item):
    self.synthNav.getVoiceList('queued').add(item.voice)
    
  def onKeypressEvent(self, event):
    if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
      self.synthNav.getVoiceList('queued').adds(item.voice for item in self.tw_currVoices.selectedItems())

class QueuedVoiceListWidget(VoiceListWidget):

  def __init__(self, parent, synthNav):
    self.voiceList = synthNav.getVoiceList('queued')
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






