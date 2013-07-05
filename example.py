from src.engine import synthnav
s = synthnav.SynthNav()
s.newVoiceList('v.device.portName == "FANTOM-X" and v.channel == 1')
print(s.currVoiceList[0])

s.selectVoice(0)
