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
import tkinter as tk
from tkinter import scrolledtext

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
        log_message("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            log_message("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-US')
            log_message(f"You said: {command}")
        except Exception as e:
            log_message("Sorry, I didn't catch that. Please repeat.")
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

# GUI Functions
def log_message(message):
    output_box.insert(tk.END, message + "\n")
    output_box.see(tk.END)
    if "You said" not in message:  # Speak only non-input messages
        speak(message)

def execute_command(command):
    if 'set volume' in command:
        try:
            level = int(command.replace('set volume', '').strip())
            set_volume(level)
            log_message(f"Volume set to {level} percent.")
        except ValueError:
            log_message("Please specify a valid volume level between 0 and 100.")

    elif 'set brightness' in command:
        try:
            level = int(command.replace('set brightness', '').strip())
            adjust_brightness(level)
            log_message(f"Brightness set to {level} percent.")
        except ValueError:
            log_message("Please specify a valid brightness level between 0 and 100.")

    elif 'shutdown' in command:
        log_message("Shutting down the system.")
        shutdown_system()

    elif 'restart' in command:
        log_message("Restarting the system.")
        restart_system()

    elif 'search wikipedia' in command:
        query = command.replace('search wikipedia', '').strip()
        log_message(f"Searching Wikipedia for {query}")
        try:
            result = wikipedia.summary(query, sentences=2)
            log_message(f"According to Wikipedia: {result}")
        except wikipedia.exceptions.DisambiguationError:
            log_message("The topic is too ambiguous. Try to be more specific.")
        except Exception:
            log_message("Sorry, I couldn't find any information on Wikipedia.")

    elif 'search google' in command:
        query = command.replace('search google', '').strip()
        log_message(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        log_message(f"The current time is {current_time}.")

    elif 'play song' in command:
        query = command.replace('play song', '').strip()
        log_message(f"Playing {query} on YouTube.")
        pywhatkit.playonyt(query)

    elif 'open facebook' in command:
        log_message("Opening Facebook.")
        webbrowser.open("https://www.facebook.com")

    elif 'exit' in command or 'shut down' in command:
        log_message("Goodbye! Have a great day.")
        window.destroy()

    else:
        log_message("I didn't understand that. Can you rephrase?")

def voice_command():
    command = take_command()
    execute_command(command)

def text_command():
    command = command_input.get()
    command_input.delete(0, tk.END)
    log_message(f"You said: {command}")
    execute_command(command)

# Create GUI
window = tk.Tk()
window.title("JARVIS Assistant")
window.geometry("600x400")

# Create widgets
command_label = tk.Label(window, text="Enter Command or Use Voice:")
command_label.pack()

command_input = tk.Entry(window, width=50)
command_input.pack()

text_command_button = tk.Button(window, text="Submit", command=text_command)
text_command_button.pack()

voice_command_button = tk.Button(window, text="Voice Command", command=voice_command)
voice_command_button.pack()

output_label = tk.Label(window, text="JARVIS Output:")
output_label.pack()

output_box = scrolledtext.ScrolledText(window, width=70, height=15)
output_box.pack()

# Run the assistant
log_message("Hello! I am JARVIS, your personal assistant. How can I help you?")
window.mainloop()
