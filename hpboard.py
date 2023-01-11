#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import spidev
import RPi.GPIO as GPIO
import struct

class TCDevice:
    def __init__(self):
        ''' Set init values '''
        # cs_list order from max31855 chip no. U1_1 to U1_8
        self.cs_list = [37,36,33,31,29,15,13,11]

        self.spi = spidev.SpiDev()
        self.spi_bus = 0
        self.spi_device = 0

        self.data = None
        self.board = GPIO.BOARD

        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = 1000000
        
        # Initialise GPIO
        GPIO.setmode(self.board)
        
        # Set all cs pins to output and pull up to inactive
        for cs_pin in self.cs_list:
            GPIO.setup(cs_pin, GPIO.OUT)
            GPIO.output(cs_pin, GPIO.HIGH)
            
    def read(self, channel):
        '''Reads SPI bus and returns current value of thermocouple.'''
        def reader():
            cs_pin = self.cs_list[channel]
            GPIO.output(cs_pin, GPIO.LOW)
            bytelist = self.spi.readbytes(6)
            if bytelist[-2:]!=[0,0]:
                raise Exception("error! return longer than 32 bits.")
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

            # print(f'{cs_pin=} {t1=} {t2=} {fault=} {fault_short_vcc=} {fault_short_gnd=} {fault_open_connection=}')
            return t1
        return reader

    def __end__(self):
        GPIO.cleanup()
    
