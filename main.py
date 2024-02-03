import max7219
import time
import network
import sys
import ubinascii
from umqtt.simple import MQTTClient
from machine import Pin, SPI
import machine


spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(4), mosi=Pin(2))
ss = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 4)

def char(off_x, off_y, c):
    global display
    if c == "0":
        display.rect(off_x,off_y,3,3,1)
    elif c == "1":
        display.pixel(off_x,off_y,1)
        display.vline(off_x+1, off_y, 2, 1)
        display.hline(off_x, off_y+2, 3, 1)
    elif c == "2":
        display.pixel(off_x,off_y,1)
        display.vline(off_x+1, off_y, 3, 1)
        display.pixel(off_x+2, off_y+2, 1)
    elif c == "3":
        display.pixel(off_x,off_y, 1)
        display.pixel(off_x,off_y+2, 1)
        display.rect(off_x+1,off_y,2,3,1)
    elif c == "4":
        display.pixel(off_x+1,off_y+1, 1)
        display.vline(off_x+2,off_y,3,1)
        display.vline(off_x,off_y,2,1)
    elif c == "5":
        display.pixel(off_x+2,off_y, 1)
        display.vline(off_x+1,off_y,3,1)
        display.pixel(off_x,off_y+2, 1)
    elif c == "6":
        display.rect(off_x,off_y+1,3,2,1)
        display.pixel(off_x, off_y, 1)
    elif c == "7":
        display.hline(off_x,off_y,2,1)
        display.vline(off_x+2, off_y, 3, 1)
    elif c == "8":
        display.rect(off_x,off_y+1,3,2,1)
        display.hline(off_x+1,off_y,2,1)
    elif c == "9":
        display.fill_rect(off_x, off_y, 2, 2, 1)
        display.hline(off_x, 2 + off_y, 2, 0)
    elif c == ">":
        display.pixel(0+off_x,0+off_y,1)
        display.pixel(1+off_x,1+off_y,1)
        display.pixel(0+off_x,2+off_y,1)
    elif c == "...":
        display.pixel(0+off_x,1+off_y,1)
        display.pixel(2+off_x,1+off_y,1)
        display.pixel(4+off_x,1+off_y,1)
    elif c == "'":
        display.vline(0+off_x,0+off_y,2,1)
    elif c == "A":
        display.pixel(off_x+1,off_y,1)
        display.hline(off_x,1+off_y,3,1)
        display.pixel(off_x,2+off_y,1)
        display.pixel(2+off_x,2+off_y,1)
    elif c == "C":
        display.rect(off_x, off_y, 3, 3, 1)
        display.pixel(2 + off_x, 1 + off_y, 0)
    elif c == "D":
        display.rect(off_x, off_y, 3, 3, 1)
        display.pixel(2 + off_x, off_y, 0)
        display.pixel(2 + off_x, 2 + off_y, 0)
    elif c == "R":
        display.fill_rect(off_x, off_y, 3, 3, 1)
        display.pixel(2 + off_x, off_y, 0)
        display.pixel(1 + off_x, 2 + off_y, 0)
    elif c == "X":
        display.line(off_x, off_y, 2, 2, 1)
        display.line(2 + off_x, off_y, off_x, 2 + off_y, 1)
    elif c == ".":
        display.pixel(off_x, 2 + off_y, 1)
    display.show()

def sub_cb(topic, msg):
    global display
    display.fill(0)
    display.text(msg, 0, 0, 1)
    display.show()
    print((topic, msg))


#display.hline(0,4,10,1)

timeout = 0

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

networks = wifi.scan()

print(wifi.ifconfig())

wifi.connect('','')

if not wifi.isconnected():
    print('connecting..')
    while (not wifi.isconnected() and timeout < 5):
        print(5 - timeout)
        timeout = timeout + 1
        time.sleep(1)

MQTT_BROKER = "192.168.1.27"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"orari_atm"
mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER)
mqttClient.set_callback(sub_cb)

if(wifi.isconnected()):
    print('WIFI Connected')
    char(0,0, ">")
    mqttClient.connect()
    mqttClient.subscribe(TOPIC)
    while True:
        mqttClient.wait_msg()
        time.sleep(1)
        #mqttClient.disconnect()
