import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import pyautogui
import schedule
from plyer import notification
from selenium import webdriver
import openai
import platform
from datetime import datetime
import json
import requests

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

def speak(text):
    """Speak the given text using pyttsx3"""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Take voice input from the user and return the recognized command"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't understand that."

def execute_command(command):
    """Execute commands based on user input"""
    if "open browser" in command:
        speak("Opening browser")
        webbrowser.open("https://www.google.com")
    elif "open file" in command:
        speak("Opening file explorer")
        os.system("explorer")
    elif "shutdown" in command:
        speak("Shutting down the system")
        os.system("shutdown /s /t 1")
    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        search_google(query)
    elif "set reminder" in command:
        task = command.replace("set reminder", "").strip()
        schedule_task(task)
    elif "open folder" in command:
        path = command.replace("open folder", "").strip()
        open_file(path)
    elif "tell me the weather" in command:
        get_weather()
    elif "what is the time" in command:
        tell_time()
    elif "chat with ai" in command:
        query = command.replace("chat with ai", "").strip()
        response = chat_with_ai(query)
        speak(response)
    else:
        speak("I can't perform that task yet.")

# Google Search Automation
def search_google(query):
    """Search Google for the given query using Selenium"""
    driver = webdriver.Chrome(executable_path="path_to_chromedriver")
    driver.get(f"https://www.google.com/search?q={query}")

# Reminder Setup
def reminder(task):
    """Display a desktop notification for the reminder"""
    notification.notify(
        title="Task Reminder",
        message=f"Reminder: {task}",
        timeout=10
    )

def schedule_task(task):
    """Schedule a task at a specific time"""
    speak("At what time should I remind you? For example, say 14:00.")
    time = take_command()
    schedule.every().day.at(time).do(reminder, task=task)
    speak(f"Task scheduled for {time}.")

# File/Folder Opening
def open_file(path):
    """Open a file or folder path using PyAutoGUI"""
    pyautogui.hotkey('win', 'r')
    pyautogui.typewrite(path)
    pyautogui.press('enter')

# Chat with OpenAI
def chat_with_ai(prompt):
    """Interact with OpenAI's GPT API for intelligent conversation"""
    openai.api_key = "your-api-key"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()

# Weather Information
def get_weather():
    """Fetch and speak the current weather using a weather API"""
    api_key = "your-weather-api-key"
    city = "your-city"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        speak(f"The current temperature in {city} is {temp} degrees Celsius with {weather}.")
    else:
        speak("I couldn't fetch the weather details right now.")

# Time Information
def tell_time():
    """Tell the current system time"""
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"The current time is {current_time}.")

# Wake Word Detection (Placeholder for Snowboy or similar tools)
def wake_word_detected():
    """Simulate wake word detection"""
    speak("I am ready to assist you!")
    while True:
        command = take_command()
        if "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        execute_command(command)

# Main Function
if __name__ == "__main__":
    speak("Hello! I am your AI Assistant. Say 'Hey Assistant' to activate me.")
    # Wake word detection logic would go here (e.g., using Snowboy)
    while True:
        wake_word_detected()
