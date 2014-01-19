PatchCorral
===========
This is a program I'm writing to bring my Roland Fantom XR into a more manageable environment (and other synthesizers, in time).  It uses an interface similar to what you would find in a media player program to allow users to easily work down the patches to find that perfect sound from their library.  It also enables the user to do WireShark-style filters on the patch list for more advanced queries.

![PatchCorral Screenshot](./screenshot.png "Screenshot")

Right now, the filtering and queueing of patches is all working.  The next features to implement include:
 - Generated patch lists can be saved/loaded to/from file, including a "favorites list".
 - Add "star" button for favoriting patches.
 - Add support for multiple patch lists in the queue section.
 - Roland Fantom XR: Add support for Rhythm patches
 - Add ability to route MIDI events from an input device to an output device
 - Add ability to record and loop MIDI events from an input device to an output device so you don't have to constantly be playing the loop manually.
 - "Speed Search" mode that will automatically step through the patches and let the user delete patches from the queue as it goes.
 - Add ability to sort patches based on column value.

License
=======
GNU GPL v3 (http://www.gnu.org/licenses/#GPL)

Installation
============
This project requires:
 - Python 3.3 (will likely work on any Python 3 version)
 - "python-rtmidi" (https://pypi.python.org/pypi/python-rtmidi).
 - PySide

Usage
=====
1. Execute "main.py".
2. If everything works well, you'll get a window with your current MIDI output devices and General MIDI instruments mapped to them that you can then filter and select.  Double-click or press "Enter" in the filtered voice list to move the selected patch(es) to the queue view.  From the queue view, you can press "Enter" to issue the program change event to the underlying device/channel and press "Delete" to remove the voice from the list.