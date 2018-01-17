from __future__ import division
import time
import os
import RPi.GPIO as GPIO
import MySQLdb as mysql
import aver


GPIO.setmode(GPIO.BCM)
DEBUG = 1
GPIO.setwarnings(False)


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x01

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout


# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8


# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)


# 10k trim pot connected to adc #0
potentiometer_adc = 0
potentiometer_adc1 = 1


# mysql conf
conn=mysql.connect('localhost', 'root', 'admin','smart')
curs=conn.cursor()
sql = "insert into raw(leftdata, rightdata) values (%s,%s)"


# default
start = False
preLeft = 0
preRight = 0
preDay =0

while True:
    day = time.localtime().tm_mday
	if(preDay!=day):
		aver.day()
		print "use def day_aver"
        preDay=day

    rData = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
    lData = readadc(potentiometer_adc1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # how much has it changed since the last read?

	print "r",rData
	print "l",lData

	if(rData !=0 or lData !=0):

		print "state of measure"
		sum = rData+lData
		print (sum)
		r2 = (rData*100/sum)
		l2 = (lData*100/sum)
		print (round(r2))
		print (round(l2))
		curs.execute(sql,(l2,r2))

		start = True
		preLeft = lData
		preRight = rData

	else:
		if(preLeft==0 and  preRight==0 and start== True):

			aver.term()
			start=False
			print "changed from measure to idle"

		else:
			preLeft=0
			preRight=0
			print "idle state"


        # hang out and do nothing for a half second
        time.sleep(2)
	conn.commit()

conn.close()
