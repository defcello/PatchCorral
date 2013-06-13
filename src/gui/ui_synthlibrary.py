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

from PySide import QtGui



class MainWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    super().__init__(parent)
    self.synthNav = synthNav
    self.setWindowTitle('SynthLibrary')
    self.setGeometry(300, 300, 800, 600)
    #Add the selector group.
    filter_coarse = CoarseFilterWidget(self, self.synthNav)

class CoarseFilterWidget(QtGui.QWidget):

  def __init__(self, parent, synthNav):
    self.synthNav = synthNav
    super().__init__(parent)
    #Synth Select
    lv_synth = QtGui.QListWidget(self)
    lv_synth.addItems(map(lambda x: x.ID, self.synthNav.getMIDIOutDevs()))
    #Channel Select
    lv_channel = QtGui.QListWidget(self)
    #Group Select
    lv_group = QtGui.QListWidget(self)

