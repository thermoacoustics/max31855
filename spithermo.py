#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spidev
import RPi.GPIO as GPIO
import struct
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

GPIO.cleanup()

board = GPIO.BOARD
cs_list = [11,13,15,29,31,33,36,37]
#cs_pin = 33

GPIO.setmode(board)

def readtemp(cs_pin):
    for cs in cs_list:
        GPIO.setup(cs, GPIO.OUT)
        GPIO.output(cs, GPIO.HIGH)
    
    GPIO.output(cs_pin, GPIO.LOW)
    bytelist = (spi.readbytes(6))
    if bytelist[-2:]!=[0,0]:
        print("error! return longer than 32 bits.")
    else:
        bytelist = bytelist[:4]
    GPIO.output(cs_pin, GPIO.HIGH)
    
    t1b, t2b = struct.unpack('>2h', struct.pack('4B', *bytelist))
    
    fault = bool(t1b & 1)
    fault_short_vcc = bool(t2b & 4)
    fault_short_gnd = bool(t2b & 2)
    fault_open_connection = bool(t2b & 1)
    
    
    if fault_open_connection:
        t1 = None
    else:
        t1 = (t1b & ~3) / 16
    t2 = (t2b & ~7) / 256

    print(f'{cs_pin=} {t1=} {t2=} {fault=} {fault_short_vcc=} {fault_short_gnd=} {fault_open_connection=}')  

for cs in cs_list:
    readtemp(cs)