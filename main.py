import openai
from apikey import api_data
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import sqlite3
import requests
from bs4 import BeautifulSoup
import psutil

openai.api_key=api_data

completion=openai.Completion()

def Reply(question):
    prompt=f'Parth: {question}\n Jarvis: '
    response=completion.create(prompt=prompt, engine="text-davinci-002", stop=['\Parth'], max_tokens=200)
    answer=response.choices[0].text.strip()
    return answer

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

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

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Fetching weather information")
    search = "temperature in kandivali"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    speak(f"current {search} is {temp}")

    battery = psutil.sensors_battery()
    percent = battery.percent
    speak(f"Sir, your device's battery percentage is {percent} percent.")
    speak("How can I help you today?")


def tellDateTime():
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")
    day = now.strftime("%A")
    time = now.strftime("%I:%M %p")
    month = now.strftime("%B")
    speak("Today is " + date + " and it's " + day)
    speak("The current time is " + time)
    speak("The current month is " + month)

greet()

def google_search():
    speak("What should I search for you, Sir?")
    search_query = Take_query()
    url = f'https://www.google.com.tr/search?q={search_query}'
    webbrowser.open_new_tab(url)
    speak("Here is what I found for " + search_query + " on Google.")

def youtube_search():
    speak("What video should I search?")
    video = Take_query()
    query = video.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.get().open(url)
    speak(f"Playing {video} on YouTube.")

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

while True:
    query=takeCommand().lower()
    if 'time' in query or 'date' in query or 'day' in query or 'month' in query:
        tellDateTime()
    else:
        ans=Reply(query)
        print(ans)
        speak(ans)
        if 'open youtube' in query:
            webbrowser.open("www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("www.google.com")
        elif "open whatsapp" in query:
             subprocess.run(["C:\\Users\\Parth\\AppData\\Local\\WhatsApp\\WhatsApp.exe"])
        elif "open Pycharm" in query:
            subprocess.run(["C:\\Program Files\\ldplayer9box\\New folder\\PyCharm Edu 2022.2.2\\bin\\pycharm64.exe"])
        elif "open word" in query:
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Word 2019.lnk')
        elif "open excel" in query:
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Excel 2019.lnk')
        elif "open powerpoint" in query:
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft PowerPoint 2019.lnk')
        elif "open notepad" in query:
            os.system('notepad')
        elif "open clock" in query:
            os.system('start ms-clock:')
        elif "jarvis shutdown" in query:
            shutdown()
        elif "open calculator" in query:
            os.system('calculator')
        elif "play" in query:
            youtube_search()
        elif "joke" in query:
            tell_joke()
        elif "screenshot" in query:
            speak("Taking Screenshot")
            screenshot = ImageGrab.grab()
            screenshot.save("screenshot.png")
            speak("Screenshot saved")
        elif "search" in query:
            google_search()

        elif 'bye' in query:
            speak("Goodbye!")
            break
