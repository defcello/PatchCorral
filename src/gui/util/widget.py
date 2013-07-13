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

## @file
#  Widget metaclass that eliminates boilerplate from the GUI code.

from PySide import QtGui



##
#  Metaclass for constructing subclasses of PySide.QtGui.QWidget objects minus a
#  lot of the boilerplate.
#  - Automatically calls "setupUi" after widget construction.   This saves most
#    users from having to define an "__init__" method.
#  @code{.py}
#  class MyWidget(PySide.QtGui.MainWindow):
#    __metaclass__ = src.gui.util.widget.metawidget
#    def setupUi(self):
#      #Add a bunch of child widgets.
#  @endcode
class metawidget(type):

  ##
  #  Returns a new class.
  def __new__(mcs, name, bases, attrs):
    def newInit(self, parent=None, f=0):
      super().__init__(parent, f)
      self.setupUi()
    def newSetupUi(self):
      pass
    attrs['__init__'] = newInit
    attrs.setdefault('setupUi', newSetupUi)
    return super().__new__(mcs, name, bases, attrs)

##
#  Subclass of widget that handles actions that are being done for everything.
  ##
  #  Class initializer.
  #  @param parent Parent of the widget.  If "None", will be treated as a
  #    stand-alone window.
  #  @param f Style flags for the widget (see PySide documentation).
  #  @return "None".
  def __init__(self, parent=None, f=0):
    super().__init__(parent, f)
    self.setupUi()

  ##
  #  Populates the widget with stuff.  Intended to be overridden by subclasses.
  #  @return "None".
  def setupUi(self):
    pass

