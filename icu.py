from __future__ import division
import time
import os
import RPi.GPIO as GPIO
import MySQLdb as mysql
import aver

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)
        GPIO.output(cspin, False)

        commandout = adcnum
        commandout |= 0x18
        commandout <<= 3
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0

        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x01

        GPIO.output(cspin, True)

        adcout >>= 1
        return adcout

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

adc0 = 0
adc1 = 1

# mysql conf
conn=mysql.connect('localhost', 'root', 'admin','smart')
curs=conn.cursor()
sql = "insert into raw(leftdata, rightdata) values (%s,%s)"

# default
start = False
preLeft = 0
preRight = 0
preDay =time.localtime().tm_mday


while True:
	day = time.localtime().tm_mday
	if(preDay!=day):
		aver.day()
		print "use def day_aver"
		preDay=day

	rData = readadc(adc0, SPICLK, SPIMOSI, SPIMISO, SPICS)
	lData = readadc(adc1, SPICLK, SPIMOSI, SPIMISO, SPICS)
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
		if(preLeft==0 and preRight==0 and start== True):

			aver.term()
			start=False
			print "changed from measure to idle"

		else:
			preLeft=0
			preRight=0
            if(start==false):
                print "idle state"
            else:
                print "first 0 data"

        # hang out and do nothing for a half second
        time.sleep(2)
	conn.commit()

conn.close()
