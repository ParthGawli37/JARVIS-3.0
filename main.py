import datetime
import random
import sqlite3
import time
import webbrowser
import subprocess
import psutil
import pyttsx3
import requests
from bs4 import BeautifulSoup
import speech_recognition as sr
import winsound
import wikipedia
import openai
from apikey import api_data

openai.api_key=api_data

completion=openai.Completion()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


conn = sqlite3.connect('voice_input.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS voice_input
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             input TEXT NOT NULL,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

def Reply(question):
    prompt=f'Parth: {question}\n Jarvis: '
    response=completion.create(prompt=prompt, engine="text-davinci-002", stop=['\Parth'], max_tokens=124)
    answer=response.choices[0].text.strip()
    return answer

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

speak("Hello How Are You? ")

def time_():
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    speak("The current time is")
    speak(Time)

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


def date_():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)


def wishme():
    speak("Activating mini project  Jarvis")
    speak("Please wait")
    speak("Welcome back Sir!")
    time_()
    date_()
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")
    elif 18 <= hour < 24:
        speak("Good Evening Sir!")
    else:
        speak("Good Night Sir!")

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

    speak("Jarvis at your service. Please tell me how can I help you?")

def set_alarm():
    alarm_time_str = input("Enter the time in 'HH:MM:SS AM/PM' format: ")
    speak("Enter the time in 'HH:MM:SS AM/PM' format: ")
    try:
        datetime.datetime.strptime(alarm_time_str, '%I:%M:%S %p')
    except ValueError:
        print("Invalid time format! Please enter time in 'HH:MM:SS AM/PM' format.")
        speak("Invalid time format! Please enter time in 'HH:MM:SS AM/PM' format.")
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


def google_search():
    speak("What should I search for you, Sir?")
    search_query = Take_query()
    url = f'https://www.google.com.tr/search?q={search_query}'
    webbrowser.open_new_tab(url)
    speak("Here is what I found for " + search_query + " on Google.")

def youtube_search():
    speak("What song should I search?")
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


def open_whatsapp():
    subprocess.run(["C:\\Users\\Parth\\AppData\\Local\\WhatsApp\\WhatsApp.exe"])


def open_pycharm():
    subprocess.run(["C:\\Program Files\\ldplayer9box\\New folder\\PyCharm Edu 2022.2.2\\bin\\pycharm64.exe"])


def open_gta5():
    subprocess.run(["C:\\Users\\Parth\\Desktop\\project\\Grand Theft Auto V.url"])


def open_steam():
    subprocess.run(["C:\\Users\\Public\\Desktop\\Steam.lnk"])


def open_epic_games():
    subprocess.run(["C:\\Users\\Parth\\Desktop\\Epic Games Launcher.lnk"])


def open_ms_word():
    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Word 2019.lnk')


def open_ms_excel():
    os.startfile(
        'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Excel 2019.lnk')


def open_ms_powerpoint():
    os.startfile(
        'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft PowerPoint 2019.lnk')


def open_settings():
    os.system('start ms-settings:')


def open_notepad():
    os.system('notepad')


def open_calculator():
    os.system('calculator')


def open_clock():
    os.system('start ms-clock:')


def open_app():
    speak("Which app would you like me to open?")
    app = Take_query()

    try:
        subprocess.Popen(app)
        speak(f"Opening {app}")

    except:
        speak(f"Sorry, I couldn't open {app}")


def take_screenshot():
    speak("Taking Screenshot")
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    speak("Screenshot saved")

def shutdown():
    os.system("shutdown /s /t 1")

def send_whatsapp_message(name):

    contacts = {'pappa': '+919930008990', 'mummy': '+918779761584', 'ayush': '+917718068314', 'om': '9224477282'}
    if name.lower() in contacts:
        phone_number = contacts[name.lower()]

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("What do you want to say?")
            audio = recognizer.listen(source)
            message = recognizer.recognize_google(audio)

        print(f"Sending message '{message}' to {name}")

        pywhatkit.sendwhatmsg(phone_number, message, int(time.strftime("%H")), int(time.strftime("%M")) + 1, wait_time=20)
    else:
        print(f"Sorry, I don't have a contact named {name}.")


if __name__ == '__main__':
    while True:
        query=takeCommand().lower()
        ans=Reply(query)
        print(ans)
        speak(ans)
        if 'open youtube' in query:
            webbrowser.open("www.youtube.com")
        if 'open google' in query:
            webbrowser.open("www.google.com")

        elif "open whatsapp" in query:
            open_whatsapp()

        elif "open code" in query:
            open_pycharm()

        elif "send message" in query:
            send_whatsapp_message(name)

        elif "open gta" in query:
            open_gta5()

        elif "open steam" in query:
            open_steam()

        elif "open epic games" in query:
            open_epic_games()

        elif "open word" in query:
            open_ms_word()

        elif "open excel" in query:
            open_ms_excel()

        elif "open powerpoint" in query:
            open_ms_powerpoint()

        elif "open notepad" in query:
            open_notepad()

        elif "open clock" in query:
            open_clock()

        elif "jarvis shutdown" in query:
            shutdown()

        elif "open calculator" in query:
            open_calculator()

        elif "open settings" in query:
            open_settings()

        elif "search" in query:
            youtube_search()

        elif "time" in query:
            time_()

        elif "history" in query:
            show_history()

        elif "alarm" in query:
            set_alarm()

        elif "joke" in query:
            tell_joke()

        elif "date" in query:
            date_()

        elif "screenshot" in query:
            take_screenshot()

        elif "google" in query:
            google_search()

        elif "bye" in query:
            speak("Goodbye Sir, Jarvis signing off")

            exit()
        else:
            speak("I didn't understand what you said. Can you please repeat?")
