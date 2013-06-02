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
#  Represents a YAML file, simplying procedures such as loading and saving.

from . import file
import yaml



##
#  Represents a YAML file, simplying procedures such as loading and saving.
class File(file.File):

  ##
  #  Class initializer.
  #  @param filename Name of the file to load.  If "None", will not be associated with a file until
  #    "load" or "save" is called.
  #  @param
  def __init__(self, filename=None, root=None):
    self.root = root
    super().__init__(filename)

  def _load(self, filename):
    with open(filename, 'r') as fd:
      self.root = yaml.load(fd)

  ##
  #  Returns the object considered to be the root of the document.
  #  @return Python object.
  def getRoot(self):
    return self.root

  ##
  #  Sets the given object as the root of the document.
  #  @param root Python object.
  def setRoot(self, root):
    self.root = root

  def _save(self, filename):
    with open(filename, 'w') as fd:
      fd.write(yaml.dump(self.root))
