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
#  Initializes the GUI for SynthNav.

from PySide import QtGui, QtCore
from src.engine import synthnav



class MainWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    super().__init__(parent)
    self.synthNav = synthNav
    self.setWindowTitle('SynthLibrary')
    self.setGeometry(300, 300, 800, 600)
    #Build the widgets.
    widget_filter_coarse = CoarseFilterWidget(self, self.synthNav)
    widget_filter_custom = CustomFilterWidget(self, self.synthNav)
    widget_voice_list = FilteredVoiceListWidget(self, self.synthNav)
    widget_queued_list = QueuedVoiceListWidget(self, self.synthNav)
    #Lay it out.
    hbox_main = QtGui.QHBoxLayout(self)
    splitter_main = QtGui.QSplitter(QtCore.Qt.Orientation.Horizontal, self)
    
    splitter_filtering = QtGui.QSplitter(QtCore.Qt.Orientation.Vertical, splitter_main)  #For customizing size of filtering widgets
    widget_filters = QtGui.QWidget(splitter_filtering)  #Groups filter widgets
    vbox_filters = QtGui.QVBoxLayout()  #Layout for filter widgets
    vbox_filters.addWidget(widget_filter_coarse)  
    vbox_filters.addWidget(widget_filter_custom)
    widget_filters.setLayout(vbox_filters)
    splitter_filtering.addWidget(widget_filters)
    splitter_filtering.addWidget(widget_voice_list)
    splitter_main.addWidget(splitter_filtering)
    
    splitter_main.addWidget(widget_queued_list)
    hbox_main.addWidget(splitter_main)

class CoarseFilterWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    self.synthNav = synthNav
    super().__init__(parent)
    #Synth Select
    lw_synth = QtGui.QListWidget(self)
    lw_synth.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    lw_synth.addItems([x.getPortName() for x in self.synthNav.getMIDIOutDevs()])
    #Channel Select
    lw_channel = QtGui.QListWidget(self)
    lw_channel.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    lw_channel.addItems(list(str(x) for x in self.synthNav.getCurrChannels()))
    #Category Select
    lw_category = QtGui.QListWidget(self)
    lw_category.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    lw_category.addItems(list(self.synthNav.getCurrCategories()))

    hbox = QtGui.QHBoxLayout(self)
    hbox.addWidget(lw_synth)
    hbox.addWidget(lw_channel)
    hbox.addWidget(lw_category)

class CustomFilterWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    self.synthNav = synthNav
    super().__init__(parent)

    vbox = QtGui.QVBoxLayout(self)
    vbox.addWidget(QtGui.QLabel(
      'Params: {}'.format(','.join(self.synthNav.getVoiceList()[0].keys())),
      self,
    ))
    hbox = QtGui.QHBoxLayout()
    le_filter = QtGui.QLineEdit('True', self)
    pb_applyFilter = QtGui.QPushButton('Apply', self)
    hbox.addWidget(le_filter)
    hbox.addWidget(pb_applyFilter)
    vbox.addLayout(hbox)

class FilteredVoiceListWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    self.synthNav = synthNav
    super().__init__(parent)

    self.voices = self.synthNav.getFilteredVoiceList()
    self.cols = list(self.voices[0].keys())
    self.numCols = len(self.cols)
    self.tw_currVoices = QtGui.QTableWidget(0, self.numCols, self)
    self.tw_currVoices.setHorizontalHeaderLabels(self.cols)
    self.refreshCurrVoices()

    vbox = QtGui.QVBoxLayout(self)
    vbox.addWidget(self.tw_currVoices)

  def refreshCurrVoices(self):
    self.voices = self.synthNav.getFilteredVoiceList()
    self.tw_currVoices.setRowCount(len(self.voices))
    for row, voice in enumerate(self.voices):
      for col, attr in enumerate(self.cols):
        self.tw_currVoices.setItem(row, col, QtGui.QTableWidgetItem(str(voice[attr])))

class QueuedVoiceListWidget(FilteredVoiceListWidget):

  def refreshCurrVoices(self):
    self.voices = self.synthNav.getVoiceList('queued')
    self.tw_currVoices.setRowCount(len(self.voices))
    for row, voice in enumerate(self.voices):
      for col, attr in enumerate(self.cols):
        self.tw_currVoices.setItem(row, col, QtGui.QTableWidgetItem(str(voice[attr])))






