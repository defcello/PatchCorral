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
#  Represents a file in the file system.  Simplifies operations such as loading, saving, and
#  tracking modifications outside of the process.

import os



##
#  Represents a file in the file system.  Simplifies operations such as loading, saving, and
#  tracking modifications outside of the process.
class File():

  ##
  #  Class initializer.
  #  @param filename Name of the file to load.  If "None", will not be associated with a file until
  #    "load" or "save" is called.
  #  @return "None".
  def __init__(self, filename=None):
    self.filename = filename
    if filename is not None:
      if not os.path.exists(filename):
        open(filename, 'w').close()
      self.load()

  ##
  #  Loads the given file.
  #  @param filename Path of the file to load.
  #  @return "None".
  def load(self, filename=None):
    if filename is None:
      if self.filename is None:
        raise ValueError('No associated filename.  One must be provided.')
      filename = self.filename
    self._load(filename)
    self.filename = filename

  ##
  #  Helper function for "load".  Intended to be overridden by subclasses.
  #  @param filename Path of the file to load.
  #  @return "None".
  def _load(self, filename):
    pass

  ##
  #  Saves the current contents to file.
  #  @param filename Path to save to.
  #  @return "None".
  def save(self, filename=None):
    if filename is None:
      if self.filename is None:
        raise ValueError('No associated filename.  One must be provided.')
      filename = self.filename
    self._save(filename)
    self.filename = filename

  ##
  #  Helper function for "save".  Intended to be overridden by subclasses.
  #  @param filename Path to save to.
  #  @return "None".
  def _save(self, filename):
    pass
