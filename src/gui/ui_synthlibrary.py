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
from patchcorral.src.gui import ui_midirecplay, ui_voicelists




class MainWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    super().__init__(parent)
    self.synthNav = synthNav
    self.setWindowTitle('PatchCorral')
    self.setGeometry(300, 300, 800, 600)
    #Build the widgets.
    self.widget_filter = FilterWidget(self, self.synthNav)
    self.widget_voice_list = ui_voicelists.FilteredVoiceListWidget(self, self.synthNav)
    self.widget_queued_list = ui_voicelists.VoiceListEditWidget(self, self.synthNav)
    self.widget_recplay = ui_midirecplay.RecPlayWidget(self, self.synthNav)
    self.widget_listsel = ui_voicelists.VoiceListSelectWidget(self, self.synthNav)
    #Lay it out.
    hbox_main = QtGui.QHBoxLayout(self)
    splitter_main = QtGui.QSplitter(QtCore.Qt.Orientation.Horizontal, self)

    splitter_filtering = QtGui.QSplitter(QtCore.Qt.Orientation.Vertical, splitter_main)  #For customizing size of filtering widgets
    widget_filters = QtGui.QWidget(splitter_filtering)  #Groups filter widgets
    vbox_filters = QtGui.QVBoxLayout()  #Layout for filter widgets
    vbox_filters.addWidget(self.widget_filter)
    widget_filters.setLayout(vbox_filters)
    splitter_filtering.addWidget(widget_filters)
    splitter_filtering.addWidget(self.widget_voice_list)

    splitter_rhs = QtGui.QSplitter(QtCore.Qt.Orientation.Vertical, splitter_main)
    splitter_rhs.addWidget(self.widget_listsel)
    splitter_rhs.addWidget(self.widget_queued_list)
    splitter_rhs.addWidget(self.widget_recplay)
    
    splitter_main.addWidget(splitter_filtering)
    splitter_main.addWidget(splitter_rhs)
    hbox_main.addWidget(splitter_main)
    #Connect the signals.
    self.widget_listsel.selectionChanged.connect(self.widget_queued_list.setVoiceList)
    self.widget_voice_list.voiceDoubleClicked.connect(self.addVoiceToCurrList)
    
  def addVoiceToCurrList(self, voice):
    self.getCurrVoiceList().add(voice)
    
  def getCurrVoiceList(self):
    return self.widget_queued_list.voiceList

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
    self.lw_synth.addItems([x.get_port_name() for x in self.synthNav.getMIDIOutDevs()])
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





