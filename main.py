from machine import Pin,I2C,ADC
from bmp280 import *
import time
import machine
import onewire, ds18x20
import urequests as requests

from machine import reset
import network
import json

def avergearray (arr , number) :
    if(number<=0) :
        print("Error number for the array to avraging!\n")
        return 0
    amount = 0
    if(number<5) :
        for i in range(0,number) :
            amount+=arr[i]
        avg = amount/number
        return avg
    else :
        if(arr[0]<arr[1]) :
            min = arr[0]
            max = arr[1]
        else :
            min = arr[1]
            max = arr[0]
        for i in range(2,number) :
            if(arr[i]<min) :
                amount = amount + min
                min = arr[i]
            else :
                if(arr[i]>max) :
                    amount = amount + max
                    max = arr[i]
                else :
                    amount = amount + arr[i]
        avg = amount/(number-2) 
    return avg

sdaPIN=machine.Pin(21)  #右6
sclPIN=machine.Pin(22)  #右3   #3.3V左1 GND右7
bus = I2C(0,sda=sdaPIN, scl=sclPIN, freq=100000)
bmp = BMP280(bus)
bmp.use_case(BMP280_CASE_INDOOR)

VOLTAGE = 5.0
OFFSET = 0.0
ArrayLenth = 40 
orpArray = [0.0 for i in range(ArrayLenth)]
orpArrayIndex = 0
orpTimer = time.ticks_ms()
printTime = time.ticks_ms()


# the device is on GPIO12 #5V外接 GND右1
dat = machine.Pin(14)  #左15
# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))
# scan for devices on the bus
roms = ds.scan()
#print('found devices:', roms)
tmp=0.0

def connect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(False)
  wlan.active(True)
  if not wlan.isconnected():
      print('connecting to network...')
      wlan.connect('B510_Wifi', 'mjchen0821')
      #wlan.ifconfig(('192.168.0.125', '255.255.255.0', '192.168.0.1', '192.168.0.1'))
      #wlan.connect('墜神   漆夜','00000000')
      while not wlan.isconnected():
          pass
  print('network config: ', wlan.ifconfig())

connect()


while True :
    pressure=bmp.pressure
    p_bar=pressure/100000
    p_mmHg=pressure/133.3224
    #temperature=bmp.temperature
    
    ds.convert_temp()
    time.sleep_ms(750)
    
    
    if(time.ticks_ms() >= orpTimer) :
        orpTimer=time.ticks_ms()+20
        adc = ADC(Pin(32))  #左7
        adc.atten(ADC.ATTN_11DB)
        adc.width(ADC.WIDTH_9BIT)
        orppin = adc.read()
        #orppin = machine.pin(13)
        #print("Analog Reading: ", orppin)
        orpArray[orpArrayIndex]=orppin
        orpArrayIndex+=1
        if (orpArrayIndex==ArrayLenth) :
            orpArrayIndex=0
        orpValue=((30.0*VOLTAGE*1000)-(75.0*avergearray(orpArray, ArrayLenth)*VOLTAGE*1000/1024.0))/75.0 #-OFFSET
        #averge = avergearray(orpArray, ArrayLenth)
        #orpValue=((30*VOLTAGE*1000)-(75*averge*VOLTAGE*1000/1024))/75 #-OFFSET
        #print(averge)
    if(time.ticks_ms() >= printTime) :
        printTime=time.ticks_ms()+800
        print("Pressure: {} Pa, {} bar, {} mmHg".format(pressure,p_bar,p_mmHg))
        print('temperatures:', end=' ')
        tmp=0
        for rom in roms:
            print(ds.read_temp(rom), end=' ')
            tmp = ds.read_temp(rom)
        print("ORP: " , orpValue , " mV")
        data = {'Pressure': str(pressure) ,
                'Temperature': str(tmp) ,
                'ORP' : str(orpValue)}
        web = requests.post('http://192.168.0.118:500/value',
            headers = {'content-type': 'application/json'},
            data=json.dumps(data))
        #web = requests.post('http://192.168.25.182:500/value',
            #headers = {'content-type': 'application/json'},
            #data=json.dumps(data))   # 發送 POST 請求
        print(web.text)
        time.sleep(5)