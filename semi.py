import pyttsx3
import speech_recognition as sr
import os
import subprocess
import pywhatkit
import wikipedia
import datetime
import webbrowser
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import tkinter as tk
from tkinter import Text, Scrollbar, Canvas
from math import pi, cos, sin
from threading import Thread

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

# Global variables
user_name = ""

# Log and update the terminal
def update_terminal(message):
    terminal_area.config(state=tk.NORMAL)
    terminal_area.insert(tk.END, f"{message}\n")
    terminal_area.see(tk.END)
    terminal_area.config(state=tk.DISABLED)
    speak(message)

# Execute Bash Command
def execute_bash_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
        update_terminal(f"Output:\n{output}")
    except Exception as e:
        update_terminal(f"Error executing command: {e}")

# Volume Control
def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume_range = volume.GetVolumeRange()  # Min and max volume levels
    min_volume, max_volume = volume_range[0], volume_range[1]
    if level == 0:
        volume.SetMute(1, None)  # Mute volume
        update_terminal("Volume muted.")
    else:
        volume.SetMute(0, None)  # Unmute volume
        new_volume = min_volume + (max_volume - min_volume) * (level / 100)
        volume.SetMasterVolumeLevel(new_volume, None)
        update_terminal(f"Volume set to {level}%.")

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
            update_terminal(f"You said: {command}")
        except sr.UnknownValueError:
            update_terminal("Sorry, I didn't catch that. Please repeat.")
            return ""
        except sr.RequestError:
            update_terminal("Network error. Please check your internet connection.")
            return ""
        return command.lower()

# Update status in the GUI
def update_status(message, color):
    status_label.config(text=message, fg=color)

# Handle voice commands
def execute_command(command):
    global user_name

    if 'my name is' in command:
        user_name = command.replace('my name is', '').strip().capitalize()
        update_terminal(f"Hello, {user_name}! Nice to meet you.")
    elif 'what is my name' in command:
        if user_name:
            update_terminal(f"Your name is {user_name}.")
        else:
            update_terminal("I don't know your name yet. Please tell me by saying 'My name is ...'.")
    elif 'open file' in command:
        speak("Which file should I open?")
        file_name = take_command()
        if file_name and os.path.exists(file_name):
            os.startfile(file_name)
            update_terminal(f"Opening file: {file_name}")
        else:
            update_terminal(f"File not found: {file_name}")
    elif 'open folder' in command:
        speak("Which folder should I open?")
        folder_name = take_command()
        if folder_name and os.path.exists(folder_name):
            os.startfile(folder_name)
            update_terminal(f"Opening folder: {folder_name}")
        else:
            update_terminal(f"Folder not found: {folder_name}")
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        update_terminal(f"The current time is {current_time}.")
    elif 'search wikipedia' in command:
        query = command.replace('search wikipedia', '').strip()
        update_terminal(f"Searching Wikipedia for {query}...")
        try:
            result = wikipedia.summary(query, sentences=2)
            update_terminal(f"According to Wikipedia: {result}")
        except Exception as e:
            update_terminal("Sorry, no information found.")
    elif 'search google' in command:
        query = command.replace('search google', '').strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        update_terminal(f"Searching Google for {query}...")
    elif 'open' in command:
        website = command.replace('open', '').strip().lower()
        url = f"https://{website}.com" if '.' not in website else website
        webbrowser.open(url)
        update_terminal(f"Opening website: {url}")
    elif 'set volume' in command:
        try:
            level = int(command.replace('set volume', '').strip())
            set_volume(level)
        except ValueError:
            update_terminal("Please specify a valid volume level between 0 and 100.")
    elif 'mute volume' in command or 'mute' in command:
        set_volume(0)
    elif 'exit' in command:
        update_terminal("Goodbye! Have a great day.")
        window.quit()
    else:
        update_terminal("I didn't understand that. Please rephrase.")

# Continuous listening in a separate thread
def continuous_listening():
    while True:
        command = take_command()
        if command:
            execute_command(command)

# GUI Setup
window = tk.Tk()
window.title("JARVIS Assistant")
window.geometry("900x700")
window.configure(bg="#0F0F0F")

# Header
header = tk.Label(window, text="Moueen Togarvi", font=("Courier New", 32, "bold"), fg="lime", bg="#0F0F0F")
header.pack(pady=10)

# Circular Design
canvas = Canvas(window, width=500, height=500, bg="#0F0F0F", highlightthickness=0)
canvas.pack()
circle = canvas.create_oval(50, 50, 450, 450, outline="lime", width=3)
for i in range(0, 360, 30):
    angle = i * pi / 180
    x1, y1 = 250 + 200 * cos(angle), 250 + 200 * sin(angle)
    x2, y2 = 250 + 220 * cos(angle), 250 + 220 * sin(angle)
    canvas.create_line(x1, y1, x2, y2, fill="lime", width=2)

# Status Label
status_label = tk.Label(window, text="Initializing...", font=("Courier New", 20), fg="white", bg="#0F0F0F")
status_label.pack(pady=10)

# Terminal Area
terminal_frame = tk.Frame(window)
terminal_frame.pack(pady=10, fill=tk.BOTH, expand=True)

terminal_scrollbar = Scrollbar(terminal_frame)
terminal_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

terminal_area = Text(terminal_frame, font=("Courier New", 12), bg="#101010", fg="lime", wrap=tk.WORD, state=tk.DISABLED,
                     yscrollcommand=terminal_scrollbar.set)
terminal_area.pack(fill=tk.BOTH, expand=True)
terminal_scrollbar.config(command=terminal_area.yview)

# Bash Command Input
bash_input = tk.Entry(window, font=("Courier New", 14), bg="#101010", fg="lime")
bash_input.pack(fill=tk.X, padx=10, pady=5)

def handle_bash_command(event):
    command = bash_input.get()
    if command.strip():
        update_terminal(f"Executing Bash Command: {command}")
        execute_bash_command(command)
        bash_input.delete(0, tk.END)

bash_input.bind("<Return>", handle_bash_command)

# Start assistant
update_terminal("Hello! I am JARVIS, your personal assistant.")
Thread(target=continuous_listening, daemon=True).start()

window.mainloop()
