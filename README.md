SynthServer
===========
Earlier this year (2013), I participated in a production of "Children of Eden" which required 3 keyboardists and a vast array of instruments, often exotic, for them to switch around on.  Using some electronic pianos, a laptop, and a Roland Fantom XR, I wrote a Python program that would pipe the keyboards' MIDI events into different input channels of the Roland Fantom XR and would host a web server for the keyboardists to use the browser of a WiFi touchscreen device (e.g. tablet, smart phone, etc.) to select the instrument they wanted to play.  My next musical "Shrek the Musical" looks to have a similar situation.  Therefore, I'm opening this project to the public since others may be able to use it and/or contribute.

Installation
============
This project requires:
 - Python 2.7
 - "pyrtmidi" (http://trac.assembla.com/pkaudio/wiki/pyrtmidi)
 
Usage
=====
1. Execute "main.py".
2. If everything works well, you'll get the showtime message and a message giving the IP that the HTTP server is listening on.
3. Point your web browser to the IP address.  The welcome page will list the available parts.  Selecting a part will display each song and the instruments available for that song.