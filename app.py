import os
from twilio.rest import Client
import requests
import time
import random
import schedule

#Twilio authentication
account_sid = '' #Add your account SID here
auth_token = '' #Add your authentication token here
client = Client(account_sid, auth_token)

#Lists of messages
good_morning = ["Good morning, have a wonderful day sweetie", 
    "Morning my love", 
    "Morning sweetheart, go slay your day"]

good_night = ["Good night sweetie, I missed you today", 
    "Good night beautiful", 
    "Nighty night sweetie"]

rain_message = ["Remember to bring an umbrella with you cause it's raining today", 
        "It's raining today honey, bring umbrella if you go out", 
        "Should we meet for a coffee today? Because it's going to be raining"]

snow_message = ["Do you wanna build a snowman?", "It's snowing, look outside!"]

cloud_message = ["It's cloudy, I know you hate it so let's hang out?", "Remember to take your Vitamin D"]


#Check weather with Open Weather Map API: https://rapidapi.com/community/api/open-weather-map/details
def check_weather(): 
    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {"q":"Helsinki,fi","lat":"0","lon":"0","id":"2172797","lang":"null","units":"metric"}

    headers = {
        'x-rapidapi-key': "", #Add your Rapid API key here
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    description = response["weather"][0]["main"]
    #Choosing the messages to send based on the weather, feel free to add more here
    if description == "Rain": 
        send_message(rain_message)
    elif description == "Snow": 
        send_message(snow_message)
    elif description == "Clouds": 
        send_message(cloud_message)

#Send message by choosing one of the phrases in the messages list
def send_message(message_list): 
    message = client.messages.create(
                                from_="whatsapp:", #Sender phone number
                                body=random.choice(message_list),
                                to="whatsapp:" #Receiver phone number
                            )


def main(): 
    #Check weather everyday at 7:00AM
    schedule.every().day.at("07:00").do(check_weather)
    #Then say good morning to them right away
    schedule.every().day.at("07:03").do(send_message, good_morning)
    #Don't forget to tell them good night
    schedule.every().day.at("22:25").do(send_message, good_night)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
