#import library
import speech_recognition as sr 
import playsound  
from gtts import gTTS  
import random
import win32api
import pywhatkit
import datetime
import webbrowser
import os   
import wikipedia
import weathercom
import json
import sys
import pyttsx3

#define function class person
class person:
    name = ''
    #define function name of person 
    def setName(self, name):
        self.name = name

#define function class assistant
class assistant:
    name = ''
    #define function name of person 
    def setName(self, name):
        self.name = name

#define function to list text message on audio speak
def audio_exists(terms):
    for term in terms:
        if term in voice_db:
            return True

#define function to present the weather
def audio_weather(city):
    weather = weathercom.getCityWeatherDetails(city)
    humidity = json.loads(weather)['vt1observation']['humidity']
    temp = json.loads(weather)['vt1observation']['temperature']
    phrase = json.loads(weather)['vt1observation']['phrase']
    return humidity, temp, phrase

#define function engine audio speak
def audio_speak(text):
    txt = str(text)
    engine.say(txt)
    engine.runAndWait()

#generate speech recognition
recognition = sr.Recognizer()

#define function for listen audio to convert text
def audio_record(ask = False):
    with sr.Microphone() as source:
        if ask:
            audio_speak(ask)

        audio_listen = recognition.listen(source, 5, 5)
        print('finding at database')
        voice_db = ''

        try:
            voice_db = recognition.recognize_google(audio_listen)

        except sr.UnknownValueError:
            audio_speak('I am sorry Sir, I did not understand what you said. Can you please repeat again!')
        except sr.RequestError:
            audio_speak('I am sorry Sir, my server is going down')
        print(voice_db)
        return voice_db


#define function for get string of audio file 
def audio_speak(audio_string):
    audio_string = str(audio_string)
    google_text = gTTS(text = audio_string, lang = 'en')
    r = random.randint(1, 2000000)
    file = 'audio' + str(r) + '.mp3'
    google_text.save(file)
    playsound.playsound(file)
    print(assistantObj.name + ':', audio_string)
    os.remove(file)

#generate function class person and assistant
personObj = person()
assistantObj = assistant()
assistantObj.name = 'Ace'
engine = pyttsx3.init()

#define function to response the audio
def audio_response(voice_db):
    if audio_exists(['tell me your name']):
        audio_speak('hello, my name is ace. Can I help you, Sir?')

    if audio_exists(['Ace what time is it']):
        time = datetime.datetime.now().strftime('%I:%M %p')
        audio_speak('Current time is ' + time)

    if audio_exists(['Ace search weather for']):
        city = audio_record('which city')
        humidity, temp, phrase = audio_weather(city)
        audio_speak("currently in " + city + "  temperature is " + str(temp)
                       + " degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)
        print("currently in " + city + "  temperature is " + str(temp)
              + "degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)

    if audio_exists(['Ace play for']):
        song = voice_db.split('for')[-1]
        url = 'http://www.youtube.com/results?search_query=' + song
        pywhatkit.playonyt(url)

    if audio_exists(['Ace who is']):
        person = voice_db.split('for')[-1]
        info = wikipedia.summary(person, 1)
        audio_speak(info)
    
    if audio_exists(['Ace search news for']):
        search = voice_db.split('for')[-1]
        url = 'https://search.kompas.com/search/?q=' + search
        webbrowser.get().open(url)
        audio_speak('Hello Sir, Here is what I found for ' + search + 'on kompas news!')
    
    if audio_exists(['Ace search for']):
        search = voice_db.split('for')[-1]
        url = 'http://www.google.com/search?q=' + search
        webbrowser.get().open(url)
        audio_speak('Hello Sir, Here is what I found for ' + search + 'on google!')
    
    if audio_exists(['thank you']):
        audio_speak('you are welcome Sir. See you later!')
        sys.exit(0)

#define function to record the audio
while (1):
    voice_db = audio_record('Recording')
    print('Succesfully Recorded')
    print('Q:', voice_db)
    audio_response(voice_db)
