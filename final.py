import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import datetime
import webbrowser
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


##########################################



                                # Commands #

# apna name batany ky liye  "my name is (your name)"                                

# For Time      "Time"

# for asking name     "What is your name"

# for asking my name     "What is my name"

# for search wikipedia      "Search Wikipedia"

# for Search Google         "Search Google"

# for Set Volume        "Set Volume (e.g 90)"

# "How are you"

# for playing any video on yt   "Youtube (any name of video or channel)"

# For open any website             "open(name any website)"






## Voice Configure

# Initialize voice engine
engine = pyttsx3.init()

def configure_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Male voice
    engine.setProperty('rate', 150)  

configure_voice()

def speak(text):
    print(f"JARVIS: {text}")  # Output to terminal
    engine.say(text)
    engine.runAndWait()

### Voice







# Global variables
user_name = ""

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You: {command}")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return ""
        return command.lower()
    





## Set Volume Function to Set Volume Of System

def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume_range = volume.GetVolumeRange()  # Min and max volume levels
    min_volume, max_volume = volume_range[0], volume_range[1]
    new_volume = min_volume + (max_volume - min_volume) * (level / 100)
    volume.SetMasterVolumeLevel(new_volume, None)
    speak(f"Volume set to {level} percent.")








## Basic Commands 

def execute_command(command):
    global user_name

    if 'my name is' in command:
        user_name = command.replace('my name is', '').strip().capitalize()
        speak(f"Hello, {user_name}! Nice to meet you.")

    elif 'what is my name' in command:
        if user_name:
            speak(f"Your name is {user_name}.")
        else:
            speak("I don't know your name yet. Please tell me by saying 'My name is ...'.")

    elif 'what is your name' in command:
        if user_name:
            speak(f"Your name is Jarvis. I am your Assistant.")

    elif 'How are You?' in command:
        if user_name:
            speak(f"I am Fine.Thanks For asking?")        

    elif 'set volume' in command:
        try:
            level = int(command.replace('set volume', '').strip())
            if 0 <= level <= 100:
                set_volume(level)
            else:
                speak("Please specify a valid volume level between 0 and 100.")
        except ValueError:
            speak("Please specify a valid volume level between 0 and 100.")

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}.")

    elif 'search wikipedia' in command:
        query = command.replace('search wikipedia', '').strip()
        speak(f"Searching Wikipedia for {query}...")
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia: {result}")
        except Exception:
            speak("Sorry, no information found.")

    elif 'search google' in command:
        query = command.replace('search google', '').strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}...")

    elif 'open' in command:
        website = command.replace('open', '').strip().lower()
        url = f"{website}" if '.' not in website else website
        webbrowser.open(url)
        speak(f"Opening website: {url}")

    elif 'Youtube' in command:
        query = command.replace("Youtube", "").strip()
        pywhatkit.playonyt(query)
        speak(f"Playing {query} on YouTube.")

    elif 'exit' in command:
        speak("Goodbye! Have a great day.")
        exit()
    else:
        speak("I didn't understand that. Please rephrase.")






## initially Speech

def main():
    speak("Salaam! I am JARVIS, I am your Assistant.")
    while True:
        command = take_command()
        if command:
            execute_command(command)

if __name__ == "__main__":
    main()



