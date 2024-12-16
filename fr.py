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
from tkinter import Canvas
from math import pi, cos, sin

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
        update_status("Listening...", "blue")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            update_status("Recognizing...", "yellow")
            command = recognizer.recognize_google(audio, language='en-US')
            update_status(f"You said: {command}", "green")
        except Exception as e:
            update_status("Sorry, I didn't catch that. Please repeat.", "red")
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

# Update status in the GUI
def update_status(message, color):
    status_label.config(text=message, fg=color)
    speak(message)

# Execute commands
def execute_command(command):
    if 'set volume' in command:
        try:
            level = int(command.replace('set volume', '').strip())
            set_volume(level)
            update_status(f"Volume set to {level} percent.", "green")
        except ValueError:
            update_status("Please specify a valid volume level between 0 and 100.", "red")

    elif 'set brightness' in command:
        try:
            level = int(command.replace('set brightness', '').strip())
            adjust_brightness(level)
            update_status(f"Brightness set to {level} percent.", "green")
        except ValueError:
            update_status("Please specify a valid brightness level between 0 and 100.", "red")

    elif 'shutdown' in command:
        update_status("Shutting down the system.", "red")
        shutdown_system()

    elif 'restart' in command:
        update_status("Restarting the system.", "red")
        restart_system()

    elif 'search wikipedia' in command:
        query = command.replace('search wikipedia', '').strip()
        update_status(f"Searching Wikipedia for {query}", "blue")
        try:
            result = wikipedia.summary(query, sentences=2)
            update_status(f"According to Wikipedia: {result}", "green")
        except wikipedia.exceptions.DisambiguationError:
            update_status("The topic is too ambiguous. Try to be more specific.", "red")
        except Exception:
            update_status("Sorry, I couldn't find any information on Wikipedia.", "red")

    elif 'search google' in command:
        query = command.replace('search google', '').strip()
        update_status(f"Searching Google for {query}", "blue")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        update_status(f"The current time is {current_time}.", "blue")

    elif 'play song' in command:
        query = command.replace('play song', '').strip()
        update_status(f"Playing {query} on YouTube.", "blue")
        pywhatkit.playonyt(query)

    elif 'open facebook' in command:
        update_status("Opening Facebook.", "blue")
        webbrowser.open("https://www.facebook.com")

    elif 'exit' in command or 'shut down' in command:
        update_status("Goodbye! Have a great day.", "green")
        window.destroy()

    else:
        update_status("I didn't understand that. Can you rephrase?", "red")

# Continuous voice listening
def continuous_listening():
    command = take_command()
    if command:
        execute_command(command)
    window.after(1000, continuous_listening)

# Create GUI
window = tk.Tk()
window.title("JARVIS Assistant")
window.geometry("800x600")
window.configure(bg="#101010")

# Main heading
heading_label = tk.Label(window, text="Moueen Togarvi", font=("Helvetica", 30, "bold"), fg="cyan", bg="#101010")
heading_label.pack(pady=10)

# Circular Canvas Design
canvas = Canvas(window, width=400, height=400, bg="#101010", highlightthickness=0)
canvas.pack(pady=10)
circle = canvas.create_oval(50, 50, 350, 350, outline="cyan", width=3)

# Add dynamic text to the canvas
status_label = tk.Label(window, text="Initializing...", font=("Helvetica", 18), fg="white", bg="#101010")
status_label.pack(pady=20)

# Animation for the circular canvas
for i in range(0, 360, 30):
    x = 200 + 150 * cos(i * pi / 180)
    y = 200 + 150 * sin(i * pi / 180)
    canvas.create_text(x, y, text="•", font=("Helvetica", 12), fill="cyan")

# Start the assistant
update_status("Hello! I am JARVIS, your personal assistant. How can I help you?", "green")
window.after(1000, continuous_listening)

window.mainloop()
