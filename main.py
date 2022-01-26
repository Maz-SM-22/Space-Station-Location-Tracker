import os 
import requests
from datetime import datetime as dt 
import smtplib
import time 

LATITUDE = 41.385063
LONGITUDE = 2.173404
GMAIL_ADDRESS = os.environ['GMAIL_ADDRESS']
PASSWORD = os.environ['GMAIL_PASSWORD']

def check_position(): 
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    iss_data = response.json()['iss_position']
    iss_latitude = float(iss_data['latitude'])
    iss_longitude = float(iss_data['longitude'])
    lat_within_range = bool(iss_latitude > (LATITUDE - 5) and iss_latitude < (LATITUDE + 5))
    long_within_range = bool(iss_longitude > (LONGITUDE - 5) and iss_longitude < (LONGITUDE + 5))
    return lat_within_range and long_within_range

def is_nighttime(): 
    response = requests.get('https://api.sunrise-sunset.org/json', params={
        'lat': LATITUDE, 
        'lng': LONGITUDE, 
        'formatted': 0
    })
    response.raise_for_status()
    data = response.json()
    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']
    sunrise_hour = int(sunrise.split('T')[1].split(':')[0])
    sunset_hour = int(sunset.split('T')[1].split(':')[0])
    current_hour = dt.now().hour
    return current_hour < sunrise_hour or current_hour > sunset_hour

def send_notification(): 
    with smtplib.SMTP('smtp.gmail.com') as connection: 
        connection.starttls()
        connection.login(GMAIL_ADDRESS, PASSWORD)
        connection.sendmail(
            from_addr=GMAIL_ADDRESS, 
            to_addrs='pythontest.mariasmickersgill@yahoo.com', 
            msg='Subject:The International Space Station is overhead \n\nI\'m not joking bitch. Look up!!'
        )

def check_position_and_send_mail(): 
    if check_position() and is_nighttime(): 
        send_notification()

while True: 
    time.sleep(60)
    check_position_and_send_mail()