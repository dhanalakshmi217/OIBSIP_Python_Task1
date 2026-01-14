import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import requests
import smtplib
import spacy
from dateutil import parser
import time

# NLP model
nlp = spacy.load("en_core_web_sm")

# Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print("You:", query)
        return query.lower()
    except:
        speak("Sorry, please repeat")
        return ""

def general_knowledge(question):
    speak("Searching for the answer")
    result = wikipedia.summary(question, sentences=3)
    speak(result)


def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning")
    elif hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am your advanced voice assistant. How can I help you?")

# ---------------- FEATURES ---------------- #

def get_time():
    time_now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time_now}")

def get_date():
    date_now = datetime.datetime.now().strftime("%d %B %Y")
    speak(f"Today's date is {date_now}")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("Sorry, I could not find information")

def google_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak("Here are the search results")

def get_weather(city):
    api_key = "123456789"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    data = requests.get(url).json()
    if data["cod"] != 200:
        speak("City not found")
    else:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degree celsius with {desc}")

def get_news():
    api_key = "sdftyuio09876"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"

    data = requests.get(url).json()
    for article in data["articles"][:3]:
        speak(article["title"])


def send_email():
    speak("Tell the receiver email")
    receiver = input("Enter receiver email")
    speak("Tell the message")
    message = take_command()

    sender = "dhanunatarajan5@gmail.com"
    password = "lhok fzsc bzut jfyb"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
        server.quit()
        speak("Email sent successfully")
    except:
        speak("Failed to send email")

def set_reminder():
    try:
        speak("Tell the reminder time")
        time_text = take_command()

        reminder_time = parser.parse(time_text, fuzzy=True)

        speak(f"Reminder set for {reminder_time.strftime('%I:%M %p on %d %B')}")

        while True:
            if datetime.datetime.now() >= reminder_time:
                speak("Reminder alert!")
                break
            time.sleep(10)

    except Exception as e:
        print(e)
        speak("Sorry, I could not set the reminder")


# ---------------- MAIN ---------------- #

wish_user()

while True:
    command = take_command()

    if "time" in command:
        get_time()

    elif "date" in command:
        get_date()

    elif "who is" in command or "what is" in command or "why" in command:
        general_knowledge(command)

    elif "wikipedia" in command:
        search_wikipedia(command.replace("wikipedia", ""))

    elif "search" in command:
        google_search(command.replace("search", ""))

    elif "weather" in command:
        speak("Tell the city name")
        city = take_command()
        print("CITY:",city)
        get_weather(city)



    elif "send email" in command or "send mail" in command:
        send_email()

    elif "remind me" in command or "set reminder" in command:
        set_reminder()

    elif "exit" in command and "stop" or "bye" in command:
        speak("Thank you. Goodbye!")
        break

    else:
        speak("Sorry, I cannot perform that task yet")
