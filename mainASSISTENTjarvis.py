import openai
from api_key import api_data
import pyttsx3
import speech_recognition as sr
import webbrowser
import sqlite3
import random
import requests
from PIL import ImageGrab
import subprocess
import psutil
import winsound
import datetime
import pywhatkit
import os
import ctypes
import cv2
from api_key import api_key_news
from contact import whatsapp


openai.api_key=api_data

completion=openai.Completion()

def Reply(question):
    prompt=f'Parth: {question}\n Jarvis: '
    if 'thank you' in question:
        return "You're welcome."
    response=completion.create(prompt=prompt, engine="text-davinci-002", stop=['\Parth'], max_tokens=124)
    answer=response.choices[0].text.strip()
    return answer

def searchOnGoogle(query):
    query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def searchOnYoutube():
    speak("What video should I search?")
    video = takeCommand()
    query = video.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.get().open(url)
    speak(f"Playing {video} on YouTube.")

def PlayOnYoutube():
    speak("What video should I search?")
    video = takeCommand()
    query = video.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.get().open(url)
    speak(f"Searching for {video} on YouTube.")
    video_results = pafy.search(query)
    first_video = video_results[0]
    best_stream = first_video.getbest()
    media_player = vlc.MediaPlayer(best_stream.url)
    media_player.play()
    speak(f"Now playing {first_video.title} on YouTube.")

def send_whatsapp_message():
    speak("Whom should I send this message?")
    name = takeCommand().lower()
    speak("What message should I send?")
    message = takeCommand()
    hour = datetime.datetime.now().strftime('%I')
    minute = datetime.datetime.now().strftime('%M')
    try:
        pywhatkit.sendwhatmsg(f'+91{whatsapp[name]}', message, int(hour), int(minute)+1)
        speak("Message sent successfully")
    except Exception as e:
        print(e)
        speak("Unable to send message")


def set_alarm():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please speak the time in 'HH:MM:SS AM/PM' format.")
        audio = r.listen(source)

    try:
        alarm_time_str = r.recognize_google(audio)
        datetime.datetime.strptime(alarm_time_str, '%I:%M:%S %p')
    except (ValueError, sr.UnknownValueError, sr.RequestError):
        print("Invalid time format! Please speak the time in 'HH:MM:SS AM/PM' format.")
        speak("Invalid time format! Please speak the time in 'HH:MM:SS AM/PM' format.")
        return

    current_time = datetime.datetime.now().strftime('%I:%M:%S %p')
    print(f"Current time is {current_time}.")
    speak(f"Current time is {current_time}.")
    while True:
        time.sleep(1)
        current_time = datetime.datetime.now().strftime('%I:%M:%S %p')
        if current_time == alarm_time_str:
            speak("Time's up!")
            print("Time's up!")
            for i in range(3):
                winsound.Beep(1000, 1000)
            break

def tell_joke():
    jokes = [
        "Why did the tomato turn red? Because it saw the salad dressing!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why did the cookie go to the doctor? Because it was feeling crummy!",
        "Why did the teddy bear say no to dessert? Because it was already stuffed!",
        "Why did the chicken cross the playground? To get to the other slide!"
    ]
    joke = random.choice(jokes)
    speak(joke)

def get_news(api_key_news):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key_news}"
    response = requests.get(url)
    articles = response.json()["articles"]

    for article in articles:
        print(article["title"])
        print(article["description"])
        print(article["url"])
        print()


def take_screenshot():
    speak("Taking Screenshot")
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    speak("Screenshot saved")

def take_selfie():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    cv2.imwrite('selfie.jpg', frame)
    print('Selfie taken and saved as selfie.jpg')
    speak('Selfie taken and saved as selfie.jpg')


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How can I assist you?")

def introduce():
    speak("My name is Jarvis. I am an AI virtual assistant created by Parth , Ayush , Om , Amey . I can help you with a variety of tasks including searching the web, playing music, setting alarms, taking notes, and much more.")

def thank():
    speak("Thank you for creating me. It's a pleasure to serve you!")


conn = sqlite3.connect('voice_input.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS voice_input 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             input TEXT NOT NULL,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print("Parth Said: {} \n".format(query))
        c.execute("INSERT INTO voice_input (input) VALUES (?)", (query,))
        conn.commit()

    except Exception as e:
        print("Say That Again....")
        return "None"
    return query

if __name__ == '__main__':
    greet()
    while True:
        query=takeCommand().lower()
        ans=Reply(query)
        print(ans)
        speak(ans)
        if 'open youtube' in query:
            webbrowser.open("www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("www.google.com")
        elif 'google search' in query:
            query = query.replace("search", "")
            searchOnGoogle(query)
        elif 'youtube search' in query:
            query = query.replace("search youtube", "")
            searchOnYoutube()
        elif "open whatsapp" in query:
            subprocess.run(["C:\\Users\\Parth\\AppData\\Local\\WhatsApp\\WhatsApp.exe"])
        elif "open code" in query:
            subprocess.run(["C:\\Program Files\\ldplayer9box\\New folder\\PyCharm Edu 2022.2.2\\bin\\pycharm64.exe"])
        elif "open word" in query:
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Word 2019.lnk')
        elif "open excel" in query:
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Excel 2019.lnk')
        elif "open powerpoint" in query:
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft PowerPoint 2019.lnk')
        elif "open notepad" in query:
            os.system('start notepad.exe')
        elif "open clock" in query:
            os.system('start ms-clock:')
        elif "open calculator" in query:
            os.system('calculator')
        elif "open settings" in query:
            open_settings()
        elif "introduce your self" in query:
            introduce()
        elif "set alarm" in query:
            set_alarm()
        elif "news" in query:
            get_news(api_key_news)
        elif "tell me a joke" in query:
            tell_joke()
        elif "take a screenshot" in query:
            take_screenshot()
        elif "take selfie" in query:
            take_selfie()
        elif "shutdown" in query:
            os.system('shutdown /s /t 1')
        elif "restart" in query:
            os.system("shutdown /r /t 1")
        elif "cpu usage" in query:
            usage = str(psutil.cpu_percent())
            speak('CPU usage is at ' + usage)
        elif "battery status" in query:
            battery = psutil.sensors_battery()
            speak("Battery is at ")
            speak(battery.percent)
        elif "send message" in query.lower():
            send_whatsapp_message()
        elif "bye" in query:
            goodbye_messages =[
                                "Goodbye! Thanks for chatting with me.",
                                "Take care and have a great day!",
                                "Bye for now! It was great talking with you.",
                                "Thanks for stopping by! Have a wonderful day.",
                                "See you later! It was nice to chat with you.",
                               ]
            goodbye = random.choice(goodbye_messages)
            speak(goodbye)
            exit()
        else:
            pass
