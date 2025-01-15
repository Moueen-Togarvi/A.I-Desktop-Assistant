import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import os
import webbrowser
import subprocess

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import pywhatkit
from ai import ask_ai
from open_program import get_program_path
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


# Global variables
user_name = ""

#
# def take_command():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         try:
#             audio = recognizer.listen(source)
#             print("Recognizing...")
#             command = recognizer.recognize_google(audio, language='en-US')
#             print(f"You: {command}")
#         except sr.UnknownValueError:
#             speak("Sorry, I didn't catch that. Please repeat.")
#             return ""
#         return command.lower()


def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()
    for index, mic_name in enumerate(mic_list):
        print(f"Microphone {index}: {mic_name}")


list_microphones()


def take_command():
    recognizer = sr.Recognizer()
    mic_index = 3

    with sr.Microphone(device_index=mic_index) as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You: {command}")
        except sr.UnknownValueError:
            return ""
        return command.lower()


def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume_range = volume.GetVolumeRange()  # Min and max volume levels
        min_volume, max_volume = volume_range[0], volume_range[1]
        new_volume = min_volume + (max_volume - min_volume) * (level / 100)
        volume.SetMasterVolumeLevel(new_volume, None)
        speak(f"Volume set to {level} percent.")
    except Exception as e:
        speak(f"Unable to set volume. Error: {e}")


def execute_command(command):
    global user_name

    if 'my name is' in command:
        user_name = command.replace('my name is', '').strip().capitalize()
        speak(f"Hello, {user_name}! Nice to meet you.")

    elif 'what is my name' in command:
        if user_name:
            speak(f"Your name is{user_name}.")
        else:
            speak(
                "I don't know your name yet. Please tell me by saying 'My name is ...'.")

    elif 'what is your name' in command:
        speak("My name is Jarvis. I am your assistant.")

    elif 'how are you' in command or 'how r u' in command:
        speak("I am fine, thank you. How can I assist you today?")

    elif 'set silent' in command.lower():
        set_volume(0)
        speak("Volume has been set to silent mode.")

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
        try:
            # Remove 'open' from command and clean
            target = command.replace('open', '').strip().lower()
            
            # Check if it's a program
            program_path = get_program_path(target)
            if program_path:
                os.startfile(os.path.expandvars(program_path))
                speak(f"Opening {target}")
            # If not a program, treat as website
            else:
                url = f"https://{target}" if '.' not in target else target
                webbrowser.open(url)
                speak(f"Opening website: {url}")
                
        except FileNotFoundError:
            speak(f"Sorry, I couldn't find {target}")
        except Exception as e:
            speak(f"Error opening {target}: {str(e)}")




    elif 'youtube' in command:
        song = command.replace('youtube', '').strip()
        speak(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)

    elif 'shutdown system' in command:
        speak("Shutting down the system. Goodbye!")
        os.system('shutdown /s /t 1')

    elif 'restart system' in command:
        speak("Restarting the system. Please wait.")
        os.system('shutdown /r /t 1')

    elif 'exit' in command:
        speak("Goodbye! Have a great day.")
        exit()

    else:
        result = ask_ai(command)
        speak(result)


def main():
    speak("Salaam! I am JARVIS, your assistant. How can I help you today?")
    while True:
        command = take_command()
        if command:
            execute_command(command)


if __name__ == "__main__":
    main()


#   About this project   Resources


# python -m venv .venv

# Activate Virtual Env

# pip install -r requirements.txt


#  .venv\Scripts\activate


# Resources: How I Developed the Idea and Created This Project


#       Idea of this Project

#    >>>>>   https://platform.openai.com/docs/assistants/overview


#        Resources

# 1) https://pyttsx3.readthedocs.io/en/latest/    >>  library for output
# 2) https://cloud.google.com/speech-to-text     >> Library for input
# 3) https://pycaw.readthedocs.io/en/latest/     >>
# 4) https://pypi.org/project/wikipedia/         >> for searching wikipedia
# 5) https://pypi.org/project/pywhatkit/         >> forr play yt
# 6)
