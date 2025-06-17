# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 19:00:08 2025

@author: Jagta
"""
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

def engine_talk(text):
    engine.say(text)
    engine.runAndWait()

def user_command():
    try:
        with sr.Microphone() as source:
            print("Start Speaking!!")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command

def get_weather(city):
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geocoding_response = requests.get(geocoding_url)

    if geocoding_response.status_code == 200 and geocoding_response.json().get('results'):
        location_data = geocoding_response.json()['results'][0]
        latitude = location_data['latitude']
        longitude = location_data['longitude']
        city_name = location_data['name']
        country = location_data['country']

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        weather_response = requests.get(weather_url)

        if weather_response.status_code == 200:
            weather_data = weather_response.json()['current_weather']
            temperature = weather_data['temperature']
            wind_speed = weather_data['windspeed']
            condition_code = weather_data['weathercode']

            weather_descriptions = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Fog",
                48: "Depositing rime fog",
                51: "Light drizzle",
                53: "Moderate drizzle",
                55: "Dense drizzle",
                61: "Slight rain",
                63: "Moderate rain",
                65: "Heavy rain",
                71: "Slight snow",
                73: "Moderate snow",
                75: "Heavy snow",
                95: "Thunderstorm",
            }

            description = weather_descriptions.get(condition_code, "Unknown condition")
            weather_info = (
                f"Weather in {city_name}, {country}:\n"
                f"Temperature: {temperature}°C\n"
                f"Condition: {description}\n"
                f"Wind Speed: {wind_speed} km/h"
            )
            print(weather_info)
            engine_talk(weather_info)
        else:
            error_message = f"Unable to fetch weather data for '{city}'."
            print(error_message)
            engine_talk(error_message)
    else:
        error_message = f"City '{city}' not found. Please check the spelling."
        print(error_message)
        engine_talk(error_message)

def send_whatsapp_message():
    engine_talk("Please say the phone number with country code.")
    phone_number = user_command()

    if phone_number:
        phone_number = phone_number.replace(" ", "").replace("+", "")
        phone_number = f"+{phone_number}"

        engine_talk("What message would you like to send?")
        message = user_command()

        if message:
            engine_talk(f"Sending message: {message} to {phone_number}")
            print(f"Sending message: {message} to {phone_number}")
            
            pywhatkit.sendwhatmsg(phone_number, message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
            engine_talk("Message sent successfully!")
        else:
            engine_talk("Message was not received. Please try again.")
    else:
        engine_talk("Phone number was not understood. Please try again.")

def run_alexa():
    command = user_command()

    if 'play' in command:
        song = command.replace('play', '')
        print('New command is: ' + song)
        engine_talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        engine_talk('The current time is ' + time)

    elif 'tell me about' in command:
        name = command.replace('tell me about', '')
        info = wikipedia.summary(name, 2)
        print(info)
        engine_talk(info)

    elif 'joke' in command:
        j = pyjokes.get_joke()
        print(j)
        engine_talk(j)

    elif 'weather' in command:
        engine_talk("Please tell me the city name.")
        city = user_command()
        if city:
            get_weather(city)
        else:
            engine_talk("Sorry, I could not hear the city name. Please try again.")

    elif 'message' in command:
        send_whatsapp_message()

    else:
        engine_talk("Sorry, I did not understand the command. Please try again.")

# Run Alexa
run_alexa()


        

