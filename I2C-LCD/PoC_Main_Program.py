# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 16:51:34 2020

@author: Utilisateur
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import csv
import lcddriver
from codecs import open
import time
import requests
import datetime
import smtplib

def weathertom():
    lcd = lcddriver.lcd()
    lcd.lcd_clear()
    d=str(datetime.date.today() + datetime.timedelta(days=-1))

    params = {
  'access_key': 'b4b8c3cd76ddc589b6c3962ba7a45a66',
  'query': 'Paris'
    }
    api_result2 = requests.get('http://api.weatherstack.com/forecast?access_key=b4b8c3cd76ddc589b6c3962ba7a45a66&query=Paris', params)
    api_response2 = api_result2.json()
    mintemptom = int(api_response2['forecast'][d]['mintemp'])
    maxtemptom = int(api_response2['forecast'][d]['maxtemp'])
    if mintemptom <15:
        lcd.lcd_display_string("Tommorow, min temp is ", 1)
        lcd.lcd_display_string(str(mintemptom) + " think to", 2)
        lcd.lcd_display_string("put the heating on", 3)
    if maxtemptom >28:
        lcd.lcd_display_string("Tommorow, max temp is", 1)
        lcd.lcd_display_string(str(maxtemptom) + " think about", 2)
        lcd.lcd_display_string("put the air", 3)
        lcd.lcd_display_string("conditionning on", 4)
    if maxtemptom<28 and mintemptom>15:
        lcd.lcd_display_string("Tommorow's temp", 1)
        lcd.lcd_display_string("don't need", 2)
        lcd.lcd_display_string("heating nor air con", 3)
    time.sleep(5)

def mail():
	gmail_user = 'poctestmail@gmail.com'
	gmail_password = 'Aet356?!8UI'
	sent_from = gmail_user
	to = ['giffardpierrelouis@gmail.com']
	subject = 'Some problems occured in the nursery'
	body = 'Hi you,\n\nSomething has happened in the nursery and needs your attention \nVisit the monitoring page'

	email_text = """\
	From: %s
	To: %s
	Subject: %s

	%s
	""" % (sent_from, ", ".join(to), subject, body)

	try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, to, email_text)
                server.close()

                print ("Email sent!")
	except:
                print ("Something went wrong...")

def display(temp, humidity, resair, sound):
    lcd = lcddriver.lcd()
    lcd.lcd_clear()
    if temp < 24 and temp > 19:
        lcd.lcd_display_string(str(temp)+ " °C ideal temp", 1)
    if temp <18 :
        lcd.lcd_display_string(str(temp) +" °C low temp", 1)
    if temp>24:
        lcd.lcd_display_string(str(temp)+ " °C high temp", 1)
    if humidity <60 and humidity >40:
        lcd.lcd_display_string(str(humidity)+ " correct hum", 2)
    if humidity >60:
        lcd.lcd_display_string(str(humidity)+ " open window", 2)
    if humidity<40:
        lcd.lcd_display_string(str(humidity)+ " low hum", 2)
    resair = abs((160000-resair)/160000)
    if resair > 10:
        lcd.lcd_display_string("Open the windows", 3)
    if resair<10:
        lcd.lcd_display_string("Nice IAQ", 3)
    if sound > 350:
        lcd.lcd_display_string(str(sound)+ " TOO LOUD", 4)
    if sound < 350:
        lcd.lcd_display_string(str(sound)+ " It's calm", 4)
    time.sleep(11)

def writtingcsv(temp,humidity,resair,sound):
    with open('/var/www/html/templated-linear/poc.csv','a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter =',')
        now = datetime.datetime.now()
        dt_string=now.strftime("%Y/%m/%d %H:%M:%S")
        csv_writer.writerow([dt_string,str(temp),str(humidity),str(resair),str(sound)])

if __name__ == '__main__':
    # Create library object using our Bus I2C port
    i = 0
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            temp = float(ser.readline().decode('utf-8').rstrip())
            humidity = float(ser.readline().decode('utf-8').rstrip())
            resair = float(ser.readline().decode('utf-8').rstrip())
            sound = float(ser.readline().decode('utf-8').rstrip())
            writtingcsv(temp,humidity,resair,sound)
            if(i%11==0 or i==0):
                display(temp,humidity,resair,sound)
            if (i%47==0 and i!=0):
                weathertom()
            if(i%10==0 and i!=0 and temp>24):
                mail()
            i = i+1
