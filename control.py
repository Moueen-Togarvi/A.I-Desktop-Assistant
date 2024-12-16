import pyttsx3
import speech_recognition as sr
import os
import pywhatkit
import wikipedia
import datetime
import webbrowser
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# Initialize voice engine
engine = pyttsx3.init()

# Configure voice settings
def configure_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Use male voice
    engine.setProperty('rate', 150)

configure_voice()

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen to user commands
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {command}")
        except Exception as e:
            print("Sorry, I didn't catch that. Please repeat.")
            return ""
        return command.lower()

# System Control Functions
def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume_range = volume.GetVolumeRange()  # Min and max volume levels
    min_volume, max_volume = volume_range[0], volume_range[1]
    new_volume = min_volume + (max_volume - min_volume) * (level / 100)
    volume.SetMasterVolumeLevel(new_volume, None)

def adjust_brightness(level):
    sbc.set_brightness(level)

def shutdown_system():
    os.system("shutdown /s /t 1")

def restart_system():
    os.system("shutdown /r /t 1")

# Main JARVIS function
def jarvis():
    speak("Hello! I am JARVIS, your personal assistant. How can I help you?")
    while True:
        command = take_command()
        if not command:
            continue

        if 'exit' in command or 'shut down' in command:
            speak("Goodbye! Have a great day.")
            break

        # System Control Commands
        elif 'set volume' in command:
            try:
                level = int(command.replace('set volume', '').strip())
                set_volume(level)
                speak(f"Volume set to {level} percent.")
            except ValueError:
                speak("Please specify a valid volume level between 0 and 100.")

        elif 'set brightness' in command:
            try:
                level = int(command.replace('set brightness', '').strip())
                adjust_brightness(level)
                speak(f"Brightness set to {level} percent.")
            except ValueError:
                speak("Please specify a valid brightness level between 0 and 100.")

        elif 'shutdown' in command:
            speak("Shutting down the system.")
            shutdown_system()

        elif 'restart' in command:
            speak("Restarting the system.")
            restart_system()

        # Other Pre-existing Features
        elif 'search wikipedia' in command:
            query = command.replace('search wikipedia', '').strip()
            speak(f"Searching Wikipedia for {query}")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("The topic is too ambiguous. Try to be more specific.")
            except Exception:
                speak("Sorry, I couldn't find any information on Wikipedia.")

        elif 'search google' in command:
            query = command.replace('search google', '').strip()
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")

        elif 'search file' in command:
            query = command.replace('search file', '').strip()
            speak(f"Searching for files containing {query} in the E drive.")
            results = search_files(query)
            if results:
                speak(f"I found {len(results)} file(s). Opening the first one.")
                os.startfile(results[0])
            else:
                speak("No files found with that name.")

        elif 'play song' in command:
            query = command.replace('play song', '').strip()
            speak(f"Playing {query} on YouTube.")
            pywhatkit.playonyt(query)

        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {current_time}.")

        elif 'open facebook' in command:
            webbrowser.open("https://www.facebook.com")
            speak("Opening Facebook.")

        else:
            speak("I didn't understand that. Can you rephrase?")

# Run the assistant
if __name__ == "__main__":
    jarvis()