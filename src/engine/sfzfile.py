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
#  Represents a SFZ file, simplying procedures such as loading and saving.
#  @note SFZ format details taken from "http://www.camelaudio.com/alchemymanual/sfz-files/".
#  @note Full SFZ format specification can be obtained from
#    "http://www.cakewalk.com/DevXchange/article.aspx?aid=108".

from . import file
import re



##
#  Represents an SFZ file, simplying procedures such as loading and saving.
#  @note For details on the SFZ format, see
#    "http://www.cakewalk.com/DevXchange/article.aspx?aid=108".
#  @note Comments are not currently handled by this interface (well, they work,
#    but not the way you would expect them to).
class File(file.File):

  def __init__(self, filename=None):
    self.groups = []
    super().__init__(filename)

  ##
  #  Appends the given Group to the file.
  #  @param group Group object.
  #  @return "None".
  def append(self, group):
    if not isinstance(group, Group):
      raise ValueError('Given group "{}" is not an instance of "{}".'.format(group, Group))
    self.groups.append(group)
    
  ##
  #  Clears the contents of this file.
  def clear(self):
    self.groups = []

  ##
  #  Returns the list of Groupsin the file.
  #  @return List of Group objects.
  def getGroups(self):
    return list(self.groups)

  ##
  #  Returns the index of the given Group in the file.
  #  @param group Group object.
  #  @return Integer.
  def index(self, group):
    if not isinstance(group, Group):
      raise ValueError('Given group "{}" is not an instance of "{}".'.format(group, Group))
    return self.groups.index(group)

  ##
  #  Inserts the given Group into the file.
  #  @param idx List index to insert the group at.
  #  @param group Group object.
  #  @return "None".
  def insert(self, idx, group):
    if not isinstance(group, Group):
      raise ValueError('Given group "{}" is not an instance of "{}".'.format(group, Group))
    self.groups.insert(idx, group)

  def __len__(self):
    return len(self.groups)

  def _load(self, filename):
    self.clear()
    s = ''
    with open(filename, 'r') as fd:
      s = fd.read()
    s = s.split('<group>')
    for g in s[1:]:
      group = Group()
      group.load(g)
      self.groups.append(group)
      
  ##
  #  Looks for samples in the given directory matching the given name prefix.
  #  It will then attempt to construct itself into a proper SFZ using the given
  #  files.
  def loadFromSamples(self, dir, prefix):
    r = re.compile(r'^{}(\d*)\D+(\d+)\.[^\.]*$'.format(prefix))
    files = []
    for f in os.listdir(dir):
      m = r.match(f)
      if m is not None:
        files.append((
          os.path.join(dir, m.group(0)),
          m.group(1),
          m.group(2),
        ))

  ##
  #  Pops the Group at the given index from the file.
  #  @param idx List index to pop the group from.  If "None", will pop from the
  #    end of the list.
  #  @return Group object.
  def pop(self, idx):
    return self.groups.pop(idx)

  ##
  #  Removes the given Group from the file.
  #  @param group Group object.
  #  @return "None".
  def remove(self, group):
    if not isinstance(group, Group):
      raise ValueError('Given group "{}" is not an instance of "{}".'.format(group, Group))
    self.groups.remove(group)

  def _save(self, filename):
    s = ''
    for group in self.groups:
      s += group.save()
    with open(filename, 'w') as fd:
      fd.write(s)
  
##
#  Represents an SFZ "<region>" tag.  Define opcodes by simply setting them as
#  attributes to an instance of the class:
#  @code{.py}
#  region = Region()
#  region.sample = 'mySample.wav'
#  @endcode
#  @note For a list of all opcodes and what they do, see
#    "http://www.cakewalk.com/DevXchange/article.aspx?aid=108".
class Region:

  defaults = {
    'default_path': None,  #Defines the starting location for resolving relative filenames.
    'sample': None,  #Filename of the sample file.
    'volume': None,  #Velocity to play the sample at (-127 to 0)
    'tune': None,  #Pitch offset (-63 to 63)
    'key': None,  #Note that will trigger the sample (0 to 127)
    'pitch_keycenter': None,  #Specify the pitch of the sample for accurate retuning (0 to 127; default is 60)
    'lokey': 0,  #Lowest note that should trigger the sample (0 to 127)
    'hikey': 127,  #Highest note that should trigger the sample (0 to 127)
    'lovel': 0,  #Lowest velocity that should trigger the sample (0 to 127)
    'hivel': 127,  #Highest velocity that should trigger the sample (0 to 127)
    'loop_mode': None,  #0=no loop(default); 1=continuous; 2=sustain; 3=forward/back; 4=all
    'cutoff': None,  #Filter cutoff point in Hz (global value!)
    'fil_veltrack': None,  #Filter cutoff keyboard tracking (0 to 127; global value!)
    'seq_position': None,  #See spec for info.
    'sw_last': None,  #For key switching; region will only play if the last received MIDI note number matches this value.
    'trigger': None,  #Sets the trigger for playing the sample ("attack"(default), "release", "first", "legato")
  }
  
  __slots__ = ['attrs']

  ##
  #  Class constructor.
  #  @code{.py}
  #  region = Region(sample='mySample.wav')
  #  @endcode
  #  @param kargs Any number of keyword arguments with "key" being the attribute
  #    to set and "value" being the value to set the attribute to.
  def __init__(self, **kargs):
    self.attrs = dict(self.defaults)
    self.attrs.update(kargs)

  ##
  #  Clears all set attributes and regions.
  def clear(self):
    self.attrs = dict(self.defaults)

  def __getattr__(self, attr):
    if attr in type(self).__slots__:
      return super().__getattr__(attr)
    if not isinstance(attr, str):
      raise ValueError('Given attr "{}" is of type "{}"; expected "{}".'.format(
        attr,
        type(attr),
        str,
      ))
    return self.attrs[attr]

  ##
  #  Loads the given string into this object.  All current data will be cleared.
  def load(self, string):
    self.clear()
    r = re.compile(r'^(\S+)=(.*)$')
    for s in string.split('\n'):
      if s == '':
        continue
      m = r.match(s)
      if m is None:
        raise ValueError('Unable to parse "{}" in string "{}".'.format(s, string))
      k = m.group(1)
      try:
        v = int(m.group(2))
      except ValueError:
        v = m.group(2)
      setattr(self, k, v)

  ##
  #  Generates the string for use in the SFZ file.
  #  @return Str object.
  def save(self):
    ret = '<region>\n'
    for k, v in self.attrs:
      if v is None:
        continue
      ret += '{}={}\n'.format(k, v)
    return ret

  def __setattr__(self, attr, value):
    if attr in type(self).__slots__:
      return super().__setattr__(attr, value)
    if not isinstance(attr, str):
      raise ValueError('Given attr "{}" is of type "{}"; expected "{}".'.format(
        attr,
        type(attr),
        str,
      ))
    self.attrs[attr] = value

##
#  Represents an SFZ "<group>" tag.  Opcodes defined in groups serve as
#  default values for any regions contained within it.  Define opcodes by
#  simply setting them as attributes of the instance of the class.
#  @note For a list of all opcodes and what they do, see
#    "http://www.cakewalk.com/DevXchange/article.aspx?aid=108".
class Group(Region):
  
  __slots__ = ['attrs', 'regions']

  ##
  #  Class constructor.
  #  @code{.py}
  #  region = Group(default_path='../My Samples')
  #  @endcode
  #  @param kargs Any number of keyword arguments with "key" being the attribute
  #    to set and "value" being the value to set the attribute to.
  def __init__(self, **kargs):
    super().__init__(**kargs)
    self.regions = []

  ##
  #  Appends the given Region to the file.
  #  @param region Region object.
  #  @return "None".
  def append(self, region):
    if not isinstance(region, Region):
      raise ValueError('Given region "{}" is of type "{}"; expected "{}".'.format(
        region, type(region), Region,
      ))
    self.regions.append(region)

  ##
  #  Clears all set attributes and regions.
  def clear(self):
    super().clear()
    self.regions.clear()

  ##
  #  Returns the list of Groupsin the file.
  #  @return List of Region objects.
  def getRegions(self):
    return list(self.regions)

  ##
  #  Returns the index of the given Region in the file.
  #  @param region Region object.
  #  @return Integer.
  def index(self, region):
    if not isinstance(region, Region):
      raise ValueError('Given region "{}" is of type "{}"; expected "{}".'.format(
        region, type(region), Region,
      ))
    return self.regions.index(region)

  ##
  #  Inserts the given Region into the file.
  #  @param idx List index to insert the region at.
  #  @param region Region object.
  #  @return "None".
  def insert(self, idx, region):
    if not isinstance(region, Region):
      raise ValueError('Given region "{}" is of type "{}"; expected "{}".'.format(
        region, type(region), Region,
      ))
    self.regions.insert(idx, region)

  def __len__(self):
    return len(self.regions)

  ##
  #  Loads the given string into this object.  All current data will be cleared.
  def load(self, string):
    s = string.split('<region>')
    super().load(s[0])
    for r in s[1:]:
      region = Region()
      region.load(r)
      self.regions.append(region)

  ##
  #  Pops the Region at the given index from the file.
  #  @param idx List index to pop the region from.  If "None", will pop from the end of the list.
  #  @return Region object.
  def insert(self, idx):
    return self.regions.pop(idx)

  ##
  #  Removes the given Region from the file.
  #  @param region Region object.
  #  @return "None".
  def remove(self, region):
    if not isinstance(region, Region):
      raise ValueError('Given region "{}" is of type "{}"; expected "{}".'.format(
        region, type(region), Region,
      ))
    self.regions.remove(region)

  ##
  #  Generates the string for use in the SFZ file.
  #  @return Str object.
  def save(self):
    ret = '<group>\n'
    for k, v in self.attrs:
      ret += '{}={}\n'.format(k, v)
    for region in self.regions:
      ret += region.save()
    return ret
