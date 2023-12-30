import urequests as requests
import json
import network
def connect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(False)
  wlan.active(True)
  if not wlan.isconnected():
      print('connecting to network...')
      #wlan.connect('B510_Wifi', 'mjchen0821')
      #wlan.ifconfig(('192.168.0.125', '255.255.255.0', '192.168.0.1', '192.168.0.1'))
      wlan.connect('墜神   漆夜','00000000')
      while not wlan.isconnected():
          pass
  print('network config: ', wlan.ifconfig())

#connect()

data = {"Pressure": "10.11", "Temperatures": "25.452", "ORP": "811.9"}
web = requests.post('http://192.168.25.182:500/value',headers = {'content-type': 'application/json'}, data=json.dumps(data))
#r = requests.post(url, headers = {'content-type': 'image/jpeg'}, data = frame)
print(web.text)	