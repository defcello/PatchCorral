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
#  Tree data structure that can set and get data using path lookups.


##
#  Tree data structure that can set and get data using tuple-delimited path lookups.
class AddressableTree():

  ##
  #  Class initializer.
  #  @param _key Key to initialize this object with.  Intended for internal use only.
  #  @param _value Value to initialize this object with.  Intended for internal use only.
  #  @return "None".
  def __init__(self, _key=None, _value=None):
    self.key = _key
    self.value = _value
    self.children = []

  ##
  #  Returns the AddressableTree item representing the given key.
  #  @param key Tuple of objects forming a path to look up.
  #  @param createMissing If "True", will create elements to resolve missing parts of the given
  #    path.
  #  @throws KeyError If the given key could not be found.
  #  @return AddressableTree object.
  def find(self, key, createMissing=False):
    print('find called with key={} and createMissing={}.'.format(repr(key), repr(createMissing)))
    token = key[0]
    keyR = key[1:]
    #Resolve the token.
    at = None
    for child in self.children:
      if child.key == token:
        at = child
        break
    if at is None:
      if createMissing:
        at = AddressableTree(token)
        self.children.append(at)
      else:
        raise KeyError('Unable to resolve key "{}" on element "{}" with key "{}".'.format(key, self, self.key))
    #Token resolved.  Recurse or return the object.
    if len(keyR) == 0:
      return at
    return at.find(keyR, createMissing)

  ##
  #  Fetches the value corresponding to the given key.  If the key does not exist, returns
  #  "default".
  #  @param key Tuple of objects forming a path to look up.
  #  @param default Value to return if "key" could not be resolved.
  #  @return Value at given key, or "default" if key could not be resolved.
  def get(self, key, default=None):
    try:
      return self.__getitem__(key)
    except KeyError:
      return default

  ##
  #  Fetches the value corresponding to the given key.
  #  @param key Tuple of objects forming a path to look up.
  #  @throws KeyError If the given key could not be found.
  #  @return Value at given key.
  def __getitem__(self, key):
    return self.find(key).value

  ##
  #  Stores the given value at the given key.
  #  @param key Key to store "value" at.
  #  @param value Value to store at "key".
  #  @return "None".
  def set(self, key, value=None):
    self.__setitem__(key, value)

  ##
  #  Stores the given value at the given key.
  #  @param key Key to store "value" at.
  #  @param value Value to store at "key".
  #  @return "None".
  def __setitem__(self, key, value):
    self.find(key, True).value = value
