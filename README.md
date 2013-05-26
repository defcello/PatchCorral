SynthServer
===========
Earlier this year (2013), I participated in a production of "Children of Eden" which required 3 keyboardists and a vast array of instruments, often exotic, for them to switch around on.  Using some electronic pianos, a laptop, a wireless router, and a Roland Fantom XR, I wrote a Python program that would pipe the keyboards' MIDI events into different input channels of the Roland Fantom XR and would host a web server for the keyboardists to use the browser of a WiFi touchscreen device (e.g. tablet, smart phone, etc.) to select the instrument they wanted to play.  My next musical "Shrek the Musical" looks to have a similar situation.  Therefore, I'm opening this project to the public since others may be able to use it and/or contribute.

Currently, the software is strongly catered to "Children of Eden" and my own synthesis equipment.  The design of the program will likely improve, making it easier to swap out shows and expanding its synthesizer support.

License
=======
GNU GPL v3 (http://www.gnu.org/licenses/#GPL)

Installation
============
This project requires:
 - Python 3.3 (will likely work on any Python 3 version)
 - "pyrtmidi" (http://trac.assembla.com/pkaudio/wiki/pyrtmidi) installed as a library for Python 3.3.  Note that the current public version of pkaudio supports Python 2.  I have adapted it to Python 3 and am attempting to contact the author to get his input on how this new code should be shared.

Usage
=====
1. Execute "main.py".
2. If everything works well, you'll get the showtime message and a message giving the IP that the HTTP server is listening on.
3. Point your web browser to the IP address.  The welcome page will list the available parts.  Selecting a part will display each song and the instruments available for that song.